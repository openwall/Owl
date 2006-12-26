/* run-parts: run a bunch of scripts in a directory
 *
 * Debian run-parts program
 * Copyright (C) 1996 Jeff Noxon <jeff at router.patch.net>,
 * Copyright (C) 1996-1999 Guy Maor <maor at debian.org>
 * Copyright (C) 2002, 2003, 2004, 2005 Clint Adams <schizo at debian.org>
 *
 * This is free software; see the GNU General Public License version 2
 * or later for copying conditions.  There is NO warranty.
 *
 * Based on run-parts.pl version 0.2, Copyright (C) 1994 Ian Jackson.
 *
 */

#ifndef _GNU_SOURCE
# define _GNU_SOURCE 1
#endif

#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <getopt.h>
#include <string.h>
#include <errno.h>
#include <error.h>
#include <ctype.h>
#include <signal.h>
#include <sys/time.h>
#include <regex.h>

#define PACKAGE_VERSION "2.17.4-owl"

static int test_mode = 0;
static int list_mode = 0;
static int verbose_mode = 0;
static int report_mode = 0;
static int reverse_mode = 0;
static int exitstatus = 0;
static int lsbsysinit_mode = 0;
static int exit_on_error_mode = 0;

static int argcount = 0, argsize = 0;
static const char **args = NULL;

static void
my_error_print_progname(void)
{
  fprintf(stderr, "%s: ", program_invocation_short_name);
}

static void __attribute__((noreturn))
print_version()
{
  printf("Debian run-parts program, version " PACKAGE_VERSION
	 "\nCopyright (C) 1994 Ian Jackson, Copyright (C) 1996 Jeff Noxon.\n"
	 "Copyright (C) 1996,1997,1998,1999 Guy Maor\n"
	 "Copyright (C) 2002, 2003, 2004, 2005 Clint Adams\n"
	 "This is free software; see the GNU General Public License version 2\n"
	 "or later for copying conditions.  There is NO warranty.\n");
  exit(EXIT_SUCCESS);
}

static void __attribute__((noreturn))
print_help(void)
{
  printf("Usage: %s [OPTION]... DIRECTORY\n"
	 "      --test          print script names which would run, but don't run them.\n"
	 "      --list          print names of all valid files (can not be used with\n"
	 "                      --test)\n"
	 "  -v, --verbose       print script names before running them.\n"
	 "      --report        print script names if they produce output.\n"
	 "      --reverse       reverse execution order of scripts.\n"
	 "      --exit-on-error exit as soon as a script returns with a non-zero exit\n"
	 "                      code.\n"
	 "      --lsbsysinit    validate filenames based on LSB sysinit specs.\n"
	 "  -u, --umask=UMASK   sets umask to UMASK (octal), default is 077.\n"
	 "  -a, --arg=ARGUMENT  pass ARGUMENT to scripts, use once for each argument.\n"
	 "  -V, --version       output version information and exit.\n"
	 "  -h, --help          display this help and exit.\n",
	 program_invocation_short_name);
  exit(EXIT_SUCCESS);
}

static void __attribute__((noreturn, format(printf, 1, 2)))
show_usage(const char *fmt, ...)
{
  if (fmt) {
    va_list arg;

    fprintf(stderr, "%s: ", program_invocation_short_name);
    va_start(arg, fmt);
    vfprintf(stderr, fmt, arg);
    va_end(arg);
    fputc('\n', stderr);
  }
  fprintf(stderr, "Try `%s --help' for more information.\n",
	  program_invocation_short_name);
  exit(EXIT_FAILURE);
}

static void
set_umask(const char *str)
{
  char *p = NULL;
  unsigned long n = strtoul(str, &p, 8);

  if (!*str || !p || *p || n > 0777)
    error(EXIT_FAILURE, 0, "%s: invalid umask value", str);

  umask(n);
}

/* Add an argument to the commands that we will call.  Called once for
   every argument. */
static void
add_argument(const char *newarg)
{
  if (argcount + 1 >= argsize) {
    argsize = argsize ? argsize * 2 : 4;
    args = realloc(args, argsize * (sizeof(char *)));
    if (!args)
      error(EXIT_FAILURE, errno, "failed to reallocate memory for arguments");
  }
  args[argcount++] = newarg;
  args[argcount] = NULL;
}

static void __attribute__((noreturn))
reg_fatal(const char *where, int rc, regex_t *preg)
{
  size_t len = regerror(rc, preg, NULL, 0UL);
  char *errbuf = alloca(len);

  regerror(rc, preg, errbuf, len);
  error(EXIT_FAILURE, 0, "%s failed: %s", where, errbuf);
  exit(EXIT_FAILURE);
}

static regex_t hierre, tradre, excsre, classicalre;

static void
reg_compile(regex_t *preg, const char *regex)
{
  int rc = regcomp(preg, regex, REG_EXTENDED | REG_NOSUB);

  if (rc)
    reg_fatal("regcomp", rc, preg);
}

static void
reg_init(void)
{
  static int initialized = 0;

  if (initialized)
    return;
  initialized = 1;

  if (lsbsysinit_mode) {
    reg_compile(&hierre, "^_?([a-z0-9_.]+-)+[a-z0-9]+$");
    reg_compile(&excsre, "^[a-z0-9-].*rpm(orig|new|save)$");
    reg_compile(&tradre, "^[a-z0-9][a-z0-9-]*$");
  }
  else
    reg_compile(&classicalre, "^[a-zA-Z0-9_-]+$");
}

static int
reg_match(regex_t *preg, const char *sample)
{
  int rc = regexec(preg, sample, 0UL, NULL, 0);

  if (rc == 0 || rc == REG_NOMATCH)
    return rc;

  reg_fatal("regexec", rc, preg);
}

/* True or false? Is this a valid filename? */
static int
valid_name(const struct dirent *d)
{
  const char *c = d->d_name;

  reg_init();

  if (lsbsysinit_mode) {
    if (!reg_match(&hierre, c))
      return reg_match(&excsre, c);

    return !reg_match(&tradre, c);
  }
  else
    return !reg_match(&classicalre, c);
}

static ssize_t
write_loop(int fd, const char *buffer, size_t count)
{
  ssize_t offset = 0;

  while (count > 0) {
    ssize_t block = write(fd, &buffer[offset], count);

    if (block < 0 && errno == EINTR)
      continue;
    if (block <= 0)
      return offset ? offset : block;
    offset += block;
    count -= block;
  }
  return offset;
}

/* Execute a file */
static void
run_part(const char *progname)
{
  int result;
  int pid;
  int pout[2], perr[2];

  if (report_mode && (pipe(pout) || pipe(perr)))
    error(EXIT_FAILURE, errno, "pipe");
  if ((pid = fork()) < 0)
    error(EXIT_FAILURE, errno, "failed to fork");
  else if (!pid) {
    setsid();
    if (report_mode) {
      if (dup2(pout[1], STDOUT_FILENO) != STDOUT_FILENO ||
	  dup2(perr[1], STDERR_FILENO) != STDERR_FILENO)
	error(EXIT_FAILURE, errno, "dup2");
      close(pout[0]);
      close(perr[0]);
      close(pout[1]);
      close(perr[1]);
    }
    args[0] = progname;
    execv(progname, (char *const *) args);
    error(EXIT_SUCCESS, errno, "failed to exec %s", progname);
    _exit(EXIT_FAILURE);
  }

  if (report_mode) {
    fd_set set;
    int max, r, printflag;
    ssize_t c;
    char buf[4096];

    close(pout[1]);
    close(perr[1]);
    max = pout[0] > perr[0] ? pout[0] + 1 : perr[0] + 1;
    printflag = 0;

    while (pout[0] >= 0 || perr[0] >= 0) {

      do {
	FD_ZERO(&set);
	if (pout[0] >= 0)
	  FD_SET(pout[0], &set);
	if (perr[0] >= 0)
	  FD_SET(perr[0], &set);
	r = select(max, &set, NULL, NULL, NULL);
      } while (r < 0 && errno == EINTR);

      if (r < 0)
	error(EXIT_FAILURE, errno, "select");
      else if (r > 0) {
	if (pout[0] >= 0 && FD_ISSET(pout[0], &set)) {
	  c = read(pout[0], buf, sizeof(buf));
	  if (c > 0) {
	    if (!printflag) {
	      printf("%s:\n", progname);
	      fflush(stdout);
	      printflag = 1;
	    }
	    write_loop(STDOUT_FILENO, buf, (size_t)c);
	  }
	  else if (c == 0) {
	    close(pout[0]);
	    pout[0] = -1;
	  }
	  else if (c < 0) {
	    close(pout[0]);
	    pout[0] = -1;
	    error(EXIT_SUCCESS, errno, "failed to read from stdout pipe"); 
	  }
	}
	if (perr[0] >= 0 && FD_ISSET(perr[0], &set)) {
	  c = read(perr[0], buf, sizeof(buf));
	  if (c > 0) {
	    if (!printflag) {
	      fprintf(stderr, "%s:\n", progname);
	      fflush(stderr);
	      printflag = 1;
	    }
	    write_loop(STDERR_FILENO, buf, (size_t)c);
	  }
	  else if (c == 0) {
	    close(perr[0]);
	    perr[0] = -1;
	  }
	  else if (c < 0) {
	    close(perr[0]);
	    perr[0] = -1;
	    error(EXIT_SUCCESS, errno, "failed to read from error pipe"); 
	  }
	}
      }
      else {
	/* assert(FALSE): select was called with infinite timeout, so
	   it either returns successfully or is interrupted */
      }				/*if */
    }				/*while */
  }

  waitpid(pid, &result, 0);

  if (WIFEXITED(result) && WEXITSTATUS(result)) {
    error(EXIT_SUCCESS, 0, "%s exited with return code %d",
      progname, WEXITSTATUS(result));
    exitstatus = 1;
  }
  else if (WIFSIGNALED(result)) {
    error(EXIT_SUCCESS, 0, "%s terminated by signal %d",
      progname, WTERMSIG(result));
    exitstatus = 1;
  }
}

/* Find the parts to run & call run_part() */
static void
run_parts(const char *dirname)
{
  struct dirent **namelist;
  char *filename;
  size_t filename_length, dirname_length;
  int entries, i;
  struct stat st;

  /* dirname + "/" */
  dirname_length = strlen(dirname) + 1;
  /* dirname + "/" + ".." + "\0" (This will save one realloc.) */
  filename_length = dirname_length + 2 + 1;
  if (!(filename = malloc(filename_length)))
    error(EXIT_FAILURE, errno, "failed to allocate memory for path");
  strcpy(filename, dirname);
  strcat(filename, "/");

  /* scandir() isn't POSIX, but it makes things easy. */
  entries = scandir(dirname, &namelist, valid_name, alphasort);
  if (entries < 0)
    error(EXIT_FAILURE, errno, "failed to open directory: %s", dirname);

  i = reverse_mode ? 0 : entries;
  for (i = reverse_mode ? (entries - 1) : 0;
       reverse_mode ? (i >= 0) : (i < entries); reverse_mode ? i-- : i++) {
    if (filename_length < dirname_length + strlen(namelist[i]->d_name) + 1) {
      filename_length = dirname_length + strlen(namelist[i]->d_name) + 1;
      if (!(filename = realloc(filename, filename_length)))
	error(EXIT_FAILURE, errno, "failed to reallocate memory for path");
    }
    strcpy(filename + dirname_length, namelist[i]->d_name);

    if (stat(filename, &st)) {
      if (!list_mode)
	error(EXIT_SUCCESS, errno, "stat: %s", filename);
    }
    else if (S_ISREG(st.st_mode)) {
      if (list_mode)
	printf("%s\n", filename);
      else if (!access(filename, X_OK)) {
	if (test_mode)
	  printf("%s\n", filename);
	else {
	  if (verbose_mode)
	    error(EXIT_SUCCESS, 0, "executing %s", filename);
	  run_part(filename);
	  if (exitstatus && exit_on_error_mode) break;
	}
      }
    }
    else if (!list_mode && !S_ISDIR(st.st_mode))
	error(EXIT_SUCCESS, 0, "%s: not a regular file", filename);

    free(namelist[i]);
  }
  for (; reverse_mode ? (i >= 0) : (i < entries); reverse_mode ? i-- : i++)
    free(namelist[i]);
  free(namelist);
  free(filename);
}

static void
sanitize_std_fds(void)
{
  int fd;

  for (fd = STDIN_FILENO; fd <= STDERR_FILENO; ++fd) {
    int null;
    struct stat st;

    if (fstat(fd, &st) < 0) {
      null = open("/dev/null", O_RDWR);
      if (null < 0)
	  error(EXIT_FAILURE, errno, "open: %s", "/dev/null");
      if (null > STDERR_FILENO)
	close(null);
    }
  }
}

/* Process options */
int main(int argc, char *argv[])
{
  error_print_progname = my_error_print_progname;
  umask(077);
  add_argument(NULL);

  for (;;) {
    int c;
    int option_index = 0;

    static struct option long_options[] = {
      {"test", 0, &test_mode, 1},
      {"list", 0, &list_mode, 1},
      {"verbose", 0, 0, 'v'},
      {"report", 0, &report_mode, 1},
      {"reverse", 0, &reverse_mode, 1},
      {"umask", 1, 0, 'u'},
      {"arg", 1, 0, 'a'},
      {"help", 0, 0, 'h'},
      {"version", 0, 0, 'V'},
      {"lsbsysinit", 0, &lsbsysinit_mode, 1},
      {"exit-on-error", 0, &exit_on_error_mode, 1},
      {NULL, 0, NULL, 0}
    };

    c = getopt_long(argc, argv, "u:ha:vV", long_options, &option_index);
    if (c == EOF)
      break;
    switch (c) {
    case 0:
      break;
    case 'u':
      set_umask(optarg);
      break;
    case 'a':
      add_argument(optarg);
      break;
    case 'h':
      print_help();
      break;
    case 'v':
      verbose_mode = 1;
      break;
    case 'V':
      print_version();
      break;
    default:
      show_usage(NULL);
    }
  }

  /* We require exactly one argument: the directory name */
  if (optind != (argc - 1))
    show_usage("missing operand");

  if (list_mode && test_mode)
    show_usage("--list and --test can not be used together");

  if (report_mode)
    sanitize_std_fds();

  run_parts(argv[optind]);

  return exitstatus;
}

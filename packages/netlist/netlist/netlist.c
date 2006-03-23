/*
 * 18 nov 1999  netlist for linux by stran9er
 * 19 nov 1999  hacked for strict /proc with ip hidding by freelsd
 *  5 nov 2001  udp/raw support by stran9er
 *  6 nov 2001  various relatively unimportant modifications by solar
 *  6 nov 2001  speed up by stran9er
 *  5 jul 2005  v2.1: compatibility with linux kernel 2.6 and some speed-ups
 */

#include <sys/ioctl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <ctype.h>
#include <dirent.h>
#include <errno.h>
#include <pwd.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <search.h>
#include <unistd.h>

static int connsize = 0;	/* number of sockets */
static int commcols = 0;	/* determined columns for command name */
static int commlen = 7;		/* determined maximum command length */

static void fatal(const char *, ...)
  __attribute__ ((noreturn))
  __attribute__ ((format (printf, 1, 2)));

struct netinfo {
  struct netinfo *next;
  unsigned long locip;
  unsigned short locport;
  unsigned long remip;
  unsigned short remport;
  int state;
  int uid;
  unsigned long inode;
  int matched;	/* if found file descriptor */
  int pid;	/* pid of found process */
  int fd;	/* fd number */
  int type; /* tcp, udp, raw */
  char comm[16];
};

static struct netinfo *ni = NULL;
static struct netinfo **bi_idx = NULL;

static void fatal(const char *fmt, ...) {
  va_list args;

  va_start(args, fmt);
  vfprintf(stderr, fmt, args);
  va_end(args);

  exit(1);
}

/* determine device code for sockets */
dev_t determine_sockdev(void) {
  int fd;
  dev_t ret = 0;

  if ((fd = socket(AF_INET, SOCK_STREAM, 0)) != -1) {
    struct stat st;

    if (fstat(fd, &st) != -1)
      ret = st.st_dev;

    close(fd);
  }

  return ret; 
}

/* qsort/bsearch helper */
static int netinfo_cmp(const void *l, const void *r) {
  return (*(struct netinfo **)l)->inode - (*(struct netinfo **)r)->inode;
}

/* read socket tables from /proc */
static struct netinfo *read_net_tables(void) {
  char *fnames[] = {
    "/proc/net/raw",
    "/proc/net/udp",
    "/proc/net/tcp"
  };
  FILE *f;
  struct netinfo *tmp;
  uid_t uid = getuid();
  int fno, i;
  struct stat st;
  gid_t glist[NGROUPS_MAX];
  int size, proc;

  if ( stat("/proc/net", &st) != 0 )
    fatal("stat: /proc/net: %s\n", strerror(errno));

  if ( (size = getgroups(NGROUPS_MAX, glist)) == -1 )
    fatal("getgroups: %s\n", strerror(errno));

  proc = st.st_gid == getgid();
  while (size--)
    proc |= st.st_gid == glist[size];

  for (fno = 0; fno < (sizeof(fnames) / sizeof(char *)); fno++) {
    if (!(f = fopen(fnames[fno], "r")))
      fatal("fopen: %s: %s\n", fnames[fno], strerror(errno));

    while (!feof(f)) {
      int n;

      if ( !(tmp = (struct netinfo *)calloc(1, sizeof(struct netinfo))) )
	fatal("calloc: %s\n", strerror(ENOMEM));

      n = fscanf(f,
	"%*[^\n]\n%*d: %lx:%hx %lx:%hx %x %*x:%*x %*x:%*x %*x %d %*d %ld",
	&tmp->locip, &tmp->locport,
	&tmp->remip, &tmp->remport,
	&tmp->state, &tmp->uid, &tmp->inode);

      if (n == 7 && tmp->inode && (tmp->uid == uid || !uid || proc)) {
	if (tmp->inode)
	  connsize++;
	tmp->type = fno;
	tmp->next = ni;
	ni = tmp;
      } else
	free(tmp);
      if (n != 7) break;
    } /* for each line */

    fclose(f);
  } /* for each file */

  /* build sorted table of inodes */
  if ( !(bi_idx = malloc(connsize * sizeof(struct netinfo *))) )
    fatal("malloc: %s\n", strerror(ENOMEM));
    
  for (i = 0, tmp = ni; tmp; tmp = tmp->next)
    if (tmp->inode)
      bi_idx[i++] = tmp;

  qsort(bi_idx, connsize, sizeof(struct netlist *), netinfo_cmp);
  
  return ni;
}

/* gather opened sockets from /proc/pid/fd/ */
static void scan_proc_fd_dirs(void) {
  DIR *d_proc, *d_fd;
  struct dirent *proc_ent, *fd_ent;
  dev_t sockdev = determine_sockdev();

  if (!(d_proc = opendir("/proc")))
    fatal("opendir: /proc: %s\n", strerror(errno));

  while ((proc_ent = readdir(d_proc))) {
    char fd_path[PATH_MAX];
    int pid;

    if (!isdigit((int)(unsigned char)proc_ent->d_name[0]))
      continue;

    pid = atoi(proc_ent->d_name);
    snprintf(fd_path, PATH_MAX, "/proc/%d/fd", pid);

    if (!(d_fd = opendir(fd_path)))
      continue;

    while ((fd_ent = readdir(d_fd))) {
      char file_path[PATH_MAX];
      struct stat st;
      struct netinfo key, *mat = &key, **xmat;

      if (!isdigit((int)(unsigned char)fd_ent->d_name[0]))
	continue;

      snprintf(file_path, PATH_MAX, "%s/%s", fd_path, fd_ent->d_name);

      if (stat(file_path, &st) == -1 ||
	   st.st_dev != sockdev)
	continue;

      key.inode = st.st_ino;
      xmat = bsearch(&mat, bi_idx, connsize, sizeof(struct netinfo *),
		      netinfo_cmp);
      if (xmat) {
	mat = *xmat;
	if (mat->pid) {
	  struct netinfo *tmp;

	  if ( !(tmp = (struct netinfo *)malloc(sizeof(struct netinfo))) )
	    fatal("malloc: %s\n", strerror(ENOMEM));
	  memcpy(tmp, mat, sizeof(struct netinfo));
	  mat->next = tmp;
	  mat = tmp;
	}
	mat->matched++;
	mat->pid = pid;
	mat->fd = atoi(fd_ent->d_name);
      }
    } /* for each file descriptor */

    closedir(d_fd);
  } /* for each pid */

  closedir(d_proc);
}

/* gather process info */
static void read_proc_stat(void) {
  struct netinfo *np;
  FILE *f;

  for (np = ni; np; np = np->next)
    if (np->pid) {
      char stat_path[PATH_MAX];
      char *p;

      snprintf(stat_path, PATH_MAX, "/proc/%d/stat", np->pid);
      if (!(f = fopen(stat_path, "r"))) continue;
      fscanf(f, "%*d (%15[^)])", np->comm);
      fclose(f);

      for (p = np->comm; *p; p++)
	if (!isprint((int)(unsigned char)*p))
	  *p = '?';

      if ((p - np->comm) > commlen)
	commlen = p - np->comm;
    }
}

/* cache for getpwuid() */
void *du_root = NULL;
struct du_entry {
  uid_t uid;	// *(struct du_entry *) is *(uid_t *)
  char name[0];
};

int du_cmp(const void *pa, const void *pb) {
  return *(uid_t *)pa - *(uid_t *)pb;
}

char *determine_user(uid_t uid) {
  struct du_entry *du, **dup;
  struct passwd *pw;
  static char buf[32];
  char *user = buf;

  if ((dup = (struct du_entry **)tfind(&uid, &du_root, du_cmp))) {
    return (*dup)->name;
  }

  if (!(pw = getpwuid(uid)))
    snprintf(buf, sizeof(buf), "%d", uid);
  else
    user = pw->pw_name;

  if ((du = malloc(sizeof(struct du_entry) + strlen(user) + 1))) {
    du->uid = uid;
    strcpy(du->name, user);
    tsearch(du, &du_root, du_cmp);
  }

  return user;
}

static char *state[] = {
  "??", "ESTAB", "SYNSNT", "SYNRCV", "FINW1", "FINW2", "TIMEW", "CLOSE",
  "CLOSEW", "LASTACK", "LISTEN", "CLOSING"
};

/* output all together */
static void output_netlist(void) {
  struct netinfo *np;

  for (np = ni; np; np = np->next)
    if (np->inode) {
      printf("%-8s ", determine_user(np->uid));

      if (np->matched)
	printf("%-5d %-*.*s%c%2d ", np->pid,
	    commcols, commcols, np->comm, strlen(np->comm) > commcols ? '+' : ' ',
	    np->fd);
      else
	printf("%-5s %-*.*s %2s ", "-", commcols, commcols, "-", "-");

      switch (np->type) {
	case 2: printf("tcp "); break;
	case 1: printf("udp "); break;
	case 0: printf("raw ");
      }

      printf("%15s:%-5d ",
	inet_ntoa(*(struct in_addr *)&np->locip), np->locport);

      printf("%15s:%-5d ",
	inet_ntoa(*(struct in_addr *)&np->remip), np->remport);

      printf("%s\n",
	(np->state > (sizeof(state) / sizeof(char *))) ?
	"??" : state[np->state]);
    }
}

int main(void) {
  struct winsize ws;
  
  if (!read_net_tables())
    fatal("No active Internet connections found\n");

  if (setgid(getgid())) /* drop egid for restricted /proc */
    fatal("setgid: %s\n", strerror(errno));

  if (setuid(getuid()))
    fatal("setuid: %s\n", strerror(errno));

  scan_proc_fd_dirs();

  read_proc_stat();

  commcols = 7;
  if (ioctl(1, TIOCGWINSZ, &ws) != -1) {
    commcols = ws.ws_col - 73;
    if (commcols < 7)
      commcols = 7;
    if (commcols > commlen)
      commcols = commlen;
  }

  printf("USER     PID   %-*s FD TYPE       LOCAL IP:PORT "
    "       REMOTE IP:PORT  STATE\n", commcols, "COMMAND");
  output_netlist();

  return 0;
}

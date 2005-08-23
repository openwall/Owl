/*
 * Pam_listfile written by Michael Tokarev <mjt@corpit.ru> Dec, 2000
 * based on ideas and original work
 * by Elliot Lee <sopwith@redhat.com>, Red Hat Software. July 25, 1996.
 * log refused access error christopher mccrory <chrismcc@netus.com> 1998/7/11
 *
 * This code began life as the pam_rootok module.
 */

#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <syslog.h>
#include <stdarg.h>
#include <string.h>
#include <pwd.h>
#include <grp.h>

#define PAM_SM_AUTH
#define PAM_SM_ACCOUNT
#include <security/pam_modules.h>
#include <security/_pam_modutil.h>

#ifdef HAVE_FNMATCH
# ifdef HAVE_FNMATCH_H
#  include <fnmatch.h>
# else
   extern int fnmatch(const char *, const char *, int);
# endif
# define match(pattern, string) (fnmatch(pattern, string, 0) == 0)
#else
  /* we can implement simple matcher here */
# define match(pattern, string) (strcmp(pattern, string) == 0)
#endif

DEFINE_PAM_LOG("pam_listfile")

static int
in_list(const char *member, const char * const *list)
{
  while (*list)
    if (strcmp(*list++, member) == 0)
      return 1;
  return 0;
}

static int
match_list(const char *pattern, const char *const *list)
{
  while(*list)
    if (match(pattern, *list++))
      return 1;
  return 0;
}

/* Extended Items that are not directly available via pam_get_item() */
#define EI_GROUP 1
#define EI_SHELL 2
#define EI_HOME  3

static int
pam_list(pam_handle_t *pamh, int argc, const char **argv)
{
  /* defaults */
  int item = 0; /* item to get from PAM */
  int eitem = 0; /* for "extended" (EI_*) items from struct passwd */
  int onerr = PAM_SERVICE_ERR; /* what to do in case of error */
  int sense = -1; /* what to do: allow(0)/deny(1)/unknown(-1) */
  const char *list = NULL; /* file or direct list */
  const char *apply = NULL; /* for apply= */
  const void *void_item; /* for pam_get_item */
  int r;

  const char *user = NULL; /* PAM_USER */

#define MAXITEMS 128 /* max. 256 items to check */
  const char *items[MAXITEMS+1];

  /* process arguments */
  r = 1; /* 0 means error */
  while(argc--) {
    const char *a = *argv++;

    if (!strcmp(a, "onerr=succeed") || !strcmp(a, "errsucceed") || !strcmp(a, "errok"))
      onerr = PAM_SUCCESS;
    else if (!strcmp(a, "onerr=fail") || !strcmp(a, "errfail"))
      onerr = PAM_SERVICE_ERR;

    else if (sense < 0 && (!strcmp(a, "sense=allow") || !strcmp(a, "allow")))
      sense = 0;
    else if (sense < 0 && (!strcmp(a, "sense=deny") || !strcmp(a, "deny")))
      sense = 1;

    else if (!list && (!strncmp(a, "file=", 5) || !strncmp(a, "list=", 5)))
      list = a + 5;

    else if (!list && sense < 0 && !strncmp(a, "allow=", 6))
      list = a + 6, sense = 0;
    else if (!list && sense < 0 && !strncmp(a, "deny=", 5))
      list = a + 5, sense = 1;

    else if (!item && (!strcmp(a, "item=user") || !strcmp(a, "user")))
      item = PAM_USER;
    else if (!item && (!strcmp(a, "item=tty") || !strcmp(a, "tty")))
      item = PAM_TTY;
    else if (!item && (!strcmp(a, "item=rhost") || !strcmp(a, "rhost")))
      item = PAM_RHOST;
    else if (!item && (!strcmp(a, "item=ruser") || !strcmp(a, "ruser")))
      item = PAM_RUSER;
    else if (!item && (!strcmp(a, "item=group") || !strcmp(a, "group")))
      item = PAM_USER, eitem = EI_GROUP;
    else if (!item && (!strcmp(a, "item=shell") || !strcmp(a, "shell")))
      item = PAM_USER, eitem = EI_SHELL;
    else if (!item && (!strcmp(a, "item=home") || !strcmp(a, "home")))
      item = PAM_USER, eitem = EI_HOME;

    else if (!item && !list && !strncmp(a, "user=", 5))
      item = PAM_USER, list = a + 5;
    else if (!item && !list && !strncmp(a, "tty=", 4))
      item = PAM_TTY, list = a + 4;
    else if (!item && !list && !strncmp(a, "rhost=", 6))
      item = PAM_RHOST, list = a + 6;
    else if (!item && !list && !strncmp(a, "ruser=", 6))
      item = PAM_RUSER, list = a + 6;
    else if (!item && !list && !strncmp(a, "group=", 6))
      item = PAM_USER, eitem = EI_GROUP, list = a + 6;
    else if (!item && !list && !strncmp(a, "shell=", 6))
      item = PAM_USER, eitem = EI_SHELL, list = a + 6;
    else if (!item && !list && !strncmp(a, "home=", 5))
      item = PAM_USER, eitem = EI_HOME, list = a + 5;

    else if (!apply && !strncmp(a, "apply=", 6) && a[6])
      apply = a + 6;

    else {
      _pam_log(LOG_ERR, "Unknown, invalid or duplicated option: %s", a);
      r = 0;
    }
  }

  if (!item)
    _pam_log (LOG_ERR, "Item not specified"), r = 0;
  if (!list)
    _pam_log (LOG_ERR, "List not specified"), r = 0;
  if (sense < 0)
    _pam_log (LOG_ERR, "Sense not specified"), r = 0;

  /* if any command-line processing fails, we also fail, ignoring onerr= value.
     Command line should be fixed. */
  if (!r)
    return PAM_SERVICE_ERR;

  /* Check if it makes sense to use the apply= parameter */
  if (apply) {
    if (item == PAM_USER || item == PAM_RUSER || eitem == EI_GROUP) {
      /*XXX FIXME: why deny=user,... apply=@group is non-sense? */
      _pam_log(LOG_WARNING, "Non-sense use for apply= parameter");
      //apply = NULL; /*XXX FIXME -- above */
    }
  }

  /* Note: fragile logic here -- be careful! */
  if (item == PAM_USER || apply) {
    /* for PAM_USER (ext)item and for apply= -- get user info */

    r = pam_get_user(pamh, &user, NULL); /* retrieve username from PAM */
    if (r != PAM_SUCCESS) {
      _pam_log(LOG_WARNING, "unable to obtain user: %s", pam_strerror(pamh, r));
      return onerr;
    }
    if (!user || !*user) { /* empty user?! */
      _pam_log(LOG_WARNING, "no user specified");
      if (apply)
        return PAM_IGNORE; /* assume "not apply" */
      else /* assume "not listed" */
        return sense ? PAM_SUCCESS : PAM_AUTH_ERR;
    }

    /* user is ok.  But it may not exists... */

    if (apply && *apply != '@') /* check apply=user */
      if (strcmp(user, apply)) /* applies */
        apply = NULL; /* apply done */
      else /* not applies */
        return PAM_IGNORE;

    if (apply) { /* apply to group */
      const struct group *gr = getgrnam(++apply); /* skip @ and get group name */
      if (!gr)
        _pam_log(LOG_WARNING, "apply group %s does not exists", apply);
        /*XXXX FIXME: error or warning? Maybe command-line error... */
      else if (in_list(user, (const char **)gr->gr_mem))
	/* applies, found in group */
        apply = NULL; /* apply done */
      /* else for apply we need to check primary group also */
    }

    if (apply || eitem) { /* for that, we need primary group */
      struct passwd *pw = getpwnam(user);
      if (!pw) {
        if (apply) {
          _pam_log(LOG_ERR, "user not found, can't apply group");
          return PAM_IGNORE;
        }
        if (eitem) /* assume "not listed" */
          return sense ? PAM_SUCCESS : PAM_AUTH_ERR;
        /* for item=user it is ok to continue without having passwd entry.
           If it is (eitem == 0), we will not look to here at all... */
      }

      if (apply || eitem == EI_GROUP) { /* need primary group */
        const struct group *gr = getgrgid(pw->pw_gid);
        if (!gr) {
          _pam_log(LOG_WARNING, "unable to find primary group %d for %s",
                   (int)pw->pw_gid, user);
          if (apply) /* not applies */
            return PAM_IGNORE;
          /* for EI_GROUP, supplement groups still can be matched */
          /*XXX FIXME: should we complain here? Log?  sense=group but no
            primary group? */
        }
        else if (apply && strcmp(apply, gr->gr_name)) /* last apply=, done */
          return PAM_IGNORE; /* does not apply */

        if (eitem == EI_GROUP) { /* init group list */
          int n = 0; /* count of group items */
          if (gr) { /* add primary group */
            if ((items[n++] = strdup(gr->gr_name)) == NULL) {
              _pam_log(LOG_ERR, "no memory for primary group");
              return onerr;
            }
          }
          setgrent();
          while((gr = getgrent()) != NULL) {
            if (!in_list(user, (const char **)gr->gr_mem))
              continue;
            if (n == MAXITEMS) { /* items[] has additional entry for NULL */
              _pam_log(LOG_WARNING, "too many groups for %s", user);
              break; /*XXX maybe return onerr here? */
            }
            if ((items[n++] = strdup(gr->gr_name)) == NULL) {
              while(n--) free((void*)items[n]);
              _pam_log(LOG_ERR, "no memory for group list");
              return onerr;
            }
          }
          items[n] = NULL;
        } /* end of EI_GROUP */

      } /* end of apply || EI_GROUP */

      if (eitem == EI_SHELL)
        items[0] = pw->pw_shell && (pw->pw_shell)[0] ?
          pw->pw_shell : "/bin/sh"; /*XXX FIXME: should be _PATH_BSHELL */
      else if (eitem == EI_HOME)
        items[0] = pw->pw_dir;
      /* for eitem == 0 it is just user, eitem == EI_GROUP already done */

    } /* end of apply || eitem */

    if (item == PAM_USER && !eitem)
      items[0] = user;

  } /* end of item == PAM_USER || apply */

  if (item != PAM_USER) {
    /* get any PAM item */
    const char *val;
    void_item = NULL;
    r = pam_get_item(pamh, item, &void_item);
    val = void_item;
    if (r != PAM_SUCCESS) {
      _pam_log(LOG_ERR, "unable to get pam item: %s", pam_strerror(pamh, r));
      return onerr;
    }
    if (!val || !*val)
      /* The item was NULL - we are sure not to match */
      return sense ? PAM_SUCCESS : PAM_AUTH_ERR;
    items[0] = val;
  }

  if (eitem != EI_GROUP)
    items[1] = NULL; /* NULL-terminate */

  /* fragile logic ends */

  /* here, we have NULL-terminated list of items[] to match for */

  if (*list != '/') { /* this is not a file, but direct list */

    char *next; /* pointer to next comma */

    r = 0; /* not found */
    do {
      int not = *list == '!' ? ++list, 1 : 0; /* negation? skip to next char */
      if ((next = strchr(list, ',')) != NULL)
        *next = '\0'; /* temporarily turn comma to zero inside argv[i] */
      r = *list && match_list(list, items);
      if (next)
        *next++ = ','; /* restore comma */
      if (r) {
        if (not) r = 0;
        break;
      }
    } while ((list = next) != NULL);

  }
  else { /* else it is a filename */

    struct stat st;
    FILE *f;

    /* check file */
    if (lstat(list, &st) != 0) {
      if (onerr == PAM_SERVICE_ERR) /* Only report if it's an error... */
        _pam_log(LOG_ERR, "unable to stat %s", list);
      r = -1;
    }
    else if ((st.st_mode & S_IWOTH) || !S_ISREG(st.st_mode)) {
      /* If the file is world writable or is not a normal file, return error */
      _pam_log(LOG_ERR,
         "%s is either world writable or not a normal file", list);
      r = -1;
    }
    else if ((f = fopen(list, "r")) == NULL) {
      if (onerr == PAM_SERVICE_ERR) /* Only report if it's an error... */
        _pam_log(LOG_ERR, "unable to open %s", list);
      r = -1;
    }
    else {
      char line[256];
      int not = 0;
      r = 0; /* not found */
      while (fgets(line, sizeof(line), f) != NULL) {
        int l = strlen(line);
        char *p = line + l;
        if (!l) continue; /* should never happen? */
        if (p[-1] == '\n') /* line is terminated good */
          --p;
        else if ((l = getc(f)) != EOF) { /* oops, not terminated and !eof */
          _pam_log(LOG_ERR, "line in %s is too long", list);
          while (l != '\n') /*XXX FIXME: skip this line completely? Or error? */
            if ((l = getc(f)) == EOF)
              break;
          continue;
        }
        /* strip trailing spaces */
        while(p > line && (p[-1] == ' ' || p[-1] == '\t')) --p;
        *p = '\0'; /* terminate */
        p = line;
        while(*p == ' ' || *p == '\t') ++p; /* skip leading spaces */
        if (*p == '!') { /* negation */
          not = 1;
          ++p;
          while(*p == ' ' || *p == '\t') ++p; /* skip further spaces */
        }
        else
          not = 0;
        if (*p && *p != '#' /* ignore empty line and comment(s) */
            && match_list(p, items)) {
          r = 1;
          break;
        }
      }
      if (!r && ferror(f)) {
        /* if not found but error */
        _pam_log(LOG_ERR, "error reading %s", list);
        r = -1;
      }
      fclose(f);
      if (r == 1 && not) /* negate it */
        r = 0;
    }

  } /* list is file */

  if (eitem == EI_GROUP) { /* for EI_GROUP only -- free group list */
    char **ii = (char**)items;
    while(*ii)
      free(*(ii++));
  }

  if (r < 0) /* error of some kind, should be reported already */
    return onerr;

  if (r != sense)
    return PAM_SUCCESS;

  /* no, should deny either by deny= and !found or the opposite */
  void_item = ""; /* just temporary: service name */
  pam_get_item(pamh, PAM_SERVICE, &void_item);
  list = void_item;
  if (!user) { /* if user still unknown */
    void_item = NULL;
    pam_get_item(pamh, PAM_USER, &void_item);
    user = void_item;
  }
  _pam_log(LOG_ERR,  "Refused user %s for service %s", user, list);
  return PAM_AUTH_ERR;
}

PAM_EXTERN
int pam_sm_authenticate(pam_handle_t *pamh, int flags,
                        int argc, const char **argv)
{
  return pam_list(pamh, argc, argv);
}

PAM_EXTERN
int pam_sm_setcred(pam_handle_t *pamh, int flags, int argc, const char **argv)
{
  return PAM_SUCCESS;
}

PAM_EXTERN
int pam_sm_acct_mgmt(pam_handle_t *pamh, int flags, int argc, const char **argv)
{
  return pam_list(pamh, argc, argv);
}

#ifdef PAM_STATIC

struct pam_module _pam_listfile_modstruct = {
  "pam_listfile",
  pam_sm_authenticate,
  pam_sm_setcred,
  pam_sm_acct_mgmt,
  NULL,
  NULL,
  NULL,
};

#endif

/* end of module definition */

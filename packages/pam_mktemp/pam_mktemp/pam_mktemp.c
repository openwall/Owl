/*
 * Copyright (c) 2000-2002 by Solar Designer. See LICENSE.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pwd.h>
#include <grp.h>
#include <errno.h>
#include <sys/stat.h>

#ifdef __linux__
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/ext2_fs.h>
#endif

#define PAM_SM_SESSION
#ifndef LINUX_PAM
#include <security/pam_appl.h>
#endif
#include <security/pam_modules.h>

#if !defined(PAM_EXTERN) && !defined(PAM_STATIC)
#define PAM_EXTERN			extern
#endif

#define PRIVATE_PREFIX			"/tmp/.private"

#ifdef __linux__
static int ext2fs_chflags(const char *name, int set, int reset)
{
	int fd, flags;
	int retval;

	if ((fd = open(name, O_RDONLY)) < 0)
		return -1;

	if (ioctl(fd, EXT2_IOC_GETFLAGS, &flags)) {
		close(fd);
		return -1;
	}

	flags |= set;
	flags &= ~reset;

	retval = ioctl(fd, EXT2_IOC_SETFLAGS, &flags);

	close(fd);
	return retval;
}
#else
#define ext2fs_chflags(name, set, reset)
#endif

static int assign(pam_handle_t *pamh, const char *name, const char *value)
{
	char *string;

	string = alloca(strlen(name) + strlen(value) + 2);
	if (string) {
		sprintf(string, "%s=%s", name, value);
		return pam_putenv(pamh, string);
	}

	return -1;
}

PAM_EXTERN int pam_sm_open_session(pam_handle_t *pamh, int flags,
	int argc, const char **argv)
{
	struct passwd *pw;
	struct group *gr;
	struct stat st;
	const char *user;
	char *userdir;
	int usergroups;
	int status;

	if (geteuid() != 0)
		return PAM_SESSION_ERR;

	status = pam_get_item(pamh, PAM_USER, (const void **)&user);
	if (status != PAM_SUCCESS)
		return status;

/* "Can't happen" (the user should have been authenticated by now) */
	if (user[0] == '.' || strchr(user, '/'))
		return PAM_SESSION_ERR;

	if (!(pw = getpwnam(user)))
		return PAM_USER_UNKNOWN;
	memset(pw->pw_passwd, 0, strlen(pw->pw_passwd));

/* Could have multiple UID 0 accounts, no need for separate directories */
	if (pw->pw_uid == 0) user = "root";

/* If there's a private group for this user, use it as this makes it safe
 * to su to another user (or root) even if su doesn't use this module. */
	usergroups = 0;
	if (pw->pw_uid != 0 && (gr = getgrgid(pw->pw_gid))) {
		memset(gr->gr_passwd, 0, strlen(gr->gr_passwd));
		if (!strcmp(user, gr->gr_name)) usergroups = 1;
	}

/* This directory should be created at system installation time and never
 * removed, or there's the obvious DoS possibility here. */
	if (mkdir(PRIVATE_PREFIX, 0711) && errno != EEXIST)
		return PAM_SESSION_ERR;

	if (lstat(PRIVATE_PREFIX, &st) ||
	    !S_ISDIR(st.st_mode) ||
	    st.st_uid != 0)
		return PAM_SESSION_ERR;

	if ((st.st_mode & 0777) != 0711 && chmod(PRIVATE_PREFIX, 0711))
		return PAM_SESSION_ERR;

/*
 * At this point we have a directory which is only writable by root, and
 * is itself in a root-owned +t directory (/tmp). Thus, only root can do
 * anything in the directory or rename/unlink it and we can play safely.
 */

	if (ext2fs_chflags(PRIVATE_PREFIX, EXT2_APPEND_FL, 0))
		return PAM_SESSION_ERR;

	userdir = alloca(strlen(PRIVATE_PREFIX) + strlen(user) + 2);
	if (!userdir)
		return PAM_SESSION_ERR;

	sprintf(userdir, "%s/%s", PRIVATE_PREFIX, user);

	if (mkdir(userdir, 01700) && errno != EEXIST)
		return PAM_SESSION_ERR;

	/* Don't let the append-only flag get inherited from the parent
	 * directory. */
	if (ext2fs_chflags(userdir, 0, EXT2_APPEND_FL))
		return PAM_SESSION_ERR;

	if (usergroups) {
		if (chown(userdir, 0, pw->pw_gid) ||
		    chmod(userdir, 01770))
			return PAM_SESSION_ERR;
	} else {
		if (chmod(userdir, 01700) ||
		    chown(userdir, pw->pw_uid, pw->pw_gid))
			return PAM_SESSION_ERR;
	}

	if (assign(pamh, "TMPDIR", userdir) ||
	    assign(pamh, "TMP", userdir))
		return PAM_SESSION_ERR;

	return PAM_SUCCESS;
}

PAM_EXTERN int pam_sm_close_session(pam_handle_t *pamh, int flags,
	int argc, const char **argv)
{
/* There're good reasons to NOT remove the directory here, not even when
 * it is empty. */
	return PAM_SUCCESS;
}

#ifdef PAM_STATIC
#define pam_sm_acct_mgmt pam_sm_open_session
#elif defined(__linux__) && defined(__ELF__)
__asm__(".globl pam_sm_acct_mgmt; .set pam_sm_acct_mgmt, pam_sm_open_session");
#else
PAM_EXTERN int pam_sm_acct_mgmt(pam_handle_t *pamh, int flags,
	int argc, const char **argv)
{
	return pam_sm_open_session(pamh, flags, argc, argv);
}
#endif

#ifdef PAM_STATIC
struct pam_module _pam_mktemp_modstruct = {
	"pam_mktemp",
	NULL,
	NULL,
	pam_sm_acct_mgmt,
	pam_sm_open_session,
	pam_sm_close_session,
	NULL
};
#endif

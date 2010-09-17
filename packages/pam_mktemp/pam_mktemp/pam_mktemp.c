/*
 * Copyright (c) 2000-2002,2005,2010 by Solar Designer
 * Copyright (c) 2005,2006,2010 by Dmitry V. Levin
 * See LICENSE
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pwd.h>
#include <grp.h>
#include <errno.h>
#include <sys/stat.h>
#ifdef USE_SELINUX
#include <selinux/selinux.h>
#endif /* USE_SELINUX */

#ifndef HAVE_APPEND_FL
# ifdef __linux__
#  define HAVE_APPEND_FL 1
# endif /* __linux__ */
#endif /* ! HAVE_APPEND_FL */

#ifdef HAVE_APPEND_FL
/*
 * We may want to use the append-only flag on /tmp/.private such that
 * tmpwatch(8) does not remove users' temporary file directories and
 * /tmp/.private itself.  This would be a security problem because a malicious
 * user would then be able to create a directory of this name and thus violate
 * reasonable assumptions of temporary file using programs of other users that
 * had TMPDIR set by pam_mktemp previously.
 *
 * stmpclean(8), which we have in Owl, does not remove root-owned directories
 * (so it won't remove /tmp/.private) and switches to each directory's owner
 * euid when it tries to remove other directories (so it won't actually remove
 * subdirectories of /tmp/.private).  Thus, we do not need the append-only flag
 * on /tmp/.private on Owl.
 *
 * Since the append-only flag posed a usability problem (it was not immediately
 * clear to many how to remove an Owl userland tree) and since it did not apply
 * to tmpfs filesystems anyway, we now have this disabled by default.  However,
 * if /tmp/.private is already set to append-only (perhaps by an older version
 * of pam_mktemp), we take care of resetting this flag for subdirectories of
 * /tmp/.private (we don't let it get inherited, which would be the default).
 */
# include <fcntl.h>
# include <sys/ioctl.h>
# include <ext2fs/ext2_fs.h>
#else
# undef USE_APPEND_FL
#endif /* HAVE_APPEND_FL */

#define PAM_SM_SESSION
#if !defined(__LIBPAM_VERSION) && !defined(__LINUX_PAM__)
# include <security/pam_appl.h>
#endif
#include <security/pam_modules.h>

#if !defined(__LIBPAM_VERSION) && !defined(__LINUX_PAM__) && !defined(_OPENPAM)
/* Sun's PAM doesn't use const here, while Linux-PAM and OpenPAM do */
#define lo_const
#else
#define lo_const			const
#endif

#if !defined(PAM_EXTERN) && !defined(PAM_STATIC)
# define PAM_EXTERN			extern
#endif

#define PRIVATE_PREFIX			"/tmp/.private"

#ifdef HAVE_APPEND_FL
static int ext2fs_chflags(const char *name, int set, int clear)
{
	int fd, old_flags, new_flags;
	int retval = 0;

	if ((fd = open(name, O_RDONLY)) < 0)
		return -1;

	if (ioctl(fd, EXT2_IOC_GETFLAGS, &old_flags)) {
		if ((errno == ENOTTY) /* Inappropriate ioctl for device */
		    || (errno == ENOSYS)) /* Function not implemented */
			errno = EOPNOTSUPP;
		close(fd);
		return -1;
	}

	new_flags = (old_flags | set) & ~clear;
	if (new_flags != old_flags)
		retval = ioctl(fd, EXT2_IOC_SETFLAGS, &new_flags);

	if (close(fd))
		retval = -1;
	return retval;
}
#endif /* HAVE_APPEND_FL */

#ifdef USE_SELINUX
static int check_scontext(const security_context_t scontext, const char *file)
{
	security_context_t fscon = NULL;
	int ret;

	if (getfilecon(file, &fscon) < 0)
		return -1;
	ret = selinux_file_context_cmp(scontext, fscon);
	freecon(fscon);

	return ret;
}
#endif /* USE_SELINUX */

static int assign(pam_handle_t *pamh, const char *name, const char *value)
{
	char *string;
	int rc;

	string = malloc(strlen(name) + strlen(value) + 2);
	if (!string)
		return PAM_BUF_ERR;

	sprintf(string, "%s=%s", name, value);
	rc = pam_putenv(pamh, string);
	free(string);
	return rc;
}

PAM_EXTERN int pam_sm_open_session(pam_handle_t *pamh, int flags,
	int argc, const char **argv)
{
	struct passwd *pw;
	struct group *gr;
	struct stat st;
	lo_const void *item;
	const char *user;
	char *userdir = NULL;
	int usergroups;
	int status;
#ifdef USE_SELINUX
	security_context_t scontext = NULL;
	int selinux_enabled;
#endif /* USE_SELINUX */

	if (geteuid() != 0)
		return PAM_SESSION_ERR;

	status = pam_get_item(pamh, PAM_USER, &item);
	if (status != PAM_SUCCESS)
		return status;
	user = item;

	status = PAM_SESSION_ERR;

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

#ifdef USE_SELINUX
/* Load SELinux file contexts configuration.
 * In case of any error reported by SELinux functions, the error
 * itself will be ignored (it is not a problem of the PAM module), but
 * selinux_enabled will be reset to 0, to skip subsequent SELinux
 * function calls. */
	selinux_enabled = is_selinux_enabled() > 0;
	if (selinux_enabled && matchpathcon_init_prefix(NULL, PRIVATE_PREFIX))
		selinux_enabled = 0;

	/* Set file creation context before mkdir() call */
	if (selinux_enabled) {
		if (matchpathcon(PRIVATE_PREFIX, S_IFDIR, &scontext) ||
		    setfscreatecon(scontext))
			selinux_enabled = 0;
	}
#endif /* USE_SELINUX */

/* This directory should be created at system installation or bootup time and
 * never removed, or there's the obvious DoS possibility here. */
	if (mkdir(PRIVATE_PREFIX, 0711) && errno != EEXIST)
		goto out;

	if (lstat(PRIVATE_PREFIX, &st) ||
	    !S_ISDIR(st.st_mode) ||
	    st.st_uid != 0)
		goto out;

	if ((st.st_mode & 0777) != 0711 && chmod(PRIVATE_PREFIX, 0711))
		goto out;

#ifdef USE_SELINUX
	if (selinux_enabled &&
	    check_scontext(scontext, PRIVATE_PREFIX) &&
	    setfilecon(PRIVATE_PREFIX, scontext))
		selinux_enabled = 0;
#endif /* USE_SELINUX */

/*
 * At this point we have a directory which is only writable by root, and
 * is itself in a root-owned +t directory (/tmp).  Thus, only root can do
 * anything in the directory or rename/unlink it and we can play safely.
 */

#ifdef USE_APPEND_FL
	ext2fs_chflags(PRIVATE_PREFIX, EXT2_APPEND_FL, 0);
#endif /* USE_APPEND_FL */

	userdir = malloc(strlen(PRIVATE_PREFIX) + strlen(user) + 2);
	if (!userdir) {
		status = PAM_BUF_ERR;
		goto out;
	}
	sprintf(userdir, "%s/%s", PRIVATE_PREFIX, user);

#ifdef USE_SELINUX
	if (selinux_enabled) {
		freecon(scontext);
		scontext = NULL;
		if (matchpathcon(userdir, S_IFDIR, &scontext) ||
		    setfscreatecon(scontext))
			selinux_enabled = 0;
	}
#endif /* USE_SELINUX */

	if (mkdir(userdir, 01700)) {
		if (errno != EEXIST)
			goto out;
#ifdef HAVE_APPEND_FL
	} else {
		/* Don't let the append-only flag get inherited
		 * from the parent directory. */
		if (ext2fs_chflags(userdir, 0, EXT2_APPEND_FL) &&
		    errno != EOPNOTSUPP)
			goto out;
#endif /* HAVE_APPEND_FL */
	}

	if (usergroups) {
		if (chown(userdir, 0, pw->pw_gid) ||
		    chmod(userdir, 01770))
			goto out;
	} else {
		if (chmod(userdir, 01700) ||
		    chown(userdir, pw->pw_uid, pw->pw_gid))
			goto out;
	}

#ifdef USE_SELINUX
	if (selinux_enabled && check_scontext(scontext, userdir))
		setfilecon(userdir, scontext);
#endif /* USE_SELINUX */

	if ((status = assign(pamh, "TMPDIR", userdir)) != PAM_SUCCESS ||
	    (status = assign(pamh, "TMP", userdir)) != PAM_SUCCESS)
		goto out;

out:
#ifdef USE_SELINUX
	freecon(scontext);
	matchpathcon_fini();
#endif /* USE_SELINUX */
	free(userdir);

	return status;
}

PAM_EXTERN int pam_sm_close_session(pam_handle_t *pamh, int flags,
	int argc, const char **argv)
{
/* There are good reasons to NOT remove the directory here, not even when
 * it is empty. */
	return PAM_SUCCESS;
}

#ifdef PAM_STATIC
#define pam_sm_acct_mgmt pam_sm_open_session
#elif defined(__linux__) && defined(__ELF__)
__asm__(".globl pam_sm_acct_mgmt; pam_sm_acct_mgmt = pam_sm_open_session");
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

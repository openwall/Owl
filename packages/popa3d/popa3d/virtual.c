/*
 * Virtual domain support.
 */

#include "params.h"

#if POP_VIRTUAL

#define _XOPEN_SOURCE 4
#define _XOPEN_SOURCE_EXTENDED
#define _XOPEN_VERSION 4
#define _XPG4_2
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h>
#include <errno.h>
#include <pwd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#ifndef NAME_MAX
#define NAME_MAX			255
#endif

#include "misc.h"

extern int log_error(char *s);

char *virtual_domain;
char *virtual_spool;

int virtual_startup(void)
{
	return 0;
}

static char *lookup(void)
{
	struct sockaddr_in sin;
	socklen_t length;

	length = sizeof(sin);
	if (getsockname(0, (struct sockaddr *)&sin, &length)) {
		if (errno == ENOTSOCK) return "";
		log_error("getsockname");
		return NULL;
	}
	if (length != sizeof(sin) || sin.sin_family != AF_INET) return NULL;

	return inet_ntoa(sin.sin_addr);
}

static int is_valid_user(char *user)
{
	unsigned char *p;

/* This is pretty liberal, but we're going to use direct syscalls only,
 * and they have to accept all the printable characters */
	for (p = (unsigned char *)user; *p; p++)
		if (*p < ' ' || *p > 0x7E || *p == '.' || *p == '/') return 0;

	if (p - (unsigned char *)user > NAME_MAX) return 0;

	return 1;
}

struct passwd *virtual_userpass(char *user, char *pass, int *known)
{
	struct passwd *pw, *result;
	struct stat stat;
	char auth[VIRTUAL_AUTH_SIZE];
	char *address, *pathname;
	char *template, *passwd;
	int fail;
	int fd, size;

	*known = 0;

/* Make sure we don't try to authenticate globally if something fails
 * before we find out whether the virtual domain is known to us */
	virtual_domain = "UNKNOWN";
	virtual_spool = NULL;

	if (!(address = lookup())) return NULL;

/* Authenticate globally (if supported) if run on a non-socket */
	if (!*address) {
		virtual_domain = NULL;
		return NULL;
	}

	fail = 0;
	if (!is_valid_user(user)) {
		user = "INVALID";
		fail = 1;
	}

/* This "can't happen", but is just too critical to not check explicitly */
	if (strchr(address, '/') || strchr(user, '/'))
		return NULL;

	pathname = concat(VIRTUAL_HOME_PATH, "/", address, NULL);
	if (!pathname) return NULL;

	if (lstat(pathname, &stat)) {
		free(pathname);
		if (errno == ENOENT)
			virtual_domain = NULL;
		else
			log_error("lstat");
		return NULL;
	}
	free(pathname);

	if (!(address = strdup(address))) return NULL;
	virtual_domain = address;

	pathname = concat(VIRTUAL_HOME_PATH, "/", address, "/",
		VIRTUAL_AUTH_PATH, "/", user, NULL);
	if (!pathname) return NULL;

	if ((fd = open(pathname, O_RDONLY)) < 0 && errno != ENOENT) {
		log_error("open");
		fail = 1;
	}

	free(pathname);

	virtual_spool = concat(VIRTUAL_HOME_PATH, "/", virtual_domain, "/",
		VIRTUAL_SPOOL_PATH, NULL);
	if (!virtual_spool) {
		if (fd >= 0) close(fd);
		return NULL;
	}

	size = 0;
	if (fd >= 0) {
		*known = !fail;

		if ((size = read(fd, auth, sizeof(auth))) < 0) {
			log_error("read");
			size = 0;
			fail = 1;
		}

		close(fd);
	}

	if (size >= sizeof(auth)) {
		size = 0;
		fail = 1;
	}

	auth[size] = 0;

	if (!(template = strtok(auth, ":")) || !*template) {
		template = "INVALID";
		fail = 1;
	}
	if (!(passwd = strtok(NULL, ":")) || !*passwd ||
	    *passwd == '*' || *passwd == '!') {
		passwd = AUTH_DUMMY_SALT;
		fail = 1;
	}
	if (!strtok(NULL, ":")) fail = 1;

	if ((pw = getpwnam(template)))
		memset(pw->pw_passwd, 0, strlen(pw->pw_passwd));
	endpwent();

	result = NULL;
	{
		char *computed_hash = crypt(pass, passwd);
		if (computed_hash && !strcmp(computed_hash, passwd) && !fail)
			result = pw;
	}

	memset(auth, 0, sizeof(auth));

	return result;
}

#endif

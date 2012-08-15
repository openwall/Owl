/*
 * The /etc/shadow authentication routine.  This one is really tricky,
 * in order to make sure we don't have an /etc/shadow fd or sensitive
 * data in our address space after we drop the root privileges.  It is
 * arguable whether this was worth the extra code and the performance
 * penalty or not, but such discussions are outside of the scope of a
 * comment like this. ;^)
 */

#include "params.h"

#if AUTH_SHADOW && !VIRTUAL_ONLY

#define _XOPEN_SOURCE 4
#define _XOPEN_SOURCE_EXTENDED
#define _XOPEN_VERSION 4
#define _XPG4_2
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <pwd.h>
#include <shadow.h>
#include <sys/wait.h>
#include <sys/types.h>

extern int log_error(char *s);

struct passwd *auth_userpass(char *user, char *pass, int *known)
{
	int channel[2];
	struct passwd *pw;
	struct spwd *spw;
	char result;

	if ((*known = (pw = getpwnam(user)) != NULL))
		memset(pw->pw_passwd, 0, strlen(pw->pw_passwd));
	endpwent();
	result = 0;

	if (pipe(channel)) {
		log_error("pipe");
		return NULL;
	}

	switch (fork()) {
	case -1:
		log_error("fork");
		return NULL;

	case 0:
		close(channel[0]);
		if (!(spw = getspnam(user)) || !pw || !*spw->sp_pwdp ||
		    *spw->sp_pwdp == '*' || *spw->sp_pwdp == '!')
			crypt(pass, AUTH_DUMMY_SALT);
		else {
			char *hash = crypt(pass, spw->sp_pwdp);
			if (hash && !strcmp(hash, spw->sp_pwdp))
				result = 1;
		}
		write(channel[1], &result, 1);
		exit(0);
	}

	if (close(channel[1]))
		pw = NULL;
	else {
		if (read(channel[0], &result, 1) != 1) pw = NULL;
		if (result != 1) pw = NULL;
		if (close(channel[0])) pw = NULL;
	}

	wait(NULL);

	return result == 1 ? pw : NULL;
}

#endif

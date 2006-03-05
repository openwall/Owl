/*
 * PAM authentication routines.
 */

#include "params.h"

#if (AUTH_PAM || AUTH_PAM_USERPASS) && !VIRTUAL_ONLY

#define _XOPEN_SOURCE 4
#define _XOPEN_SOURCE_EXTENDED
#define _XOPEN_VERSION 4
#define _XPG4_2
#include <string.h>
#include <stdlib.h>
#include <pwd.h>
#include <sys/types.h>

#include <security/pam_appl.h>

#if (defined(__sun) || defined(__hpux)) && \
    !defined(LINUX_PAM) && !defined(_OPENPAM)
#define lo_const			/* Sun's PAM doesn't use const here */
#else
#define lo_const			const
#endif
typedef lo_const void *pam_item_t;

#if USE_LIBPAM_USERPASS
#include <security/pam_userpass.h>

#else

#if AUTH_PAM_USERPASS
#include <security/pam_client.h>

#ifndef PAM_BP_RCONTROL
/* Linux-PAM prior to 0.74 */
#define PAM_BP_RCONTROL	PAM_BP_CONTROL
#define PAM_BP_WDATA	PAM_BP_DATA
#define PAM_BP_RDATA	PAM_BP_DATA
#endif

#define USERPASS_AGENT_ID		"userpass"
#define USERPASS_AGENT_ID_LENGTH	8

#define USERPASS_USER_MASK		0x03
#define USERPASS_USER_REQUIRED		1
#define USERPASS_USER_KNOWN		2
#define USERPASS_USER_FIXED		3
#endif

typedef struct {
	char *user;
	char *pass;
} pam_userpass_t;

static int pam_userpass_conv(int num_msg, lo_const struct pam_message **msg,
	struct pam_response **resp, void *appdata_ptr)
{
	pam_userpass_t *userpass = (pam_userpass_t *)appdata_ptr;
#if AUTH_PAM_USERPASS
	pamc_bp_t prompt;
	const char *input;
	char *output;
	char flags;

	if (num_msg != 1 || msg[0]->msg_style != PAM_BINARY_PROMPT)
		return PAM_CONV_ERR;

	prompt = (pamc_bp_t)msg[0]->msg;
	input = PAM_BP_RDATA(prompt);

	if (PAM_BP_RCONTROL(prompt) != PAM_BPC_SELECT ||
	    strncmp(input, USERPASS_AGENT_ID "/", USERPASS_AGENT_ID_LENGTH + 1))
		return PAM_CONV_ERR;

	flags = input[USERPASS_AGENT_ID_LENGTH + 1];
	input += USERPASS_AGENT_ID_LENGTH + 1 + 1;

	if ((flags & USERPASS_USER_MASK) == USERPASS_USER_FIXED &&
	    strcmp(input, userpass->user))
		return PAM_CONV_AGAIN;

	if (!(*resp = malloc(sizeof(struct pam_response))))
		return PAM_CONV_ERR;

	prompt = NULL;
	PAM_BP_RENEW(&prompt, PAM_BPC_DONE,
		strlen(userpass->user) + 1 + strlen(userpass->pass));
	output = PAM_BP_WDATA(prompt);

	strcpy(output, userpass->user);
	output += strlen(output) + 1;
	memcpy(output, userpass->pass, strlen(userpass->pass));

	(*resp)[0].resp_retcode = 0;
	(*resp)[0].resp = (char *)prompt;
#else
	char *string;
	int i;

#if (defined(__sun) || defined(__hpux)) && \
    !defined(LINUX_PAM) && !defined(_OPENPAM)
/*
 * Insist on only one message per call because of differences in the
 * layout of the "msg" parameter.  It can be an array of pointers to
 * struct pam_message (Linux-PAM, OpenPAM) or a pointer to an array of
 * struct pam_message (Sun PAM).  We only fully support the former.
 */
	if (num_msg != 1)
		return PAM_CONV_ERR;
#endif

	if (!(*resp = malloc(num_msg * sizeof(struct pam_response))))
		return PAM_CONV_ERR;

	for (i = 0; i < num_msg; i++) {
		string = NULL;
		switch (msg[i]->msg_style) {
		case PAM_PROMPT_ECHO_ON:
			string = userpass->user;
		case PAM_PROMPT_ECHO_OFF:
			if (!string)
				string = userpass->pass;
			if (!(string = strdup(string)))
				break;
		case PAM_ERROR_MSG:
		case PAM_TEXT_INFO:
			(*resp)[i].resp_retcode = PAM_SUCCESS;
			(*resp)[i].resp = string;
			continue;
		}

		while (--i >= 0) {
			if (!(*resp)[i].resp) continue;
			memset((*resp)[i].resp, 0, strlen((*resp)[i].resp));
			free((*resp)[i].resp);
			(*resp)[i].resp = NULL;
		}

		free(*resp);
		*resp = NULL;

		return PAM_CONV_ERR;
	}
#endif

	return PAM_SUCCESS;
}
#endif /* USE_LIBPAM_USERPASS */

static int is_user_known(char *user)
{
	struct passwd *pw;

	if ((pw = getpwnam(user)))
		memset(pw->pw_passwd, 0, strlen(pw->pw_passwd));
	endpwent();

	return pw != NULL;
}

struct passwd *auth_userpass(char *user, char *pass, int *known)
{
	struct passwd *pw;
	pam_handle_t *pamh;
	pam_userpass_t userpass;
	struct pam_conv conv = {pam_userpass_conv, &userpass};
	pam_item_t item;
	lo_const char *template;
	int status;

	*known = 0;

	userpass.user = user;
	userpass.pass = pass;

	if (pam_start(AUTH_PAM_SERVICE, user, &conv, &pamh) != PAM_SUCCESS) {
		*known = is_user_known(user);
		return NULL;
	}

	if ((status = pam_authenticate(pamh, 0)) != PAM_SUCCESS) {
		pam_end(pamh, status);
		*known = is_user_known(user);
		return NULL;
	}

	if ((status = pam_acct_mgmt(pamh, 0)) != PAM_SUCCESS) {
		pam_end(pamh, status);
		*known = is_user_known(user);
		return NULL;
	}

	status = pam_get_item(pamh, PAM_USER, &item);
	if (status != PAM_SUCCESS) {
		pam_end(pamh, status);
		*known = is_user_known(user);
		return NULL;
	}
	template = item;

	template = strdup(template);

	if (pam_end(pamh, PAM_SUCCESS) != PAM_SUCCESS || !template) {
		*known = is_user_known(user);
		return NULL;
	}

	if ((pw = getpwnam(template))) {
		memset(pw->pw_passwd, 0, strlen(pw->pw_passwd));
		*known = 1;
	}
	endpwent();

	return pw;
}

#endif

#include <string.h>
#include <stdlib.h>

#define PAM_SM_AUTH
#include <security/pam_modules.h>
#include <security/pam_client.h>

#ifndef PAM_BP_RCONTROL
/* Linux-PAM prior to 0.74 */
#define PAM_BP_RCONTROL	PAM_BP_CONTROL
#define PAM_BP_WDATA	PAM_BP_DATA
#define PAM_BP_RDATA	PAM_BP_DATA
#endif

#include <security/_pam_userpass.h>

PAM_EXTERN int pam_sm_authenticate(pam_handle_t *pamh, int flags,
	int argc, const char **argv)
{
	const void *item;
	const struct pam_conv *conv;
	pamc_bp_t prompt;
	struct pam_message msg, *pmsg;
	struct pam_response *resp;
	const char *user;
	const char *input;
	char *output;
	int status;

	status = pam_get_item(pamh, PAM_CONV, &item);
	if (status != PAM_SUCCESS)
		return status;
	conv = item;

	status = pam_get_item(pamh, PAM_USER, &item);
	if (status != PAM_SUCCESS)
		return status;
	user = item;

	prompt = NULL;
	PAM_BP_RENEW(&prompt, PAM_BPC_SELECT,
		USERPASS_AGENT_ID_LENGTH + 1 + 1 + (user ? strlen(user) : 0));
	output = (char *)PAM_BP_WDATA(prompt);

	memcpy(output, USERPASS_AGENT_ID "/", USERPASS_AGENT_ID_LENGTH + 1);
	output += USERPASS_AGENT_ID_LENGTH + 1;
	if (user && *user) {
		*output++ = USERPASS_USER_KNOWN;
		memcpy(output, user, strlen(user));
	} else
		*output = USERPASS_USER_REQUIRED;

	pmsg = &msg;
	msg.msg_style = PAM_BINARY_PROMPT;
	msg.msg = (const char *)prompt;

	resp = NULL;
	status = conv->conv(1, (const struct pam_message **)&pmsg, &resp,
		conv->appdata_ptr);

	PAM_BP_RENEW(&prompt, 0, 0);

	if (status != PAM_SUCCESS)
		return status;

	if (!resp)
		return PAM_AUTH_ERR;

	prompt = (pamc_bp_t)resp->resp;
	input = (const char *)PAM_BP_RDATA(prompt);

	if (PAM_BP_RCONTROL(prompt) == PAM_BPC_DONE &&
	    strlen(input) + 1 <= PAM_BP_LENGTH(prompt)) {
		status = pam_set_item(pamh, PAM_USER, input);
		if (status == PAM_SUCCESS) {
			input += strlen(input) + 1;
			/* "Note, all non-NULL binary prompts ... are
			 * terminated with a '\0', even when the full
			 * length of the prompt ... does not contain this
			 * delimiter. This is a defined property of the
			 * PAM_BP_RENEW macro, and can be relied upon." */
			status = pam_set_item(pamh, PAM_AUTHTOK, input);
		}
	} else
		status = PAM_AUTH_ERR;

	PAM_BP_RENEW(&prompt, 0, 0);
	free(resp);

	return status;
}

PAM_EXTERN int pam_sm_setcred(pam_handle_t *pamh, int flags,
	int argc, const char **argv)
{
	return PAM_SUCCESS;
}

#ifdef PAM_STATIC
#define pam_sm_chauthtok pam_sm_authenticate
#elif defined(__linux__) && defined(__ELF__)
__asm__(".globl pam_sm_chauthtok; pam_sm_chauthtok = pam_sm_authenticate");
#else
PAM_EXTERN int pam_sm_chauthtok(pam_handle_t *pamh, int flags,
	int argc, const char **argv)
{
	return pam_sm_authenticate(pamh, flags, argc, argv);
}
#endif

#ifdef PAM_STATIC
struct pam_module _pam_userpass_modstruct = {
	"pam_userpass",
	pam_sm_authenticate,
	pam_sm_setcred,
	NULL,
	NULL,
	NULL,
	pam_sm_chauthtok
};
#endif

#include <string.h>
#include <stdlib.h>

#include <security/pam_appl.h>
#include <security/pam_client.h>

#ifndef PAM_BP_RCONTROL
/* Linux-PAM prior to 0.74 */
#define PAM_BP_RCONTROL	PAM_BP_CONTROL
#define PAM_BP_WDATA	PAM_BP_DATA
#define PAM_BP_RDATA	PAM_BP_DATA
#endif

#include <security/_pam_userpass.h>
#include <security/pam_userpass.h>

int pam_userpass_conv(int num_msg, const struct pam_message **msg,
	struct pam_response **resp, void *appdata_ptr)
{
	pam_userpass_t *userpass = (pam_userpass_t *)appdata_ptr;
	pamc_bp_t prompt;
	const char *input;
	char *output;
	char flags;

	if (num_msg != 1 || msg[0]->msg_style != PAM_BINARY_PROMPT)
		return PAM_CONV_ERR;

	prompt = (pamc_bp_t)msg[0]->msg;
	input = (const char *)PAM_BP_RDATA(prompt);

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
	output = (char *)PAM_BP_WDATA(prompt);

	strcpy(output, userpass->user);
	output += strlen(output) + 1;
	memcpy(output, userpass->pass, strlen(userpass->pass));

	(*resp)[0].resp_retcode = 0;
	(*resp)[0].resp = (char *)prompt;

	return PAM_SUCCESS;
}

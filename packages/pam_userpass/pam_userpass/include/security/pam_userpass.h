#ifndef _PAM_USERPASS_H
#define _PAM_USERPASS_H

#include <security/pam_appl.h>

typedef struct {
	char *user;
	char *pass;
} pam_userpass_t;

extern int pam_userpass_conv(int num_msg, const struct pam_message **msg,
	struct pam_response **resp, void *appdata_ptr);

#endif

#include <stdio.h>
#include <string.h>

#include <security/pam_userpass.h>

#define SERVICE				"example_userpass"

static char *auth_pam_userpass(const char *user, const char *pass)
{
	pam_handle_t *pamh;
	pam_userpass_t userpass;
	struct pam_conv conv = {pam_userpass_conv, &userpass};
	const char *template;
	char *retval;
	int status;

	userpass.user = user;
	userpass.pass = pass;

	if (pam_start(SERVICE, user, &conv, &pamh) != PAM_SUCCESS)
		return NULL;

	if ((status = pam_authenticate(pamh, 0)) != PAM_SUCCESS) {
		pam_end(pamh, status);
		return NULL;
	}

	if ((status = pam_acct_mgmt(pamh, 0)) != PAM_SUCCESS) {
		pam_end(pamh, status);
		return NULL;
	}

	status = pam_get_item(pamh, PAM_USER, (const void **)&template);
	if (status != PAM_SUCCESS) {
		pam_end(pamh, status);
		return NULL;
	}

	retval = strdup(template);

	if (pam_end(pamh, PAM_SUCCESS) != PAM_SUCCESS)
		return NULL;

	return retval;
}

int main(int argc, char **argv)
{
	char *user;

	if (argc != 3) {
		printf("Usage: %s USER PASS\n",
			argv[0] ? argv[0] : "example_userpass");
		return 0;
	}

	user = auth_pam_userpass(argv[1], argv[2]);
	printf(user ? "User \"%s\"\n" : "Authentication failed\n", user);

	return 0;
}

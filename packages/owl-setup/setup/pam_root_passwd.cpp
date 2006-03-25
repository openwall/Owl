#include <string.h>
#include <stdlib.h>
#include <security/pam_appl.h>
#include "scriptpp/scrvar.hpp"

#include "iface.hpp"

struct pam_data {
    OwlInstallInterface *the_iface;
    ScriptVariable info;
};

static int str_request(pam_data* data, const char *prompt, bool blind,
                       char **response)
{
    if(data->info != "") {
        data->the_iface->Message(data->info);
        data->info = "";
    }
    ScriptVariable res = data->the_iface->QueryString(prompt, blind);
    if(res == OwlInstallInterface::qs_cancel ||
       res == OwlInstallInterface::qs_escape ||
       res == OwlInstallInterface::qs_eof)
    {
        return PAM_CONV_ERR;
    }
    *response = strdup(res.c_str());
    return PAM_SUCCESS;
}

static int conv_fun(int num_msg, const struct pam_message **msg,
                    struct pam_response **resp, void *data)
{
    pam_data *pd = (pam_data*)data;
    OwlInstallInterface *the_iface = pd->the_iface;
    
    if(num_msg != 1) {
        the_iface->Message("Unexpected multiop within PAM conversation");
        return PAM_CONV_ERR;
    }

    *resp = (pam_response*) calloc(sizeof(pam_response), 1);
        // remember calloc() fills the memory with 0s

    const char *pr = (*msg)->msg;
    bool blind = false;
    switch((*msg)->msg_style) {
        case PAM_PROMPT_ECHO_OFF:
            blind = true; /* no break here -- intensionally */
        case PAM_PROMPT_ECHO_ON:
            return str_request(pd, pr, blind, &((*resp)->resp));
        case PAM_ERROR_MSG:
            the_iface->Message(ScriptVariable("PAM ERROR: ") + pr);
            return PAM_SUCCESS;
        case PAM_TEXT_INFO:
            pd->info += pr;
            return PAM_SUCCESS;
        default:
            return PAM_CONV_ERR;
    }
}


void pam_root_passwd(OwlInstallInterface *the_iface)
{
    struct pam_data pd;
    pam_handle_t *ph;
    struct pam_conv pc = { conv_fun, (void*)&pd };

    pd.the_iface = the_iface;
    pd.info = "";

    int r = pam_start("passwd", "root", &pc, &ph);
    if(r != PAM_SUCCESS) {
        the_iface->Message(ScriptVariable(0, "PAM ERROR: %s\n",
                                          pam_strerror(ph, r)));
    }

    r = pam_chauthtok(ph, 0);
    if(r != PAM_SUCCESS) {
        the_iface->Message(ScriptVariable(0, "PAM ERROR: %s\n",
                                          pam_strerror(ph, r)));
    }

    pam_end(ph, r);
}

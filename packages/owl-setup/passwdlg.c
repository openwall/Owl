/*********************************************************************/
/* passwdlg -- passwd with hooks                                     */
/*                                                                   */
/* Based on passwd from SimplePAMApps by Andrew G. Morgan            */
/*                                       <morgan@linux.kernel.org>   */
/*                                                                   */
/* Compile: gcc passwdlg.c -o passwdlg -lpam -Wall                   */
/*                                                                   */
/* Example:                                                          */
/*  passwdlg -e 'dialog --passwordbox "$PAM_MSG" 0 0'                */
/*           -E 'dialog --inputbox "$PAM_MSG" 0 0'\                  */
/*           -m 'dialog --msgbox "$PAM_MSG" 0 0' \                   */
/*           -u USER \                                               */
/*           -s SERVICE                                              */
/*********************************************************************/

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>

#include <sys/types.h>
#include <sys/wait.h>

#include <security/pam_appl.h>
#include <security/pam_misc.h>

extern char **environ;

static char *echo_on_cmd = NULL, *echo_off_cmd = NULL, *msg_cmd = NULL;

#define MAXSTR   1024            // Buffer size for input string
#define MSG_SZ   2048            // Buffer size for conversation messages

#define SERVICE  "passwd"

static char *user = NULL, *service = SERVICE;
static char *msg_str = NULL;     // Buffer for conversation messages

/* From Solar Designer's popa3d */
/*
 * Attempts to read until EOF, and returns the number of bytes read.
 * We don't expect any signals, so even EINTR is considered an error.
 */
static int read_loop(int fd, char *buffer, int count)
{
    int offset, block;

    offset = 0;
    while (count > 0) {
        block = read(fd, &buffer[offset], count);

        if (block < 0) return block;
        if (!block) return offset;

        offset += block;
        count -= block;
    }

    return offset;
}

char *run_cmd(char *cmd) 
{
    int status, asize;
    int chan[2];
    char *argv[4], *buff;

    buff = malloc(MAXSTR + 1);
    if (buff == NULL) 
        return NULL;

    if (pipe(chan)) {
        perror("pipe");
        return NULL;
    }

    switch (fork()) {
    case -1:
        perror("fork");
        return NULL;

    case 0:
        close(chan[0]);
        close(2);
        dup2(chan[1], 2);

        argv[0] = "sh";
        argv[1] = "-c";
        argv[2] = cmd;
        argv[3] = 0;
        execve("/bin/sh", argv, environ);
        return NULL;
    }

    if (close(chan[1])) {
        perror("close");
        return NULL;
    } else
        do {
            if (wait(&status) == -1) {
                if (errno != EINTR) {
                    perror("waitpid");
                    return NULL;
                } 
            } else {
                if ((asize = read_loop(chan[0], buff, MAXSTR)) < 0)
                    return NULL;
		buff[asize] = '\0';

                if (close(chan[0])) {
                    perror("close");
                    return NULL;
                }

                if (WEXITSTATUS(status) == 0) {
                    return buff;
                } else {
                    fprintf(stderr, "run_cmd: %s\n", buff);
                    return NULL;
                }
            }
        } while(1);
}

int run_conv(int num_msg, const struct pam_message **msgm,
	struct pam_response **response, void *appdata_ptr)
{

    int count = 0;
    struct pam_response *reply;

    if (num_msg <= 0)
        return PAM_CONV_ERR;

    reply = (struct pam_response *)calloc(num_msg, sizeof(struct pam_response));
    if (reply == NULL)
        return PAM_CONV_ERR;

    for (count = 0; count < num_msg; ++count) {
        char *string = NULL;

        switch (msgm[count]->msg_style) {
        case PAM_PROMPT_ECHO_OFF:
            if (msg_str != NULL) {
                strncat(msg_str, msgm[count]->msg, MSG_SZ - strlen(msg_str) - 1);
            } else {
                msg_str = strdup(msgm[count]->msg);
            }

            setenv("PAM_MSG", msg_str, 1);
            string = run_cmd(echo_off_cmd);

            free(msg_str);
            msg_str = NULL;

            if (string == NULL) 
                goto failed_conversation;
            break;
        case PAM_PROMPT_ECHO_ON:
            setenv("PAM_MSG", msgm[count]->msg, 1);
            string = run_cmd(echo_on_cmd);
            if (string == NULL) 
                goto failed_conversation;
            break;
        case PAM_ERROR_MSG:
            setenv("PAM_MSG", msgm[count]->msg, 1);
            string = run_cmd(msg_cmd);
            if (string == NULL) 
                goto failed_conversation;
	    break;
        case PAM_TEXT_INFO:
            if (msg_str == NULL) {
                msg_str = malloc(MSG_SZ);
		if (!msg_str) goto failed_conversation;
		msg_str[0] = '\0';
            }
            strncat(msg_str, msgm[count]->msg, MSG_SZ -	strlen(msg_str) - 1);
	    strncat(msg_str, "\n", MSG_SZ - strlen(msg_str) - 1);
            break;
        default:
            fprintf(stderr, "erroneous conversation (%d)\n",
		msgm[count]->msg_style);
            goto failed_conversation;
        }
        if (string) {                         
            /* must add to reply array */
            /* add string to list of responses */                               
            reply[count].resp_retcode = 0;                                      
            reply[count].resp = string;                                         
            string = NULL;
        }
    }

    *response = reply;
    reply = NULL;

    return PAM_SUCCESS;

failed_conversation:
    if (reply) {
        for (count=0; count<num_msg; ++count) {
            if (reply[count].resp == NULL) 
                continue;

            switch (msgm[count]->msg_style) {
            case PAM_PROMPT_ECHO_ON:
            case PAM_PROMPT_ECHO_OFF:
                _pam_overwrite(reply[count].resp);
                free(reply[count].resp);
                break;
            case PAM_ERROR_MSG:
            case PAM_TEXT_INFO:
                /* should not actually be able to get here... */
                free(reply[count].resp);
            }                                            
            reply[count].resp = NULL;
        }
        /* forget reply too */
        free(reply);
        reply = NULL;
    }

    return PAM_CONV_ERR;
}

static struct pam_conv conv = {
    run_conv,
    NULL
};

void usage(void) 
{
    printf("Usage:\n");
    printf(" run -e <cmd> -E <cmd> -m <cmd> -u username\n");
    printf("      -e <cmd>   PAM_PROMPT_ECHO_OFF hook\n");
    printf("      -E <cmd>   PAM_PROMPT_ECHO_ON hook\n");
    printf("      -m <cmd>   PAM_ERROR_MSG hook\n");
    printf("      -u USER    username\n");
    printf("      -s SERVICE PAM service name\n");
    printf("\n");
}

void parse_args(int argc, char * const argv[])
{
    int c;

    while (1) {
        c = getopt(argc, argv, "e:E:m:u:s:");
        if (c == -1)
            break;
        switch (c) {
        case 'e':
            echo_off_cmd = strdup(optarg);
            break;
        case 'E':
            echo_on_cmd = strdup(optarg);
            break;
        case 'm':
            msg_cmd = strdup(optarg);
            break;
        case 'u':
            user = strdup(optarg);
            break;
	case 's':
	    service = strdup(optarg);
	    break;
        case '?':
        case ':':
            usage();
            exit(1);
        }
    }

    if (!(echo_on_cmd && echo_off_cmd && msg_cmd && user)) {
        usage();
        exit(1);
    }
}

int main(int argc, char * const argv[])
{
    pam_handle_t *pamh = NULL;
    char *pam_msg;
    int retval;

    parse_args(argc, argv);

    retval = pam_start(service, user, &conv, &pamh);

    while (retval == PAM_SUCCESS) {      /* use loop to avoid goto... */
        retval = pam_chauthtok(pamh, 0);
        if (retval != PAM_SUCCESS)
            break;

        retval = pam_end(pamh, PAM_SUCCESS);
        if (retval != PAM_SUCCESS)
            break;

        setenv("PAM_MSG", "Password changed", 1);
        run_cmd(msg_cmd);

        exit(0);
    }

    if (retval != PAM_SUCCESS) {
	asprintf(&pam_msg, "PAM: %s.\n\nPassword not changed.",
	    pam_strerror(pamh, retval));
	if (pam_msg) {
	    setenv("PAM_MSG", pam_msg, 1);
	    run_cmd(msg_cmd);
	}
    }

    if (pamh != NULL) {
        (void) pam_end(pamh, PAM_SUCCESS);
        pamh = NULL;
    }

    exit(1);
}

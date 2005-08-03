#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#include "iface.hpp"

void run_shell(OwlInstallInterface *the_iface)
{
    const char *s = getenv("SHELL");
    if(!s) {
        s = "/bin/sh";
    }
    the_iface->ExecWindow("Running shell interpreter; "
                          "type ``exit'' to leave it");
    if(fork() == 0) {
        setenv("PS1", "# ", 1);
        execl(s, s, 0);
        exit(1);
    }
    int status;
    wait(&status);
    the_iface->CloseExecWindow();
}

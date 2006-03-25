#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>

#include "cmd.hpp"
#include "iface.hpp"
#include "config.hpp"

#if 0
void set_root_password(OwlInstallInterface *the_iface)
{
    PreserveTerminalMode mode;
    the_iface->ExecWindow(ScriptVariable("Invoking ") +
                          the_config->PasswdPath() +
                          " within " + the_config->OwlRoot());
    ChrootExecWait passwd(the_config->OwlRoot().c_str(),
                          the_config->PasswdPath().c_str(),
                          "root", 0);
    the_iface->CloseExecWindow();
}
#else

/* defined in pam_root_passwd.cpp */
void pam_root_passwd(OwlInstallInterface *the_iface);

static void do_passwd(OwlInstallInterface *the_iface)
{
    int r = chroot(the_config->OwlRoot().c_str());
    if(r == -1) {
        the_iface->Message("Couldn't chroot, password unchanged");
        return;
    }
    pam_root_passwd(the_iface);
}

void set_root_password(OwlInstallInterface *the_iface)
{
    int pid = fork();
    switch(pid) {
        case -1:
            the_iface->Message("Couldn't fork(), password unchanged");
            return;
        case 0:
            do_passwd(the_iface);
            exit(0);
        default:
            waitpid(pid, 0, 0);
    }
}
#endif

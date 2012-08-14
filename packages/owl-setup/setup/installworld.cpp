#include <unistd.h>
#include <stdlib.h>

#include "iface.hpp"
#include "cmd.hpp"
#include "config.hpp"

void install_packages(OwlInstallInterface *the_iface)
{
    the_iface->ExecWindow("Installing packages");
    chdir(the_config->WorldDir().c_str());
    putenv((char*)"KERNEL_FAKE=no");
    ExecAndWait mkinst(the_config->MakePath().c_str(),
                the_config->InstallWorldTarget().c_str(), (const char *)0);
    unsetenv("KERNEL_FAKE");
    the_iface->CloseExecWindow(true);
    if(!mkinst.Success()) {
        the_iface->Message("There were problems during packages installation");
    }
}

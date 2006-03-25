#include <unistd.h>

#include "iface.hpp"
#include "cmd.hpp"
#include "config.hpp"

void install_packages(OwlInstallInterface *the_iface)
{
    the_iface->ExecWindow("Installing packages");
    chdir(the_config->WorldDir().c_str());
    ExecAndWait mkinst(the_config->MakePath().c_str(),
                the_config->InstallWorldTarget().c_str(), 0);
    the_iface->CloseExecWindow(true);
    if(!mkinst.Success()) {
        the_iface->Message("There were problems during packages installation");
    }
}

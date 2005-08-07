#include "cmd.hpp"
#include "iface.hpp"
#include "config.hpp"

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

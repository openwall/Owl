#include "cmd.hpp"
#include "iface.hpp"
#include "config.hpp"

void set_root_password(OwlInstallInterface *the_iface)
{
    PreserveTerminalMode mode;
    the_iface->ExecWindow(ScriptVariable("Invoking ") +
                          the_config->PasswdPath());
    ExecAndWait passwd(the_config->PasswdPath().c_str(), "root", 0);
    the_iface->CloseExecWindow();
}

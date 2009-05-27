#if defined(__i386__) || defined(__x86_64__)

#include <unistd.h>

#include "iface.hpp"
#include "cmd.hpp"
#include "config.hpp"
#include "state.hpp"

   /* implemented in select_partitions.cpp */
void unmount_all(OwlInstallInterface *the_iface);



void reboot_it(OwlInstallInterface *the_iface)
{
    bool res = the_iface->YesNoMessage("Really reboot the system?");
    if(!res) return;
    the_iface->Notice("Unmounting partitions...");
    unmount_all(the_iface);

    ScriptVariable runlevel = get_runlevel();
    the_iface->Notice(ScriptVariable(0, "Runlevel is [%s]...",
                                        runlevel.c_str()));

    bool r;
    if(runlevel == "2" || runlevel == "3" ||
       runlevel == "4" || runlevel == "5")
    {
        the_iface->ExecWindow("Invoking /sbin/shutdown -r now");
        ExecAndWait shut("/sbin/shutdown", "-r", "now", (const char *)0);
        the_iface->CloseExecWindow();
        r = shut.Success();
    } else {
        the_iface->ExecWindow("Doesn't seem to be multiuser, "
                          "preparing for a hard reboot");
        ExecAndWait(the_config->UmountPath().c_str(), "-far", (const char *)0);
        ExecAndWait(the_config->MountPath().c_str(),
                           "-no", "remount,ro", "/", (const char *)0);
        the_iface->Notice("Invoking /sbin/reboot -df");
        ExecAndWait shut("/sbin/reboot", "-df", (const char *)0);
        the_iface->CloseExecWindow();
        r = shut.Success();
    }
    if(r) {
        the_iface->Notice("Rebooting the system, good bye");
        while(1) pause();
    } else {
        the_iface->Message("Failed to proceed, please reboot manually");
    }
}

#endif // __i386__ || __x86_64__

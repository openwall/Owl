#include <stdio.h>

#include "scriptpp/scrvar.cpp"
#include "scriptpp/scrvect.cpp"

#include "cmd.hpp"
#include "iface.hpp"
#include "state.hpp"
#include "config.hpp"


static ScriptVariable get_root_device()
{
    ScriptVector dirs, parts;
    enumerate_owl_dirs(dirs, parts);
    for(int i=0; i<dirs.Length(); i++) {
        if(dirs[i] == "/")
            return parts[i];
    }
    return "";
}

void install_kernel_and_lilo(OwlInstallInterface *the_iface)
{
    ScriptVariable root_dev = get_root_device();
    if(root_dev == "") {
        the_iface->Message("Unable to determine root device.  Aborted.");
        return;
    }

    the_iface->Notice("Now choose what device will hold your boot loader\n"
                      "(e.g., /dev/hda for the first IDE disk).");
    ScriptVariable boot_dev =
        the_iface->QueryString("What is your boot device?");
    the_iface->ClearNotices();
    if(boot_dev == "" || boot_dev == OwlInstallInterface::qs_cancel
                      || boot_dev == OwlInstallInterface::qs_eof)
        return;

    the_iface->ExecWindow("Copying files...");
    ExecAndWait(the_config->CpPath().c_str(),
                the_config->DefaultKernel().c_str(),
                the_config->TargetKernel().c_str(), 0);
    ExecAndWait(the_config->CpPath().c_str(),
                the_config->DefaultKernelMap().c_str(),
                the_config->TargetKernelMap().c_str(), 0);
    the_iface->CloseExecWindow();

    FILE* f = fopen(the_config->LiloconfFile().c_str(), "w");
    if(!f) {
        the_iface->Message(ScriptVariable("Failed to open ") +
                           the_config->LiloconfFile());
        return;
    }
    fprintf(f,
            "boot=%s\n\nimage=%s\n\tlabel=%s\n\tread-only\n\troot=%s\n",
            boot_dev.c_str(),
            "/boot/bzImage",
            "Linux",
            root_dev.c_str());
    fclose(f);

    the_iface->ExecWindow(ScriptVariable("Invoking ") +
                          the_config->LiloPath() +
                          " within " + the_config->OwlRoot());
    ChrootExecWait lilo(the_config->OwlRoot().c_str(),
                        the_config->LiloPath().c_str(), 0);
    the_iface->CloseExecWindow();
    if(!lilo.Success())
        the_iface->Message("Warning: LILO failed");
}

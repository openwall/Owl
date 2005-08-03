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
        the_iface->Message("Unable to determine root device. Aborted");
        return;
    }

    the_iface->Notice("Now choose what device will hold your boot "
                      "loader; e.g., /dev/hda for the first IDE disk "
                      "or /dev/hda1 for its first partition");
    ScriptVariable boot_dev =
        the_iface->QueryString("What is your boot device?");
    if(boot_dev == "" || boot_dev == OwlInstallInterface::qs_cancel
                      || boot_dev == OwlInstallInterface::qs_eof)
        return;

    ExecAndWait(the_config->CpPath().c_str(),
                the_config->DefaultKernel().c_str(),
                the_config->TargetKernel().c_str(), 0);

    ExecAndWait(the_config->CpPath().c_str(),
                the_config->DefaultKernelMap().c_str(),
                the_config->TargetKernelMap().c_str(), 0);

    FILE* f = fopen(the_config->LiloconfFile().c_str(), "w");
    if(!f) {
        the_iface->Message("Couldn't open your lilo.conf file");
        return;
    }
    fprintf(f,
            "boot=%s\n\nimage=%s\n\tlabel=%s\n\tread-only\n\troot=%s\n",
            boot_dev.c_str(),
            "/boot/bzImage",
            "Linux",
            root_dev.c_str());
    fclose(f);

    the_iface->ExecWindow("Executing lilo");
    ChrootExecWait lilo(the_config->OwlRoot().c_str(),
                        the_config->LiloPath().c_str(), 0);
    the_iface->CloseExecWindow();
    if(!lilo.Success())
        the_iface->Message("Warning: lilo failed");
}


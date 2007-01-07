#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

#include "iface.hpp"
#include "cmd.hpp"
#include "config.hpp"

void repartition_hard_drive(OwlInstallInterface *the_iface, bool use_cfdisk)
{
    IfaceSingleChoice *dm = the_iface->CreateSingleChoice();

    //
    {
        ExecResultParse fdisk(the_config->FdiskPath().c_str(), "-l", 0);
        ScriptVector v;
        ScriptVariable defval;
        while(fdisk.ReadLine(v, 1)) {
            if(v[0].Range(0,5).Get()=="Disk ") {
                ScriptVariable::Substring sub(v[0].Range(5));
                ScriptVariable::Substring disk;
                sub.FetchToken(disk, ":(", " \n\t\r");
                dm->AddItem(disk.Get(), sub.Get());
                if(defval == "") defval = disk.Get();
            }
        }
        dm->AddItem("q", "quit (return to main menu)");
        dm->SetDefault(defval);
    }
    for(;;) {
        ScriptVariable choice = dm->Run();
        if(choice=="q" || choice=="" ||
           choice == OwlInstallInterface::qs_cancel ||
           choice == OwlInstallInterface::qs_escape ||
           choice == OwlInstallInterface::qs_eof)
        {
            return;
        }
        ScriptVariable fds = use_cfdisk ?
            the_config->CfdiskPath() : the_config->FdiskPath();
        ScriptVariable msg = ScriptVariable("Invoking ") +
                             fds + " " + choice + "\n";
        if(use_cfdisk) {
        } else {
            msg += "When you're done, type \"w\" to save changes \n"
                   "or \"q\" to abort\n";
        }

        the_iface->ExecWindow(msg);
        ExecAndWait(fds.c_str(), choice.c_str(), 0);
        the_iface->CloseExecWindow();
    }
    delete dm;
}

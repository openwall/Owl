#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

#include "iface.hpp"
#include "cmd.hpp"
#include "config.hpp"

void repartition_hard_drive(OwlInstallInterface *the_iface)
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
                sub.FetchToken(disk, ":", " \n\t\r");
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
        the_iface->ExecWindow(ScriptVariable("Invoking ") +
                              the_config->FdiskPath() + " " + choice + "\n"
                              "When you're done, type \"w\" to save changes "
                              "or \"q\" to abort\n");
        ExecAndWait(the_config->FdiskPath().c_str(), choice.c_str(), 0);
        the_iface->CloseExecWindow();
    }
    delete dm;
}

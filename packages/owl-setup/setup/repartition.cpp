#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

#include "iface.hpp"
#include "cmd.hpp"
#include "config.hpp"

// defined in part_scan.cpp
void scan_proc_partitions(ScriptVector &result);

void repartition_hard_drive(OwlInstallInterface *the_iface,
                            bool use_cfdisk, bool select_fdisk)
{
    IfaceSingleChoice *dm = the_iface->CreateSingleChoice();

    //
    {
        ScriptVariable defval;
#if 0
        ExecResultParse fdisk(the_config->FdiskPath().c_str(), "-l", 0);
        ScriptVector v;
        while(fdisk.ReadLine(v, 1)) {
            if(v[0].Range(0,5).Get()=="Disk ") {
                ScriptVariable::Substring sub(v[0].Range(5));
                ScriptVariable::Substring disk;
                sub.FetchToken(disk, ":(", " \n\t\r");
                dm->AddItem(disk.Get(), sub.Get());
                if(defval == "") defval = disk.Get();
            }
        }
#else
        ScriptVector v;
        scan_proc_partitions(v);
        for(int i=0; i<v.Length(); i++)
            dm->AddItem(v[i].Range(5).Get(), v[i]);
        defval = v[0].Range(5).Get();
#endif
        dm->AddItem("q", "quit (return to main menu)");
        dm->SetDefault(defval);
    }
    if(select_fdisk) {
        IfaceSingleChoice *pm = the_iface->CreateSingleChoice();
        pm->SetCaption("Select fdisk program to use");
        pm->AddItem("f", "Use traditional fdisk");
        pm->AddItem("c", "Use ncurses-based cfdisk");
        pm->AddItem("x", "Cancel, return to main menu");
        if(use_cfdisk) pm->SetDefault("c");
        ScriptVariable res = pm->Run();
        delete pm;
        if(res == "f")
            use_cfdisk = false;
        else if(res == "c")
            use_cfdisk = true;
        else {
            delete dm;
            return;
        }
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

#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

#include "iface.hpp"
#include "cmd.hpp"
#include "state.hpp"
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
        ExecResultParse fdisk(the_config->FdiskPath().c_str(), "-l", (const char *)0);
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
        if(!v.Length()) {
            the_iface->Message("No suitable devices found.\n"
                               "This may be because you do not in fact have "
                               "any hard disks or similar\n"
                               "devices connected, or it may be because you "
                               "do not have drivers for the\n"
                               "appropriate controllers "
                               "loaded into the kernel.");
            return;
        }
        for(int i=0; i<v.Length(); i++)
            dm->AddItem(v[i], ScriptVariable("/dev/")+v[i]);
        defval = v[0];
#endif
        dm->AddItem("q", "Quit, return to main menu");
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
        ScriptVariable dev = ScriptVariable("/dev/") + choice;
        bool dev_m = is_device_mounted(dev);
        bool dev_s = !dev_m && is_device_swap(dev);
        if(dev_m || dev_s)
            the_iface->Message(dev + " appears to have " +
                               (dev_m ? "mounted" : "active swap") +
                               " partitions.\n"
                               "If you apply any changes to its partition "
                               "table now, those will likely\n"
                               "not take effect until reboot.  The fdisk "
                               "program will indicate this error,\n"
                               "and you'd be required to reboot "
                               "before you're able to reliably create\n"
                               "filesystems and so on.\n"
                               "It is strongly recommended that you cancel "
                               "and " +
                               (dev_m ? "unmount your filesystem" :
                               "deactivate your swap") + "(s).");
        ScriptVariable fds = use_cfdisk ?
            the_config->CfdiskPath() : the_config->FdiskPath();
        ScriptVariable msg = ScriptVariable("Invoking ") +
                             fds + " " + dev + "\n";
        if(use_cfdisk) {
        } else {
            msg += "When you're done, type \"w\" to save changes \n"
                   "or \"q\" to abort\n";
        }

        the_iface->ExecWindow(msg);
        ExecAndWait fdisk(fds.c_str(), dev.c_str(), (const char *)0);
        the_iface->CloseExecWindow();
        if (!fdisk.Success())
            the_iface->Message(ScriptVariable("The fdisk program indicates "
                               "that an error occurred.") +
                               ((dev_m || dev_s) ?
                               "\nIf you have updated the partition table "
                               "despite of the device being in use,\n"
                               "you need to reboot now." : ""));
    }
    delete dm;
}

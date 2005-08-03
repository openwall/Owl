#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#include "scriptpp/scrvect.hpp"

#include "cmd.hpp"
#include "iface.hpp"
#include "state.hpp"
#include "config.hpp"

static void mount_at(OwlInstallInterface *the_iface,
                     ScriptVariable part,
                     ScriptVariable mountpoint)
{
    if(is_mounted(part)) {
        the_iface->Message(part + " seems to be already mounted (why?..)");
        return;
    }

    IfaceSingleChoice *pm = the_iface->CreateSingleChoice();
    pm->SetCaption(ScriptVariable("Do you want to format ")+part+"?");

    pm->AddItem("ext2", "Format as ext2 filesystem");
    pm->AddItem("ext3", "Format as ext3 filesystem");
    pm->AddItem("no", "Don't format it! try mount now");
    pm->AddItem("q", "Quit/cancel");

    ScriptVariable choice = pm->Run();
    delete pm;
    if(choice=="q" || choice=="" ||
       choice == OwlInstallInterface::qs_cancel ||
       choice == OwlInstallInterface::qs_escape ||
       choice == OwlInstallInterface::qs_eof)
    {
        return;
    }

    if(choice != "no") {
        bool r = the_iface->YesNoMessage(
            ScriptVariable("Warning! All the data at ")+part+
            " will be lost!\nAre you really sure you want to format it?"
        );
        if(!r) return;
    }

    bool format_success = true;
    if(choice == "ext2" || choice == "ext3") {
        ExecAndWait e(the_config->MkfsPath(choice).c_str(), part.c_str(), 0);
        format_success = e.Success();
    }
    if(!format_success) {
        the_iface->Message("Formatting failed");
        return;
    }

    ScriptVariable mp(the_config->OwlRoot());
    if(mountpoint != "/")
        mp += mountpoint;
    ExecAndWait mkdir(the_config->MkdirPath().c_str(), "-p", mp.c_str(), 0);
    sync();
    chmod(mp.c_str(), 0755);
    sync();
      /* now we need all the operations with the dir to be completed */
    usleep(500000); /* yes, I know this is dirty -- so, what would you
                       recommend instead? */
    ExecAndWait mnt(the_config->MountPath().c_str(),
                    part.c_str(), mp.c_str(), 0);

    if(!mnt.Success()) {
        the_iface->Message("Mount failed");
    }
}

static void add_mount(OwlInstallInterface *the_iface,
                      ScriptVariable part)
{
    ScriptVariable mp;
    do {
        ScriptVariable prompt(0,
            "Please enter the mount point for %s "
            "(e.g. /usr, /home, /var, ...)",
            part.c_str());
        mp = the_iface->QueryString(prompt);
        if(mp == "" ||
           mp == OwlInstallInterface::qs_cancel ||
           mp == OwlInstallInterface::qs_escape ||
           mp == OwlInstallInterface::qs_eof)
        {
            return;
        }
    } while(mp[0] != '/');
    mount_at(the_iface, part, mp);
}

void unmount_all(OwlInstallInterface *the_iface)
{
    ScriptVector parts, dirs;
    enumerate_owl_dirs(dirs, parts);

    bool sorted = true;
    do {
        sorted = true;
        for(int j=0; j<dirs.Length()-1; j++) {
            if(dirs[j].Length() < dirs[j+1].Length()) {
                ScriptVariable tmp = dirs[j];
                dirs[j] = dirs[j+1];
                dirs[j+1] = tmp;
                sorted = false;
            }
        }
    } while(!sorted);
    for(int i=0; i<dirs.Length(); i++) {
        ScriptVariable mp(the_config->OwlRoot());
        mp += dirs[i];
        ExecAndWait umnt(the_config->UmountPath().c_str(), mp.c_str(), 0);
        if(!umnt.Success()) {
            the_iface->Message(ScriptVariable("umount failed for ") + mp);
        }
    }
}

static void view_tree(OwlInstallInterface *the_iface)
{
    ScriptVector parts, dirs;
    enumerate_owl_dirs(dirs, parts);

    ScriptVariable msg;

    for(int i=0; i<parts.Length(); i++) {
        while(parts[i].Length() < 20) parts[i] += " ";
        msg += parts[i];
        msg += dirs[i];
        msg += "\n";
    }

    the_iface->Message(msg);
}

static void enumerate_available_partitions(ScriptVector &res)
{
    ScriptVector parts, m_parts, dirs;
    enumerate_linux_partitions(parts);
    enumerate_owl_dirs(dirs, m_parts);

    res.Clear();

    for(int i=0; i<parts.Length(); i++) {
        bool avail = true;
        for(int j = 0; j<m_parts.Length(); j++) {
            if(parts[i] == m_parts[j]) {
                avail = false;
                break;
            }
        }
        if(avail) {
            res.AddItem(parts[i]);
        }
    }

}

void select_and_mount_partitions(OwlInstallInterface *the_iface)
{
    for(;;) {
        if(!owl_dir_mounted()) { // we need the root partition
            ScriptVector parts;
            enumerate_linux_partitions(parts);
            IfaceSingleChoice *pm = the_iface->CreateSingleChoice();
            pm->SetCaption("Select your root partition");

            for(int i=0; i<parts.Length(); i++) {
                pm->AddItem(parts[i],
                            ScriptVariable(0, "Select %s as your root",
                                              parts[i].c_str()));
            }
            pm->AddItem("q", "Quit/cancel");
            if(parts.Length()>0) {
                pm->SetDefault(parts[0]);
            }
            ScriptVariable choice = pm->Run();
            delete pm;
            if(choice == "q" || choice == "" ||
               choice == OwlInstallInterface::qs_eof ||
               choice == OwlInstallInterface::qs_escape ||
               choice == OwlInstallInterface::qs_cancel)
            {
                return;
            }
            mount_at(the_iface, choice, "/");
        } else {
            ScriptVector parts;
            enumerate_available_partitions(parts);
            IfaceSingleChoice *pm = the_iface->CreateSingleChoice();
            pm->SetCaption("Partitions selection");
            pm->AddItem("v", "View the current tree");
            for(int i=0; i<parts.Length(); i++) {
                pm->AddItem(parts[i],
                            ScriptVariable(0,
                                           "Attach %s somewhere to the tree",
                                           parts[i].c_str()));
            }
            pm->AddItem("u", "Unmount all, select another root");
            pm->AddItem("q", "Done, return to main menu");
            if(parts.Length()>0) {
                pm->SetDefault(parts[0]);
            } else {
                pm->SetDefault("q");
            }
            ScriptVariable choice = pm->Run();
            if(choice == "q" || choice == "" ||
               choice == OwlInstallInterface::qs_eof ||
               choice == OwlInstallInterface::qs_escape ||
               choice == OwlInstallInterface::qs_cancel)
            {
                return;
            }
            else if(choice=="u")
                unmount_all(the_iface);
            else if(choice=="v")
                view_tree(the_iface);
            else add_mount(the_iface, choice);
        }
    }
}

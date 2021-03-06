#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>
#include <string.h>

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
    pm->SetCaption(ScriptVariable("Do you want to format ") + part + "?");

    pm->AddItem("ext2", "Format as ext2 filesystem");
    pm->AddItem("ext3", "Format as ext3 filesystem");
    pm->AddItem("ext4", "Format as ext4 filesystem (recommended)");
    pm->AddItem("no", "Don't format it, try to mount now");
    pm->AddItem("q", "Quit/cancel");

    pm->SetDefault("ext4");

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
            ScriptVariable("Warning: all data on ") + part + " will be lost!\n"
                           "Are you really sure you want to format it?");
        if(!r) return;
    }

    ScriptVariable fstype = "";
    if(choice == "ext2" || choice == "ext3" || choice == "ext4") {
        the_iface->ExecWindow("Executing mkfs...");
        ExecAndWait e(the_config->MkfsPath(choice).c_str(), part.c_str(), (const char *)0);
        the_iface->CloseExecWindow();
        if(!e.Success()) {
            the_iface->Message("Formatting failed");
            return;
        }
        fstype = choice;
    }

    ScriptVariable mp(the_config->OwlRoot());
    if(mountpoint != "/")
        mp += mountpoint;

    ScriptVector mpv(mp, "/", "");
    ScriptVariable pp;
    for(int i=0; i<mpv.Length(); i++) {
        pp += "/";
        pp += mpv[i];

        FileStat thedir(pp.c_str());
        if(!thedir.IsDir()) {
            int res = mkdir(pp.c_str(), 0755);
            if(res == -1) {
                the_iface->Message(ScriptVariable(0,
                    "Failed to create directory: %s: %s",
                    pp.c_str(), strerror(errno)));
            }

        }
        chmod(pp.c_str(), 0755);
    }
    chmod(mp.c_str(), 0700);
    sync();
    the_iface->ExecWindow("Executing mount...");
    if (fstype == "") {
        ExecAndWait mnt(the_config->MountPath().c_str(),
                        part.c_str(), mp.c_str(), "-onoatime",
                        (const char *)0);
/*
 * For an ext4 filesystem, the kernel happens to try ext3 instead and fail.
 * So if we didn't know the fs type for sure, just try ext4 next.
 */
        if (!mnt.Success())
            fstype = "ext4";
    }
    if (fstype != "") {
        ExecAndWait mnt(the_config->MountPath().c_str(),
                        "-t", fstype.c_str(),
                        part.c_str(), mp.c_str(), "-onoatime",
                        (const char *)0);
        the_iface->CloseExecWindow();
        if (!mnt.Success())
            the_iface->Message("Mount failed");
    } else
        the_iface->CloseExecWindow();
}

static void add_mount(OwlInstallInterface *the_iface,
                      ScriptVariable part)
{
    ScriptVariable mp;
    do {
        ScriptVariable prompt(0,
            "Please enter the mount point for %s "
            "(e.g., /var or /home)",
            part.c_str());
        mp = the_iface->QueryString(prompt, false);
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

/*
 * The use of tmpfs is now the default in both owl-etc and mkfstab.cpp, yet it
 * makes some sense to also mount tmpfs here for use during the install as well
 * as to display it in the mounted filesystems list.
 */
static void use_tmpfs(OwlInstallInterface *the_iface)
{
    ScriptVariable mp(the_config->OwlRoot() + "/tmp");

    ScriptVector mpv(mp, "/", "");
    FileStat thedir(mp.c_str());
    if(!thedir.IsDir()) {
        int res = mkdir(mp.c_str(), 0755);
        if(res == -1) {
            the_iface->Message(ScriptVariable(0,
                "Failed to create directory: %s: %s",
                mp.c_str(), strerror(errno)));
        }
    }
    chmod(mp.c_str(), 01777);

    sync();
    the_iface->ExecWindow(ScriptVariable("Executing mount on ") + mp + " ...");
    ExecAndWait mnt(the_config->MountPath().c_str(),
                    "tmpfs", "-t", "tmpfs", mp.c_str(), (const char *)0);
    the_iface->CloseExecWindow();

    if(!mnt.Success()) {
        the_iface->Message(ScriptVariable("Mount of ") + mp + " failed");
    }

#if 0
    // /var/tmp is now a symlink by default (in owl-hier)
    ScriptVariable vt(the_config->OwlRoot() + "/var/tmp");
    FileStat vartmp(vt.c_str(), false /* no symlink dereference */);
    if(!vartmp.Exists() || !vartmp.IsSymlink()) {
        bool r = the_iface->YesNoMessage(ScriptVariable(
            "Do you want your /var/tmp to be a symlink to /tmp?"),
             true);
        if(r) {
            ScriptVariable v(the_config->OwlRoot() + "/var");
            FileStat vardir(v.c_str(), false /* no symlink dereference */);
            if(!vardir.Exists()) {
                if(-1 == mkdir(v.c_str(), 0755)) {
                    the_iface->Message("Couldn't create /var");
                    return;
                } else {
                    chmod(v.c_str(), 0755);
                    the_iface->Notice("/var directory created");
                }
            } else {
                if(vartmp.IsDir()) {
                    if(-1 == rmdir(vt.c_str())) {
                        the_iface->Message("Couldn't rmdir /var/tmp");
                        return;
                    }
                } else {
                    if(vartmp.Exists()) {
                        the_iface->Message(
                            "/var/tmp already exists and is not a directory");
                        return;
                    }
                }
            }
            if(-1 == symlink("/tmp", vt.c_str())) {
                the_iface->Message("symlink failed");
            }
        }
    }
#endif
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
    the_iface->ExecWindow("Executing umount...");
    for(int i=0; i<dirs.Length(); i++) {
        ScriptVariable mp(the_config->OwlRoot());
        mp += dirs[i];
        ExecAndWait umnt(the_config->UmountPath().c_str(), mp.c_str(), (const char *)0);
        if(!umnt.Success()) {
            the_iface->CloseExecWindow();
            the_iface->Message(ScriptVariable("umount failed for ") + mp);
            the_iface->ExecWindow("");
        }
    }
    the_iface->CloseExecWindow();
}

static void mount_unlisted(OwlInstallInterface *the_iface,
                           bool for_root = false)
{
    ScriptVariable part;
    do {
        ScriptVariable prompt(
            "Please enter the device path\n"
            "(e.g., /dev/sda1 or /dev/md0)");
        part = the_iface->QueryString(prompt, false);
        if(part == "" ||
           part == OwlInstallInterface::qs_cancel ||
           part == OwlInstallInterface::qs_escape ||
           part == OwlInstallInterface::qs_eof)
        {
            return;
        }
    } while(part[0] != '/');
    if(for_root)
        mount_at(the_iface, part, "/");
    else
        add_mount(the_iface, part);
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
    if(!linux_partition_exists()) {
        // no linux partitions found
        the_iface->Message(
            "No Linux partitions (of type 83)\n"
            "could be found.\n"
            "\n"
            "You might want to return to main menu\n"
            "and create some, or specify your\n"
            "chosen partitions manually using the\n"
            "``uNlisted'' option.");
    }
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
            pm->AddItem("n", "Use uNlisted partition for root (experts only)");
            pm->AddItem("q", "Quit/cancel, return to main menu");
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
            } else
            if(choice == "n") {
                mount_unlisted(the_iface, true);
            } else
                mount_at(the_iface, choice, "/");
            use_tmpfs(the_iface);
        } else {
            if(!mountpoint_mounted(the_config->OwlRoot()+"/tmp"))
                use_tmpfs(the_iface);
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
            pm->AddItem("n", "Mount uNlisted partition (experts only)");
#if 0
            if(!mountpoint_mounted(the_config->OwlRoot()+"/tmp"))
                pm->AddItem("t", "Use tmpfs for /tmp (strongly recommended)");
#endif
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
            else if(choice=="n")
                mount_unlisted(the_iface);
            else if(choice=="u")
                unmount_all(the_iface);
            else if(choice=="v")
                view_tree(the_iface);
#if 0
            else if(choice=="t")
                use_tmpfs(the_iface);
#endif
            else add_mount(the_iface, choice);
        }
    }
}

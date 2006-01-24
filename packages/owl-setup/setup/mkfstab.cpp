#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>


#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

#include "cmd.hpp"
#include "state.hpp"
#include "iface.hpp"
#include "config.hpp"

static ScriptVariable fs_options(ScriptVariable mpoint)
{
    if(mpoint == "/") return "defaults";
    if(mpoint == "/dev") return "nosuid";
    if(mpoint == "/usr") return "nodev";
    return "nosuid,nodev";
}

static void generate_standard_fstab(
    OwlInstallInterface *the_iface, bool scan_std_lines = true)
{
    ScriptVariable entry_proc("proc\t\t/proc\t\t\tproc\tgid=110\t\t\t0 0");
    ScriptVariable entry_devpts(
                    "devpts\t\t/dev/pts\t\tdevpts\tgid=5,mode=620\t\t0 0");
    ScriptVariable entry_cdrom(
         "/dev/cdrom\t/mnt/cdrom\t\tiso9660\tnoauto,nosuid,owner,ro\t0 0");
    ScriptVariable entry_floppy(
                "/dev/fd0\t/mnt/floppy\t\text2\tnoauto,nosuid,owner\t0 0");

    if(scan_std_lines)
    {
        ReadText fstab(the_config->FstabFile().c_str());
        ScriptVariable line;
        while(fstab.ReadLine(line)) {
            ScriptVector entry(line, " \t\r\n");
            if(entry[0] == "proc")
                entry_proc = line;
            else
            if(entry[0] == "devpts")
                entry_devpts = line;
            else
            if(entry[0] == "/dev/cdrom" && entry[1] == "/mnt/cdrom")
                entry_cdrom = line;
            else
            if(entry[0] == "/dev/fd0" && entry[1] == "/mnt/floppy")
                entry_floppy = line;
        }
    }


    FILE* f = fopen(the_config->FstabFile().c_str(), "w");
    if(!f) {
        the_iface->Message(ScriptVariable("Failed to open ") +
                           the_config->FstabFile() + " for writing");
        return;
    }
    fchmod(fileno(f), 0644);
    ScriptVector dirs, parts, types;
    enumerate_owl_dirs3(dirs, parts, types);
    for(int i=0; i<dirs.Length(); i++) {
        int pri = 2;
        if(parts[i] == "tmpfs")
            pri = 0;
        else
        if(dirs[i] == "/")
            pri = 1;

        fprintf(f, "%s%s%s\t\t\t%s\t%s\t\t%d %d\n",
                   parts[i].c_str(),
                       parts[i].Length() < 8 ? "\t\t" : "\t",
                   dirs[i].c_str(),
                   types[i].c_str(),
                   fs_options(dirs[i]).c_str(),
                   0,
                   pri
        );
    }

    ScriptVector swaps;
    enumerate_active_swaps(swaps);
    for(int i=0; i<swaps.Length(); i++) {
        fprintf(f, "%s\t%s\t\t\t%s\t%s\t\t%d %d\n",
                   swaps[i].c_str(),
                   "swap",
                   "swap",
                   "defaults",
                   0,
                   0
        );
    }

    fputs(entry_proc  .c_str(), f); fputc('\n', f);
    fputs(entry_devpts.c_str(), f); fputc('\n', f);
    fputs(entry_cdrom .c_str(), f); fputc('\n', f);
    fputs(entry_floppy.c_str(), f); fputc('\n', f);

    fclose(f);
}

static void edit_fstab(OwlInstallInterface *the_iface)
{
    bool r = the_iface->YesNoMessage(
        "I'm going to run the vi editor for you\n"
        "\n"
        "NEWBIE NOTICE: to quit vi, press Escape, then type `:q!'\n"
        "\n"
        "Continue?",
        true
    );
    if(!r) return;
    the_iface->ExecWindow("Launching an editor on your /etc/fstab");
    ExecAndWait passwd(the_config->EditorPath().c_str(),
                       the_config->FstabFile().c_str(), 0);
    the_iface->CloseExecWindow();
}

void create_fstab(OwlInstallInterface *the_iface)
{
    if(!fstab_contains_root()) {
        generate_standard_fstab(the_iface);
        the_iface->Message("/etc/fstab didn't contain a root entry "
                           "or was not found.  A new fstab file\n"
                           "with your selected entries has just been "
                           "generated.");
    }

    for(;;) {
        IfaceSingleChoice *m = the_iface->CreateSingleChoice();
        m->AddItem("edit", "Edit /etc/fstab");
        m->AddItem("reset", "Generate default /etc/fstab "
                            "(changes will be lost)");
        m->AddItem("q", "Done (return to main menu)");

        m->SetDefault("q");

        ScriptVariable choice = m->Run();
        delete m;

        if(choice=="q" || choice=="" ||
           choice == OwlInstallInterface::qs_cancel ||
           choice == OwlInstallInterface::qs_escape ||
           choice == OwlInstallInterface::qs_eof)
        {
            return;
        }
        else if(choice == "reset")
            generate_standard_fstab(the_iface, false);
        else if(choice == "edit")
            edit_fstab(the_iface);
    }
}


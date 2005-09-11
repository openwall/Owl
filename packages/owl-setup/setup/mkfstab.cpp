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

static void generate_standard_fstab(OwlInstallInterface *the_iface)
{
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
        fprintf(f, "%s\t%s\t%s\t%s\t%d %d\n",
                   parts[i].c_str(),
                   dirs[i].c_str(),
                   types[i].c_str(),
                   fs_options(dirs[i]).c_str(),
                   0,
                   (dirs[i]=="/") ? 1 : 2
        );
    }

    ScriptVector swaps;
    enumerate_active_swaps(swaps);
    for(int i=0; i<swaps.Length(); i++) {
        fprintf(f, "%s\t%s\t%s\t%s\t%d %d\n",
                   swaps[i].c_str(),
                   "swap",
                   "swap",
                   "defaults",
                   0,
                   0
        );
    }

    fputs(the_config->DefaultFstabContent().c_str(), f);

    fclose(f);
}

static void edit_fstab(OwlInstallInterface *the_iface)
{
    the_iface->ExecWindow("Launching an editor on your /etc/fstab");
    ExecAndWait passwd(the_config->EditorPath().c_str(),
                       the_config->FstabFile().c_str(), 0);
    the_iface->CloseExecWindow();
}

void create_fstab(OwlInstallInterface *the_iface)
{
    if(!fstab_exists()) {
        generate_standard_fstab(the_iface);
        the_iface->Message("No /etc/fstab was found or it didn't contain a "
                           "root entry.  A new fstab file\n"
                           "with your selected entries has just been "
                           "generated.");
    }

    for(;;) {
        IfaceSingleChoice *m = the_iface->CreateSingleChoice();
        m->AddItem("edit", "Edit /etc/fstab");
        m->AddItem("reset", "Regenerate default /etc/fstab (cancel changes)");
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
            generate_standard_fstab(the_iface);
        else if(choice == "edit")
            edit_fstab(the_iface);
    }
}


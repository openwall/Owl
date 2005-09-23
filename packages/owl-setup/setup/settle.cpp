#include <stdio.h>

#include "scriptpp/scrvar.hpp"

#include "state.hpp"
#include "config.hpp"
#include "iface.hpp"
#include "iface_dumb.hpp"
#ifdef NCURSES_ENABLE
#include "iface_ncurses.hpp"
#endif

#include "version.h"

extern void repartition_hard_drive(OwlInstallInterface *);
extern void select_and_mount_partitions(OwlInstallInterface *);
extern void activate_swap(OwlInstallInterface *);
extern void install_packages(OwlInstallInterface *);
extern void run_shell(OwlInstallInterface *);

extern void select_keyboard_layout(OwlInstallInterface *);
extern void set_root_password(OwlInstallInterface *);
extern void create_fstab(OwlInstallInterface *);
extern void select_timezone(OwlInstallInterface *);
extern void configure_network(OwlInstallInterface *);
extern void install_kernel_and_lilo(OwlInstallInterface *);
extern void reboot_it(OwlInstallInterface *);

#ifdef NCURSES_ENABLE

#ifdef NCURSES_DEFAULT
bool ncurses_interface = true;
#else
bool ncurses_interface = false;
#endif

void process_cmdline(int argc, char **argv)
{
    if(argc>1) {
        ScriptVariable a1(argv[1]);
        if(a1 == "-m") {
            ncurses_interface = true;
        } else
        if(a1 == "-d") {
            ncurses_interface = false;
        }
    }
}

#endif

int main(int argc, char **argv)
{
#ifdef NCURSES_ENABLE
    process_cmdline(argc, argv);
#endif

    the_config = new OwlInstallConfig("/owl");

    struct MainMenuItem {
        const char *label;
        const char *comment;
        bool (*enabled)(void);
        bool (*passed)(void);
    };

    bool (* const never_done)(void) = (bool(*)(void))(-1);

    MainMenuItem main_menu[] = {
        { "f", "Repartition your hard drive",
            always_true, linux_partition_exists },
        { "m", "Select & mount install partitions",
            linux_partition_exists, owl_dir_mounted  },
        { "s", "Activate swap space", always_true, active_swap_exists },
        { "i", "Install packages", owl_dir_mounted, packages_installed },
        { "k", "Select keyboard layout",
            packages_installed, keyboard_selected },
        { "p", "Set root password", packages_installed, root_password_set },
        { "t", "Create /etc/fstab", fstab_exists, fstab_contains_root },
        { "z", "Select timezone", packages_installed, timezone_selected },
        { "n", "Configure network", packages_installed, network_configured },
        { "b", "Install kernel and bootloader",
            packages_installed, kernel_installed },
        { "r", "Reboot to the newly-installed system",
            minimal_install_ready, never_done },

        { "!", "Run shell", always_true, never_done },
        { "x", "Exit", always_true, never_done },
        { 0,0,0,0 }
    };

    OwlInstallInterface *the_interface;

#ifdef NCURSES_ENABLE
    if(ncurses_interface)
        the_interface = new NcursesOwlInstallInterface;
    else
        the_interface = new DumbOwlInstallInterface;
#else
    the_interface = new DumbOwlInstallInterface;
#endif

    for(;;) {
        IfaceSingleChoice *mm = the_interface->CreateSingleChoice();
        ScriptVariable defval("");
        for(int i=0; main_menu[i].label; i++) {
            bool enabled = main_menu[i].enabled();
            bool passed;
            const char *mark;
            if(main_menu[i].passed != never_done) {
                passed = main_menu[i].passed();
                mark = passed ? "[OK]     " : "[--]     ";
            } else {
                passed = false;
                mark = "         ";
            }
            mm->AddItem(main_menu[i].label,
                        ScriptVariable(mark)+main_menu[i].comment,
                        enabled);
            if(defval=="" && enabled && !passed)
                defval = main_menu[i].label;
        }
        mm->SetDefault(defval);
        mm->SetCaption("Openwall GNU/*/Linux installer version " SETUP_VERSION);
        ScriptVariable choice = mm->Run();
        delete mm;
        if(choice == "") {
            the_interface->Notice("Got EOF, exiting...");
            break;
        } else
        if(choice == "f") {
            repartition_hard_drive(the_interface);
        } else
        if(choice == "m") {
            select_and_mount_partitions(the_interface);
        } else
        if(choice == "s") {
            activate_swap(the_interface);
        } else
        if(choice == "i") {
            install_packages(the_interface);
        } else
        if(choice == "k") {
            select_keyboard_layout(the_interface);
        } else
        if(choice == "p") {
            set_root_password(the_interface);
        } else
        if(choice == "t") {
            create_fstab(the_interface);
        } else
        if(choice == "z") {
            select_timezone(the_interface);
        } else
        if(choice == "n") {
            configure_network(the_interface);
        } else
        if(choice == "b") {
            install_kernel_and_lilo(the_interface);
        } else
        if(choice == "r") {
            reboot_it(the_interface);
        } else
        if(choice == "!") {
            run_shell(the_interface);
        } else
        if(choice == "x") {
            ScriptVector parts, dirs;
            enumerate_owl_dirs(dirs, parts);
            if(parts.Length()>0) {
                if(parts.Length()==1) {
                    the_interface->Message(ScriptVariable("Warning: ") +
                                          parts[0] +
                                          " is still mounted at " +
                                          dirs[0]);
                } else {
                    the_interface->Message(ScriptVariable("Warning: ") +
                                          parts.Join(", ") +
                                          " are still mounted at " +
                                          dirs.Join(", ") + ", respectively");
                }
            }
            the_interface->Notice("Exiting...");
            break;
        } else
        if(choice == OwlInstallInterface::qs_cancel) {
            the_interface->Notice("Please use \"x\" to exit");
        } else
        if(choice == OwlInstallInterface::qs_eof) {
            the_interface->Notice("Got EOF, exiting...");
            break;
        } else {
            the_interface->Message("Warning: internal error (unknown choice)");
        }
    }
    delete the_interface;
    return 0;
}

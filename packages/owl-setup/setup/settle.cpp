#include <stdio.h>
#include <stdlib.h>

#include "scriptpp/scrvar.hpp"

#include "state.hpp"
#include "config.hpp"
#include "iface.hpp"
#include "iface_dumb.hpp"
#ifdef NCURSES_ENABLE
#include "iface_ncurses.hpp"
#endif

#include "version.h"

#include "command_line.hpp"

extern void repartition_hard_drive(OwlInstallInterface *, bool);
extern void select_and_mount_partitions(OwlInstallInterface *);
extern void activate_swap(OwlInstallInterface *);
extern void install_packages(OwlInstallInterface *);
extern void run_shell(OwlInstallInterface *);

extern void i18n_settings(OwlInstallInterface *);
extern void set_root_password(OwlInstallInterface *);
extern void create_fstab(OwlInstallInterface *);
extern void select_timezone(OwlInstallInterface *);
extern void configure_network(OwlInstallInterface *);
#if defined(__i386__) || defined(__x86_64__)
extern void install_kernel_headers(OwlInstallInterface *);
extern void install_kernel_and_lilo(OwlInstallInterface *);
extern void reboot_it(OwlInstallInterface *);
#endif // __i386__ || __x86_64__

#ifdef NCURSES_ENABLE
/* defined in curs_detect.cpp */
bool is_terminal_curses_capable();
#endif

struct CommandLine : public OwlSetupCommandline {
    enum { use_whatever, use_fdisk, use_cfdisk } fdisk_mode;
    const char* HelpMessage() const {
        return "Usage: settle -d      use dumb terminal interface\n"
               "              -m      use ncurses interface\n"
               "              -b      force bw mode for ncurses\n"
               "              -f      force using of plain fdisk\n"
               "              -c      force using of cfdisk\n";
    }
    virtual const char* OptChars() const { return "dmbhfc"; }
    virtual bool SpecificProcess(int c)
    {
        switch(c) {
            case 'f':
                fdisk_mode = use_fdisk;
                return true;
            case 'c':
                fdisk_mode = use_cfdisk;
                return true;
            default:
                return false;
        }
    }
};

int main(int argc, char **argv)
{
    CommandLine cmdline;
    cmdline.Process(argc, argv);

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
        { "l", "Configure localization (i18n)",
            packages_installed, keyboard_selected },
        { "p", "Set root password", packages_installed, root_password_set },
        { "t", "Create /etc/fstab", fstab_exists, fstab_contains_root },
        { "z", "Select timezone", packages_installed, timezone_selected },
        { "n", "Configure network", packages_installed, network_configured },
#if defined(__i386__) || defined(__x86_64__)
        { "h", "Install kernel headers (optional)",
            can_install_kheaders, kheaders_installed },
        { "b", "Install kernel and bootloader",
            packages_installed, kernel_installed },
        { "r", "Reboot to the newly-installed system",
            minimal_install_ready, never_done },
#endif // __i386__ || __x86_64__
        { "!", "Run shell", always_true, never_done },
        { "x", "Exit", always_true, never_done },
        { 0,0,0,0 }
    };

    OwlInstallInterface *the_interface;

#ifdef NCURSES_ENABLE
    if(cmdline.ncurses_interface && !is_terminal_curses_capable())
        cmdline.ncurses_interface = false;

    if(cmdline.ncurses_interface)
        the_interface =
            new NcursesOwlInstallInterface(cmdline.allow_ncurses_color);
    else
        the_interface =
            new DumbOwlInstallInterface;
#else
    the_interface = new DumbOwlInstallInterface;
#endif

    bool use_cfdisk;
    switch(cmdline.fdisk_mode) {
        case CommandLine::use_fdisk:
            use_cfdisk = false;
            break;
        case CommandLine::use_cfdisk:
            use_cfdisk = true;
            break;
        case CommandLine::use_whatever:
        default: // default is just to make the compiler happy
            use_cfdisk = cmdline.ncurses_interface;
            break;
    }


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
            repartition_hard_drive(the_interface, use_cfdisk);
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
        if(choice == "l") {
            i18n_settings(the_interface);
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
#if defined(__i386__) || defined(__x86_64__)
        if(choice == "h") {
            install_kernel_headers(the_interface);
        } else
        if(choice == "b") {
            install_kernel_and_lilo(the_interface);
        } else
        if(choice == "r") {
            reboot_it(the_interface);
        } else
#endif // __i386__ || __x86_64__
        if(choice == "!") {
            run_shell(the_interface);
        } else
        if(choice == "x") {
            ScriptVector parts, dirs;
            enumerate_owl_dirs(dirs, parts, false);
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

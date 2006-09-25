#include <stdio.h>
#include <stdlib.h>

#include "scriptpp/scrvar.hpp"

#include "config.hpp"
#include "iface.hpp"
#include "iface_dumb.hpp"
#ifdef NCURSES_ENABLE
#include "iface_ncurses.hpp"
#endif

#include "version.h"

#include "command_line.hpp"

extern void run_shell(OwlInstallInterface *);
extern void i18n_settings(OwlInstallInterface *);
extern void set_root_password(OwlInstallInterface *);
extern void select_timezone(OwlInstallInterface *);
extern void configure_network(OwlInstallInterface *);

struct CommandLine : public OwlSetupCommandline {
    const char* HelpMessage() const {
        return "Usage: setup -d      use dumb terminal interface\n"
               "       setup -m      use ncurses interface\n"
               "       setup -b      force bw mode for ncurses\n";
    }
};

#ifdef NCURSES_ENABLE
/* defined in curs_detect.cpp */
bool is_terminal_curses_capable();
#endif

int main(int argc, char **argv)
{
    CommandLine cmdline;
    cmdline.Process(argc, argv);

    the_config = new OwlInstallConfig("");

    struct MainMenuItem {
        const char *label;
        const char *comment;
    };
    MainMenuItem main_menu[] = {
        { "l", "Configure localization (i18n)" },
        { "p", "Set root password" },
        { "z", "Select timezone" },
        { "n", "Configure network" },
        { "!", "Run shell" },
        { "x", "Exit" },
        { 0,0 }
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


    for(;;) {
        IfaceSingleChoice *mm = the_interface->CreateSingleChoice();
        for(int i=0; main_menu[i].label; i++) {
            mm->AddItem(main_menu[i].label,
                        main_menu[i].comment,
                        true);
        }
        mm->SetCaption("Openwall GNU/*/Linux setup version " SETUP_VERSION);
        ScriptVariable choice = mm->Run();
        delete mm;
        if(choice == "") {
            the_interface->Notice("Got EOF, exiting...");
            return 1;
        } else
        if(choice == "l") {
            i18n_settings(the_interface);
        } else
        if(choice == "p") {
            set_root_password(the_interface);
        } else
        if(choice == "z") {
            select_timezone(the_interface);
        } else
        if(choice == "n") {
            configure_network(the_interface);
        } else
        if(choice == "!") {
            run_shell(the_interface);
        } else
        if(choice == "x") {
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

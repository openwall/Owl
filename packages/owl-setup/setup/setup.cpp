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

extern void run_shell(OwlInstallInterface *);
extern void select_keyboard_layout(OwlInstallInterface *);
extern void set_root_password(OwlInstallInterface *);
extern void select_timezone(OwlInstallInterface *);
extern void configure_network(OwlInstallInterface *);


#ifdef NCURSES_ENABLE

#ifdef NCURSES_DEFAULT
bool ncurses_interface = true;
#else
bool ncurses_interface = false;
#endif

bool allow_ncurses_color = true;

/* defined in curs_detect.cpp */
bool is_terminal_curses_capable();

void display_usage(bool by_option)
{
    if(!by_option) {
        printf("Invalid command line\n");
    }
    printf("Usage: setup -d      use dumb terminal interface\n"
           "       setup -m [-b] use ncurses interface [force bw mode]\n");
    exit(by_option ? 0 : 1);
}


void process_cmdline(int argc, char **argv)
{
    for(int i=1; i<argc; i++) {
        ScriptVariable a1(argv[i]);
        if(a1 == "-b") {
            allow_ncurses_color = false;
        } else
        if(a1 == "-m") {
            ncurses_interface = true;
        } else
        if(a1 == "-d") {
            ncurses_interface = false;
        } else
        if(a1 == "-h" || a1 == "--help") {
            display_usage(true);
        } else
            display_usage(false);
    }
}

#endif

int main(int argc, char **argv)
{
#ifdef NCURSES_ENABLE
    process_cmdline(argc, argv);
#endif

    the_config = new OwlInstallConfig("");

    struct MainMenuItem {
        const char *label;
        const char *comment;
    };
    MainMenuItem main_menu[] = {
        { "k", "Select keyboard layout" },
        { "p", "Set root password" },
        { "z", "Select timezone" },
        { "n", "Configure network" },
        { "!", "Run shell" },
        { "x", "Exit" },
        { 0,0 }
    };

    OwlInstallInterface *the_interface;

#ifdef NCURSES_ENABLE
    if(ncurses_interface && !is_terminal_curses_capable())
        ncurses_interface = false;

    if(ncurses_interface)
        the_interface = new NcursesOwlInstallInterface(allow_ncurses_color);
    else
        the_interface = new DumbOwlInstallInterface;
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
        if(choice == "k") {
            select_keyboard_layout(the_interface);
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

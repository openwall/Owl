#include <stdio.h>

#include "scriptpp/scrvar.hpp"

#include "iface.hpp"
#include "iface_dumb.hpp"
#include "config.hpp"

#include "version.h"

extern void run_shell(OwlInstallInterface *);
extern void select_keyboard_layout(OwlInstallInterface *);
extern void set_root_password(OwlInstallInterface *);
extern void select_timezone(OwlInstallInterface *);
extern void configure_network(OwlInstallInterface *);

int main()
{
    the_config = new OwlInstallConfig();

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

    OwlInstallInterface *the_interface = new DumbOwlInstallInterface;

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
            return 0;
        } else
        if(choice == OwlInstallInterface::qs_cancel) {
            the_interface->Notice("Please use \"x\" to exit");
        } else
        if(choice == OwlInstallInterface::qs_eof) {
            the_interface->Notice("Got EOF, exiting...");
            return 1;
        } else {
            the_interface->Message("Warning: internal error (unknown choice)");
        }
    }
}

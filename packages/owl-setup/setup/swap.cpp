#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

#include "cmd.hpp"
#include "state.hpp"
#include "iface.hpp"
#include "config.hpp"

static void enumerate_available_swaps(ScriptVector &res)
{
    ScriptVector all, active;
    enumerate_swap_partitions(all);
    enumerate_active_swaps(active);

    res.Clear();

    for(int i=0; i<all.Length(); i++) {
        bool avail = true;
        for(int j = 0; j<active.Length(); j++) {
            if(all[i] == active[j]) {
                avail = false;
                break;
            }
        }
        if(avail) {
            res.AddItem(all[i]);
        }
    }

}

static void view_active(OwlInstallInterface *the_iface)
{
    ScriptVector v;
    enumerate_active_swaps(v);
    if(v.Length()<1) {
        the_iface->Message(
           "No active swaps.  You might want to activate some.");
        return;
    }
    ScriptVariable msg("The following swaps are active: ");
    msg += v.Join(", ");
    msg += ".";
    the_iface->Message(msg);
}

#if 0
static void swap_file(OwlInstallInterface *the_iface)
{
    the_iface->Message("Sorry, the feature isn't implemented yet");
}
#endif

static void swapoff_all(OwlInstallInterface *the_iface)
{
    ScriptVector v;
    enumerate_active_swaps(v);
    for(int i=0; i<v.Length(); i++) {
        the_iface->ExecWindow("Executing swapoff...");
        ExecAndWait s_off(the_config->SwapoffPath().c_str(), v[i].c_str(), (const char *)0);
        the_iface->CloseExecWindow();
        if(!s_off.Success())
            the_iface->Message(ScriptVariable("swapoff failed for ") + v[i]);
    }
}

static void swapon(OwlInstallInterface *the_iface, ScriptVariable& part)
{
    ScriptVector sw;
    enumerate_active_swaps(sw);
    for(int i=0; i<sw.Length(); i++)
        if(sw[i] == part) {
            the_iface->Message(part + " already active, swapon cancelled");
            return;
        }
    if(is_mounted(part)) {
        the_iface->Message(part + " is *mounted* (why?..), swapon cancelled");
        return;
    }

    YesNoCancelResult mk = the_iface->YesNoCancelMessage(
        ScriptVariable("Run mkswap on ") + part + " before swapon?",
        ync_yes
    );
    if(mk == ync_cancel) return;
    if(mk == ync_yes) {
        bool confirm =
            the_iface->YesNoMessage(ScriptVariable("All data on ") + part +
                                    " will be destroyed.  Continue?");
        if(!confirm) return;
        the_iface->ExecWindow("Executing mkswap...");
        ExecAndWait mks(the_config->MkswapPath().c_str(), part.c_str(), (const char *)0);
        the_iface->CloseExecWindow();
        if(!mks.Success())
            the_iface->Message(ScriptVariable("mkswap failed for ") + part);
    }
    the_iface->ExecWindow("Executing swapon...");
    ExecAndWait s_on(the_config->SwaponPath().c_str(), part.c_str(), (const char *)0);
    the_iface->CloseExecWindow();
    if(!s_on.Success())
        the_iface->Message(ScriptVariable("swapon failed for ") + part);
}

static void swap_unlisted(OwlInstallInterface *the_iface)
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
    swapon(the_iface, part);
}

void activate_swap(OwlInstallInterface *the_iface)
{
    {
        ScriptVector all;
        enumerate_swap_partitions(all);
        if(!all.Length()) {
            // no swap partitions found
            the_iface->Message(
                "No Linux swap partitions (of type 82)\n"
                "could be found.\n"
                "\n"
                "You might want to return to main menu\n"
                "and create some, or specify your\n"
                "chosen partitions manually using the\n"
                "``uNlisted'' option.");
        }
    }
    for(;;) {
        IfaceSingleChoice *sm = the_iface->CreateSingleChoice();
        sm->AddItem("v", "View active swaps");
        ScriptVector avail;
        enumerate_available_swaps(avail);
        for(int i=0; i<avail.Length(); i++) {
            sm->AddItem(avail[i],
                        ScriptVariable("Prepare & activate swap partition ") +
                        avail[i]);
        }
        sm->AddItem("n", "Use uNlisted swap partition (experts only)");
#if 0
        sm->AddItem("file", "Create/activate a swap file");
#endif
        sm->AddItem("off", "Deactivate all and start again");
        sm->AddItem("q", "Done, return to main menu");
        if(avail.Length()>0) {
            sm->SetDefault(avail[0]);
        } else {
            sm->SetDefault("q");
        }

        ScriptVariable choice = sm->Run();
        delete sm;

        if(choice=="q" || choice=="" ||
           choice == OwlInstallInterface::qs_cancel ||
           choice == OwlInstallInterface::qs_escape ||
           choice == OwlInstallInterface::qs_eof)
        {
            return;
        }
        else if(choice == "n")
            swap_unlisted(the_iface);
        else if(choice == "v")
            view_active(the_iface);
#if 0
        else if(choice == "file")
            swap_file(the_iface);
#endif
        else if(choice == "off")
            swapoff_all(the_iface);
        else {
            swapon(the_iface, choice);
        }
    }
}

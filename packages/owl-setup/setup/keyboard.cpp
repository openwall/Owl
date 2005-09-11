#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

#include "cmd.hpp"
#include "iface.hpp"
#include "config.hpp"

static void do_scan_keyb_dirs(ScriptVector &res,
                              const ScriptVariable &path)
{
    ReadDir dir(path.c_str());
    const char *ent;
    while((ent = dir.Next())) {
        if(ent[0] == '.') continue;
        ScriptVariable ents(ent);
        ScriptVariable::Substring pref, suf;
        suf = ents.Whole();
        suf.FetchToken(pref, ".");
        if(suf.Get() == the_config->KeymapFileSuffix()) {
            res.AddItem(pref.Get());
            continue;
        }

        ScriptVariable fname = path + "/" + ents;
        FileStat st(fname.c_str());
        if(st.IsDir()) {
            do_scan_keyb_dirs(res, fname);
        }
    }
}

static void uniq_sort(ScriptVector &res)
{
    bool ok;
    do {
        ok = true;
        for(int i=0; i<res.Length()-1; i++) {
            if(res[i]>res[i+1]) {
                ScriptVariable tmp(res[i]);
                res[i] = res[i+1];
                res[i+1] = tmp;
                ok = false;
            } else if(res[i]==res[i+1]) {
                res.Remove(i);
                ok = false;
            }
        }
    } while(!ok);
}

static void scan_keyb_dirs(ScriptVector &res)
{
    do_scan_keyb_dirs(res, the_config->KeymapDbPath());
    uniq_sort(res);
}

void select_keyboard_layout(OwlInstallInterface *the_iface)
{
    IfaceHierChoice *hc = the_iface->CreateHierChoice();
    ScriptVector v;
    scan_keyb_dirs(v);
    for(int i=0; i<v.Length(); i++)
        hc->AddItem(v[i]);
    ScriptVector res;
    bool ok = hc->Run(res);
    delete hc;
    if(ok) {
        FILE* f = fopen(the_config->KeymapSysconf().c_str(), "w");
        if(!f) {
            the_iface->Message(ScriptVariable("Failed to open ") +
                               the_config->KeymapSysconf() + " for writing");
            return;
        }
        fchmod(fileno(f), 0644);
        fprintf(f, "KEYTABLE=%s\n", res[0].c_str());
        fclose(f);
        the_iface->Message("Keyboard layout set");
        bool r = the_iface->YesNoMessage("Try to load it now?");
        if(r) {
            the_iface->ExecWindow(ScriptVariable("Invoking ") +
                                  the_config->LoadkeysPath() + " " + res[0]);
            ExecAndWait lk(the_config->LoadkeysPath().c_str(),
                           res[0].c_str(), 0);
            the_iface->CloseExecWindow();
            if(lk.Success()) {
                the_iface->Message("Seems to be successful");
            } else {
                the_iface->Message("Failed");
            }
        }
    }
    else the_iface->Message("Cancelled, keyboard layout unchanged");
}

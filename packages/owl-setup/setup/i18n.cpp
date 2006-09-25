#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

#include "cmd.hpp"
#include "iface.hpp"
#include "config.hpp"
#include "parmfile.hpp"


/////////////////////////////////////////////////
// common routines

static void plain_dir_scan(ScriptVector &res,
                           const ScriptVariable &path,
                           const ScriptVariable &suffix)
{
    ReadDir dir(path.c_str());
    const char *ent;
    while((ent = dir.Next())) {
        if(ent[0] == '.') continue;
        ScriptVariable ents(ent);
        int slen = suffix.Length();
        ScriptVariable::Substring suf(ents, -slen, slen);
        if(suf.Get() == suffix) {
            suf.Erase();
            res.AddItem(ents);
            continue;
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

/////////////////////////////////////////////////////////////
// info class

class LocalizationInfo {
    ParametersFile file_keyboard;
    ParametersFile file_i18n;

    bool keyboard_changed;
    bool console_changed;
public:
    LocalizationInfo() : keyboard_changed(false), console_changed(false) {}
    ~LocalizationInfo() {}

    void Scan()
    {
        file_keyboard.Load(the_config->KeymapSysconf());
        file_i18n.Load(the_config->I18nSysconf());
    }
    bool Save()
    {
        return
            file_keyboard.SaveAs(the_config->KeymapSysconf()) && 
            file_i18n.SaveAs(the_config->I18nSysconf());
    }

    ScriptVariable GetKeyboard() const
    {
        if(file_keyboard.IsDefined("KEYTABLE"))
            return file_keyboard["KEYTABLE"].Value();
        else
            return "";
    }

    void SetKeyboard(const ScriptVariable &k)
    {
        file_keyboard["KEYTABLE"].Value() = k;
        keyboard_changed = true;
    }

    ScriptVariable GetConsolefont() const
    {
        if(file_i18n.IsDefined("SYSFONT"))
            return file_i18n["SYSFONT"].Value();
        else
            return "";
    }

    void SetConsolefont(const ScriptVariable &k)
    {
        file_i18n["SYSFONT"].Value() = k;
        console_changed = true;
    }

    ScriptVariable GetUnimap() const
    {
        if(file_i18n.IsDefined("UNIMAP"))
            return file_i18n["UNIMAP"].Value();
        else
            return "";
    }

    bool HaveUnimap() const
    {
        return file_i18n.IsDefined("UNIMAP");
    }

    void SetUnimap(const ScriptVariable &k)
    {
        file_i18n["UNIMAP"].Value() = k;
        console_changed = true;
    }

    void RemoveUnimap()
    {
        file_i18n.Undefine("UNIMAP");
        console_changed = true;
    }

    bool KeyboardChanged() const { return keyboard_changed; }
    bool ConsoleChanged() const { return console_changed; }

    void SetMainLocale(const ScriptVariable& s)
    {
        if(s == "C" || s == "") {
            file_i18n.Undefine("LANG");
            file_i18n.Undefine("LANGUAGE");
            file_i18n.Undefine("LC_ALL");
        } else {
            file_i18n["LANG"].Value() = s;
            file_i18n["LANGUAGE"].Value() = s;
            file_i18n["LC_ALL"].Value() = s;
        }
    }


    ScriptVariable Summary() const
    {
        ScriptVariable res;
        res += KeyboardChanged() ? "* " : "  ";
        res += "keyboard:     ";
        res += GetKeyboard();
        res += "\n";

        res += ConsoleChanged() ? "* " : "  ";
        res += "console font: ";
        res += GetConsolefont();
        if(HaveUnimap()) {
            res += "   map: ";
            res+= GetUnimap();
        }
        res += "\n";

        ParametersFile::Parameter *p;
        ParametersFile::Iterator i(file_i18n);
        while((p = i.GetNext())) {
            if(p->GetName() == "LANG" || p->GetName().HasPrefix("LC_")) {
                res += "  ";
                res += p->GetName();
                res += "=";
                res += p->Value();
                res += "\n";
            }
        }

        return res;
    }
};



/////////////////////////////////////////////////////////////
// keyboard

static void do_scan_keyb_dirs(ScriptVector &res,
                              const ScriptVariable &path)
{
    ScriptVariable suffix = the_config->KeymapFileSuffix();
    int slen = suffix.Length();
    ReadDir dir(path.c_str());
    const char *ent;
    while((ent = dir.Next())) {
        if(ent[0] == '.') continue;
        ScriptVariable ents(ent);
        ScriptVariable::Substring suf(ents, -slen, slen);
        if(suf.Get() == the_config->KeymapFileSuffix()) {
            suf.Erase();
            res.AddItem(ents);
            continue;
        }

        ScriptVariable fname = path + "/" + ents;
        FileStat st(fname.c_str());
        if(st.IsDir()) {
            do_scan_keyb_dirs(res, fname);
        }
    }
}

static void scan_keyb_dirs(ScriptVector &res)
{
    do_scan_keyb_dirs(res, the_config->KeymapDbPath());
    uniq_sort(res);
}

static void select_keyboard_layout(OwlInstallInterface *the_iface,
                                   LocalizationInfo *the_info)
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
        the_info->SetKeyboard(res[0]);
    }
    else the_iface->Message("Cancelled, keyboard layout unchanged");
}

static void request_and_load_keys(OwlInstallInterface *the_iface,
                                  LocalizationInfo *the_info)
{
    if(!the_info->KeyboardChanged()) return;

    bool r = the_iface->YesNoMessage("Keyboard layout selected\n"
                                     "Try to load it now?");
    if(r) {
        the_iface->ExecWindow(ScriptVariable("Invoking ") +
                              the_config->LoadkeysPath() + " " +
                              the_info->GetKeyboard());
        ExecAndWait lk(the_config->LoadkeysPath().c_str(),
                       the_info->GetKeyboard().c_str(), 0);
        if(lk.Success()) {
            the_iface->CloseExecWindow(false);
            the_iface->Message("Seems to be successful");
        } else {
            the_iface->CloseExecWindow(true);
            the_iface->Message("Loadkeys failed, sorry");
        }
    }
}

/////////////////////////////////////////////////////////////////
// screen fonts	

static void configure_screen_font(OwlInstallInterface *the_iface,
                                  LocalizationInfo *the_info)
{
    IfaceHierChoice *hc = the_iface->CreateHierChoice();
    hc->SetCaption("Select console font");
    ScriptVector v;
    plain_dir_scan(v, the_config->ConsolefontsDbPath(),
                      the_config->ConsolefontsSuffix());
    for(int i=0; i<v.Length(); i++)
        hc->AddItem(v[i]);
    ScriptVector res;
    bool ok = hc->Run(res);
    delete hc;
    if(!ok) {
        return;
    }
    ScriptVariable selected_font = res[0];

    // as stated in /lib/kbd/consolefonts/README.psfu,
    // .psfu fonts have built-in unimap so we don't need to choose
    // an external map for them


    ScriptVariable selected_map = "";
    if(selected_font.Range(-5, 5).Get() != ".psfu") {
        // so, let's choose a unimap
        const char nomap[] = "   [NONE]";

        IfaceHierChoice *hc = the_iface->CreateHierChoice();
        hc->SetCaption("Please choose unimap");
        ScriptVector v;
        plain_dir_scan(v, the_config->UnimapsDbPath(),
                          the_config->UnimapsSuffix());
        hc->AddItem(nomap);
        for(int i=0; i<v.Length(); i++)
            hc->AddItem(v[i]);
        ScriptVector res;
        bool ok = hc->Run(res);
        delete hc;
        if(!ok) {
            return;
        }
        if(res[0] != nomap) selected_map = res[0];
    }


    the_info->SetConsolefont(selected_font);
    if(selected_map != "")
        the_info->SetUnimap(selected_map);
    else
        the_info->RemoveUnimap();
}

static void request_and_load_console(OwlInstallInterface *the_iface,
                                     LocalizationInfo *the_info)
{
    if(!the_info->ConsoleChanged()) return;

    bool r = the_iface->YesNoMessage("Console font/map selected\n"
                                     "Try to load it now?");
    if(r) {
        ScriptVector sf;
        sf.AddItem(the_config->SetfontPath());
        sf.AddItem(the_info->GetConsolefont());
        if(the_info->HaveUnimap()) {
            sf.AddItem("-u");
            sf.AddItem(the_info->GetUnimap());
        }
        the_iface->ExecWindow(ScriptVariable("Invoking ") +
                              sf.Join(" "));
        char **sfargv = sf.MakeArgv();
        ExecAndWait fsrun(sfargv);
        sf.DeleteArgv(sfargv);
        if(fsrun.Success()) {
            the_iface->CloseExecWindow(false);
            the_iface->Message("Seems to be successful");
        } else {
            the_iface->CloseExecWindow(true);
            the_iface->Message("Setfont failed, sorry");
        }
    }
}

/////////////////////////////////////////////////////////////////
// locales

static void scan_locales(ScriptVector &res)
{
    ExecResultParse loca(the_config->LocalePath().c_str(), "-a", 0);
    res.Clear();
    ScriptVariable v;
    while(loca.ReadLine(v)) {
        v.Trim();
        res.AddItem(v);
    }
}


static void configure_main_locale(OwlInstallInterface *the_iface,
                                  LocalizationInfo *the_info)
{
    IfaceHierChoice *hc = the_iface->CreateHierChoice();
    hc->SetCaption("Select your primary locale");
    hc->SetSorting(false);
    ScriptVector v;
    scan_locales(v);
    for(int i=0; i<v.Length(); i++)
        hc->AddItem(v[i]);
    ScriptVector res;
    bool ok = hc->Run(res);
    delete hc;
    if(!ok) {
        return;
    }
    the_info->SetMainLocale(res[0]);
}


	

/////////////////////////////////////////////////////////////////
// main	

void i18n_settings(OwlInstallInterface *the_iface)
{
    IfaceSingleChoice *pm = the_iface->CreateSingleChoice();
    pm->SetCaption("Internationalization settings");
    pm->AddItem("v", "View the current settings");
    pm->AddItem("k", "Select keyboard layout");
    pm->AddItem("f", "Configure console font and charmap");
    pm->AddItem("l", "Configure main locale");
#if 0
    pm->AddItem("c", "Customize locale settings");
#endif
    pm->AddItem("s", "Save and return to main menu");
    pm->AddItem("x", "Return to main menu without saving");
    LocalizationInfo info;
    info.Scan();
    do {
        ScriptVariable choice = pm->Run();
        if(choice=="") continue;
        else if(choice=="v") {
            the_iface->Message(info.Summary());
        }
        else if(choice=="k") {
            select_keyboard_layout(the_iface, &info);
        }
        else if(choice=="f") {
            configure_screen_font(the_iface, &info);
        }
        else if(choice=="l") {
            configure_main_locale(the_iface, &info);
        }
#if 0
        else if(choice=="c") {
        }
#endif
        else if(choice=="s") {
            if(the_iface->YesNoMessage("Really save and quit?")) {
                if(info.Save())
                    the_iface->Message("Changes saved");
                else
                    the_iface->Message("Problems saving configuration");
                request_and_load_keys(the_iface, &info);
                request_and_load_console(the_iface, &info);
                break;
            }
        }
        else if(choice == "x" ||
                choice == OwlInstallInterface::qs_escape ||
                choice == OwlInstallInterface::qs_cancel)
        {
            if(the_iface->YesNoMessage("Really quit without saving?")) break;
        }
        else if(choice == OwlInstallInterface::qs_eof)
        {
            break;
        }
    } while(1);
    delete pm;
}

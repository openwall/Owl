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
        if(suffix != "") {
            int slen = suffix.Length();
            ScriptVariable::Substring suf(ents, -slen, slen);
            if(suf.Get() == suffix) {
                suf.Erase();
                res.AddItem(ents);
            }
        } else {
            res.AddItem(ents);
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
            file_keyboard.SaveAs(the_config->KeymapSysconf(), 0600) &&
            file_i18n.SaveAs(the_config->I18nSysconf(), 0644);
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
    void RemoveConsolefont()
    {
        file_i18n.Undefine("SYSFONT");
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

    ScriptVariable GetACM() const
    {
        if(file_i18n.IsDefined("SYSFONTACM"))
            return file_i18n["SYSFONTACM"].Value();
        else
            return "";
    }
    bool HaveACM() const
    {
        return file_i18n.IsDefined("SYSFONTACM");
    }
    void SetACM(const ScriptVariable &k)
    {
        file_i18n["SYSFONTACM"].Value() = k;
        console_changed = true;
    }
    void RemoveACM()
    {
        file_i18n.Undefine("SYSFONTACM");
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
    void SetLocale(const ScriptVariable& name, const ScriptVariable& val)
    {
        if(!name.HasPrefix("LC_")) return;
        if(val == "C" || val == "") {
            file_i18n.Undefine(name);
        } else {
            file_i18n[name].Value() = val;
        }
    }
    void ClearLocaleSettings()
    {
        file_i18n.Undefine("LANG");
        file_i18n.Undefine("LANGUAGE");
        bool done;
        do {
            done = true;
            ParametersFile::Parameter *p;
            ParametersFile::Iterator i(file_i18n);
            while((p = i.GetNext())) {
                if(p->GetName().HasPrefix("LC_")) {
                    done = false;
                    file_i18n.Undefine(p->GetName());
                    break;
                }
            }
        } while(!done);
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

    ScriptVariable ConsoleFontSummary() const
    {
        ScriptVariable res;
        res += "console font (SYSFONT): ";
        res += GetConsolefont();
        res += "\n";
        res += "unimap (UNIMAP):        ";
        res += GetUnimap();
        res += "\n";
        res += "char map (SYSFONTACM):  ";
        res += GetACM();
        res += "\n";
        return res;
    }

    ScriptVariable LocaleSummary() const
    {
        ScriptVariable res;
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
        if(res == "") res = "No locale values defined";
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
                       the_info->GetKeyboard().c_str(), (const char *)0);
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

static void configure_screen_font_preset(OwlInstallInterface *the_iface,
                                         LocalizationInfo *the_info)
{
    IfaceHierChoice *hc = the_iface->CreateHierChoice();
    hc->SetCaption("Select console font scheme");
    hc->SetSorting(false);
    ScriptVector v;
    const OwlInstallConfig::PresetFontItem *presets =
        the_config->PresetSetfontCombinations();
    hc->AddItem("* NONE *", 0, true);
    for(int i=0; presets[i].comment; i++)
        hc->AddItem(presets[i].comment, presets+i);
    ScriptVector r;
    OwlInstallConfig::PresetFontItem *res_p;
    bool ok = hc->Run(r, (const void**)&res_p);
    delete hc;
    if(!ok) {
        return;
    }
    if(res_p) {
        the_info->SetConsolefont(res_p->sysfont);
        if(res_p->unimap)
            the_info->SetUnimap(res_p->unimap);
        else
            the_info->RemoveUnimap();
        if(res_p->sysfontacm)
            the_info->SetACM(res_p->sysfontacm);
        else
            the_info->RemoveACM();
    } else {
        // this means the user has just selected "NONE"
        the_info->RemoveConsolefont();
        the_info->RemoveUnimap();
        the_info->RemoveACM();
    }
}

static bool check_file(ScriptVariable fname,
                       const ScriptVariable &dir,
                       const ScriptVector &suffixes)
{
    if(fname[0] != '/') {
         fname = dir + "/" + fname;
    }
    if(FileStat(fname.c_str()).Exists()) return true;
    for(int i=0; i<suffixes.Length(); i++)
        if(FileStat((fname+suffixes[i]).c_str()).Exists()) return true;
    return false;
}

static const char choose_none[] = "* NONE *";
static const char choose_unlisted[] = "* UNLISTED *";

static void configure_screen_font_font(OwlInstallInterface *the_iface,
                                       LocalizationInfo *the_info)
{
    IfaceHierChoice *hc = the_iface->CreateHierChoice();
    hc->SetCaption("Select console font");
    ScriptVector v;
    hc->AddItem(choose_none, 0, true);
    hc->AddItem(choose_unlisted, 0, true);
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
    if(res[0] == choose_none) {
        the_info->RemoveConsolefont();
        the_info->RemoveUnimap();
        the_info->RemoveACM();
    } else if(res[0] == choose_unlisted) {
        ScriptVariable s =
            the_iface->QueryString("Please enter your font file name",
                                   "", false);
        if(s == OwlInstallInterface::qs_cancel ||
           s == OwlInstallInterface::qs_eof)
        {
            the_iface->Notice("Unimap unchanged");
        } else {
            the_info->SetConsolefont(s);
            ScriptVector suf;
            the_config->ConsolefontsSuffixes(suf);
            if(!check_file(s, the_config->ConsolefontsDbPath(), suf)) {
                the_iface->Message("WARNING: I couldn't find the file");
            }
        }
    } else {
        the_info->SetConsolefont(res[0]);
    }
}

static void configure_screen_font_unimap(OwlInstallInterface *the_iface,
                                         LocalizationInfo *the_info)
{
    IfaceHierChoice *hc = the_iface->CreateHierChoice();
    hc->SetCaption("Select unicode mapping for console");
    ScriptVector v;
    hc->AddItem(choose_none, 0, true);
    hc->AddItem(choose_unlisted, 0, true);
    plain_dir_scan(v, the_config->UnimapsDbPath(),
                      the_config->UnimapsSuffix());
    for(int i=0; i<v.Length(); i++)
        hc->AddItem(v[i] + the_config->UnimapsSuffix());
    ScriptVector res;
    bool ok = hc->Run(res);
    delete hc;
    if(!ok) {
        return;
    }
    if(res[0] == choose_none) {
        the_info->RemoveUnimap();
    } else if(res[0] == choose_unlisted) {
        ScriptVariable s =
            the_iface->QueryString("Please enter your "
                                       "unimap file name",
                                   "", false);
        if(s == OwlInstallInterface::qs_cancel ||
           s == OwlInstallInterface::qs_eof)
        {
            the_iface->Notice("Unimap unchanged");
        } else {
            the_info->SetUnimap(s);
            ScriptVector suf;
            the_config->UnimapsSuffixes(suf);
            if(!check_file(s, the_config->UnimapsDbPath(), suf)) {
                the_iface->Message("WARNING: I couldn't find the file");
            }
        }
    } else {
        the_info->SetUnimap(res[0]);
    }
}

static void configure_screen_font_acm(OwlInstallInterface *the_iface,
                                      LocalizationInfo *the_info)
{
    IfaceHierChoice *hc = the_iface->CreateHierChoice();
    hc->SetCaption("Select charmap");
    ScriptVector v;
    hc->AddItem(choose_none, 0, true);
    hc->AddItem(choose_unlisted, 0, true);
    plain_dir_scan(v, the_config->CharmapsDbPath(),
                      the_config->CharmapsSuffix());
    for(int i=0; i<v.Length(); i++)
        if(v[i].Strstr("to_uni.trans").IsInvalid())
            hc->AddItem(v[i]);
    ScriptVector res;
    bool ok = hc->Run(res);
    delete hc;
    if(!ok) {
        return;
    }
    if(res[0] == choose_none) {
        the_info->RemoveACM();
    } else if(res[0] == choose_unlisted) {
        ScriptVariable s =
            the_iface->QueryString("Please enter your "
                                       "charmap file name",
                                   "", false);
        if(s == OwlInstallInterface::qs_cancel ||
           s == OwlInstallInterface::qs_eof)
        {
            the_iface->Notice("Charmap unchanged");
        } else {
            the_info->SetACM(s);
            ScriptVector suf;
            the_config->CharmapsSuffixes(suf);
            if(!check_file(s, the_config->CharmapsDbPath(), suf)) {
                the_iface->Message("WARNING: I couldn't find the file");
            }
        }
    } else {
        the_info->SetACM(res[0]);
    }
}

static void configure_screen_font(OwlInstallInterface *the_iface,
                                  LocalizationInfo *the_info)
{
    IfaceSingleChoice *pm = the_iface->CreateSingleChoice();
    pm->SetCaption("Console font settings");
    pm->AddItem("v", "View the current settings");
    pm->AddItem("p", "Pick a preset combination of parameters");
    pm->AddItem("f", "Choose a font file (experts only)");
    pm->AddItem("u", "Choose a unimap file (experts only)");
    pm->AddItem("c", "Choose a charmap/encoding file (experts only)");
    pm->AddItem("q", "Return to i18n menu");
    do {
        ScriptVariable choice = pm->Run();
        if(choice=="") continue;
        else if(choice=="v") {
            the_iface->Message(the_info->ConsoleFontSummary());
        }
        else if(choice=="p") {
            configure_screen_font_preset(the_iface, the_info);
        }
        else if(choice=="f") {
            configure_screen_font_font(the_iface, the_info);
        }
        else if(choice=="u") {
            configure_screen_font_unimap(the_iface, the_info);
        }
        else if(choice=="c") {
            configure_screen_font_acm(the_iface, the_info);
        }
        else if(choice == "q" ||
                choice == OwlInstallInterface::qs_escape ||
                choice == OwlInstallInterface::qs_cancel)
        {
            break;
        }
        else if(choice == OwlInstallInterface::qs_eof)
        {
            break;
        }
    } while(1);
    delete pm;
}

static void request_and_load_console(OwlInstallInterface *the_iface,
                                     LocalizationInfo *the_info)
{
    if(!the_info->ConsoleChanged()) return;

    bool r = the_iface->YesNoMessage("Console font/map selected\n"
                                     "Try to load it now?");
    if(r) {
        ScriptVector sf;
#if 0
        sf.AddItem(the_config->SetfontPath());
        sf.AddItem(the_info->GetConsolefont());
        if(the_info->HaveUnimap()) {
            sf.AddItem("-u");
            sf.AddItem(the_info->GetUnimap());
        }
#else
        sf.AddItem(the_config->SetsysfontPath());
#endif
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
    ExecResultParse loca(the_config->LocalePath().c_str(), "-a", (const char *)0);
    res.Clear();
    ScriptVariable v;
    while(loca.ReadLine(v)) {
        v.Trim();
        res.AddItem(v);
    }
}

static void scan_lc_vars(ScriptVector &res)
{
   /*
       The locale(1) command displays several strings which pretend
       to be standard shell VAR=VAL assignments. Surprisingly enough,
       locale(1) doesn't handle most of the "variables" displayed so
       it doesn't make any sense to set them. Therefore, this function
       (initially intended to scan the locale(1)'s output) just returns
       the list of variables explicitly enumerated in the locale(1) man
       page.
    */
#if 0
    ExecResultParse loc(the_config->LocalePath().c_str(), (const char *)0);
    res.Clear();
    ScriptVector v;
    while(loc.ReadLine(v, 2, "=")) {
        res.AddItem(v[0]);
    }
#else
    res.AddItem("LANG");
    res.AddItem("LANGUAGE");
    res.AddItem("LC_ALL");
    res.AddItem("LC_CTYPE");
    res.AddItem("LC_COLLATE");
    res.AddItem("LC_TIME");
    res.AddItem("LC_NUMERIC");
    res.AddItem("LC_MONETARY");
    res.AddItem("LC_MESSAGES");
#endif
}

static bool choose_locale(OwlInstallInterface *the_iface,
                          const ScriptVariable& caption,
                          ScriptVariable& result)
{
    IfaceHierChoice *hc = the_iface->CreateHierChoice();
    hc->SetCaption(caption);
    hc->SetSorting(false);
    ScriptVector v;
    scan_locales(v);
    for(int i=0; i<v.Length(); i++)
        hc->AddItem(v[i]);
    ScriptVector res;
    bool ok = hc->Run(res);
    delete hc;
    if(!ok) {
        return false;
    }
    result = res[0];
    return true;
}

static void configure_locale_default(OwlInstallInterface *the_iface,
                                     LocalizationInfo *the_info)
{
    ScriptVariable r;
    bool res = choose_locale(the_iface, "Select your main locale", r);
    if(res) {
        the_info->ClearLocaleSettings();
        the_info->SetMainLocale(r);
    }
}

static void configure_locale_geek(OwlInstallInterface *the_iface,
                                  LocalizationInfo *the_info)
{
    ScriptVariable r;
    bool res = choose_locale(the_iface, "Select locale for LC_CTYPE", r);
    if(res) {
        the_info->ClearLocaleSettings();
        the_info->SetLocale("LC_CTYPE", r);
    }
}

static void configure_locale_customize(OwlInstallInterface *the_iface,
                                       LocalizationInfo *the_info)
{
    IfaceHierChoice *hc = the_iface->CreateHierChoice();
    hc->SetCaption("Choose the locale variable to set");
    hc->SetSorting(false);
    ScriptVector v;
    scan_lc_vars(v);
    for(int i=0; i<v.Length(); i++)
        hc->AddItem(v[i]);
    ScriptVector res;
    bool ok = hc->Run(res);
    delete hc;
    if(!ok) {
        return;
    }

    ScriptVariable r;
    bool rs = choose_locale(the_iface,
                            ScriptVariable("Select locale for ")+res[0],
                            r);
    if(rs) the_info->SetLocale(res[0], r);
}

static void configure_locales(OwlInstallInterface *the_iface,
                              LocalizationInfo *the_info)
{
    IfaceSingleChoice *pm = the_iface->CreateSingleChoice();
    pm->SetCaption("Locale settings");
    pm->AddItem("v", "View the current settings");
    pm->AddItem("d", "Default configuration (LC_ALL only)");
    pm->AddItem("g", "Geek configuration (LC_CTYPE only)");
    pm->AddItem("c", "Customize locale variables");
    pm->AddItem("u", "Unset all");
    pm->AddItem("q", "Return to i18n menu");
    do {
        ScriptVariable choice = pm->Run();
        if(choice=="") continue;
        else if(choice=="v") {
            the_iface->Message(the_info->LocaleSummary());
        }
        else if(choice=="d") {
            configure_locale_default(the_iface, the_info);
        }
        else if(choice=="g") {
            configure_locale_geek(the_iface, the_info);
        }
        else if(choice=="c") {
            configure_locale_customize(the_iface, the_info);
        }
        else if(choice=="u") {
            the_info->ClearLocaleSettings();
        }
        else if(choice == "q" ||
                choice == OwlInstallInterface::qs_escape ||
                choice == OwlInstallInterface::qs_cancel)
        {
            break;
        }
        else if(choice == OwlInstallInterface::qs_eof)
        {
            break;
        }
    } while(1);
    delete pm;
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
    pm->AddItem("l", "Configure locales");
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
            configure_locales(the_iface, &info);
        }
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

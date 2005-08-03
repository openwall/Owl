#include "iface.hpp"
#include "cmd.hpp"
#include "config.hpp"


static void scan_dirs(IfaceHierChoice *hc,
                      const ScriptVariable &path)
{
    ReadDir dir(path.c_str());
    const char *ent;
    while((ent = dir.Next())) {
        if(ent[0] == '.') continue;
        ScriptVariable ents(ent);
        if(ents.HasPrefix("GMT+") ||
           ents.HasPrefix("GMT-") ||
           ents.Strchr(' ').Valid() ||
           ents.Strchr('.').Valid() ||
           ents[0] == '-')
        {
            continue;
        }
        ScriptVariable fname = path + "/" + ents;
        FileStat st(fname.c_str());
        if(st.IsDir()) {
            hc->AddDir(ent);
            scan_dirs(hc, fname);
            hc->EndDir();
        } else {
            if(st.IsRegularFile())
                hc->AddItem(ent);
        }
    }
}


void select_timezone(OwlInstallInterface *the_iface)
{
    IfaceHierChoice *hc = the_iface->CreateHierChoice();
    scan_dirs(hc, the_config->ZoneinfoDbPath());
    ScriptVector res;
    bool ok = hc->Run(res);
    delete hc;
    if(ok) {
        ScriptVariable path(the_config->ZoneinfoDbPath());
        path += "/";
        path += res.Join("/");
        ExecAndWait cp(the_config->CpPath().c_str(),
                       path.c_str(),
                       the_config->ZoneinfoSysconf().c_str(), 0);
        if(cp.Success())
            the_iface->Message("Timezone set");
        else
            the_iface->Message("Error copying the timezone file");
    }
    else the_iface->Message("Cancelled, timezone unchanged");
}

#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>


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
           ents.Strchr(' ').IsValid() ||
           ents.Strchr('.').IsValid() ||
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
        the_iface->ExecWindow("Copying zone file");
        ExecAndWait cp(the_config->CpPath().c_str(),
                       path.c_str(),
                       the_config->ZoneinfoFile().c_str(),
                       (const char *)0);
        the_iface->CloseExecWindow();
        chmod(path.c_str(), 0644);
        if(cp.Success()) {
            bool utc =
                the_iface->YesNoMessage("Hardware clock set to UTC?",
                                        true);

            FILE *f = fopen(the_config->ZoneinfoSysconf().c_str(), "w");
            if(f) {
                fchmod(fileno(f), 0644);
                fprintf(f, "UTC=%s\nARC=false\nZONE=%s\n",
                        utc ? "true" : "false",
                        res.Join("/").c_str());
                fclose(f);
            } else {
                the_iface->Message("Error writing clock config file");
            }

        }
        else
            the_iface->Message("Error copying the timezone file");
    }
    else the_iface->Message("Cancelled, timezone unchanged");
}

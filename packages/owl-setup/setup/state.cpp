#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

#include "cmd.hpp"
#include "state.hpp"
#include "config.hpp"

bool always_true()
{
    return true;
}

bool always_false()
{
    return false;
}

bool linux_partition_exists()
{
    bool ret = false;
    ExecResultParse fdisk(the_config->FdiskPath().c_str(), "-l", 0);

    ScriptVector v;
    while(fdisk.ReadLine(v,7)) {
        if(v[0][0]!='/') continue;
        if(v[1] == "*") {
            v.Remove(1, 1);
        }
        if(v[4] == "83") ret = true;
    }
    return ret;
}

bool owl_dir_mounted()
{
    ReadText rt(the_config->ProcMounts().c_str());
    ScriptVector v;
    while(rt.ReadLine(v,3)) {
        if(v[1] == the_config->OwlRoot()) return true;
    }
    return false;
}

bool active_swap_exists()
{
    ReadText rt(the_config->ProcSwaps().c_str());
    ScriptVector v;
    rt.ReadLine(v,1); // skip header
    return rt.ReadLine(v,1); // true if more than one line is there
}

void enumerate_owl_dirs(ScriptVector &dirs, ScriptVector &parts)
{
    ScriptVector types;
    enumerate_owl_dirs3(dirs, parts, types);
}

void enumerate_owl_dirs3(ScriptVector &dirs,
                         ScriptVector &parts,
                         ScriptVector &types)
{
    dirs.Clear();
    parts.Clear();
    ReadText rt(the_config->ProcMounts().c_str());
    ScriptVector v;
    while(rt.ReadLine(v,4)) {
        if(v[1] == the_config->OwlRoot() ||
           v[1].HasPrefix(the_config->OwlRoot()+"/"))
        {
            v[1].Range(0,4).Erase(); // removed ``/owl''
            if(v[1]=="") v[1] = "/";
            dirs.AddItem(v[1]);
            parts.AddItem(v[0]);
            types.AddItem(v[2]);
        }
    }
}

static void enumerate_partitions(ScriptVector &parts, const char *t)
{
    parts.Clear();
    ExecResultParse fdisk(the_config->FdiskPath().c_str(), "-l", 0);
    ScriptVector v;
    while(fdisk.ReadLine(v,7)) {
        if(v[0][0]!='/') continue;
        if(v[1] == "*") { // "bootable flag" could be an extra word
            v.Remove(1, 1);
        }
        if(v[4] == t) parts.AddItem(v[0]);
    }
}

void enumerate_swap_partitions(class ScriptVector &parts)
{
    enumerate_partitions(parts, "82");
}

void enumerate_linux_partitions(class ScriptVector &parts)
{
    enumerate_partitions(parts, "83");
}

void enumerate_active_swaps(class ScriptVector &swaps)
{
    ReadText rt(the_config->ProcSwaps().c_str());
    ScriptVector v;
    rt.ReadLine(v,1); // skip header
    swaps.Clear();
    while(rt.ReadLine(v,4)) {
        if(v[0][0]=='/') {
            if(v[0].HasPrefix("/ram")) {
                v[0].Range(0,4).Erase();
            }
            swaps.AddItem(v[0]);
        }
    }
}

bool is_mounted(class ScriptVariable &part)
{
    ReadText rt(the_config->ProcMounts().c_str());
    ScriptVector v;
    while(rt.ReadLine(v,2)) {
        if(v[0] == part) return true;
    }
    return false;
}

bool packages_installed()
{
    ScriptVector files;
    the_config->PkgInstalledCheckFiles(files);
    for(int i=0; i<files.Length(); i++)
        if(!FileStat(files[i].c_str()).Exists()) return false;
    return true;
}

bool keyboard_selected()
{
    return FileStat(the_config->KeymapSysconf().c_str()).IsRegularFile();
}

bool root_password_set()
{
    ReadText rt(the_config->RootShadowFile().c_str());
    ScriptVector v;
    if(!rt.ReadLine(v, 3, ":", "")) return false;
    return v[1].Length() > 3;
}

bool fstab_exists()
{
    if(!FileStat(the_config->FstabFile().c_str()).IsRegularFile())
        return false;

    ReadText rt(the_config->FstabFile().c_str());
    ScriptVector v;
    while(rt.ReadLine(v, 7)) {
        if(v[1] == "/") return true;
    }
    return false;
}

bool timezone_selected()
{
    return FileStat(the_config->ZoneinfoSysconf().c_str()).Exists();
}

bool network_configured()
{
    return FileStat(the_config->NetworkSysconf().c_str()).Exists();
}

bool kernel_installed()
{
    return
        FileStat(the_config->TargetKernel().c_str()).IsRegularFile() &&
        FileStat(the_config->LiloMap().c_str()).IsRegularFile();
}


ScriptVariable get_runlevel()
{
    ExecResultParse runlevel("/sbin/runlevel", 0);
    ScriptVector v;
    runlevel.ReadLine(v, 3);
    return v[1] == "" ? ScriptVariable("unknown") : v[1];
}

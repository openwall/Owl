#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

#include "cmd.hpp"

struct dev_item {
    int ma;
    int mi;
    ScriptVariable name;
    dev_item *next;
    dev_item() : ma(-1), mi(-1), name(""), next(0) {}
};

static dev_item* scan_part_file()
{
    dev_item *res = 0;
    ReadText procpart("/proc/partitions");
    ScriptVector rv;
    while(procpart.ReadLine(rv, 3)) {
        long major, minor;
        if(!rv[0].GetLong(major) || !rv[1].GetLong(minor))
            continue; // broken line... no problem
        dev_item *tmp = new dev_item;
        tmp->next = res;
        tmp->ma = major;
        tmp->mi = minor;
        res = tmp;
    }
    return res;
}

static void place_name(dev_item *the_list, int ma, int mi, const char *name)
{
    for(; the_list; the_list = the_list->next) {
        if(the_list->ma == ma && the_list->mi == mi) {
            the_list->name = ScriptVariable("/dev/") + name;
            return;
        }
    }
}

static void scan_dev_dir(dev_item *the_list)
{
    ReadDir devdir("/dev");
    const char *name;
    while((name = devdir.Next())) {
        FileStat st((ScriptVariable("/dev/")+name).c_str(),
                    false /* no symlinks dereference */);
        if(!st.IsBlockdev()) continue; 
        int ma, mi;
        st.GetMajorMinor(ma, mi);
        place_name(the_list, ma, mi, name);
    }
}

static bool no_digits(const char *p)
{
    for(; *p; p++)
        if(*p>='0' && *p<='9') return false;
    return true;
}


static void make_result(dev_item *the_list, ScriptVector &result)
{
    if(!the_list) return;
    if(no_digits(the_list->name.c_str())) {
        int idx;
        idx = 0;
        while(idx < result.Length()) {
            if(the_list->name < result[idx]) {
                result.Insert(idx, the_list->name);
                break;
            }
            idx++;
        }
        if(idx >= result.Length())
            result.AddItem(the_list->name);
    }
    make_result(the_list->next, result);
}

void scan_proc_partitions(ScriptVector &result)
{
    dev_item *list = scan_part_file();
    scan_dev_dir(list);
    result.Clear();
    make_result(list, result);
}

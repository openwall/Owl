#include "iface.hpp"

IfaceSingleChoice::IfaceSingleChoice()
{
    first = last = 0;
}

IfaceSingleChoice::~IfaceSingleChoice()
{
    while(first) {
        Item *tmp = first;
        first = first->next;
        delete tmp;
    }
}

void IfaceSingleChoice::AddItem(const ScriptVariable& label,
                                const ScriptVariable& comment,
                                bool enabled)
{
    if(!first) {
        first = new Item;
        last = first;
    } else {
        last->next = new Item;
        last = last->next;
    }
    last->next = 0;
    last->label = label;
    last->comment = comment;
    last->enabled = enabled;
}


/////////////////////////////////////////////////////////////
//

IfaceHierChoice::IfaceHierChoice()
{
    first = 0;
    last = &first;
    parent = 0;
    ignore_case = true;
    sorted = true;
}

IfaceHierChoice::~IfaceHierChoice()
{
    RmTree(first);
}

void IfaceHierChoice::AddItem(const ScriptVariable& name, const void *uptr)
{
    if(sorted) {
        Item **tmp = last;
        while(*tmp &&
              ((*tmp)->children || (*tmp)->name.Strcasecmp(name)<0)
             )
        {
            tmp = &((*tmp)->next);
        }
        Item *p = new Item(name, parent, uptr);
        p->next = *tmp;
        *tmp = p;
    } else {
        *last = new Item(name, parent, uptr);
        last = &((*last)->next);
    }
}

void IfaceHierChoice::AddDir(const ScriptVariable& name)
{
    if(sorted) {
        Item **tmp = last;
        while(*tmp && (*tmp)->children && (*tmp)->name.Strcasecmp(name)<0)
        {
            tmp = &((*tmp)->next);
        }
        Item *p = new Item(name, parent, 0);
        p->next = *tmp;
        *tmp = p;
        parent = p;
        last = &(p->children);
    } else {
        *last = new Item(name, parent, 0);
        parent = *last;
        last = &((*last)->children);
    }
}

void IfaceHierChoice::EndDir()
{
    if(!parent) return;
    if(sorted) {
        parent = parent->parent;
        if(parent)
            last = &(parent->children);
        else
            last = &first;
    } else {
        last = &(parent->next);
        parent = parent->parent;
    }
}

void IfaceHierChoice::RmTree(Item *t)
{
    if(!t) return;
    RmTree(t->children);
    RmTree(t->next);
    delete t;
}

/////////////////////////////////////////////////////////////
//

static void break_number(int num, int order, int &i, int &f)
{
    i = num; f = 0;
    for(int k = 0; k<order; k++) {
        int d = i % 10;
        i /= 10;
        for(int k1 = 0; k1 < k; k1++) d *= 10;
        f += d;
    }
}

ScriptVariable IfaceProgressBar::ProgressText() const
{
    ScriptVariable res;
    int i, f;
    break_number(current, order, i, f);
    res += ScriptNumber(i);
    if(f) {
        res += ".";
        res += ScriptNumber(f);
    }
    if(total != 0 && units != "%") {
        break_number(total, order, i, f);
        res += "/";
        res += ScriptNumber(i);
        if(f) {
            res += ".";
            res += ScriptNumber(f);
        }
    }
    if(units != "%") res += " ";
    res += units;
    return res;
}

/////////////////////////////////////////////////////////////
//

OwlInstallInterface::OwlInstallInterface()
{
}


ScriptVariable
OwlInstallInterface::QueryString(const ScriptVariable& prompt, bool blind)
{
    ScriptVariable defval("");
    return QueryString(prompt, defval, blind);
}

const char * OwlInstallInterface::qs_cancel = "\003";
const char * OwlInstallInterface::qs_eof    = "\004";
const char * OwlInstallInterface::qs_escape = "\033";
const char * OwlInstallInterface::qs_redraw = "\014";


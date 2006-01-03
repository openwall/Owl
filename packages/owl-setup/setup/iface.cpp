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

void IfaceHierChoice::AddItem(const ScriptVariable& name)
{
    if(sorted) {
        Item **tmp = last;
        while(*tmp && (*tmp)->name < name) tmp = &((*tmp)->next);
        Item *p = new Item(name, parent);
        p->next = *tmp;
        *tmp = p;
    } else {
        *last = new Item(name, parent);
        last = &((*last)->next);
    }
}

void IfaceHierChoice::AddDir(const ScriptVariable& name)
{
    if(sorted) {
        Item **tmp = last;
        while(*tmp && (*tmp)->name < name) tmp = &((*tmp)->next);
        Item *p = new Item(name, parent);
        p->next = *tmp;
        *tmp = p;
        parent = p;
        last = &(p->children);
    } else {
        *last = new Item(name, parent);
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

OwlInstallInterface::OwlInstallInterface()
{
}


ScriptVariable
OwlInstallInterface::QueryString(const ScriptVariable& prompt)
{
    ScriptVariable defval("");
    return QueryString(prompt, defval);
}

const char * OwlInstallInterface::qs_cancel = "\003";
const char * OwlInstallInterface::qs_eof    = "\004";
const char * OwlInstallInterface::qs_escape = "\033";
const char * OwlInstallInterface::qs_redraw = "\014";


#include <stdio.h>
#include <string.h>
#include <errno.h>

#include "cmd.hpp"

#include "parmfile.hpp"



ParametersFile::~ParametersFile()
{
    while(first) {
        Parameter* tmp = first->next;
        delete first;
        first = tmp;
    }
}

ParametersFile::Parameter&
ParametersFile::operator[](const ScriptVariable &name) const
{
    Parameter **res;
    for(res = &const_cast<Parameter*>(first); *res; res = &((*res)->next)) {
        if((*res)->name == name) return **res;
    }
    *res = new Parameter;
    (*res)->name = name;
    return **res;
}

bool ParametersFile::IsDefined(const ScriptVariable &name) const
{
    for(Parameter *tmp = first; tmp; tmp = tmp->next)
        if(tmp->name == name) return true;
    return false;
}

bool ParametersFile::Undefine(const ScriptVariable &name)
{
    Parameter **res;
    for(res = &first; *res; res = &((*res)->next)) {
        if((*res)->name == name) {
            Parameter *tmp = *res;
            *res = tmp->next;
            tmp->next = 0;
            delete tmp;
            return true;
        }
    }
    return false;
}

bool ParametersFile::Load(const ScriptVariable &filename)
{
    ReadStream f;
    if(!f.FOpen(filename.c_str())) {
        error = strerror(errno);
        return false;
    }
    this->filename = filename;
    ScriptVariable line;
    Parameter* last = new Parameter;
    first = last;
    while(f.ReadLine(line)) {
        ScriptVariable line2 = line;
        line2.Trim();
        if(line2 == "" || line2[0] == '#') {
            // comment or empty line: preserve it
            last->comment.AddItem(line);
        } else {
            // must be parameter
            ScriptVariable::Substring eq = line2.Strchr('=');
            if(eq.Invalid()) {
                error = "Invalid line: ";
                error += line2;
                return false;
            }
            ScriptVariable::Substring eq2 = eq;
            eq.ExtendToBegin();
            eq.Resize(-1);
            last->name = eq.Get();
            last->name.Trim();
            eq2.Move(1);
            eq2.ExtendToEnd();
            last->value = eq2.Get();
            last->value.Trim();
            last->next = new Parameter;
            last = last->next;
        }
    }
    return true;
}

bool ParametersFile::Save() const
{
    if(filename == "") {
        error = "No file name to save";
        return false;
    }
    return SaveAs(filename);
}

bool ParametersFile::SaveAs(const ScriptVariable &filename) const
{
    FILE *f = fopen(filename.c_str(), "w");
    if(!f) {
        error = filename + ": " + strerror(errno);
        return false;
    }
    for(Parameter *p = first; p; p = p->next) {
        if(p->comment.Length() > 0) {
            fputs(p->comment.Join("\n").c_str(), f);
            fputs("\n", f);
        }
        if(p->name != "") {
            fputs((p->name + "=" + p->value).c_str(), f);
            fputs("\n", f);
        }
    }
    fclose(f);
    return true;
}


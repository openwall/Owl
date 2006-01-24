#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <termios.h>

#include "scriptpp/scrvect.hpp"

#include "iface_dumb.hpp"

class SymbolicInterruption {
    int save_vintr;
    int save_verase;
    int save_lflag;
public:
    SymbolicInterruption();
    ~SymbolicInterruption();

    int EraseChar() const;
    int InterruptChar() const;
};

SymbolicInterruption::SymbolicInterruption()
{
    struct termios t;
    tcgetattr(0, &t);
    save_verase = t.c_cc[VERASE];
    save_vintr = t.c_cc[VINTR];
    t.c_cc[VINTR] = 0;
    save_lflag = t.c_lflag;
    t.c_lflag &= ~ICANON;
    tcsetattr(0, TCSANOW, &t);
}

SymbolicInterruption::~SymbolicInterruption()
{
    struct termios t;
    tcgetattr(0, &t);
    t.c_cc[VINTR] = save_vintr;
    t.c_lflag = save_lflag;
    tcsetattr(0, TCSANOW, &t);
}

int SymbolicInterruption::InterruptChar() const
{
    return save_vintr;
}

int SymbolicInterruption::EraseChar() const
{
    return save_verase;
}

static int get_terminal_columns()
{
    const char *env = getenv("COLUMNS");
    if(!env) return 80;
    char *endp;
    int res = strtol(env, &endp, 0);
    if(endp==env) return 80;
    return res;
}

static ScriptVariable KeyboardRead()
{
    SymbolicInterruption si;
    int c;
    ScriptVariable res;
    while((c=getchar())!=EOF) {
        if(c=='\n') break;
        if(c=='\r') continue;
        if(c==si.EraseChar() || c=='\177' || c=='\b') {
            if(res.Length() > 0) {
                res.Range(-1, 1).Erase();
                // now hide the last char and the "^?" (3 chars total)
                fputs("\b\b\b   \b\b\b", stdout);
            } else {
                // just hide the "^?" (2 chars total)
                fputs("\b\b  \b\b", stdout);
            }
            fflush(stdout);
            continue;
        }
        if(c==si.InterruptChar()) return OwlInstallInterface::qs_cancel;
        if(c=='\033') return OwlInstallInterface::qs_escape;
        if(c=='\014') return OwlInstallInterface::qs_redraw;
        if(!isprint(c)) {
            fputs("\b\b  \b\b", stdout);
            fflush(stdout);
            continue;
        }
        char x[2] = {0,0};
        x[0] = c;
        res += x;
    }
    if(c==EOF) {
        return OwlInstallInterface::qs_eof;
    }
    return res;
}

DumbIfaceSingleChoice::DumbIfaceSingleChoice()
    : IfaceSingleChoice()
{}

ScriptVariable DumbIfaceSingleChoice::Run()
{
    for(;;) {
        ScriptVariable choices;
        if(caption!="") {
            printf("\n%s\n", caption.c_str());
        }
        printf("\n");
        for(Item *p = first; p; p = p->next) {
            if(p->enabled) {
                printf("[%s]\t%s\n", p->label.c_str(), p->comment.c_str());
                choices += p->label;
                if (p->next) choices += " ";
            } else {
                printf("----\t%s\n", p->comment.c_str());
            }
        }
        for(;;) {
            if(defvalue == "") {
                printf("\nPlease type your choice (%s): ", choices.c_str());
            } else {
                printf("\nPlease type your choice (%s) [%s]: ",
                    choices.c_str(), defvalue.c_str());
            }
            ScriptVariable res = KeyboardRead();
            if(res == OwlInstallInterface::qs_redraw) {
                break; /* redraw menu */
            }
            if(res == "" && defvalue != "") {
                return defvalue;
            }
            if(res == OwlInstallInterface::qs_eof)
                return OwlInstallInterface::qs_eof;
            if(res == OwlInstallInterface::qs_cancel)
                return OwlInstallInterface::qs_cancel;
            if(res == OwlInstallInterface::qs_escape)
                return OwlInstallInterface::qs_cancel;
                   /* this is intentional! it's no bug here */
            ScriptVector v(res);
            for(Item *p = first; p; p = p->next) {
                if(p->enabled && p->label == v[0]) return p->label;
            }
            /* if no valid choice was given, we just redraw the menu */
        }
    }
}

/////////////////////////////////////////////////////////////
//

DumbIfaceHierChoice::DumbIfaceHierChoice()
    : IfaceHierChoice()
{}

bool DumbIfaceHierChoice::Run(ScriptVector &result)
{
    if(!first) {
       printf("\n\nNo items to choose\n\n");
       return false;
    }
    Item *level = first;
    do {
        int maxlen = 0;
        for(Item *p = level; p; p = p->next) {
            int l = p->name.Length();
            if(p->children) l+=2;
            if(l>maxlen) maxlen = l;
        }
        int cols = get_terminal_columns() / (maxlen+1);
        int n = 0;
        printf("\n\n");
        for(Item *p = level; p; p = p->next) {
             if(n>0 && n%cols == 0) printf("\n");
             n++;
             if(p->children)
                 printf("%-*s ", maxlen,
                        (ScriptVariable("[")+p->name+"]").c_str());
             else
                 printf("%-*s ", maxlen, p->name.c_str());
        }
        printf("\n\nYour choice? (Ctrl-C to cancel%s) ",
               level == first ? "" : ", Escape to UP");

        ScriptVariable res = KeyboardRead();

        if(res == OwlInstallInterface::qs_cancel ||
           res == OwlInstallInterface::qs_eof)
        {
            return false;
        }
        if(res == OwlInstallInterface::qs_redraw)
            continue; /* redraw the menu */
        if(res == OwlInstallInterface::qs_escape) {
            // UP
            if(level->parent) {
                if(level->parent->parent)
                    level = level->parent->parent->children;
                else
                    level = first;
            }
        } else {
            res.Trim("[] ");
            Item *p;
            for(p = level; p; p = p->next) {
                bool eq = ignore_case ?
                    strcasecmp(p->name.c_str(), res.c_str()) == 0 :
                    p->name == res;
                if(eq) {
                    if(p->children) {
                        level = p->children;
                        break;
                    } else {
                        // here it is!
                        result.Clear();
                        result[0] = p->name;
                        while(level->parent) {
                            result.Insert(0, level->parent->name);
                            level = level->parent;
                        }
                        return true;
                    }
                }
            }
            if(!p) printf("Invalid choice!\n");
        }
    } while(true);
}

/////////////////////////////////////////////////////////////
//


IfaceSingleChoice* DumbOwlInstallInterface::CreateSingleChoice() const
{
    return new DumbIfaceSingleChoice;
}

IfaceHierChoice* DumbOwlInstallInterface::CreateHierChoice() const
{
    return new DumbIfaceHierChoice;
}

void DumbOwlInstallInterface::Message(const ScriptVariable& msg)
{
    printf("\n%s\nPress Enter to continue...\n", msg.c_str());
    int c;
    do { c = getchar(); } while(c!=EOF && c!='\n');
}

void DumbOwlInstallInterface::Notice(const ScriptVariable& msg)
{
    printf("\n%s\n\n", msg.c_str());
}

bool DumbOwlInstallInterface::YesNoMessage(const ScriptVariable& msg,
                                           bool dfl)
{
    for(;;) {
        printf("\n%s (yes|no) [%s] ", msg.c_str(), dfl ? "yes" : "no");
        ScriptVariable res = KeyboardRead();
        if(res==qs_redraw) continue;
        res.Trim(" \n\r\t");
        res.Tolower();
        if(res=="") return dfl;
        if(res=="yes") return true;
        if(res=="no"||res==qs_cancel||res==qs_escape||res==qs_eof)
        {
            return false;
        }
        printf("Please answer \"yes\" or \"no\"\n");
    }
}

YesNoCancelResult
DumbOwlInstallInterface::YesNoCancelMessage(const ScriptVariable& msg, 
                                            int dfl)
{
    const char *dflname;
    switch(dfl) {
        case ync_yes:    dflname = "yes";    break;
        case ync_no:     dflname = "no";     break;
        case ync_cancel: dflname = "cancel"; break;
        default:
            dfl = ync_cancel;
            dflname = "cancel";
    }
    for(;;) {
        printf("\n%s (yes|no|cancel) [%s] ", msg.c_str(), dflname);
        ScriptVariable res = KeyboardRead();
        if(res==qs_redraw) continue;
        res.Trim(" \n\r\t");
        res.Tolower();
        if(res=="yes") return ync_yes;
        if(res=="no") return ync_no;
        if(res=="cancel"||res==qs_cancel||res==qs_escape||res==qs_eof)
            return ync_cancel;
        if(res=="") return (YesNoCancelResult)dfl;
        printf("Please answer \"yes\", \"no\", or \"cancel\"\n");
    }
}

ScriptVariable
DumbOwlInstallInterface::QueryString(const ScriptVariable& prompt,
                                     const ScriptVariable& defval)
{
    ScriptVariable res;

    for(;;) {
        const char int_pr[] = "(Interrupt (Ctrl-C) to cancel)";
        unsigned int margin = get_terminal_columns() -2;
#if 0
        if(prompt.Length() + sizeof(int_pr) > margin)  {
            printf("\n\t\t\t%s\n%s\n", int_pr, prompt.c_str());
        } else {
            printf("\n%-*s %s\n", margin - sizeof(int_pr) - 2,
                                 prompt.c_str(),
                                 int_pr);
        }
#else
        printf("\n%*s\n%s", margin - 2, int_pr, prompt.c_str());
#endif
        if(defval != "")
            printf(" [%s]", defval.c_str());
        printf(": ");
        res = KeyboardRead();
        if(res == qs_redraw) continue;
        break;
    }
    if(res == qs_escape) res = qs_cancel;
    return res == "" ? defval : res;
}

void DumbOwlInstallInterface::ExecWindow(const ScriptVariable& msg)
{
    printf("\n%s\n\n", msg.c_str());
}

void DumbOwlInstallInterface::CloseExecWindow()
{
    printf("\n\n");
}

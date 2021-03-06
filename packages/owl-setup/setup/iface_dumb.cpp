#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include <termios.h>

#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>

#include "scriptpp/scrvect.hpp"

#include "iface_dumb.hpp"

   /* if any item of a "hierarchical choice" menu is longer than
      this, then print item numbers and expect the user to type
      them instead of the item text
    */
static const int maximum_length_for_unnumbered_hierchoice = 15;
   /* reduce the number of columns until there's at least this
      many (fully filled) rows. Well, it looks ugly when there are
      2 rows and the second of them isn't filled
    */
static const int minimum_rows_for_multicol_hierchoice = 3;



class SymbolicInterruption {
    struct termios save_ti;
public:
    SymbolicInterruption();
    ~SymbolicInterruption();

    int EofChar() const;
    int EraseChar() const;
    int InterruptChar() const;
};

SymbolicInterruption::SymbolicInterruption()
{
    struct termios t;
    tcgetattr(0, &t);
    save_ti = t;
    t.c_cc[VINTR] = 0;
    t.c_cc[VMIN] = 1;
    t.c_cc[VTIME] = 0;
    t.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(0, TCSANOW, &t);
}

SymbolicInterruption::~SymbolicInterruption()
{
    tcsetattr(0, TCSANOW, &save_ti);
}

int SymbolicInterruption::InterruptChar() const
{
    return save_ti.c_cc[VINTR];
}

int SymbolicInterruption::EraseChar() const
{
    return save_ti.c_cc[VERASE];
}

int SymbolicInterruption::EofChar() const
{
    return save_ti.c_cc[VEOF];
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


static int my_getchar()
{
    char c;
    int r;
    fflush(stdout);
    r = read(0, &c, 1);
    if(r<1) return EOF;
    return c;
}

static ScriptVariable KeyboardRead(bool blind = false)
{
    SymbolicInterruption si;
    int c;
    ScriptVariable res;
    while((c=my_getchar())!=EOF) {
        if(c=='\n') break;
        if(c=='\r') continue;
        if(c==si.EraseChar() || c=='\177' || c=='\b') {
            if(res.Length() > 0) {
                res.Range(-1, 1).Erase();
                // now hide the last char
                if(!blind)
                    fputs("\b \b", stdout);
            }
            if(!blind)
                fflush(stdout);
            continue;
        }
        if(c==si.InterruptChar()) return OwlInstallInterface::qs_cancel;
        if(c==si.EofChar()) return OwlInstallInterface::qs_cancel;
        if(c=='\033') return OwlInstallInterface::qs_escape;
        if(c=='\014') return OwlInstallInterface::qs_redraw;
        if(!isprint(c)) {
            // just ignore
            continue;
        }
        if(!blind) {
            putchar(c);
            fflush(stdout);
        }
        char x[2] = {0,0};
        x[0] = c;
        res += x;
    }
    if(c==EOF) {
        return OwlInstallInterface::qs_eof;
    }
    putchar('\n');
    return res;
}

static const char interrupt_prompt[] = "(Interrupt (Ctrl-C) to cancel)";



/////////////////////////////////////////////////
//

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
    : IfaceHierChoice(), numbers(false)
{}

bool DumbIfaceHierChoice::Run(ScriptVector &result, const void **uptr)
{
    if(!first) {
        printf("\n\nNo items to choose\n\n");
        return false;
    }
    Item *level = first;
    do {
        int maxlen = 0;
        int itscount = 0;
        for(Item *p = level; p; p = p->next) {
            int l = p->name.Length();
            if(p->children) l+=2;
            if(l>maxlen) maxlen = l;
            itscount++;
        }
        if(maxlen > maximum_length_for_unnumbered_hierchoice) {
            numbers = true;
            maxlen += 5; // 5 == length("125) ")
            // well let's assume noone will ever need 1000 items
            // in a single level in the numbered mode (that is,
            // when some items are longer than 15), because no
            // user can read such a list without getting totally mad
        }
        int cols = get_terminal_columns() / (maxlen+1);
        while(cols > 1 &&
              itscount/cols < minimum_rows_for_multicol_hierchoice) cols--;
        int n = 0;
        printf("\n\n");
        for(Item *p = level; p; p = p->next) {
             if(n>0 && n%cols == 0) printf("\n");
             n++;
             ScriptVariable num;
             if(numbers) {
                 num = ScriptVariable(7, "%3d) ", n);
             }
             if(p->children)
                 printf("%-*s ", maxlen,
                        (num+"["+p->name+"]").c_str());
             else
                 printf("%-*s ", maxlen, (num+p->name).c_str());
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
            long intres;
            Item *p;
            if(numbers && res.GetLong(intres)
               && intres>0 && intres<=itscount)
            {
                // item number entered
                int i;
                for(i=1, p=level; i<intres && p; i++, p=p->next) {}
            } else {
                for(p = level; p; p = p->next) {
                    bool eq = ignore_case ?
                        strcasecmp(p->name.c_str(), res.c_str()) == 0 :
                        p->name == res;
                    if(eq) break;
                }
            }
            if(!p) {
                printf("Invalid choice!\n");
            } else if(p->children) {
                level = p->children;
            } else {
                // here it is!
                result.Clear();
                result[0] = p->name;
                if(uptr) {
                    *uptr = p->userptr;
                }
                while(level->parent) {
                    result.Insert(0, level->parent->name);
                    level = level->parent;
                }
                return true;
            }
        }
    } while(true);
}

/////////////////////////////////////////////////////////////
//

void DumbIfaceProgressBar::Draw()
{
    unsigned int margin = get_terminal_columns() -2;
    printf("\n%*s\n", margin - 2, message.c_str());
    SetCurrent(0);
}

void DumbIfaceProgressBar::SetCurrent(int c)
{
    current = c;
    printf("\r%s %s", title.c_str(), ProgressText().c_str());
    fflush(stdout);
}

void DumbIfaceProgressBar::Erase()
{
    printf("\n");
}

/////////////////////////////////////////////////////////////
//

DumbIfaceProgressCanceller::DumbIfaceProgressCanceller()
{
    pid = 0;
    si = 0;
}

DumbIfaceProgressCanceller::~DumbIfaceProgressCanceller()
{
    Remove();
}

void DumbIfaceProgressCanceller::Run(int signo)
{
    if(pid > 0) {
        Remove();
    }
    si = new SymbolicInterruption;
    int my_pid = getpid();
    pid = fork();
    if(pid == -1) { pid = 0; return; } /* silently ignore this ... */
    if(pid == 0) { /* child */
        int c;
        while((c=my_getchar()) != EOF) {
            if(c == si->InterruptChar()) {
                kill(my_pid, signo);
                exit(0);
            }
        }
        exit(1);
    }
}

void DumbIfaceProgressCanceller::Remove()
{
    if(pid != 0) {
        kill(pid, SIGTERM);
        waitpid(pid, 0, 0);
        pid = 0;
    }
    if(si) {
        delete si;
        si = 0;
    }
}

const char* DumbIfaceProgressCanceller::Message() const
{
    return interrupt_prompt;
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


IfaceProgressBar*
DumbOwlInstallInterface::CreateProgressBar(const ScriptVariable &title,
                                           const ScriptVariable &msg,
                                           int total,
                                           const ScriptVariable &units,
                                           int order) const
{
    return new DumbIfaceProgressBar(title, msg, total, units.c_str(), order);
}

IfaceProgressCanceller*
DumbOwlInstallInterface::CreateProgressCanceller() const
{
    return new DumbIfaceProgressCanceller();
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
                                     const ScriptVariable& defval,
                                     bool blind)
{
    ScriptVariable res;

    for(;;) {
        unsigned int margin = get_terminal_columns() -2;
#if 0
        if(prompt.Length() + sizeof(interrupt_prompt) > margin)  {
            printf("\n\t\t\t%s\n%s\n", interrupt_prompt, prompt.c_str());
        } else {
            printf("\n%-*s %s\n", margin - sizeof(interrupt_prompt) - 2,
                                 prompt.c_str(),
                                 interrupt_prompt);
        }
#else
        printf("\n%*s\n%s", margin - 2, interrupt_prompt, prompt.c_str());
#endif
        if(defval != "")
            printf(" [%s]", defval.c_str());
        printf(": ");
        res = KeyboardRead(blind);
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

void DumbOwlInstallInterface::CloseExecWindow(bool keywait)
{
    printf("\n\n");
    if(keywait) {
        printf("Press Enter to continue...");
        fflush(stdout);
        int c;
        do { c = getchar(); } while(c != '\n' && c != EOF);
    }
}

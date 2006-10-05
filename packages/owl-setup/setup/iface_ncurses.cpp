#ifdef NCURSES_ENABLE

#include <stdio.h>
#include <ctype.h>
#include <curses.h>
#include <menu.h>
#include <cdk/cdk.h>

#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <unistd.h>

#include "scriptpp/scrvect.hpp"

#include "iface_ncurses.hpp"

#if 1
enum the_color_pairs {
    cp_default = 57,
    cp_disabled = 25,
    cp_selection = 29,
    cp_background = 53
};
#else
enum the_color_pairs {
    cp_default = 57,
    cp_disabled = 49,
    cp_selection = 5,
    cp_background = 7
};
#endif

static ScriptVariable cdk_tag_default(0, "</%d>", cp_default);
static ScriptVariable cdk_tag_disabled(0, "</%d>", cp_disabled);
static ScriptVariable cdk_tag_selection(0, "</%d>", cp_selection);

static bool work_with_colors = false;
    /* this variable looks bad but it adds no badness to our architecture
     * because curses&cdk have their own global states for color issues;
     * so, no additional global state is really created
     */

NcursesIfaceSingleChoice::NcursesIfaceSingleChoice()
    : IfaceSingleChoice()
{}


static void do_menu_move(MENU *the_menu, int direction)
{
    ITEM* last_current = current_item(the_menu);
    ITEM* cur;
    do {
        menu_driver(the_menu, direction);
        cur = current_item(the_menu);
        if(cur == last_current) {
            // this means we're in an endless cycle, bail out
            break;
        }
    } while((item_opts(cur) & O_SELECTABLE) == 0);
}

ScriptVariable NcursesIfaceSingleChoice::Run()
{
    int nitem = 0;
    for(Item *p = first; p; p = p->next) nitem++;
    ITEM **menu_items = new ITEM* [nitem+1];
    int i = 0;
    for(Item *p = first; p; p = p->next) {
        menu_items[i] =
            new_item(p->enabled ? p->label.c_str() : "----",
                     p->comment.c_str());
        if(!p->enabled)
            item_opts_off(menu_items[i], O_SELECTABLE);
        i++;
    }
    menu_items[nitem] = 0;
    MENU *the_menu = new_menu(menu_items);


    int rows, cols;
    scale_menu(the_menu, &rows, &cols);
    int caprows = (caption == "") ? 0 : 2;
    if(cols < caption.Length())
        cols = caption.Length();
    int maxy, maxx;
    getmaxyx(stdscr, maxy, maxx);
    int begy = (maxy - rows - 4) / 2;
    int begx = (maxx - cols - 6) / 2;
    if(begy < 0) begy = 0;
    if(begx < 0) begx = 0;
    WINDOW *mwin = newwin(rows + 2 + caprows, cols + 6, begy, begx);
    set_menu_win(the_menu, mwin);
    WINDOW *mwin_d = derwin(mwin, rows, cols, 1 + caprows, 4);
    set_menu_sub(the_menu, mwin_d);

    if(work_with_colors) {
        wcolor_set(mwin, cp_default, 0);
        wbkgdset(mwin, COLOR_PAIR(cp_default));
        wbkgdset(mwin_d, COLOR_PAIR(cp_default));
        werase(mwin);
        set_menu_fore(the_menu, COLOR_PAIR(cp_selection)|A_BOLD);
        set_menu_back(the_menu, COLOR_PAIR(cp_default));
        set_menu_grey(the_menu, COLOR_PAIR(cp_disabled));
    }

    if(caption != "") {
        mvwprintw(mwin, 1, 4, "%s", caption.c_str());
    }

    refresh();

    set_menu_mark(the_menu, "");

    menu_opts_on(the_menu, O_ONEVALUE|O_SHOWDESC);
    menu_opts_off(the_menu, O_NONCYCLIC|O_SHOWMATCH);
    box(mwin, 0, 0);

    post_menu(the_menu);

    if(defvalue!="") {
        ITEM* first = current_item(the_menu);
        ITEM* cur = first;
        while(defvalue != item_name(cur))  {
            menu_driver(the_menu, REQ_NEXT_ITEM);
            cur = current_item(the_menu);
            if(cur == first) {
                // this means we're in a endless cycle, bail out
                break;
            }
        }
    }

    keypad(mwin, TRUE);
    wrefresh(mwin);

    ScriptVariable result;
    for(;;) {
        int c = wgetch(mwin);
        switch(c) {
            case '\n':
            case '\r':
            case KEY_ENTER:
            case KEY_SELECT:
            case KEY_HOME:
                result = item_name(current_item(the_menu));
                goto quit;
            case KEY_DOWN:
                do_menu_move(the_menu, REQ_DOWN_ITEM);
                break;
            case KEY_UP:
                do_menu_move(the_menu, REQ_UP_ITEM);
                break;
            case KEY_CANCEL:
            case KEY_EXIT:
            case '\033':
                result = OwlInstallInterface::qs_cancel;
                     /* this is intentionally cancel, not escape! */
                     /* it's no bug here */
                goto quit;
            default:
                for(Item *p = first; p; p = p->next, i++) {
                    char s[2];
                    s[0] = c;
                    s[1] = 0;
                    if(p->label == s) {
                        result = s;
                        goto quit;
                    }
                }
        }
    }

quit:
    unpost_menu(the_menu);
    free_menu(the_menu);
    wclear(mwin);
    wrefresh(mwin);
    delwin(mwin);
    clear();
    refresh();
    for(int i=0; i<nitem; i++) free_item(menu_items[i]);
    delete[] menu_items;

    return result;

}

/////////////////////////////////////////////////////////////
//

NcursesIfaceHierChoice::NcursesIfaceHierChoice(void *a_screen)
    : IfaceHierChoice()
{
    the_cdkscreen = a_screen;
}


static int common_prefix_length(const ScriptVariable &v1,
                                const ScriptVariable &v2)
{
    int i;
    for(i=0; v1[i] && (v1[i] == v2[i]); i++) {}
    return i;
}

static int calc_scroll_position(const ScriptVector &items,
                                ScriptVariable &str)
{
    int bestmatch = -1;
    int bestmatchcpl = 0;
    ScriptVariable strup = str;
    strup.Toupper();
    for(int i=0; i<items.Length(); i++) {
        ScriptVariable cur(items[i]);
        if(cur[0]=='<') {
            ScriptVariable::Substring s(cur.Strchr('>'));
            s.ExtendToBegin();
            s.Erase();
        }
        cur.Trim("[] ");
        cur.Toupper();
        if(cur.HasPrefix(strup)) return i;
        int cpl = common_prefix_length(cur, strup);
        if(cpl > 0) {
            if(bestmatch == -1 || bestmatchcpl < cpl) {
                bestmatch = i;
                bestmatchcpl = cpl;
            }
        }
    }
    str.Range(bestmatchcpl, -1).Erase();
    return bestmatch;
}

static int run_scroll(CDKSCREEN *screen,
                      ScriptVariable header, ScriptVariable header2,
                      ScriptVector items)
{
    int res = -1;

    ScriptVariable quick_search("");

    if(work_with_colors) {
        for(int i=0; i<items.Length(); i++)
            items[i] = cdk_tag_default + items[i];
        header = cdk_tag_default + header;
        if(header2!="")
            header2 = cdk_tag_default + header2;
    }
    if(header2!="")
        header2 = ScriptVariable("<R>") + header2;

    char **itemsv = items.MakeArgv();

    int maxlen = 0;
    for(int i=0; i<items.Length(); i++) {
        if(maxlen < items[i].Length()) maxlen = items[i].Length();
    }

    CDKSCROLL* list =
        newCDKScroll(screen, CENTER, CENTER, RIGHT, -4, maxlen + 6,
                     (char*)(header+"\n"+header2).c_str(),
                     itemsv, items.Length(),
                     false,
                     work_with_colors ?
                         COLOR_PAIR(cp_selection)|A_BOLD
                         : A_REVERSE,
                     true, false);

    if(work_with_colors)
        setCDKScrollBackgroundColor(list, (char*)cdk_tag_default.c_str());

    drawCDKScroll(list, true);

    for(;;) {
        int c = wgetch(stdscr);
        switch(c) {
#if '\n' != KEY_RETURN
            case '\n':
#endif
            case '\r':
            case KEY_ENTER:
            case KEY_RETURN:
            case KEY_SELECT:
                quick_search = "";
                res = injectCDKScroll(list, KEY_ENTER);
                if(res == -1)
                    res = injectCDKScroll(list, KEY_RETURN);
                goto quit;
            case KEY_CANCEL:
            case KEY_EXIT:
            case '\033':
                quick_search = "";
                res = -1;
                goto quit;
            case KEY_BACKSPACE:
            case DELETE:
            case CONTROL('H'):
            case KEY_DC:
                quick_search.Range(-1,1).Erase();
                break;
            default:
                if(c>0 && c<=255 && isprint(c)) {
                    quick_search += (char)c;
                    //quick_search.Toupper();
                } else {
                    quick_search = "";
                    injectCDKScroll(list, c);
                }
        }
        if(quick_search != "") {
            int pos = calc_scroll_position(items, quick_search);
            if(pos>=0) {
                setCDKScrollPosition(list, pos);
                drawCDKScroll(list, true);
            }
        }
        if(quick_search != "") {
            int maxy, maxx;
            getmaxyx(stdscr, maxy, maxx);
            int x = (maxx - maxlen) / 2 + maxlen - quick_search.Length() - 2;
            int y = maxy - 4;
            mvprintw(y, x, "[%s]", quick_search.c_str());
            refresh();
        } else {
            // restore the box
            drawCDKScroll(list, true);
        }
    }
quit:
    eraseCDKScroll(list);
    destroyCDKScroll(list);
    clear();
    refresh();
    items.DeleteArgv(itemsv);
    return res;
}

bool NcursesIfaceHierChoice::Run(ScriptVector &result)
{
    if(!first) {
       return false;
    }
    Item *level = first;
    do {
        ScriptVector items;
        for(Item *p = level; p; p = p->next) {
            if(p->children)
                items.AddItem(ScriptVariable("[")+p->name+"]");
            else
                items.AddItem(p->name);
        }

        ScriptVariable header;
        for(Item *p = level->parent; p; p = p->parent) {
            header = p->name + " >> " + header;
        }

        int rn =
            run_scroll((CDKSCREEN*)the_cdkscreen, caption, header, items);

        if(rn == -1) {
            // UP
            if(level->parent) {
                if(level->parent->parent)
                    level = level->parent->parent->children;
                else
                    level = first;
            } else {
                return false;
            }
        } else {
            ScriptVariable res = items[rn];
            res.Trim("[] ");
            Item *p;
            for(p = level; p; p = p->next) {
                if(p->name == res) {
                    if(p->children) {
                        level = p->children;
                        break;
                    } else {
                        // here it is!
                        result.Clear();
                        result[0] = res;
                        while(level->parent) {
                            result.Insert(0, level->parent->name);
                            level = level->parent;
                        }
                        return true;
                    }
                }
            }
            if(!p) {
                // in fact this should never be reached
                return false;
            }
        }
    } while(true);
}

/////////////////////////////////////////////////////////////
//

void NcursesIfaceProgressBar::Draw()
{
    ScriptVector vect(title, "\n", "");
    for(int i=0; i<vect.Length(); i++)
        vect[i] = ScriptVariable("<C>")+cdk_tag_default+vect[i];
    vect.AddItem(ScriptVariable(0, "<C></%d>[", cp_default) + message + "]");
    ScriptVariable t = vect.Join("\n");
    ScriptVariable lab(0, "</%d>%d %s ", cp_default, total, units.c_str());
    if(total == 0 || units == "%") lab = "";
    if(the_slider) destroyCDKSlider((CDKSLIDER*)the_slider);
    the_slider = (void*) newCDKSlider((CDKSCREEN*)the_screen,
                                    CENTER, CENTER,
                                    (char*)(t.c_str()),
                                    (char*)(lab.c_str()),
                                    work_with_colors ?
                                        COLOR_PAIR(cp_selection)|A_BOLD
                                        : A_REVERSE,
                                    -(lab.Length()+10),
                                    0, 0, total, 1, 1, TRUE, FALSE);
    if(work_with_colors)
        setCDKSliderBackgroundColor((CDKSLIDER*)the_slider,
                                    (char*)cdk_tag_default.c_str());
    drawCDKSlider((CDKSLIDER*)the_slider, TRUE);
    SetCurrent(0);
}

void NcursesIfaceProgressBar::SetCurrent(int c)
{
    if(!the_slider) return;
    setCDKSlider((CDKSLIDER*)the_slider, 0, total, c, FALSE);
    drawCDKSlider((CDKSLIDER*)the_slider, FALSE);
}

void NcursesIfaceProgressBar::Erase()
{
    eraseCDKSlider((CDKSLIDER*)the_slider);
    destroyCDKSlider((CDKSLIDER*)the_slider);
    the_slider = 0;
    clear();
    refresh();
}

/////////////////////////////////////////////////////////////
//

NcursesIfaceProgressCanceller::NcursesIfaceProgressCanceller()
{
    pid = 0;
}

NcursesIfaceProgressCanceller::~NcursesIfaceProgressCanceller()
{
    Remove();
}

void NcursesIfaceProgressCanceller::Run(int signo)
{
    if(pid > 0) {
        Remove();
    }
    int my_pid = getpid();
    pid = fork();
    if(pid == -1) { pid = 0; return; } /* silently ignore this ... */
    if(pid == 0) { /* child */
        int c;
        for(;;) {
            c = wgetch(stdscr);
            if(c == '\033' || c == KEY_CANCEL) {
                kill(my_pid, signo);
                exit(0);
            }
        }
        exit(1);
    }
}

void NcursesIfaceProgressCanceller::Remove()
{
    if(pid != 0) {
        kill(pid, SIGTERM);
        waitpid(pid, 0, 0);
        pid = 0;
    }
}

const char* NcursesIfaceProgressCanceller::Message() const
{
    return "Press Escape to cancel";
}

/////////////////////////////////////////////////////////////
//

NcursesOwlInstallInterface::NcursesOwlInstallInterface(bool allow_colors)
{
    /* The code with checking for the initscr()'s return value
       just found useless because in ncurses, initscr() calls
       exit(2) itself (indirectly) and doesn't seem to return NULL
       in any conditions
     */
#if 0
    if(!initscr()) {
        fprintf(stderr, "ERROR INITIALIZING SCREEN!!!\n");
        exit(22);
    }
#else
    initscr();
#endif
    keypad(stdscr, TRUE);
    nonl();
    cbreak();
    noecho();

    cdkscreen = (void*)initCDKScreen(stdscr);

    if(allow_colors && has_colors()) {
        start_color();
        initCDKColor();
        bkgdset(COLOR_PAIR(cp_background));
        erase();
        work_with_colors = true;
    } else {
        work_with_colors = false;
    }


    noticewin = 0;
    ClearNotices();


}

NcursesOwlInstallInterface::~NcursesOwlInstallInterface()
{
    delwin((WINDOW*)noticewin);
    if(work_with_colors)
        bkgdset(0);
    clear();
    refresh();
    endCDK();
    endwin();
}

IfaceSingleChoice* NcursesOwlInstallInterface::CreateSingleChoice() const
{
    return new NcursesIfaceSingleChoice;
}

IfaceHierChoice* NcursesOwlInstallInterface::CreateHierChoice() const
{
    return new NcursesIfaceHierChoice((void*)cdkscreen);
}

IfaceProgressBar*
NcursesOwlInstallInterface::CreateProgressBar(const ScriptVariable &title,
                                           const ScriptVariable &msg,
                                           int total,
                                           const ScriptVariable &units,
                                           int order) const
{
    return new NcursesIfaceProgressBar(cdkscreen,
                                title, msg, total, units.c_str(), order);
}

IfaceProgressCanceller*
NcursesOwlInstallInterface::CreateProgressCanceller() const
{
    return new NcursesIfaceProgressCanceller();
}

void NcursesOwlInstallInterface::Message(const ScriptVariable& msg)
{
    ScriptVector vect(msg, "\n", "");
    vect.AddItem("");
    for(int i=0; i<vect.Length(); i++)
        vect[i] = cdk_tag_default + vect[i];
    vect.AddItem(ScriptVariable(0, "<C></%d> [ press a key... ]",
                                cp_default));
    char **message = vect.MakeArgv();
    CDKLABEL* lab = newCDKLabel((CDKSCREEN*)cdkscreen, CENTER, CENTER, message,
                                vect.Length(), true, false);
    if(work_with_colors)
        setCDKLabelBackgroundColor(lab, (char*)cdk_tag_default.c_str());
    drawCDKLabel(lab, true);
    waitCDKLabel(lab, 0);
    eraseCDKLabel(lab);
    destroyCDKLabel(lab);
    vect.DeleteArgv(message);
    clear();
    refresh();
}

void NcursesOwlInstallInterface::Notice(const ScriptVariable& msg)
{
    scrollok((WINDOW*)noticewin, TRUE);
    scroll((WINDOW*)noticewin);
    mvwaddstr((WINDOW*)noticewin, 3, 0, msg.c_str());
    wrefresh((WINDOW*)noticewin);
}

void NcursesOwlInstallInterface::ClearNotices()
{
    if(noticewin) {
        delwin((WINDOW*)noticewin);
        refresh();
    }

    int maxy, maxx;
    getmaxyx(stdscr, maxy, maxx);
    noticewin = (void*) newwin(4, maxx - 4, maxy - 4, 2);

    if(work_with_colors) {
        wcolor_set((WINDOW*)noticewin, cp_default, 0);
        wbkgdset((WINDOW*)noticewin, COLOR_PAIR(cp_default));
        werase((WINDOW*)noticewin);
    }
}

/* this is a workaround against CDK's manner to ignore the Enter key */
/* popupDialog() could satisfy us if the problem is fixed */
static int run_dialog(CDKSCREEN *screen,
                      ScriptVector &message_vect,
                      ScriptVector &buttons_vect,
                      int dfl)
{
    int res = -1;

    if(work_with_colors) {
        for(int i=0; i<message_vect.Length(); i++)
            message_vect[i] = cdk_tag_default + message_vect[i];
        for(int j=0; j<buttons_vect.Length(); j++)
            buttons_vect[j] = cdk_tag_default + buttons_vect[j];
    }

    char **message = message_vect.MakeArgv();
    int msglen = message_vect.Length();
    char **buttons = buttons_vect.MakeArgv();
    int buttonscount = buttons_vect.Length();

    CDKDIALOG* dlg = newCDKDialog(screen, CENTER, CENTER,
                                  message, msglen, buttons, buttonscount,
                                  work_with_colors ?
                                      COLOR_PAIR(cp_selection)|A_BOLD :
                                      A_REVERSE,
                                  true, true, false);
    if(work_with_colors)
        setCDKDialogBackgroundColor(dlg, (char*)cdk_tag_default.c_str());
    drawCDKDialog(dlg, true);

    for(int k = 0; k< dfl; k++)
         injectCDKDialog(dlg, KEY_LEFT);

    for(;;) {
        int c = wgetch(stdscr);
        switch(c) {
#if '\n' != KEY_RETURN
            case '\n':
#endif
            case '\r':
            case KEY_ENTER:
            case KEY_RETURN:
            case KEY_SELECT:
                res = injectCDKDialog(dlg, KEY_ENTER);
                if(res == -1)
                    res = injectCDKDialog(dlg, KEY_RETURN);
                goto quit;
            case KEY_DOWN:
            case KEY_UP:
                break;
            case KEY_CANCEL:
            case KEY_EXIT:
            case '\033':
                res = -1;
                goto quit;
            default:
                injectCDKDialog(dlg, c);
        }
    }
quit:

    message_vect.DeleteArgv(message);
    buttons_vect.DeleteArgv(buttons);


    eraseCDKDialog(dlg);
    destroyCDKDialog(dlg);
    clear();
    refresh();
    return res;
}



bool NcursesOwlInstallInterface::YesNoMessage(const ScriptVariable& msg,
                                              bool dfl)
{
    ScriptVector yesno("Yes:No", ":");

    ScriptVector message(msg, "\n", "");
    message.AddItem("");

    int res = run_dialog((CDKSCREEN*)cdkscreen, message, yesno, dfl ? 0 : 1);

    return res == 0;
}

YesNoCancelResult
NcursesOwlInstallInterface::YesNoCancelMessage(const ScriptVariable& msg,
                                               int dfl)
{
    ScriptVector yesnoc("Yes:No:Cancel", ":");

    ScriptVector message(msg, "\n", "");
    message.AddItem("");

    int dflpos;
    switch(dfl) {
        case ync_yes:    dflpos = 0; break;
        case ync_no:     dflpos = 1; break;
        case ync_cancel: dflpos = 2; break;
        default:         dflpos = 2;
    }

    int res = run_dialog((CDKSCREEN*)cdkscreen, message, yesnoc, dflpos);

    switch(res) {
        case 0:
            return ync_yes;
        case 1:
            return ync_no;
        case 2:
            return ync_cancel;
        default:
            return ync_cancel;
    }
}


ScriptVariable
NcursesOwlInstallInterface::QueryString(const ScriptVariable& prompt,
                                        const ScriptVariable& defval,
                                        bool blind)
{
    CDKENTRY *entry;

    ScriptVector prom_v(prompt, "\n", " ");
    int i;
    for(i=0; i<prom_v.Length(); i++) {
        ScriptVariable tmp(0, "<C></%d> %s", cp_default, prom_v[i].c_str());
        prom_v[i] = tmp;
    }

    entry = newCDKEntry((CDKSCREEN*)cdkscreen, CENTER, CENTER,
                        (char*)prom_v.Join("\n").c_str(),
                        "",
                        work_with_colors ?
                            COLOR_PAIR(cp_selection)|A_BOLD
                            : A_NORMAL,
                        work_with_colors ? ' ' : '_',
                        blind ? vHMIXED : vMIXED,
                        -8, 0, 1024, TRUE, FALSE);
    if(work_with_colors)
        setCDKEntryBackgroundColor(entry, (char*)cdk_tag_default.c_str());
    if(defval != "")
        setCDKEntryValue(entry, (char*)defval.c_str());

    if(blind)
        setCDKEntryHiddenChar(entry, '*');

    const char *act_res = 0;

    drawCDKEntry(entry, true);

    for(;;) {
        int c = wgetch(stdscr);
        switch(c) {
#if '\n' != KEY_RETURN
            case '\n':
#endif
            case '\r':
            case KEY_ENTER:
            case KEY_RETURN:
            case KEY_SELECT:
                act_res = getCDKEntryValue(entry);
                goto quit;
            case KEY_DOWN:
            case KEY_UP:
                break;
            case KEY_CANCEL:
            case KEY_EXIT:
            case '\033':
                goto quit;
            case '\010': /* workaround for ru2 map... is it Ok? */
                /* I'm unsure about KEY_BACKSPACE, I only choose it because
                   in the version of CDK which I use, it appears explicitly
                   in the body of _injectCDKEntry(). However, in the
                   headers it is commented as 'unreliable'. Well... looks
                   like there's no _right_ thing, there's only a thing
                   which works.
                 */
                injectCDKEntry(entry, KEY_BACKSPACE);
                break;
            default:
                injectCDKEntry(entry, c);
        }
    }
quit:
    ScriptVariable res(act_res ? act_res : qs_cancel);
    eraseCDKEntry(entry);
    destroyCDKEntry(entry);
    clear();
    refresh();
    return res;
}

void NcursesOwlInstallInterface::ExecWindow(const ScriptVariable& msg)
{
    if(work_with_colors)
        bkgdset(0);
    erase();
    refresh();
    endwin();
    printf("%s\n", msg.c_str());
    fflush(stdout);
}

void NcursesOwlInstallInterface::CloseExecWindow(bool keywait)
{
    if(keywait) {
        printf("\n\nPress Enter to continue...");
        fflush(stdout);
        int c;
        do { c = getchar(); } while(c != '\n' && c != EOF);
    }
    if(work_with_colors) {
        bkgdset(COLOR_PAIR(cp_background));
        erase();
    }
    refresh();
}

#endif

#ifdef NCURSES_ENABLE

#include <stdio.h>
#include <ctype.h>
#include <curses.h>
#include <menu.h>
#include <cdk/cdk.h>

#include "scriptpp/scrvect.hpp"

#include "iface_ncurses.hpp"


NcursesIfaceSingleChoice::NcursesIfaceSingleChoice()
    : IfaceSingleChoice()
{}

ScriptVariable NcursesIfaceSingleChoice::Run()
{
    int nitem = 0;
    for(Item *p = first; p; p = p->next) nitem++;
    ITEM **menu_items = new (ITEM*)[nitem+1];
    int i = 0;
    for(Item *p = first; p; p = p->next, i++) {
        menu_items[i] = new_item(p->label.c_str(), p->comment.c_str());
        if(!p->enabled) 
            item_opts_off(menu_items[i], O_SELECTABLE);
    }
    menu_items[nitem] = 0;
    MENU *the_menu = new_menu(menu_items); 


    int rows, cols;
    scale_menu(the_menu, &rows, &cols);
    if(cols < caption.Length()) 
        cols = caption.Length();
    int maxy, maxx;
    getmaxyx(stdscr, maxy, maxx);
    int begy = (maxy - rows - 4) / 2;
    int begx = (maxx - cols - 6) / 2;
    if(begy < 0) begy = 0; 
    if(begx < 0) begx = 0; 
    WINDOW *mwin = newwin(rows + 4, cols + 6, begy, begx);
    set_menu_win(the_menu, mwin);
    set_menu_sub(the_menu, derwin(mwin, rows, cols, 3, 4));

    if(caption != "") {
        mvwprintw(mwin, 1, 4, "%s", caption.c_str());
    }

    refresh();

    set_menu_mark(the_menu, "");
    box(mwin, 0, 0);

    post_menu(the_menu);
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
                menu_driver(the_menu, REQ_DOWN_ITEM);
                break;
            case KEY_UP:
                menu_driver(the_menu, REQ_UP_ITEM);
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

static int run_scroll(CDKSCREEN *screen, 
                      ScriptVariable header, ScriptVector items)
{
    int res = -1;
 
    char **itemsv = items.MakeArgv();

    CDKSCROLL* list = 
        newCDKScroll(screen, CENTER, CENTER, RIGHT, -4, 20,
                     (char*)(header.c_str()), itemsv, items.Length(), 
                     false, A_REVERSE, true, false);

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
                res = injectCDKScroll(list, KEY_RETURN);
                goto quit;
            case KEY_CANCEL:
            case KEY_EXIT:
            case '\033':
                res = -1;
                goto quit;
            default:
                injectCDKScroll(list, c);
        }
    }
quit:
    eraseCDKScroll(list);
    destroyCDKScroll(list);
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
        header = caption + "\n" + header;
        
        int rn = run_scroll((CDKSCREEN*)the_cdkscreen, header, items);

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
                        // here is it! 
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

NcursesOwlInstallInterface::NcursesOwlInstallInterface()
{
    initscr();
    keypad(stdscr, TRUE);
    nonl();
    cbreak();
    noecho();
    cdkscreen = (void*)initCDKScreen(stdscr);

    int maxy, maxx;
    getmaxyx(stdscr, maxy, maxx);
    noticewin = (void*) newwin(4, maxx - 4, maxy - 5, 2);
}

NcursesOwlInstallInterface::~NcursesOwlInstallInterface()
{
    delwin((WINDOW*)noticewin);
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

void NcursesOwlInstallInterface::Message(const ScriptVariable& msg)
{
    ScriptVector vect(msg, "\n", "");
    vect.AddItem("");
    vect.AddItem("<C>[ press a key... ]");
    char **message = vect.MakeArgv();
    CDKLABEL* lab = newCDKLabel((CDKSCREEN*)cdkscreen, CENTER, CENTER, message,
                                vect.Length(), true, false);
    drawCDKLabel(lab, true);
    waitCDKLabel(lab, 0);
    eraseCDKLabel(lab);
    destroyCDKLabel(lab);
    vect.DeleteArgv(message);
    refresh();
}

void NcursesOwlInstallInterface::Notice(const ScriptVariable& msg)
{
    waddstr((WINDOW*)noticewin, msg.c_str());
    wrefresh((WINDOW*)noticewin);
}


/* this is a workaround against CDK's manner to ignore the Enter key */
/* popupDialog() could satisfy us if the problem is fixed */
static int run_dialog(CDKSCREEN *screen, 
                      char **message, int msglen, 
                      char **buttons, int buttonscount)
{
    int res = -1;

    CDKDIALOG* dlg = newCDKDialog(screen, CENTER, CENTER, 
                                  message, msglen, buttons, buttonscount, 
                                  A_REVERSE, true, true, false);
    drawCDKDialog(dlg, true);

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
    eraseCDKDialog(dlg);
    destroyCDKDialog(dlg);
    return res;
}
                      


bool NcursesOwlInstallInterface::YesNoMessage(const ScriptVariable& msg)
{
    static char *yesno[] = { "Yes", "No", 0 };
 
    ScriptVector vect(msg, "\n", "");
    vect.AddItem("");
    char **message = vect.MakeArgv();

    int res = 
        run_dialog((CDKSCREEN*)cdkscreen, message, vect.Length(), yesno, 2);

    vect.DeleteArgv(message);

    return res == 0;
}

YesNoCancelResult 
NcursesOwlInstallInterface::YesNoCancelMessage(const ScriptVariable& msg)
{
    static char *yesnoc[] = { "Yes", "No", "Cancel", 0 };
 
    ScriptVector vect(msg, "\n", "");
    vect.AddItem("");
    char **message = vect.MakeArgv();

    int res = 
        run_dialog((CDKSCREEN*)cdkscreen, message, vect.Length(), yesnoc, 3);

    vect.DeleteArgv(message);

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
                                        const ScriptVariable& defval)
{
    CDKENTRY *entry;

    entry = newCDKEntry((CDKSCREEN*)cdkscreen, CENTER, CENTER,
                        (char*)(ScriptVariable("<C> ")+prompt).c_str(), "",
                        A_NORMAL, '_', vMIXED,
                        -8, 0, 1024, TRUE, FALSE);
    if(defval != "") 
        setCDKEntryValue(entry, (char*)defval.c_str());

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
                act_res = injectCDKEntry(entry, '\r');
                goto quit;
            case KEY_DOWN:
            case KEY_UP:
                break;
            case KEY_CANCEL:
            case KEY_EXIT:
            case '\033':
                goto quit;
            default:
                injectCDKEntry(entry, c);
        }
    }
quit:   
    ScriptVariable res(act_res ? act_res : qs_cancel);
    eraseCDKEntry(entry);
    destroyCDKEntry(entry);
    refresh();
    return res;
}

void NcursesOwlInstallInterface::ExecWindow(const ScriptVariable& msg)
{
    endwin();
    printf("%s\n", msg.c_str());
}

void NcursesOwlInstallInterface::CloseExecWindow()
{
    refresh();
}

#endif

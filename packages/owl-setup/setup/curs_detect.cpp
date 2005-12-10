#include <stdio.h>
#include <curses.h>
#include <term.h>


bool is_terminal_curses_capable()
{
    int r;
    int errret;
    char *cupn;
    char *cuu1;
    char *home;

    r = setupterm(0, 1, &errret);

    if(r != OK || errret != 1)
        return false;

    /* In fact, this should be sufficient. 'man setupterm' says that
       <<A return value of OK combined with status of 1 in errret
       is normal>>, while if ERR is returned, errret can be 1, 0, or -1,
       for "hardcopy terminal", "too generic terminal" and "no termcap
       database" situations, respectively.

       Surprisingly enough, however, setupterm() pretends everything
       fine around if you specify TERM=dumb in the environment. Even
       more surprisingly (and funny, heh), ncurses starts for it and
       tries to do sometheing (without much success, though).

       So we perform an additional check here. "cup" is the termcap
       name for the escape sequence which positions the cursor. "Dumb"
       terminal doesn't have it (surprize! :), that's perhaps why
       curses can't run on it.

       Even if there's no cup, theoretically there's still a possibility
       to 'home' cursor or move it up line by line (I couldn't find
       a terminal without cup but with one of them, but let's honour the
       theory :)
     */

    cupn = tigetstr("cup");
    if(cupn && cupn != (char*)-1)
        return true;

    cuu1 = tigetstr("cuu1");
    if(cuu1 && cuu1 != (char*)-1)
        return true;

    home = tigetstr("home");
    if(home && home != (char*)-1)
        return true;


    return false;
}

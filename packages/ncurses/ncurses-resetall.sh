#!/bin/sh

# Xterm codes can be found here: 
# http://babayaga.math.fu-berlin.de/~rxvt/refer/refer.html
if [    a"$TERM" = axterm -o a"$TERM" = axterm-color -o \
        a"$TERM" = akterm -o a"$TERM" = arxvt ]; then
        # Disable X11 XTerm mouse reporting
        echo '[?1000l'
        
        # Reset foreground and background colors
        echo '[0m'
fi

# Reset the terminal
/usr/bin/reset

# Reset terminal size
if [ -f /usr/X11R6/bin/resize ]; then
        eval `resize`
fi


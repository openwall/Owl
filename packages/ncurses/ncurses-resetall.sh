#!/bin/sh

# xterm codes can be found here: 
# http://babayaga.math.fu-berlin.de/~rxvt/refer/refer.html
if [ "$TERM" = xterm -o "$TERM" = xterm-color -o \
    "$TERM" = kterm -o "$TERM" = rxvt ]; then
	# Disable X11 xterm mouse reporting
	echo -en '\033[?1000l'

	# Reset foreground and background colors
	echo -en '\033[0m'
fi

# Reset the terminal
/usr/bin/reset

# Reset terminal size
if [ -f /usr/X11R6/bin/resize ]; then
	eval `/usr/X11R6/bin/resize`
fi

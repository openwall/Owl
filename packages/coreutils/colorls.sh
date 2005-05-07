# color-ls initialization

COLORS=/etc/DIR_COLORS
if [ -f "/etc/DIR_COLORS.$TERM" -a -r "/etc/DIR_COLORS.$TERM" ]; then
	COLORS="/etc/DIR_COLORS.$TERM"
fi
if [ -f "$HOME/.dircolors" -a -r "$HOME/.dircolors" ]; then
	COLORS="$HOME/.dircolors"
fi
if [ -f "$HOME/.dircolors.$TERM" -a -r "$HOME/.dircolors.$TERM" ]; then
	COLORS="$HOME/.dircolors.$TERM"
fi
if [ -f "$HOME/.dir_colors" -a -r "$HOME/.dir_colors" ]; then
	COLORS="$HOME/.dir_colors"
fi
if [ -f "$HOME/.dir_colors.$TERM" -a -r "$HOME/.dir_colors.$TERM" ]; then
	COLORS="$HOME/.dir_colors.$TERM"
fi

if [ -f "$COLORS" -a -r "$COLORS" ]; then
	eval `dircolors --sh "$COLORS" ||:`
fi

if [ -z "${SHELL#*bash}" -o -z "${SHELL#*zsh}" ]; then
	if grep -Eqs '^COLOR[[:space:]]+all[[:space:]]*$' "$COLORS"; then
		alias ll='ls -l --color=always'
		alias l.='ls -d .[a-zA-Z]* --color=always'
		alias ls='ls --color=always'
	elif grep -Eqs '^COLOR[[:space:]]+tty[[:space:]]*$' "$COLORS"; then
		alias ll='ls -l --color=tty'
		alias l.='ls -d .[a-zA-Z]* --color=tty'
		alias ls='ls --color=tty'
	else
		alias ll='ls -l'
		alias l.='ls -d .[a-zA-Z]*'
	fi
fi

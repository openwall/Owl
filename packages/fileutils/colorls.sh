# color-ls initialization
COLORS=/etc/DIR_COLORS
[ -e "/etc/DIR_COLORS.$TERM" ] && COLORS="/etc/DIR_COLORS.$TERM"
[ -f "$HOME/.dircolors" ] && COLORS="$HOME/.dircolors"
[ -f "$HOME/.dircolors.$TERM" ] && COLORS="$HOME/.dircolors.$TERM"
[ -f "$HOME/.dir_colors" ] && COLORS="$HOME/.dir_colors"
[ -f "$HOME/.dir_colors.$TERM" ] && COLORS="$HOME/.dir_colors.$TERM"

[ -e "$COLORS" ] || exit 0

eval `dircolors --sh "$COLORS"`

if echo $SHELL | grep -Eq '/bash$|/zsh$'; then
	if grep -Eq '^COLOR[[:space:]]+all[[:space:]]*$' "$COLORS"; then
		alias ll='ls -l --color=always'
		alias l.='ls -d .[a-zA-Z]* --color=always'
		alias ls='ls --color=always'
	elif grep -Eq '^COLOR[[:space:]]+tty[[:space:]]*$' "$COLORS"; then
		alias ll='ls -l --color=tty'
		alias l.='ls -d .[a-zA-Z]* --color=tty'
		alias ls='ls --color=tty'
	else
		alias ll='ls -l'
		alias l.='ls -d .[a-zA-Z]*'
	fi
fi

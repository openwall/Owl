# color-ls initialization
COLORS=/etc/DIR_COLORS
eval `dircolors --sh /etc/DIR_COLORS`
[ -f "$HOME/.dircolors" ] && eval `dircolors --sh $HOME/.dircolors` && COLORS=$HOME/.dircolors

if echo $SHELL | grep -q bash; then # aliases are bash only
	if ! egrep -qi "^COLOR.*none" $COLORS; then
		alias ll='ls -l --color=tty'
		alias l.='ls -d .[a-zA-Z]* --color=tty'
		alias ls='ls --color=tty'
	else
		alias ll='ls -l'
		alias l.='ls -d .[a-zA-Z]*'
	fi
fi

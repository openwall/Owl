# color-ls initialization
set COLORS=/etc/DIR_COLORS
eval `dircolors -c /etc/DIR_COLORS`
test -f ~/.dircolors && eval `dircolors -c ~/.dircolors` && set COLORS=~/.dircolors

egrep -qi "^COLOR.*none" $COLORS

if ( $? != 0 ) then
alias ll 'ls -l --color=tty'
alias l. 'ls -d .[a-zA-Z]* --color=tty'
alias ls 'ls --color=tty'
else
alias ll 'ls -l'
alias l. 'ls -d .[a-zA-Z]*'
endif

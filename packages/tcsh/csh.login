# $Owl: Owl/packages/tcsh/csh.login,v 1.5 2012/07/23 08:16:04 gremlin Exp $

limit coredumpsize 0
umask 077

setenv HOSTNAME `/bin/hostname`

test -f $HOME/.inputrc || setenv INPUTRC /etc/inputrc

# That's all - everything else resides in csh.cshrc

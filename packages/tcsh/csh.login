# $Id: Owl/packages/tcsh/csh.login,v 1.1 2000/07/27 00:03:52 solar Exp $

setenv PATH "/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin"

limit coredumpsize 0
umask 077

setenv HOSTNAME `/bin/hostname`
set history=1000

test -f $HOME/.inputrc
if ($status != 0) then
	setenv INPUTRC /etc/inputrc
endif

test -d /etc/profile.d
if ($status == 0) then
	set nonomatch
	foreach i ( /etc/profile.d/*.csh )
		test -f $i
		if ($status == 0) then
			source $i
		endif
	end
	unset i nonomatch
endif

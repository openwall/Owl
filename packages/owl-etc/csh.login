# $Id: Owl/packages/owl-etc/Attic/csh.login,v 1.2 2001/02/04 23:02:52 solar Exp $

# It is recommended that this file be left unchanged to permit for upgrades,
# and any local additions go into /etc/profile.d/local.csh.

setenv PATH "/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin"

test -x /usr/X11R6/bin/xterm
if ($status == 0) then
	setenv PATH "${PATH}:/usr/X11R6/bin"
endif

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

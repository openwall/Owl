# $Id: Owl/packages/tcsh/csh.cshrc,v 1.2 2001/02/04 23:01:53 solar Exp $

if ($?prompt) then
	if ($?tcsh) then
		set prompt='%m\\!%n:%c\$ ' 
	else
		set prompt=`hostname -s`\\!`id -nu`\$\ 
	endif
endif

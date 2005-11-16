# $Owl: Owl/packages/owl-etc/Attic/csh.cshrc,v 1.3 2005/11/16 13:21:54 solar Exp $

if ($?prompt) then
	if ($?tcsh) then
		set prompt='%m\\!%n:%c\$ ' 
	else
		set prompt=`hostname -s`\\!`id -nu`\$\ 
	endif
endif

# $Owl: Owl/packages/tcsh/csh.cshrc,v 1.4 2010/12/04 01:35:23 solar Exp $

if ($?prompt && $?tcsh) then
	set prompt='%n@%m:%~ %# '
# Alternatives:
#	set prompt='%n@%m:%c09 %# '
#	set prompt='%m\\!%n:%c%# '
endif

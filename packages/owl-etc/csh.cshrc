# $Id: Owl/packages/owl-etc/Attic/csh.cshrc,v 1.1 2000/07/27 00:03:52 solar Exp $

if ($?prompt) then
  if ($?tcsh) then
    set prompt='[%n@%m %c]$ ' 
  else
    set prompt=\[`id -nu`@`hostname -s`\]\$\ 
  endif
endif

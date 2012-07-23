# $Owl: Owl/packages/tcsh/csh.cshrc,v 1.5 2012/07/23 08:16:04 gremlin Exp $

# It is recommended that this file be left unchanged to permit for upgrades,
# and any local additions go into /etc/profile.d/local.csh and ~/.tcshrc

setenv SHELL `which tcsh`

# Some locales (e.g. Russian) have inadequate defaults...
##setenv LC_NUMERIC "C"

setenv PATH "/bin:/usr/bin:/opt/bin:/usr/local/bin:/sbin:/usr/sbin:/opt/sbin:/usr/local/sbin"
test -x /usr/X11R6/bin/xterm && setenv PATH "${PATH}:/usr/X11R6/bin"

if ( -d /etc/profile.d ) then
	set nonomatch
	foreach i ( /etc/profile.d/*.csh )
		test -f "$i" && source $i
	end
	unset i nonomatch
endif

if ($?prompt) then
##	set autolist=ambiguous
##	set ellipsis
	set history=1000
	set nonomatch
	set prompt='%n@%m:%~ %# '
	unset autologout
	unset savehist

##	alias ls 'ls-F -Ca'
##	alias lh 'ls-F -lha'
##	alias ll 'ls-F -la'
##	alias psg 'ps wax | grep -v grep | egrep -i'
##	alias psl 'ps wax | less'
	unalias d
	unalias dir
	unalias v
	unalias vdir

	complete cd 'p/1/d/'
	complete exec 'p/1/c/'
	complete which 'n/*/c/'
##	complete kill 'p/*/`ps wax | awk \{print\ \$1\}`/'
endif

# $Id: Owl/packages/owl-cdrom/welcome-cdrom.sh,v 1.1 2002/08/22 03:54:11 solar Exp $

echo
echo 'Welcome to Openwall GNU/*/Linux (Owl)!'
echo
echo 'The Owl homepage is:'
echo 'http://www.openwall.com/Owl/'
echo

test "`id -u`" = "0" || return 0

WORLD=/usr/src/world
KERNEL=/usr/src/kernel
DOC=$WORLD/native/Owl/doc

HAVE_SRCS=
test -d $WORLD/native -a -d $WORLD/sources && HAVE_SRCS=yes
HAVE_RPMS=
test -d $WORLD/RPMS && HAVE_RPMS=yes

if [ -n "$HAVE_SRCS" -o -n "$HAVE_RPMS" ]; then
	cd $WORLD

	echo -n 'The Owl userland '
	if [ -n "$HAVE_SRCS" -a -n "$HAVE_RPMS" ]; then
		echo -n 'sources and binary packages'
	elif [ -n "$HAVE_SRCS" ]; then
		echo -n 'sources'
	else
		echo -n 'binary packages'
	fi
	echo " may be found under $WORLD:"
	ls $WORLD
	echo
fi

if [ -d $KERNEL ]; then
	echo -n "The kernel sources and recommended patches"
	echo " may be found under $KERNEL:"
	ls $KERNEL
	echo
fi

if [ -d $DOC ]; then
	echo "There's documentation under $DOC:"
	ls $DOC
	echo
fi

unset WORLD KERNEL DOC HAVE_SRCS HAVE_RPMS

echo -n 'You may either configure the CD-booted system '
echo 'and let it boot into multi-user'
echo -n 'or install Owl on a hard disk for long-term use.  '
echo 'Please refer to INSTALL for'
echo 'more information.'
echo

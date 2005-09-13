# $Id: Owl/packages/owl-cdrom/welcome-cdrom.sh,v 1.6 2005/09/13 14:23:12 solar Exp $

CD=/.Owl-CD-ROM
VERSION=
if [ -s $CD -a -r $CD ]; then
	VERSION=" `cat $CD`"
fi

echo
echo "Welcome to Openwall GNU/*/Linux (Owl)${VERSION}!"
echo
echo 'The Owl homepage is:'
echo 'http://www.openwall.com/Owl/'
echo

unset CD VERSION

test "`id -u`" = "0" || return 0

WORLD=/usr/src/world
KERNEL=/usr/src/kernel
DOC="`echo $WORLD/native/Owl*/doc | sed 's/^.* \([^ ]*\)$/\1/'`"

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
	ls -x $WORLD
	echo
fi

if [ -d $KERNEL ]; then
	echo -n "The kernel sources and recommended patches"
	echo " may be found under $KERNEL:"
	ls -x $KERNEL
	echo
fi

if [ -d $DOC ]; then
	echo "There's documentation under $DOC:"
	ls -x -I CVS $DOC
	if [ -d $DOC/ru ]; then
		echo
		echo "To browse Russian documentation, set Cyrillic font with:"
		echo "setfont -u koi8r koi8r-8x16"
	fi
	echo
fi

unset WORLD KERNEL DOC HAVE_SRCS HAVE_RPMS

echo 'Type "settle" to install Owl on a hard disk.'
echo -n 'Type "setup" to configure the live CD system, '
echo 'then "exit" the shell to boot.'
echo 'Please refer to INSTALL for more information.'
echo

# $Owl: Owl/packages/owl-cdrom/welcome-cdrom.sh,v 1.10 2010/07/25 00:11:58 solar Exp $

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

if [ -z "$LC_CTYPE" -a -z "$LC_ALL" -a -z "$LANG" ]; then
	export LC_CTYPE=en_US
fi

test "`id -u`" = "0" || return 0

QO='"'
QC='"'
if test -c /dev/stdout; then
	QO=`echo -en '\033[1m'`
	QC=`echo -en '\033[0m'`
fi

WORLD=/usr/src/world
DOC="`echo $WORLD/native/Owl*/doc | sed 's/^.* \([^ ]*\)$/\1/'`"

HAVE_SRCS=
test -d $WORLD/native -a -d $WORLD/sources && HAVE_SRCS=yes
HAVE_RPMS=
test -d $WORLD/RPMS && HAVE_RPMS=yes

if [ -n "$HAVE_SRCS" -o -n "$HAVE_RPMS" ]; then
	cd $WORLD

	echo -n 'The Owl '
	if [ -n "$HAVE_SRCS" -a -n "$HAVE_RPMS" ]; then
		echo -n 'source code and binary packages'
	elif [ -n "$HAVE_SRCS" ]; then
		echo -n 'source code'
	else
		echo -n 'binary packages'
	fi
	echo " may be found under $WORLD:"
	ls -x $WORLD
	echo
fi

if [ -d $DOC ]; then
	echo "There's documentation under $DOC:"
	ls -x -I CVS $DOC
	if [ -d $DOC/ru ]; then
		alias setcyrfont='setfont -u koi8-r_to_uni.trans -m koi8-r_to_uni.trans koi8r-8x16 && export LC_CTYPE=ru_RU.KOI8-R'
		echo
		echo "To browse the Russian documentation, type ${QO}setcyrfont${QC} to set a Cyrillic font."
	fi
	echo
fi

unset WORLD DOC HAVE_SRCS HAVE_RPMS

echo "Type ${QO}settle${QC} to install Owl on hard disk(s). -OR-"
echo -n "Type ${QO}setup${QC} to configure the live CD system, "
echo "then ${QO}exit${QC} the shell to boot."
echo 'Please refer to INSTALL for more information.'
echo

unset QO QC

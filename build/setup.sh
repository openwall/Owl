#!/bin/sh
# $Id: Owl/build/setup.sh,v 1.4 2001/07/27 23:25:12 solar Exp $

. installworld.conf

if [ ! -d $ROOT -o ! -O $ROOT ]; then
	echo "Invalid ROOT ($ROOT) or not running as the directory owner"
	exit 1
fi

umask $UMASK

export PATH=/sbin:/usr/sbin:$PATH
if [ $ROOT != / ]; then
	export TMPDIR= TMP=
fi
chroot $ROOT /usr/sbin/setup

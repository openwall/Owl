#!/bin/sh
# $Owl: Owl/build/setup.sh,v 1.5 2005/11/16 12:01:36 solar Exp $

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

#!/bin/sh
# $Id: Owl/build/setup.sh,v 1.3 2001/06/20 21:02:14 solar Exp $

. installworld.conf

if [ ! -d $ROOT -o ! -O $ROOT ]; then
	echo "Invalid ROOT ($ROOT) or not running as the directory owner"
	exit 1
fi

umask $UMASK

export PATH=/sbin:/usr/sbin:$PATH
chroot $ROOT /usr/sbin/setup

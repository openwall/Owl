#!/bin/sh
# $Id: Owl/build/setup.sh,v 1.2.2.1 2001/06/21 08:13:22 solar Exp $

. installworld.conf

if [ ! -d $ROOT -o ! -O $ROOT ]; then
	echo "Invalid ROOT ($ROOT) or not running as the directory owner"
	exit 1
fi

umask $UMASK

export PATH=/sbin:/usr/sbin:$PATH
chroot $ROOT /usr/sbin/setup

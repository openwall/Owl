#!/bin/sh
# $Id: Owl/build/setup.sh,v 1.1 2000/12/28 17:19:39 solar Exp $

. installworld.conf

if [ ! -d $ROOT -o ! -O $ROOT ]; then
	echo "Invalid ROOT ($ROOT) or not running as the directory owner"
	exit
fi

umask $UMASK

export PATH=/sbin:/usr/sbin:$PATH
chroot /owl /usr/sbin/setup

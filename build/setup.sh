#!/bin/sh
# $Id: Owl/build/setup.sh,v 1.2 2000/12/28 18:46:20 solar Exp $

. installworld.conf

if [ ! -d $ROOT -o ! -O $ROOT ]; then
	echo "Invalid ROOT ($ROOT) or not running as the directory owner"
	exit 1
fi

umask $UMASK

export PATH=/sbin:/usr/sbin:$PATH
chroot /owl /usr/sbin/setup

#!/bin/sh
# $Owl: Owl/packages/owl-cdrom/Attic/floppy-update.sh,v 1.7 2009/11/20 12:52:47 solar Exp $

set -e

dd if=/dev/zero of=floppy.image bs=36k count=80
/sbin/mke2fs -m 0 -N 16 -F floppy.image

mount floppy.image /mnt/floppy -oloop
trap 'umount /mnt/floppy' EXIT HUP INT TERM

rmdir /mnt/floppy/lost+found
mkdir -m 700 /mnt/floppy/boot
if [ -e boot.b ]; then
	cp -p boot.b /mnt/floppy/boot/
fi
cp -p bzImage message /mnt/floppy/boot/

/sbin/lilo -C ../etc/lilo.conf.bootcd

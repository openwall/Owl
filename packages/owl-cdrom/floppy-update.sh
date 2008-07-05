#!/bin/sh
# $Owl: Owl/packages/owl-cdrom/Attic/floppy-update.sh,v 1.6 2008/07/05 20:17:42 solar Exp $

set -e

dd if=/dev/zero of=floppy.image bs=36k count=80
/sbin/mke2fs -m 0 -F floppy.image

mount floppy.image /mnt/floppy -oloop
trap 'umount /mnt/floppy' EXIT HUP INT TERM

mkdir -m 700 /mnt/floppy/boot
if [ -e boot.b ]; then
	cp -p boot.b /mnt/floppy/boot/
fi
cp -p bzImage message /mnt/floppy/boot/

/sbin/lilo -C ../etc/lilo.conf.bootcd

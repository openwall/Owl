#!/bin/sh
# $Id: Owl/packages/owl-cdrom/Attic/floppy-update.sh,v 1.1 2005/03/06 01:59:44 solar Exp $

set -e

dd if=/dev/zero of=floppy.image bs=18k count=80
/sbin/mke2fs -m 0 -F floppy.image

mount floppy.image /mnt/floppy -oloop=/dev/loop0
trap 'umount /mnt/floppy' EXIT HUP INT TERM

mkdir -m 700 /mnt/floppy/boot
cp -p boot.b bzImage message /mnt/floppy/boot/

/sbin/lilo -C ../etc/lilo.conf

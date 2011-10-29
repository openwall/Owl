#!/bin/bash
# $Owl: Owl/build/makeiso.sh,v 1.6 2011/10/29 21:48:47 solar Exp $

set -e

. installworld.conf

ROOT="$ISOTREE_ROOT"

if [ ! -d "$ROOT" -o ! -r "$ROOT/boot/isolinux/isolinux.bin" -o \
     "$(readlink -e "$ROOT")" = / ]; then
	echo >&2 "Invalid or unavailable ISOTREE_ROOT ($ROOT)"
	exit 1
fi

umask $UMASK
cd $HOME

if [ "$BRANCH" = "Owl" ]; then
	ISO="Owl-current-$(TZ=UTC date +%Y%m%d).iso"
else
	ISO="$BRANCH-$(TZ=UTC date +%Y%m%d).iso"
fi

MKISOFS_OPTS="-quiet -lRJ
	-no-emul-boot -boot-load-size 4 -boot-info-table
	-hide-rr-moved
	-b boot/isolinux/isolinux.bin
	-c boot/isolinux/isolinux.cat"

if [ -z "$ISO_COMPRESS" ]; then
	mkisofs $MKISOFS_OPTS -o "$ISO" "$ROOT"
else
	mkisofs $MKISOFS_OPTS "$ROOT" | gzip -9 >"$ISO.gz"
fi

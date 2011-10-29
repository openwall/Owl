#!/bin/bash
# $Owl: Owl/build/makeiso.sh,v 1.7 2011/10/29 22:26:11 solar Exp $

set -e

. installworld.conf

ROOT="$ISOTREE_ROOT"

if [ ! -d "$ROOT" -o ! -r "$ROOT/boot/isolinux/isolinux.bin" -o \
     "$(readlink -e "$ROOT")" = / ]; then
	echo >&2 "Invalid or unavailable ISOTREE_ROOT ($ROOT)"
	exit 1
fi

umask $UMASK

ARCH=
if [ -r "$ROOT/.Owl-arch" ]; then
	ARCH="`cat $ROOT/.Owl-arch`"
fi
rm -f "$ROOT/.Owl-arch"
if [ -n "$ARCH" ]; then
	ARCH="-${ARCH}"
fi

if [ "$BRANCH" = "Owl" ]; then
	ISO="Owl-current-$(TZ=UTC date +%Y%m%d)${ARCH}.iso"
else
	ISO="$BRANCH-$(TZ=UTC date +%Y%m%d)${ARCH}.iso"
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

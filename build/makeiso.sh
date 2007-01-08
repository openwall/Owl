#!/bin/sh
# $Owl: Owl/build/makeiso.sh,v 1.2 2007/01/08 12:41:10 ldv Exp $

set -e

. installworld.conf

ROOT="$ISOTREE_ROOT"
if [ ! -d "$ROOT" -o ! -r "$ROOT/boot/floppy.image" -o \
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
mkisofs -quiet -lRJ -b boot/floppy.image -c boot/boot.catalog \
	-o "$ISO" "$ROOT"

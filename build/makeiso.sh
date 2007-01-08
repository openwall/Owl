#!/bin/sh
# $Owl: Owl/build/makeiso.sh,v 1.1 2007/01/08 00:54:08 ldv Exp $

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

mkisofs -quiet -lRJ -b boot/floppy.image -c boot/boot.catalog \
	-o "$BRANCH-$(TZ=UTC date +%Y%m%d).iso" "$ROOT"

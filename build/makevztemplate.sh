#!/bin/bash
# $Owl: Owl/build/makevztemplate.sh,v 1.3 2011/10/29 22:26:11 solar Exp $

set -e

. installworld.conf

ROOT="$VZTREE_ROOT"
if [ ! -d "$ROOT" -o "$(readlink -e "$ROOT")" = / ]; then
	echo >&2 "Invalid or unavailable VZTREE_ROOT ($ROOT)"
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

F="$BRANCH"
test "$F" = "Owl" && F="Owl-current" || :
# Use all-lowercase "owl" here for vzctl's substring match against owl.conf
F="${F/#O/o}-$(TZ=UTC date +%Y%m%d)${ARCH}.tar.gz"

GZIP=-9 tar czSf "/vz/template/cache/$F" --one-file-system -C "$ROOT" .

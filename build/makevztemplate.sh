#!/bin/bash
# $Owl: Owl/build/makevztemplate.sh,v 1.2 2010/12/14 10:57:09 solar Exp $

set -e

. installworld.conf

ROOT="$VZTREE_ROOT"
if [ ! -d "$ROOT" -o "$(readlink -e "$ROOT")" = / ]; then
	echo >&2 "Invalid or unavailable VZTREE_ROOT ($ROOT)"
	exit 1
fi

umask $UMASK

F="$BRANCH"
test "$F" = "Owl" && F="Owl-current" || :
# Use all-lowercase "owl" here for vzctl's substring match against owl.conf
F="${F/#O/o}-$(TZ=UTC date +%Y%m%d).tar.gz"

GZIP=-9 tar czSf "/vz/template/cache/$F" --one-file-system -C "$ROOT" .

#!/bin/sh

INCPATH=${1:-/usr/include}
cd $INCPATH || exit 1

umask 022

if [ ! -d asm-sparc -o ! -d asm-sparc64 ] ; then
	echo You must create $INCPATH/asm-sparc* symlinks first.
	exit 1
fi

test -d asm || mkdir asm
cd asm || exit 1

for I in `( ls ../asm-sparc; ls ../asm-sparc64 ) | grep '\.h$' | sort -u`; do
	J="`echo "$I" | tr a-z. A-Z_`"
	cat > "$I" <<EOF
#ifndef __SPARCSTUB__${J}__
#define __SPARCSTUB__${J}__
EOF
	if [ -f "../asm-sparc/$I" -a -f "../asm-sparc64/$I" ]; then
		cat >> "$I" <<EOF
#ifdef __arch64__
#include <asm-sparc64/$I>
#else
#include <asm-sparc/$I>
#endif
#endif
EOF
	elif [ -f "../asm-sparc/$I" ]; then
		cat >> "$I" <<EOF
#ifndef __arch64__
#include <asm-sparc/$I>
#endif
#endif
EOF
	else
		cat >> "$I" <<EOF
#ifdef __arch64__
#include <asm-sparc64/$I>
#endif
#endif
EOF
	fi
done

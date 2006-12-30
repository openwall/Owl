#!/bin/sh
# $Owl: Owl/build/Attic/buildkernel.sh,v 1.1 2006/12/30 18:05:42 ldv Exp $

set -e

. buildworld.conf

log()
{
	local stamp

	stamp="$(date +%H:%M:%S)"
	printf '%s: %s\n' "$stamp" "$*"
}

exit_handler()
{
	local rc=$?
	trap - EXIT

	log "Removing temporary files"
	rm -rf -- "$HOME/tmp-work"

	if [ $rc = 0 ]; then
		echo "`date '+%Y %b %e %H:%M:%S'`: Finished"
	else
		echo "`date '+%Y %b %e %H:%M:%S'`: Terminated, rc=$rc"
	fi

	exit $rc
}

if [ "`id -u`" = 0 -o ! -O "$HOME" ]; then
	echo >&2 "Run this as the owner of $HOME (typically, as user \"build\")"
	exit 1
fi

unset LANG LANGUAGE LINGUAS
unset LC_ADDRESS LC_ALL LC_COLLATE LC_CTYPE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE LC_TIME

umask $UMASK
cd $HOME

mkdir -p logs

exec </dev/null >logs/buildkernel 2>&1
echo "`date '+%Y %b %e %H:%M:%S'`: Started"

log "Removing stale temporary files if any"
rm -rf tmp-work kernel-work

trap exit_handler HUP INT QUIT TERM EXIT

mkdir tmp-work kernel-work kernel-work/boot

export TMPDIR=$HOME/tmp-work
export TMP=$HOME/tmp-work

KERNEL_SRC="$(find $HOME/kernel/ -name 'linux-*.tar.bz2' -printf '%f\n')"
KERNEL="${KERNEL_SRC%.tar.bz2}"
OW_SRC="$(find $HOME/kernel/ -name 'linux-*-ow*.tar.gz' -printf '%f\n')"
OW="${OW_SRC%.tar.gz}"
CRYPTO_SRC="$(find $HOME/kernel/ -name 'patch-cryptoloop-*.bz2' -printf '%f\n')"
CRYPTO="${CRYPTO_SRC%.bz2}"

PACKAGES=$BRANCH/packages
NATIVE=$HOME/native
CDROM="$NATIVE/$PACKAGES/owl-cdrom"

cd $HOME/tmp-work

log "Unpacking $KERNEL_SRC"
tar xf "$HOME/kernel/$KERNEL_SRC"

log "Unpacking $OW_SRC"
tar xf "$HOME/kernel/$OW_SRC"

log "Unpacking $CRYPTO_SRC"
bzcat "$HOME/kernel/$CRYPTO_SRC" >"$CRYPTO"

cd "$KERNEL"

log "Applying $OW.diff"
patch -s -p1 <"$HOME/tmp-work/$OW/$OW.diff"

log "Applying $CRYPTO"
patch -s -p1 <"$HOME/tmp-work/$CRYPTO"

sed -i -e 's/\(#define LINUX_COMPILE_HOST \\"\)[^"]*"/\1\${ARCH}.pvt.openwall.com\\"/' \
       -e 's/\(#define LINUX_COMPILE_DOMAIN \\"\)[^"]*"/\1\\"/' Makefile
printf '\nprint_arch:\n\t@echo ${ARCH} >&2\n' >>Makefile
ARCH="$(env MAKEFLAGS= make print_arch 2>&1 >/dev/null)"

if [ -f "$CDROM/dot-config-$ARCH" ]; then
	DOT_CONFIG="dot-config-$ARCH"
else
	DOT_CONFIG="dot-config"
fi
log "Installing $DOT_CONFIG from owl-cdrom"
cp "$CDROM/$DOT_CONFIG" .config

log "Configuring kernel"
yes '' |make oldconfig

log "Building kernel dependencies"
make dep

log "Building kernel image for $ARCH"
make bzImage
	
log "Copying kernel image"
install -pm644 System.map "arch/$ARCH/boot/bzImage" "$HOME/kernel-work/boot/"
	
log "Copying header files"
rm -rf "$HOME/kernel-work/include"
cp -a include "$HOME/kernel-work/include"
cd "$HOME/kernel-work/include"
mkdir x
mv asm asm-generic "asm-$ARCH" x/
rm -rf asm*
mv x/* .
rmdir x
chmod -R u=rwX,go=rX .

#!/bin/sh
# $Owl: Owl/build/Attic/buildkernel.sh,v 1.4 2010/03/22 18:17:32 solar Exp $

set -e

. buildworld.conf

log()
{
	local stamp

	stamp="$(date +%H:%M:%S)"
	printf '%s: %s\n' "$stamp" "$*"
	printf >&3 '%s: %s\n' "$stamp" "$*"
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

detect_arch()
{
	local MACHINE

	MACHINE=`uname -m` || MACHINE="unknown"

	case "$MACHINE" in
	*86)
		ARCHITECTURE=i386
		;;
	x86_64)
		ARCHITECTURE=x86_64
		;;
	sparc*)
		ARCHITECTURE=sparc
		;;
	alpha)
		ARCHITECTURE=alpha
		;;
	*)
		echo >&2 "Unknown architecture"
		exit 1
		;;
	esac
}

detect_proc()
{
	case "$ARCHITECTURE" in
	sparc*)
		PROCESSORS="`sed -n \
			's/^ncpus active[[:space:]]\+: \([0-9]\+\)$/\1/p' \
			/proc/cpuinfo`"
		;;
	alpha*)
		PROCESSORS="`sed -n \
			's/^cpus detected[[:space:]]\+: \([0-9]\+\)$/\1/p' \
			/proc/cpuinfo`"
		;;
	*)
		PROCESSORS="`grep -cw ^processor /proc/cpuinfo`"
		;;
	esac || :

	test -n "$PROCESSORS" || PROCESSORS=1
	test "$PROCESSORS" -ge 1 || PROCESSORS=1
}

detect()
{
	test -n "$ARCHITECTURE" || detect_arch
	test -n "$PROCESSORS" || detect_proc
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

exec 3>&1
exec </dev/null >logs/buildkernel 2>&1
echo "`date '+%Y %b %e %H:%M:%S'`: Started"

log "Removing stale temporary files if any"
rm -rf tmp-work kernel-work

trap exit_handler HUP INT QUIT TERM EXIT

detect

mkdir tmp-work kernel-work kernel-work/boot

export TMPDIR=$HOME/tmp-work
export TMP=$HOME/tmp-work

KERNEL_SRC="$(find $HOME/kernel/ -name 'linux-*.tar.bz2' -printf '%f\n')"
KERNEL="${KERNEL_SRC%.tar.bz2}"
OPENVZ_SRC="$(find $HOME/kernel/ -name 'patch-*.el*stab*-combined.bz2' -printf '%f\n')"
OW_SRC="$(find $HOME/kernel/ -name 'linux-*.el*stab*-owl*.diff.gz' -printf '%f\n')"

PACKAGES=$BRANCH/packages
NATIVE=$HOME/native
CDROM="$NATIVE/$PACKAGES/owl-cdrom"

cd $HOME/tmp-work

log "Unpacking $KERNEL_SRC"
tar xf "$HOME/kernel/$KERNEL_SRC"

cd "$KERNEL"

log "Applying $OPENVZ_SRC"
bzcat "$HOME/kernel/$OPENVZ_SRC" | patch -s -p1 -T

log "Applying $OW_SRC"
zcat "$HOME/kernel/$OW_SRC" | patch -s -p1 -Z

# Assume that our guess of the architecture matches the kernel's
ARCH=$ARCHITECTURE

if [ -f "$CDROM/dot-config-$ARCH" ]; then
	DOT_CONFIG="dot-config-$ARCH"
else
	DOT_CONFIG="dot-config"
fi
log "Installing $DOT_CONFIG from owl-cdrom"
cp "$CDROM/$DOT_CONFIG" .config

log "Configuring kernel"
yes '' |make oldconfig

log "Building kernel image for $ARCH"
make "-j$PROCESSORS" bzImage

case "$ARCH" in
*86)
	ARCH=i386
	;;
esac

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

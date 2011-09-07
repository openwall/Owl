#!/bin/bash
# $Owl: Owl/build/installisotree.sh,v 1.15.2.3 2011/09/07 07:50:05 solar Exp $

set -e

. installworld.conf

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

	if [ $rc = 0 ]; then
		echo "`date '+%Y %b %e %H:%M:%S'`: Finished"
	else
		echo "`date '+%Y %b %e %H:%M:%S'`: Terminated, rc=$rc"
	fi

	exit $rc
}

ROOT="$ISOTREE_ROOT"
if [ ! -d "$ROOT" -o ! -O "$ROOT" -o "$(readlink -e "$ROOT")" = / ]; then
	echo >&2 "Invalid ISOTREE_ROOT ($ROOT) or not running as the directory owner"
	exit 1
fi

trap exit_handler HUP INT QUIT TERM EXIT

umask $UMASK
cd $HOME

# Ensure that root directory is empty, re-create it with proper permissions.
rmdir -- "$ROOT"
mkdir -m 755 -- "$ROOT"

MAKE_CDROM=yes KERNEL_FAKE=no SKIP_EXTRA=yes "$HOME/native/$BRANCH/build/installworld.sh"

mkdir -p logs
exec 3>&1
exec </dev/null >logs/installisotree 2>&1
echo "`date '+%Y %b %e %H:%M:%S'`: Started"

log "Installing kernel"
cd "$ROOT/boot"
# Should match exactly one file
KERNEL_NAME="`echo vmlinuz-*`"
ln -s "$KERNEL_NAME" vmlinuz
chroot "$ROOT" sh -c 'cd /boot && ./floppy-update.sh'
# We'll mount the floppy image when CD-booted, so there's no need to keep a
# second copy of the kernel image outside of the floppy image.
rm "$KERNEL_NAME"
ln -s floppy/boot/"$KERNEL_NAME"
mkdir -m700 floppy

# depmod is normally run on bootup, but /lib/modules is read-only on CD
log "Pre-generating kernel module dependencies"
chroot "$ROOT" sh -c 'depmod `cd /lib/modules && echo 2.6.*`'

log "Updating config files"
cd "$ROOT/etc"
sed -i '/^tmpfs[[:space:]]/d' fstab
sed -i 's|^\(/dev/cdrom[[:space:]]*\).*|\1/\t\t\tiso9660\tro\t\t\t0 0|' fstab
echo -e '/boot/floppy.image /boot/floppy\t\text2\tloop,ro\t\t\t0 0' >> fstab
sed -i 's|^\(~~:S:wait:\).*|\1/bin/bash --login|' inittab
sed -i 's/^\(DISK_QUOTA=\)yes$/\1no/' vz/vz.conf

log "Installing sources"
cd "$ROOT/rom/world"
tar -cf- --owner=build --group=sources --exclude Root -C "$HOME" \
	"native/$BRANCH" Makefile |
	tar -xf-
if [ "`uname -m`" = x86_64 ]; then
	pushd "native/$BRANCH"
	tar cjf packages.tar.bz2 --remove-files packages
	popd
fi

cp -rpL "$HOME/RPMS" .
mkdir sources
cp -rpL "$HOME/sources/$BRANCH" sources/
chown -hR build:sources .
chmod -R u=rwX,go=rX .

log "Preparing README files"
cd "$ROOT"
if [ "$BRANCH" = "Owl" ]; then
	echo "current built on $(TZ=UTC date +%Y/%m/%d)" >.Owl-CD-ROM
else
	echo "3.0-stable built on $(TZ=UTC date +%Y/%m/%d)" >.Owl-CD-ROM
fi
chroot "$ROOT" sh -c '. /etc/profile.d/welcome-cdrom.sh >/README'
chmod 644 .Owl-CD-ROM README

> var/run/utmp
> var/log/wtmp

log "Creating mtree specification"
chroot "$ROOT" mtree -c -K sha1digest |
	tail -n +4 >"$HOME/cdrom.mtree"
mv "$HOME/cdrom.mtree" Owl-CD-ROM.mtree
xz Owl-CD-ROM.mtree

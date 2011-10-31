#!/bin/bash
# $Owl: Owl/build/installisotree.sh,v 1.26 2011/10/31 08:15:58 segoon Exp $

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

MAKE_CDROM=yes KERNEL_FAKE=no SKIP_EXTRA=yes NEED_ARCH_TAG=yes "$HOME/native/$BRANCH/build/installworld.sh"

mkdir -p logs
exec 3>&1
exec </dev/null >logs/installisotree 2>&1
echo "`date '+%Y %b %e %H:%M:%S'`: Started"

log "Installing kernel"
cd "$ROOT/boot"
# Should match exactly one file
KERNEL_NAME="`echo vmlinuz-*`"
# ISOLINUX doesn't respect symlinks :(
ln "$KERNEL_NAME" vmlinuz_iso # for owl-cdrom's isolinux.conf
ln -s "$KERNEL_NAME" vmlinuz # for owl-setup (it copies the symlink)

mkdir -p "$ROOT/boot/isolinux/"
ln "$ROOT/usr/share/syslinux/isolinux.bin" \
    "$ROOT/usr/share/syslinux/menu.c32" \
    "$ROOT/etc/isolinux.cfg" \
    "$ROOT/boot/message" \
	"$ROOT/boot/isolinux/"

# depmod is normally run on bootup, but /lib/modules is read-only on CD
log "Pre-generating kernel module dependencies"
chroot "$ROOT" sh -c 'depmod `cd /lib/modules && echo 2.6.*`'

log "Updating config files"
cd "$ROOT/etc"
sed -i '/^tmpfs[[:space:]]/d' fstab
sed -i 's|^\(/dev/cdrom[[:space:]]*\).*|\1/\t\t\tiso9660\tro\t\t\t0 0|' fstab
sed -i 's|^\(~~:S:wait:\).*|\1/bin/bash --login|' inittab
sed -i 's/^\(DISK_QUOTA=\)yes$/\1no/' vz/vz.conf

test -n "$ISO_COPY_SOURCES" || ISO_COPY_SOURCES=yes
test -n "$ISO_COPY_RPMS" || ISO_COPY_RPMS=yes

cd "$ROOT/rom/world"
if [ "$ISO_COPY_SOURCES" = yes -o "$ISO_COPY_RPMS" = yes ]; then
	TAR_EXTRA_OPTS=
	if [ "$ISO_COPY_SOURCES" = yes ]; then
		log "Copying the native tree"
	else
		log "Copying portions of the native tree"
		TAR_EXTRA_OPTS='--exclude packages'
	fi
	tar -cf- --owner=build --group=sources --exclude Root \
		$TAR_EXTRA_OPTS \
		-C "$HOME" \
		"native/$BRANCH" Makefile | tar -xf-

	if [ "$ISO_COPY_SOURCES" = yes ]; then
		log "Copying sources"
		mkdir sources
		cp -rpL "$HOME/sources/$BRANCH" sources/
	else
		log "Skipping sources copying"
	fi
else
	log "Skipping native tree and sources copying"
fi

if [ "$ISO_COPY_RPMS" = yes ]; then
	log "Copying RPMs"
	cp -rpL "$HOME/RPMS" .
else
	log "Skipping RPMs copying"
fi

chown -hR build:sources .
chmod -R u=rwX,go=rX .

log "Preparing README files"
cd "$ROOT"
if [ "$BRANCH" = "Owl" ]; then
	echo "current built on $(TZ=UTC date +%Y/%m/%d)" >.Owl-CD-ROM
else
	touch .Owl-CD-ROM
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

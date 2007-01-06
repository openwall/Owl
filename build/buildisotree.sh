#!/bin/sh
# $Owl: Owl/build/Attic/buildisotree.sh,v 1.2 2007/01/06 22:07:31 ldv Exp $

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

umask $UMASK
cd $HOME

trap exit_handler HUP INT QUIT TERM EXIT
mkdir -p logs
exec 3>&1
exec </dev/null >logs/buildisotree 2>&1
echo "`date '+%Y %b %e %H:%M:%S'`: Started"

log "Removing extra documentation"
cd "$ROOT"
chroot "$ROOT" rpm -e man-pages-posix bind-doc bash-doc cvs-doc pam-doc rpm-devel ||:

log "Installing kernel"
cd "$ROOT/boot"
install -pm644 -oroot -groot "$HOME"/kernel-work/boot/* .
chroot "$ROOT" sh -c 'cd /boot && ./floppy-update.sh'

log "Updating config files"
cd "$ROOT/etc"
sed -i 's|^\(/dev/cdrom[[:space:]]*\).*|\1/\t\t\tiso9660\tro\t\t\t0 0|' fstab
sed -i 's|^\(~~:S:wait:\).*|\1/bin/bash --login|' inittab

log "Installing kernel source"
cd "$ROOT/usr/src"
cp -rpL "$HOME/kernel" .
chown -hR sources:sources kernel
chmod -R u=rwX,go=rX kernel

log "Installing kernel headers"
mkdir linux
cd linux
cp -a "$HOME/kernel-work/include" .
chown -hR sources:sources .
chmod -R u=rwX,go=rX .

log "Installing userspace sources"
cd "$ROOT/rom/world"
tar -cf- --owner=build --group=sources --exclude Root -C "$HOME" \
	"native/$BRANCH" Makefile |
	tar -xf-

cp -rpL "$HOME/RPMS" .
cp -rpL "$HOME/sources" .
chown -hR build:sources .
chmod -R u=rwX,go=rX .

log "Preparing README files"
cd "$ROOT"
echo "current as of $(TZ=UTC date +%Y/%m/%d)" >.Owl-CD-ROM
chroot "$ROOT" sh -c '. /etc/profile.d/welcome-cdrom.sh >/README'
chmod 644 .Owl-CD-ROM README

> var/run/utmp
> var/log/wtmp

log "Creating mtree specification"
chroot "$ROOT" mtree -c -K size,md5digest,sha1digest |
	tail -n +4 >"$HOME/cdrom.mtree"
mv "$HOME/cdrom.mtree" Owl-CD-ROM.mtree
gzip -9 Owl-CD-ROM.mtree

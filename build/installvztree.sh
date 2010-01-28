#!/bin/sh
# $Owl: Owl/build/installvztree.sh,v 1.1 2010/01/28 16:57:05 solar Exp $

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

ROOT="$VZTREE_ROOT"
if [ ! -d "$ROOT" -o ! -O "$ROOT" -o "$(readlink -e "$ROOT")" = / ]; then
	echo >&2 "Invalid VZTREE_ROOT ($ROOT) or not running as the directory owner"
	exit 1
fi

trap exit_handler HUP INT QUIT TERM EXIT

umask $UMASK
cd $HOME

# Ensure that root directory is empty, re-create it with proper permissions.
rmdir -- "$ROOT"
mkdir -m 755 -- "$ROOT"

FORCE_ROOT="$ROOT" "$HOME/native/$BRANCH/build/installworld.sh"

mkdir -p logs
exec 3>&1
exec </dev/null >logs/installvztree 2>&1
echo "`date '+%Y %b %e %H:%M:%S'`: Started"

cd "$ROOT"
log "Removing packages that are undesirable inside a container"
chroot "$ROOT" rpm -e vzctl vzquota ||:
log "Removing packages that are typically not needed inside a container"
chroot "$ROOT" rpm -e bind-doc bash-doc cvs-doc pam-doc db4-doc groff-doc rpm-devel ||:

log "Removing SSH host keys"
cd "$ROOT/etc"
rm ssh/ssh_host_*

log "Updating config files"
cat >> fstab << EOF
simfs		/			simfs	defaults		0 0
tmpfs		/tmp			tmpfs	nosuid,nodev		0 0
EOF
sed -i 's|^[0-9].*mingetty.*tty|#&|' inittab
echo 'GATEWAYDEV=venet0' > sysconfig/network

log "Installing kernel headers"
chown -h root:root "$ROOT/usr/src"
cd "$ROOT/usr/src"
mkdir linux
cd linux
cp -a "$HOME/kernel-work/include" .
cd "$ROOT/usr/src"
chown -hR sources:sources .
chmod -R u=rwX,go=rX .

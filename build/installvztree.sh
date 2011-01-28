#!/bin/bash
# $Owl: Owl/build/installvztree.sh,v 1.8 2011/01/28 18:18:40 segoon Exp $

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

FORCE_ROOT="$ROOT" KERNEL_FAKE=yes "$HOME/native/$BRANCH/build/installworld.sh"

mkdir -p logs
exec 3>&1
exec </dev/null >logs/installvztree 2>&1
echo "`date '+%Y %b %e %H:%M:%S'`: Started"

cd "$ROOT"
log "Removing packages that are harmful inside a container"
chroot "$ROOT" rpm -e vzctl vzquota ||:
log "Removing packages that are typically not needed inside a container"
chroot "$ROOT" rpm -e ethtool bridge-utils hdparm smartmontools mdadm lilo dmidecode pciutils libusb1 libusb1-devel usbutils modutils losetup acct bind-doc bash-doc cvs-doc pam-doc db4-doc groff-doc rpm-devel ||:

log "Removing SSH host keys"
cd "$ROOT/etc"
rm ssh/ssh_host_*

log "Updating config files"
cat >> fstab << EOF
simfs		/			simfs	defaults		0 0
EOF
sed -i 's|^[0-9].*mingetty.*tty|#&|' inittab
echo 'GATEWAYDEV=venet0' > sysconfig/network

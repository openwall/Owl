#!/bin/sh
# $Id: Owl/build/installworld.sh,v 1.9 2002/03/13 16:25:05 solar Exp $

. installworld.conf

RPMS=$HOME/RPMS

function log()
{
	local MESSAGE

	MESSAGE="$1"

	echo "`date +%H:%M:%S`: $MESSAGE" | tee -a $HOME/logs/installworld
}

function clean_death()
{
	kill 0

	cd $HOME || exit 1
	rm -rf tmp-work $ROOT/$HOME/tmp-work

	echo "`date '+%Y %b %e %H:%M:%S'`: Interrupted" >> logs/installworld
	exit 1
}

if [ ! -d $ROOT -o ! -O $ROOT ]; then
	echo "Invalid ROOT ($ROOT) or not running as the directory owner"
	exit 1
fi

umask $UMASK
cd $HOME || exit 1

STATUS=0

mkdir -p logs

echo "`date '+%Y %b %e %H:%M:%S'`: Started" >> $HOME/logs/installworld

log "Removing stale temporary files"
rm -rf tmp-work $ROOT/$HOME/tmp-work

trap clean_death HUP INT TERM

mkdir -p tmp-work $ROOT/$HOME/tmp-work

export TMPDIR=$HOME/tmp-work
export TMP=$HOME/tmp-work

cd $RPMS || exit 1

RPM=rpm
RPM_FLAGS=
FILE="`ls rpm-[0-9]*-*.*.rpm 2>/dev/null | tail -1`"
if [ -n "$FILE" ]; then
	cd $TMPDIR || exit 1
	log "Extracting the RPM binary"
	if rpm2cpio $RPMS/$FILE | cpio -id --no-preserve-owner --quiet \
	    bin/rpm usr/lib/rpm/rpmrc; then
		RPM=$TMPDIR/bin/rpm
		RPM_FLAGS="--rcfile $TMPDIR/usr/lib/rpm/rpmrc:$HOME/.rpmrc"
	fi
	cd $RPMS || exit 1
else
	log "Missing RPM package, will try to use this system's RPM binary"
fi

if [ ! -d $ROOT/var/lib/rpm ]; then
	log "Initializing RPM database"
	umask 022
	mkdir -p $ROOT/var/lib/rpm
	$RPM $RPM_FLAGS --root $ROOT --define "home $HOME" --initdb || exit 1
	umask $UMASK
fi

grep -v ^# $HOME/installorder.conf |
while read PACKAGES; do
	FILES=
	for PACKAGE in $PACKAGES; do
		REGEX="^${PACKAGE}-[^-]*[0-9][^-]*-[^-]*[0-9][^-]*\..*\.rpm\$"
		FILE="`ls | grep "$REGEX" | tail -1`"
		if [ -z "$FILE" ]; then
			log "Missing $PACKAGE"
			continue
		fi
		test -z "$FILES" || FILES="$FILES "
		FILES="${FILES}${FILE}"
	done
	test -n "$FILES" || continue
	log "Installing $PACKAGES ($FILES)"
	$RPM $RPM_FLAGS --root $ROOT --define "home $HOME" $FLAGS $FILES && \
		continue
	STATUS=1
	log "Failed $PACKAGES"
done

log "Removing temporary files"
rm -rf $HOME/tmp-work $ROOT/$HOME/tmp-work

echo "`date '+%Y %b %e %H:%M:%S'`: Finished" >> $HOME/logs/installworld

exit $STATUS

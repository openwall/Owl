#!/bin/sh
# $Id: Owl/build/installworld.sh,v 1.2 2000/12/11 02:42:46 solar Exp $

. installworld.conf

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
	exit 0
}

if [ ! -d $ROOT -o ! -O $ROOT ]; then
	echo "Invalid ROOT ($ROOT) or not running as the directory owner"
	exit
fi

umask $UMASK
cd $HOME || exit 1

mkdir -p logs

echo "`date '+%Y %b %e %H:%M:%S'`: Started" >> $HOME/logs/installworld

log "Removing stale temporary files"
rm -rf tmp-work $ROOT/$HOME/tmp-work

trap clean_death HUP INT TERM

mkdir -p tmp-work $ROOT/$HOME/tmp-work
export TMPDIR=$HOME/tmp-work

cd $RPMS || exit 1

if [ ! -d $ROOT/var/lib/rpm ]; then
	log "Initializing RPM database"
	umask 022
	mkdir -p $ROOT/var/lib/rpm
	rpm --root $ROOT --define "home $HOME" --initdb
	umask $UMASK
fi

grep -v ^# $HOME/installorder.conf |
while read PACKAGES; do
	FILES=$(echo `echo "$PACKAGES " | sed 's/ /-[0-9]*.rpm /g'`)
	if echo "$FILES" | grep '*' &> /dev/null; then
		log "Missing $PACKAGES"
		continue
	fi
	log "Installing $PACKAGES ($FILES)"
	rpm --root $ROOT --define "home $HOME" $FLAGS $FILES && continue
	log "Failed $PACKAGES"
done

log "Removing temporary files"
rm -rf $HOME/tmp-work $ROOT/$HOME/tmp-work

echo "`date '+%Y %b %e %H:%M:%S'`: Finished" >> $HOME/logs/installworld

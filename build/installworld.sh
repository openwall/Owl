#!/bin/sh
# $Id: Owl/build/installworld.sh,v 1.1 2000/12/03 21:26:16 solar Exp $

. installworld.conf

function log()
{
	MESSAGE=$1

	echo "`date +%H:%M:%S`: $MESSAGE" | tee -a $HOME/logs/installworld
}

if [ ! -d $ROOT -o ! -O $ROOT ]; then
	echo "Invalid ROOT ($ROOT) or not running as the directory owner"
	exit
fi

umask $UMASK
cd $RPMS || exit 1

echo "`date '+%Y %b %e %H:%M:%S'`: Started" >> $HOME/logs/installworld

if [ ! -d $ROOT/var/lib/rpm ]; then
	log "Initializing RPM database"
	umask 022
	mkdir -p $ROOT/var/lib/rpm
	rpm --root $ROOT --initdb
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
	rpm --root $ROOT $FLAGS $FILES && continue
	log "Failed $PACKAGES"
done

echo "`date '+%Y %b %e %H:%M:%S'`: Finished" >> $HOME/logs/installworld

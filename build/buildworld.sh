#!/bin/sh
# $Id: Owl/build/buildworld.sh,v 1.6 2000/12/17 02:43:57 solar Exp $

REPOSITORY=Owl
PACKAGES=$REPOSITORY/packages

TIME=/usr/bin/time

. buildworld.conf

function log()
{
	local MESSAGE

	MESSAGE="$1"

	echo "`date +%H:%M:%S`: $MESSAGE" | tee -a $HOME/logs/buildworld
}

function build_native()
{
	local NUMBER PACKAGE WORK

	NUMBER=$1
	PACKAGE=$2

	WORK=$HOME/rpm-work-$NUMBER

	log "#$NUMBER: Building $PACKAGE"
	cd $WORK/SOURCES/ || exit 1
	ls $SOURCES/$PACKAGES/$PACKAGE/*.src.rpm 2>/dev/null | \
		xargs -n 1 -i sh -c 'rpm2cpio {} | cpio -i 2>/dev/null'
	ln -sf $SOURCES/$PACKAGES/$PACKAGE/* .
	rm -f '*' || :
	ln -sf $CHECKOUT/$PACKAGES/$PACKAGE/* .
	$TIME $PERSONALITY rpm -ba $PACKAGE.spec \
		$TARGET \
		--define "buildarch $BUILDARCH" \
		--define "home $HOME" \
		--define "number $NUMBER" \
		&> $HOME/logs/$PACKAGE < /dev/null
	cd $HOME/native-work || exit 1
	mv $WORK/RPMS/*/* $HOME/RPMS/ &> /dev/null
	mv $WORK/SRPMS/* $HOME/SRPMS/ &> /dev/null || \
		log "#$NUMBER: Failed $PACKAGE"
	rm -rf $WORK/BUILD/*
	rm $WORK/SOURCES/*
}

function build_foreign()
{
	local NUMBER PACKAGE WORK

	NUMBER=$1
	PACKAGE=$2

	WORK=$HOME/rpm-work-$NUMBER

	log "#$NUMBER: Building $PACKAGE"
	$TIME $PERSONALITY rpm --rebuild $FOREIGN/$PACKAGE.src.rpm \
		$TARGET \
		--define "buildarch $BUILDARCH" \
		--define "home $HOME" \
		--define "number $NUMBER" \
		&> $HOME/logs/$PACKAGE < /dev/null
	if mv $WORK/RPMS/*/* $HOME/RPMS/ &> /dev/null; then
		cp $FOREIGN/$PACKAGE.src.rpm $HOME/SRPMS/
	else
		log "#$NUMBER: Failed $PACKAGE"
	fi
	rm -rf $WORK/BUILD/*
}

function detect()
{
	local MACHINE

	MACHINE=`uname -m` || MACHINE="unknown"

	case "$MACHINE" in
	*86)
		ARCHITECTURE=i386
		;;
	alpha)
		ARCHITECTURE=alpha
		;;
	sparc*)
		ARCHITECTURE=sparc
		;;
	esac
}

function builder()
{
	local NUMBER

	NUMBER=$1

	test -n "$ARCHITECTURE" || detect

	if [ -n "$ARCHITECTURE" ]; then
		TARGET="--target ${ARCHITECTURE}-unknown-linux"
		BUILDARCH="$ARCHITECTURE"
	else
		TARGET=
		BUILDARCH="%_arch"
	fi

	if [ "$ARCHITECTURE" = "sparc" -o "$ARCHITECTURE" = "sparcv9" ]; then
		PERSONALITY=sparc32
	else
		PERSONALITY=
	fi

	log "#$NUMBER: Scanning native"

	cd $HOME/native-work || exit 1

	ls $CHECKOUT/$PACKAGES/ | grep -v '^CVS$' |
	while read PACKAGE; do
		mkdir .$PACKAGE &> /dev/null || continue
		touch .$PACKAGE/$NUMBER
		if [ -e $HOME/SRPMS/$PACKAGE-[0-9]*.src.rpm ]; then
			log "#$NUMBER: Skipping $PACKAGE"
		else
			build_native $NUMBER $PACKAGE
		fi
	done

	log "#$NUMBER: Scanning foreign"

	cd $HOME/foreign-work || exit 1

	ls $FOREIGN/ |
	while read PACKAGE; do
		PACKAGE=`basename $PACKAGE .src.rpm`
		mkdir .$PACKAGE &> /dev/null || continue
		touch .$PACKAGE/$NUMBER
		if [ -e $HOME/SRPMS/$PACKAGE.src.rpm ]; then
			log "#$NUMBER: Skipping $PACKAGE"
		else
			build_foreign $NUMBER $PACKAGE
		fi
	done

	cd $HOME || exit 1

	log "#$NUMBER: Removing temporary files"
	rm -rf rpm-work-$NUMBER

	log "#$NUMBER: Finished"
	exit 0
}

function check_includes()
{
	test `find /usr/include/linux/ /usr/include/asm/ \
		-type f ! -perm +004 -print 2>&1 | wc -c` = '0'
}

function sanity_check()
{
	log "Sanity check"

	check_includes || {
		log "Unreadable kernel includes"
		exit 1
	}

	test -r /usr/include/linux/version.h -a \
	    -r /usr/include/linux/autoconf.h || {
		log "No version.h and/or autoconf.h (kernel never configured?)"
		exit 1
	}
}

function clean_death()
{
	kill 0

	cd $HOME || exit 1
	rm -rf tmp-work rpm-work-[1-9]* native-work foreign-work

	echo "`date '+%Y %b %e %H:%M:%S'`: Interrupted" >> logs/buildworld
	exit 0
}

umask $UMASK
cd $HOME || exit 1

mkdir -p foreign
mkdir -p RPMS SRPMS logs

echo "`date '+%Y %b %e %H:%M:%S'`: Started" >> logs/buildworld

log "Removing stale temporary files"
rm -rf tmp-work rpm-work-[1-9]* native-work foreign-work

sanity_check

trap clean_death HUP INT TERM

NUMBER=1
while [ $NUMBER -le $PROCESSORS ]; do
	mkdir -p rpm-work-$NUMBER/{BUILD,SOURCES,SPECS,SRPMS}
	mkdir -p rpm-work-$NUMBER/RPMS/{noarch,i386,i686,alpha,sparc,sparcv9}
	NUMBER=$[$NUMBER + 1]
done

mkdir tmp-work native-work foreign-work || exit 1

export TMPDIR=$HOME/tmp-work
export TMP=$HOME/tmp-work

NUMBER=1
while [ $NUMBER -le $PROCESSORS ]; do
	builder $NUMBER &
	NUMBER=$[$NUMBER + 1]
done

cd $HOME || exit 1

wait

log "Removing temporary files"
rm -rf tmp-work native-work foreign-work

echo "`date '+%Y %b %e %H:%M:%S'`: Finished" >> logs/buildworld

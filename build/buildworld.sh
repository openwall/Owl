#!/bin/sh
# $Id: Owl/build/buildworld.sh,v 1.20 2002/06/21 14:45:13 solar Exp $

NATIVE_DISTRIBUTION='Openwall GNU/*/Linux'
NATIVE_VENDOR='Openwall'

TIME=/usr/bin/time

. buildworld.conf

PACKAGES=$BRANCH/packages

NATIVE=$HOME/native
SOURCES=$HOME/sources
FOREIGN=$HOME/foreign

function log()
{
	local MESSAGE

	MESSAGE="$1"

	echo "`date +%H:%M:%S`: $MESSAGE" | tee -a $HOME/logs/buildworld
}

function spec()
{
	local PACKAGE DIR SPEC

	PACKAGE=$1

	DIR=$NATIVE/$PACKAGES/$PACKAGE

	SPEC=
	if [ -f $DIR/build.spec ]; then
		SPEC="`cat $DIR/build.spec`"
		test -n "$SPEC" && SPEC="$DIR/$SPEC"
	elif [ -f $DIR/$PACKAGE.spec ]; then
		SPEC=$DIR/$PACKAGE.spec
	fi

	echo "$SPEC"
}

function build_native()
{
	local NUMBER PACKAGE WORK NAME VERSION ARCHIVE SPEC

	NUMBER=$1
	PACKAGE=$2

	WORK=$HOME/rpm-work-$NUMBER

	log "#$NUMBER: Building $PACKAGE"
	cd $WORK/SOURCES/ || exit 1
	if [ -f $NATIVE/$PACKAGES/$PACKAGE/build.archive ]; then
		while read NAME VERSION; do
			ARCHIVE=${NAME}-${VERSION}
			ln -sf $NATIVE/$PACKAGES/$PACKAGE/$NAME $ARCHIVE
			tar czhf $ARCHIVE.tar.gz $ARCHIVE \
				--exclude CVS \
				--owner=root --group=root --mode=go-rwx
			if [ $? -eq 0 -a -d $HOME/archives ]; then
				mv -f $ARCHIVE.tar.gz $HOME/archives/
				ln -s $HOME/archives/$ARCHIVE.tar.gz .
			fi
			rm $ARCHIVE
		done < $NATIVE/$PACKAGES/$PACKAGE/build.archive
	fi
	ls $SOURCES/$PACKAGES/$PACKAGE/*.src.rpm 2>/dev/null | \
		xargs -n 1 -i sh -c 'rpm2cpio {} | cpio -i --quiet'
	ln -sf $SOURCES/$PACKAGES/$PACKAGE/* .
	rm -f '*' || :
	ln -sf $NATIVE/$PACKAGES/$PACKAGE/* .
	test -e $PACKAGE.spec || ln -s "`spec $PACKAGE`" $PACKAGE.spec
	$TIME $PERSONALITY rpm -bb $PACKAGE.spec \
		$TARGET \
		--define "distribution $NATIVE_DISTRIBUTION" \
		--define "vendor $NATIVE_VENDOR" \
		--define "buildarch $BUILDARCH" \
		--define "buildhost $BUILDHOST" \
		--define "home $HOME" \
		--define "number $NUMBER" \
		&> $HOME/logs/$PACKAGE < /dev/null || \
		log "#$NUMBER: Failed $PACKAGE"
	cd $HOME/native-work || exit 1
	mv $WORK/RPMS/*/* $HOME/RPMS/ &> /dev/null
	mv $WORK/SRPMS/* $HOME/SRPMS/ &> /dev/null
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
		--define "buildhost $BUILDHOST" \
		--define "home $HOME" \
		--define "number $NUMBER" \
		&> $HOME/logs/$PACKAGE < /dev/null
	if mv $WORK/RPMS/*/* $HOME/RPMS/ &> /dev/null; then
		ln $FOREIGN/$PACKAGE.src.rpm $HOME/SRPMS/ &> /dev/null ||
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
	sparc*)
		ARCHITECTURE=sparc
		;;
	alpha)
		ARCHITECTURE=alpha
		;;
	esac
}

function builder()
{
	local NUMBER SOURCE BINARY SPEC REGEX

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

	test -n "$BUILDHOST" || BUILDHOST="`hostname -f`"

	log "#$NUMBER: Scanning native"

	cd $HOME/native-work || exit 1

	ls $NATIVE/$PACKAGES/ | grep -v '^CVS$' |
	while read SOURCE; do
		SPEC="`spec $SOURCE`"
		test -n "$SPEC" || continue
		mkdir .${SOURCE} &> /dev/null || continue
		touch .${SOURCE}/$NUMBER
		if grep -q '^%files[[:space:]]*$' $SPEC; then
			REGEX='^$'
		else
			REGEX="^${SOURCE}-[^-]*-[^-]*\$"
		fi
		rpm -q --specfile $SPEC | grep -v "$REGEX" |
		while read BINARY; do
			REGEX="^${BINARY}\.[^.]*\.rpm\$"
			if [ -z "`ls $HOME/RPMS/ | grep "$REGEX"`" ]; then
				touch .${SOURCE}/do
				break
			fi
		done
		if [ -e .${SOURCE}/do ]; then
			build_native $NUMBER $SOURCE
		else
			log "#$NUMBER: Skipping $SOURCE"
		fi
	done

	log "#$NUMBER: Scanning foreign"

	cd $HOME/foreign-work || exit 1

	ls $FOREIGN/ |
	while read SOURCE; do
		SOURCE=`basename $SOURCE .src.rpm`
		mkdir .${SOURCE} &> /dev/null || continue
		touch .${SOURCE}/$NUMBER
		if [ -e $HOME/SRPMS/$SOURCE.src.rpm ]; then
			log "#$NUMBER: Skipping $SOURCE"
		else
			build_foreign $NUMBER $SOURCE
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
	exit 1
}

if [ "`id -u`" = "0" -o ! -O $HOME ]; then
	echo "Run this as the owner of $HOME (typically, as user \"build\")"
	exit 1
fi

unset LANG LANGUAGE
unset LC_ALL LC_COLLATE LC_CTYPE LC_MESSAGES LC_MONETARY LC_NUMERIC LC_TIME
unset LINGUAS

umask $UMASK
cd $HOME || exit 1

mkdir -p foreign
mkdir -p RPMS SRPMS archives logs

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

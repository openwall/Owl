#!/bin/bash
# $Owl: Owl/build/buildworld.sh,v 1.53.2.1 2013/04/07 22:44:17 solar Exp $

NATIVE_DISTRIBUTION='Openwall GNU/*/Linux'
NATIVE_VENDOR='Openwall'

TIME=/usr/bin/time
test -x "$TIME" || TIME=

. buildworld.conf

export -n BRANCH PACKAGE
MAKEFLAGS=${MAKEFLAGS/PACKAGE=*}

PACKAGES=$BRANCH/packages

NATIVE=$HOME/native
SOURCES=$HOME/sources
FOREIGN=$HOME/foreign

RPMQ=rpm
RPMB=rpm

# Expand here %sparc, %alpha, etc. if you can build for it
ARCH_EXPAND='s/%ix86/i386 i486 i586 i686 pentium3 pentium4 athlon geode/g'

log()
{
	local MESSAGE

	MESSAGE="$1"

	echo "`date +%H:%M:%S`: $MESSAGE" | tee -a $HOME/logs/buildworld
}

spec()
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

	if [ -n "$SPEC" ]; then
		ARCH_INC=`sed -nr "$ARCH_EXPAND; /^ExclusiveArch/Ip" "$SPEC"`
		if [ -n "$ARCH_INC" ]; then
			if ! echo "$ARCH_INC" | fgrep -q $ARCHITECTURE; then
				SPEC=
			fi
		fi
	fi

	if [ -n "$SPEC" ]; then
		ARCH_EXC=`sed -nr "$ARCH_EXPAND; /^ExcludeArch/Ip" "$SPEC"`
		if [ -n "$ARCH_EXC" ]; then
			if echo "$ARCH_EXC" | fgrep -q $ARCHITECTURE; then
				SPEC=
			fi
		fi
	fi

	echo "$SPEC"
}

binaries()
{
	local SPEC SOURCE TOTAL SUB

	SPEC=$1
	SOURCE=$2

	TOTAL="`grep -cE '^%files([[:space:]]|$)' $SPEC`"
	test $? -gt 1 && return 1
	SUB="`grep -cEf - $SPEC << EOF
^%files[[:space:]]+-n
^%files[[:space:]].*[[:space:]]-n
^%files[[:space:]]+[^[:space:]-]
^%files[[:space:]].*[[:space:]][^[:space:]-][^[:space:]]*[[:space:]]+[^[:space:]-]
EOF`"
	test $? -gt 1 && return 1

	if [ $TOTAL -gt $SUB ]; then
		$RPMQ -q --specfile $SPEC
	else
		$RPMQ -q --specfile $SPEC | grep -v "^${SOURCE}-[^-]*-[^-]*\$"
	fi
}

built()
{
	local SPEC SOURCE BINARY REGEX

	SPEC=$1
	SOURCE=$2

	binaries $SPEC $SOURCE |
	while read BINARY; do
		REGEX="^${BINARY}\.[^.]*\.rpm\$"
		if [ -z "`ls $HOME/RPMS/ | grep "$REGEX"`" ]; then
			cat > /dev/null
			return 1
		fi
	done
}

build_native()
{
	local NUMBER PACKAGE WORK NAME VERSION ARCHIVE FLAGS WITH_WITHOUT_TEST

	NUMBER=$1
	PACKAGE=$2

	WORK=$HOME/rpm-work-$NUMBER

	log "#$NUMBER: Building $PACKAGE"
	cd $WORK/SOURCES/ || exit 1
	if [ -f $NATIVE/$PACKAGES/$PACKAGE/build.archive ]; then
		while read NAME VERSION; do
			ARCHIVE=${NAME}-${VERSION}
			ln -sf $NATIVE/$PACKAGES/$PACKAGE/$NAME $ARCHIVE
			tar czhf $ARCHIVE.tar.gz \
				--exclude CVS \
				--owner=root --group=root --mode=go-rwx \
				$ARCHIVE
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
	if [ "$BUILDSOURCE" = "yes" ]; then
		FLAGS=-ba
	else
		FLAGS=-bb
	fi
	case "${RUN_TESTS-}" in
		yes) WITH_WITHOUT_TEST='--with test' ;;
		no) WITH_WITHOUT_TEST='--without test' ;;
		*) WITH_WITHOUT_TEST= ;;
	esac
	if $TIME $PERSONALITY $RPMB $FLAGS $PACKAGE.spec \
		$TARGET \
		--define "distribution $NATIVE_DISTRIBUTION" \
		--define "vendor $NATIVE_VENDOR" \
		--define "buildarch $BUILDARCH" \
		--define "buildhost $BUILDHOST" \
		--define "home $HOME" \
		--define "number $NUMBER" \
		$WITH_WITHOUT_TEST \
		&> $HOME/logs/$PACKAGE < /dev/null;
	then
		mv $WORK/RPMS/*/* $HOME/RPMS/
		test "$BUILDSOURCE" = "yes" && mv $WORK/SRPMS/* $HOME/SRPMS/
	else
		rm -rf $WORK/RPMS/*
		test "$BUILDSOURCE" = "yes" && rm -rf $WORK/SRPMS/*
		log "#$NUMBER: Failed $PACKAGE"
		touch $HOME/native-work/failed
	fi
	rm -rf $WORK/buildroot
	rm -rf $WORK/BUILD/*
	rm $WORK/SOURCES/*
	cd $HOME/native-work || exit 1
}

build_foreign()
{
	local NUMBER PACKAGE WORK

	NUMBER=$1
	PACKAGE=$2

	WORK=$HOME/rpm-work-$NUMBER

	log "#$NUMBER: Building $PACKAGE"
	if $TIME $PERSONALITY $RPMB --rebuild $FOREIGN/${PACKAGE}.src.rpm \
		$TARGET \
		--define "buildarch $BUILDARCH" \
		--define "buildhost $BUILDHOST" \
		--define "home $HOME" \
		--define "number $NUMBER" \
		--define "_unpackaged_files_terminate_build 0" \
		--define "_missing_doc_files_terminate_build 0" \
		&> $HOME/logs/$PACKAGE < /dev/null;
	then
		mv $WORK/RPMS/*/* $HOME/RPMS/
	else
		rm -rf $WORK/RPMS/*
		log "#$NUMBER: Failed $PACKAGE"
	fi
	rm -rf $WORK/BUILD/*
}

builder()
{
	local NUMBER SOURCE SPEC

	NUMBER=$1

	log "#$NUMBER: Scanning native"

	cd $HOME/native-work || exit 1

	ls $NATIVE/$PACKAGES/ | grep -v '^CVS$' |
	while read SOURCE; do
		SPEC="`spec $SOURCE`"
		test -n "$SPEC" || continue
		mkdir .${SOURCE} &> /dev/null || continue
		touch .${SOURCE}/$NUMBER
		if [ -n "$PACKAGE" ]; then
			if [ "$SOURCE" = "$PACKAGE" ]; then
				touch $HOME/rpm-work-$NUMBER/built
				build_native $NUMBER $SOURCE
			fi
		elif built $SPEC $SOURCE; then
			log "#$NUMBER: Skipping $SOURCE"
		else
			build_native $NUMBER $SOURCE
		fi
	done
	if [ -n "$PACKAGE" -a ! -e "$HOME/rpm-work-$NUMBER/built" ]; then
		log "#$NUMBER: Failed $PACKAGE (no such package)"
		touch $HOME/native-work/failed
	fi

	log "#$NUMBER: Scanning foreign"

	cd $HOME/foreign-work || exit 1

	test -d $FOREIGN &&
	ls $FOREIGN/ |
	while read SOURCE; do
		SOURCE=`basename $SOURCE .src.rpm`
		mkdir .${SOURCE} &> /dev/null || continue
		cd .${SOURCE} || exit 1
		touch $NUMBER
		if [ -n "$PACKAGE" ]; then
			cd $HOME/foreign-work || exit 1
			if [ "$SOURCE" = "$PACKAGE" ]; then
				build_foreign $NUMBER $SOURCE
			fi
			continue
		fi
		rpm2cpio $FOREIGN/${SOURCE}.src.rpm | cpio -i --quiet '*.spec'
		cd $HOME/foreign-work || exit 1
		SPEC=$HOME/foreign-work/.${SOURCE}/*.spec
		if built $SPEC $SOURCE; then
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

detect_arch()
{
	local MACHINE

	MACHINE=`uname -m` || MACHINE="unknown"

	case "$MACHINE" in
	*86)
		ARCHITECTURE=i686
		;;
	x86_64)
		ARCHITECTURE=x86_64
		;;
	sparc*)
		ARCHITECTURE=sparc
		;;
	alpha)
		ARCHITECTURE=alpha
		;;
	esac
}

detect_proc()
{
	case "$ARCHITECTURE" in
	sparc*)
		PROCESSORS="`sed -n \
			's/^ncpus active[[:space:]]\+: \([0-9]\+\)$/\1/p' \
			/proc/cpuinfo`"
		;;
	alpha*)
		PROCESSORS="`sed -n \
			's/^cpus detected[[:space:]]\+: \([0-9]\+\)$/\1/p' \
			/proc/cpuinfo`"
		;;
	*)
		PROCESSORS="`grep -cw ^processor /proc/cpuinfo`"
		;;
	esac

	test -n "$PROCESSORS" || PROCESSORS=1
	test "$PROCESSORS" -ge 1 || PROCESSORS=1
}

detect()
{
	test -n "$ARCHITECTURE" || detect_arch
	test -n "$PROCESSORS" || detect_proc
	if [ -n "$PACKAGE" ]; then
		test -n "$MAKEFLAGS" || MAKEFLAGS="-j $PROCESSORS"
		if [ "$PROCESSORS" -lt 2 ]; then
# "pigz -11" requires at least 2 threads currently
			test -n "$PIGZ" || PIGZ="-p 2"
		else
			test -n "$PIGZ" || PIGZ="-p $PROCESSORS"
		fi
		PROCESSORS=1
	else
# If we build multiple packages in parallel, reduce per-package parallelism
# (pigz would use up to 8 threads by default).
		test -n "$PIGZ" || PIGZ="-p 2"
	fi
	test -n "$BUILDHOST" || BUILDHOST="`hostname -f`"
	test -n "$BUILDHOST" || BUILDHOST="localhost.localdomain"

	if [ -n "$ARCHITECTURE" ]; then
		TARGET="--target ${ARCHITECTURE}-unknown-linux"
		BUILDARCH="$ARCHITECTURE"
	else
		TARGET=
		BUILDARCH="%_arch"
	fi

	if [ -z "$PERSONALITY" ]; then
		case "$ARCHITECTURE" in
		sparc|sparcv9)
			PERSONALITY=sparc32
			;;
		*86)
			PERSONALITY=i386
			;;
		x86_64)
			PERSONALITY=x86_64
			;;
		*)
			PERSONALITY=
			;;
		esac
	fi

	PERSONALITY=$(type -P $PERSONALITY 2>/dev/null)
	test -x "$PERSONALITY" || PERSONALITY=
}

check_includes()
{
	test `find /usr/include/linux/ /usr/include/asm/ \
		-type f ! -perm +004 -print 2>&1 | wc -c` = '0'
}

sanity_check()
{
	log "Sanity check"

	check_includes || {
		log "Kernel headers are not world-readable - they should be"
		exit 1
	}

	test -r /usr/include/linux/version.h || {
		log "No /usr/include/linux/version.h (kernel never configured?)"
		exit 1
	}
}

clean_death()
{
	kill 0

	cd $HOME || exit 1
	rm -rf tmp-work rpm-work-[1-9]* native-work foreign-work

	echo "`date '+%Y %b %e %H:%M:%S'`: Interrupted" >> logs/buildworld
	exit 1
}

setup_rpm()
{
	local RPM_VERSION

	log "Detecting version of RPM"
	RPM_VERSION="`rpm --version | cut -f3 -d' '`"
	if [ -z "$RPM_VERSION" ]; then
		log "Cannot find RPM version, perhaps 'rpm' is not in PATH?"
		exit 1
	fi

	case "$RPM_VERSION" in
	4.*)
		log "It's RPM4, using different binaries for different tasks"
		RPMQ=rpmquery
		RPMB=rpmbuild
		;;
	3.*)
		log "It's RPM3, using 'rpm' for everything"
		;;
	*)
		log "Unknown version of RPM, using defaults"
		;;
	esac
}

if [ "`id -u`" = "0" -o ! -O $HOME ]; then
	echo >&2 "Run this as the owner of $HOME (typically, as user \"build\")"
	exit 1
fi

unset LANG LANGUAGE LINGUAS
unset LC_ADDRESS LC_ALL LC_COLLATE LC_CTYPE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE LC_TIME

umask $UMASK
cd $HOME || exit 1

mkdir -p logs archives RPMS
test "$BUILDSOURCE" = "yes" && mkdir -p SRPMS

echo "`date '+%Y %b %e %H:%M:%S'`: Started" >> logs/buildworld

setup_rpm

log "Removing stale temporary files"
rm -rf tmp-work rpm-work-[1-9]* native-work foreign-work

trap clean_death HUP INT TERM

detect
sanity_check

NUMBER=1
while [ $NUMBER -le $PROCESSORS ]; do
	mkdir -p rpm-work-$NUMBER/{BUILD,SOURCES,SPECS,SRPMS}
	mkdir -p rpm-work-$NUMBER/RPMS/{noarch,i386,i686,x86_64,sparc,sparcv9,alpha}
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

STATUS=0
if [ -e $HOME/native-work/failed ]; then
	STATUS=1
	log "Some packages failed to build"
fi

log "Removing temporary files"
rm -rf tmp-work native-work foreign-work

echo "`date '+%Y %b %e %H:%M:%S'`: Finished" >> logs/buildworld
exit $STATUS

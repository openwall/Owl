#!/bin/sh
# $Id: Owl/build/installworld.sh,v 1.15 2004/09/30 09:41:10 galaxy Exp $

. installworld.conf

RPMS=$HOME/RPMS

RPM=rpm
RPMD=rpm
RPM_FLAGS=

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

function setup_rpm()
{
	local FILE

	if [ -e /.Owl-CD-ROM ]; then
		log "Running off a CD, will use this system's RPM binary"
		return
	fi

	cd $RPMS || exit 1

	FILE="`ls rpm-[0-9]*-*.*.rpm 2>/dev/null | tail -1`"
	if [ -z "$FILE" ]; then
		log "Missing RPM package, will use this system's RPM binary"
		return
	fi

	cd $TMPDIR || exit 1
	log "Extracting the RPM binary"
	if rpm2cpio $RPMS/$FILE | cpio -id --no-preserve-owner --quiet \
	    usr/lib/rpm/{rpmi,rpmd,rpmrc,macros,rpmpopt\*} && \
	    sed -e "s,^\\(macrofiles:\\).*\$,\\1 $TMPDIR/usr/lib/rpm/macros," \
	    < $TMPDIR/usr/lib/rpm/rpmrc \
	    > $TMPDIR/usr/lib/rpm/rpmrc-work; then
		RPM=$TMPDIR/usr/lib/rpm/rpmi
		RPMD=$TMPDIR/usr/lib/rpm/rpmd
		export RPMALIAS_FILENAME="$TMPDIR/usr/lib/rpm/rpmpopt"
		RPM_FLAGS="--rcfile $TMPDIR/usr/lib/rpm/rpmrc-work:$HOME/.rpmrc"
	else
		log "Failed to extract RPM, will use this system's RPM binary"
	fi
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

setup_rpm

if [ -f $ROOT/var/lib/rpm/packages.rpm -o -f $ROOT/var/lib/rpm/Packages ]; then
	if [ -f $ROOT/var/lib/rpm/packages.rpm -a -s $ROOT/var/lib/rpm/Packages -a $ROOT/var/lib/rpm/packages.rpm -nt $ROOT/var/lib/rpm/Packages ]; then
		log "Cannot determine which of RPM database to use in $ROOT/var/lib/rpm"
		exit 1
	fi
	if [ -f $ROOT/var/lib/rpm/Packages -a ! -s $ROOT/var/lib/rpm/Packages ]; then
		log "Found empty $ROOT/var/lib/rpm/Packages, removed"
		rm $ROOT/var/lib/rpm/Packages
	fi
# First of all, we will do the check that no user packages make use of
# libdb.so.2 and libdb.so.3 from glibc-2.1.3. For that task we have to
# use system RPM and, if we cannot access it - we will fail.
	if ! type rpm >& /dev/null; then
		log "Cannot find system RPM, aborting"
		exit 1
	fi

	LIBDB2_DEPS=$(rpm --root $ROOT -q --whatrequires libdb.so.2 2>/dev/null | grep -vE "^no package" | grep -vE "^rpm-")
	LIBDB3_DEPS=$(rpm --root $ROOT -q --whatrequires libdb.so.3 2>/dev/null | grep -vE "^no package" | grep -vE "^(pam|perl|postfix)-")

	if [ -n "$LIBDB2_DEPS" -o -n "$LIBDB3_DEPS" ]; then
		echo "
Warning!
We found that upgrade procedure will breaks packages listed below, because
of absence of libdb.so.2 and libdb.so.3 support in supplied glibc:
" >&2
		if [ -n "$LIBDB2_DEPS" ]; then
			echo "libdb.so.2 dependend packages:" >&2
			for pkg in $LIBDB2_DEPS; do echo "$pkg" >&2 ; done
		fi
		if [ -n "$LIBDB3_DEPS" ]; then
			echo "libdb.so.3 dependend packages:" >&2
			for pkg in $LIBDB3_DEPS; do echo "$pkg" >&2 ; done
		fi
		echo "
Please resolve this issue before running Owl upgrade procedure again.

For quick and dirty solution you can use:
# rpm --root $ROOT -e --justdb package
This will remove package information and it's dependencies from RPM database,
but leaves all files inplace.
" >&2
		log "Found non-Owl packages those what unsupported libraries"
		exit 1
	fi

	log "Rebuilding RPM database"
	$RPMD $RPM_FLAGS --root $ROOT --rebuilddb || exit 1
	NEED_FAKE=yes
else
	log "Initializing RPM database"
	[ ! -d $ROOT/var/lib/rpm ] && mkdir -p $ROOT/var/lib/rpm
	chmod 0755 $ROOT/var/lib/rpm
	$RPMD $RPM_FLAGS --root $ROOT --initdb || exit 1
	NEED_FAKE=no
fi

export MAKE_CDROM

export SILO_INSTALL
export SILO_FLAGS

cd $RPMS || exit 1

grep -v ^# $HOME/installorder.conf |
while read PACKAGES; do
	FILES=
	for PACKAGE in $PACKAGES; do
		if [ "$PACKAGE" = owl-cdrom -a "$MAKE_CDROM" != yes ]; then
			log "Skipping $PACKAGE"
			continue
		fi
		if [ "$NEED_FAKE" != yes ]; then
			case "$PACKAGE" in
				glibc-compat-libdb|\
				libstdc++-compat)
				log "Skipping $PACKAGE"
				continue
				;;
			esac
		fi
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

if [ "$NEED_FAKE" == yes ]; then
	log "Removing installation support packages"
	if ! $RPM $RPM_FLAGS --root $ROOT -ev glibc-compat-libdb; then
		log "Removal of glibc-compat-libdb was failed"
	fi
	if ! $RPM $RPM_FLAGS --root $ROOT -ev libstdc++-compat; then
		log "Removal of libstdc++-compat was failed"
	fi
fi

log "Removing temporary files"
rm -rf $HOME/tmp-work $ROOT/$HOME/tmp-work

echo "`date '+%Y %b %e %H:%M:%S'`: Finished" >> $HOME/logs/installworld

exit $STATUS

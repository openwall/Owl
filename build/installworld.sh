#!/bin/sh
# $Id: Owl/build/installworld.sh,v 1.21 2004/12/26 01:18:35 galaxy Exp $

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

if [ -f $ROOT/var/lib/rpm/packages.rpm -o -f $ROOT/var/lib/rpm/Packages ]; then
	if [ -f $ROOT/var/lib/rpm/packages.rpm -a \
	    -s $ROOT/var/lib/rpm/Packages -a \
	    $ROOT/var/lib/rpm/packages.rpm -nt $ROOT/var/lib/rpm/Packages ];
	then
		log "Cannot determine which RPM database to use in $ROOT/var/lib/rpm"
		exit 1
	fi
	if [ -f $ROOT/var/lib/rpm/Packages -a \
	    ! -s $ROOT/var/lib/rpm/Packages ]; then
		log "Found empty $ROOT/var/lib/rpm/Packages, removed"
		rm $ROOT/var/lib/rpm/Packages
	fi

# First of all, we will do the check that no user packages make use of
# libdb.so.2 and libdb.so.3 from glibc 2.1.3. For that task we have to
# use the target system's RPM.
	if [ ! -x $ROOT/bin/rpm ]; then
		log "Found an RPM database but no RPM binary, aborting"
		exit 1
	fi

# XXX: Should check for errors (rpm's exit status).
	CHROOT_BIN=$(which chroot 2>/dev/null)
	LIBDB23_DEPS=$(echo `env - ${CHROOT_BIN:=/usr/sbin/chroot} $ROOT /bin/rpm -q --whatrequires libdb.so.2 libdb.so.3 2>/dev/null | sort -u | grep -vE '^(no package|rpm-|pam-|perl-|postfix-)'`)

	if [ -n "$LIBDB23_DEPS" ]; then
		cat << EOF
Warning!
We found that upgrade procedure will break packages listed below, because
of the absence of libdb.so.2 and libdb.so.3 support in our supplied glibc:

EOF
		echo "$LIBDB23_DEPS"
		cat << EOF

Please resolve this issue before running Owl upgrade procedure again.

You can try to remove the problematic packages from the system with:

	# chroot $ROOT /bin/rpm -e $LIBDB23_DEPS

This command will fail if other packages depend on those requiring the
old versions of libdb.  If so, remove those other packages in a similar
manner as well, then try again.
EOF
		log "Found non-Owl packages which depend on old libdb"
		exit 1
	fi

	setup_rpm

	log "Rebuilding RPM database"
	$RPMD $RPM_FLAGS --root $ROOT --rebuilddb || exit 1
	NEED_FAKE=yes
else
	setup_rpm

	log "Initializing RPM database"
	mkdir -m 755 -p $ROOT/var/lib/rpm
	$RPMD $RPM_FLAGS --root $ROOT --initdb || exit 1

	# XXX: (GM): This is a hack. We are cloning empty database file
	# Packages to Providename to shut our RPM during installation
	cp -a $ROOT/var/lib/rpm/{Packages,Providename} || exit 1
	$RPMD $RPM_FLAGS --root $ROOT --rebuilddb || exit 1

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
			glibc-compat-fake|libstdc++-compat)
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

if [ "$NEED_FAKE" = yes ]; then
	log "Removing installation support packages"
	if ! $RPM $RPM_FLAGS --root $ROOT -ev glibc-compat-fake; then
		log "Removal of glibc-compat-fake failed"
	fi
	if ! $RPM $RPM_FLAGS --root $ROOT -ev libstdc++-compat; then
		log "Removal of libstdc++-compat failed"
	fi
fi

log "Removing temporary files"
rm -rf $HOME/tmp-work $ROOT/$HOME/tmp-work

echo "`date '+%Y %b %e %H:%M:%S'`: Finished" >> $HOME/logs/installworld

exit $STATUS

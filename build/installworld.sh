#!/bin/bash
# $Owl: Owl/build/installworld.sh,v 1.48 2014/07/12 17:13:07 galaxy Exp $

. installworld.conf

RPMS=$HOME/RPMS

RPM=rpm
RPMD=rpm
RPMQ=rpm
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
	local RPM2CPIO
	local EXTRACT_RC

	if [ -e /.Owl-CD-ROM -a "$HOME" = /usr/src/world ]; then
		log "Running off a CD, will use this system's RPM binary"
		return
	fi

	cd $RPMS || exit 1

	# for rpm-4.11 we need libnss, libnspr (required by libnss),
	# and libpopt (required by rpm).

	FILE[0]=$(ls rpm-[0-9]*-*.*.rpm 2>/dev/null | tail -1)
	FILE[1]=$(ls rpm-rescue-[0-9]*-*.*.rpm 2>/dev/null | tail -1)
	FILE[2]=$(ls libnspr-[0-9]*-*.*.rpm 2>/dev/null | tail -1)
	FILE[3]=$(ls libnss-[0-9]*-*.*.rpm 2>/dev/null | tail -1)
	FILE[4]=$(ls libpopt-[0-9]*-*.*.rpm 2>/dev/null | tail -1)
	if [ -z "${FILE[0]}" -o -z "${FILE[1]}" -o -z "${FILE[2]}" \
			-o -z "${FILE[3]}" -o -z "${FILE[4]}" ]; then
		log "Missing RPM package or one of its deps, will use this system's RPM binary"
		return
	fi

	RPM2CPIO="$HOME/${0%/*}/rpm2cpio.sh"
	if [ ! -x "$RPM2CPIO" ]; then
		log "Missing the rpm2cpio.sh script, will use this system's RPM binary"
		return
	fi

	cd $TMPDIR || exit 1
	log "Extracting RPM support files"
	EXTRACT_RC=0

	# extracting parts from rpm
	if $RPM2CPIO $RPMS/${FILE[0]} | cpio -id --no-preserve-owner --quiet \
	    \*usr/lib/rpm/{rpmrc,macros\*,rpmpopt\*} && \
	    sed -e "s,^\\(macrofiles:\\).*\$,\\1 $TMPDIR/usr/lib/rpm/macros," \
	    < $TMPDIR/usr/lib/rpm/rpmrc \
	    > $TMPDIR/usr/lib/rpm/rpmrc-work; then
		grep '^[[:space:]]*macrofiles:' $TMPDIR/usr/lib/rpm/rpmrc-work >/dev/null 2>&1 \
			|| echo "macrofiles: $TMPDIR/usr/lib/rpm/macros" >> $TMPDIR/usr/lib/rpm/rpmrc-work
		export RPMALIAS_FILENAME=$(ls "$TMPDIR/usr/lib/rpm/rpmpopt"* 2>/dev/null | tail -1)
		RPM_FLAGS="--rcfile $TMPDIR/usr/lib/rpm/rpmrc-work:$HOME/.rpmrc"
	else
		log "Failed to extract RPM support files"
		EXTRACT_RC=1
	fi
	# extracting rpm-rescue
	if $RPM2CPIO $RPMS/${FILE[1]} | cpio -id --no-preserve-owner --quiet \
	    \*bin/rpm\*.rescue ; then
		cat << EOF > bin/rpm
#!/bin/sh
ARCH=$(uname -m)
LIB=lib
case "$ARCH" in
	*64) LIB="${LIB}64"
		;;
esac
LD_LIBRARY_PATH="$TMPDIR/$LIB:$TMPDIR/usr/$LIB"
export LD_LIBRARY_PATH
exec \$0.rescue "\$@"
EOF
		chmod 0755 bin/rpm && \
		cp -a bin/rpm bin/rpmdb && \
		RPM=$TMPDIR/bin/rpm && \
		RPMD=$TMPDIR/bin/rpmdb && \
		RPMQ=$TMPDIR/bin/rpm || \
		EXTRACT_RC=3
	else
		log "Failed to extract RPM binaries"
		EXTRACT_RC=2
	fi
	# extracting libnspr, libnss, and libpopt
	if $RPM2CPIO $RPMS/${FILE[2]} | cpio -id --no-preserve-owner --quiet && \
		$RPM2CPIO $RPMS/${FILE[3]} | cpio -id --no-preserve-owner --quiet \*lib\*/lib\* && \
		$RPM2CPIO $RPMS/${FILE[4]} | cpio -id --no-preserve-owner --quiet \*lib\*/lib\* ; then
		log "Extracted all parts of RPM"
	else
		log "Failed to extract RPM dependencies"
		EXTRACT_RC=4
	fi

	if [ $EXTRACT_RC -ne 0 ]; then
		log "Some errors detected, will use this system's RPM binary"
		unset RPMALIAS_FILENAME
		unset RPM_FLAGS
		RPM=rpm
		RPMD=rpm
		RPMQ=rpm
	fi
}

if [ "$MAKE_CDROM" = yes -a -n "$ISOTREE_ROOT" ]; then
	FORCE_ROOT="$ISOTREE_ROOT"
fi
if [ -n "$FORCE_ROOT" ]; then
	ROOT="$FORCE_ROOT"
fi

if [ ! -d $ROOT -o ! -O $ROOT ] ||
   [ -n "$FORCE_ROOT" -a "$(readlink -e "$ROOT")" = / ]; then
	echo >&2 "Invalid ROOT ($ROOT) or not running as the directory owner"
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
# libdb.so.2 and libdb.so.3 from glibc 2.1.3, or libdb-4.0.so, libdb-4.2.so,
# libdb_cxx-4.0.so and libdb_cxx-4.2.so from db4 4.3.  For that task we have
# to use the target system's RPM.
	if [ ! -x $ROOT/bin/rpm ]; then
		log "Found an RPM database but no RPM binary, aborting"
		exit 1
	fi

# XXX: Should check for errors (rpm's exit status).
	CHROOT_BIN=$(type -p chroot 2>/dev/null)
	LIBDB234_DEPS=$(echo `env - ${CHROOT_BIN:=/usr/sbin/chroot} $ROOT /bin/rpm -q --whatrequires libdb.so.2 libdb.so.3 libdb-4.0.so libdb-4.2.so libdb_cxx-4.0.so libdb_cxx-4.2.so 2>/dev/null | sort -u | grep -vE '^(no package|rpm-|pam-|perl-|postfix-|db4-utils-)'`)

	if [ -n "$LIBDB234_DEPS" ]; then
		cat << EOF
Warning!
We found that upgrade procedure will break packages listed below, because
of the absence of libdb.so.2, libdb.so.3, libdb-4.0.so, libdb-4.2.so,
libdb_cxx-4.0.so and libdb_cxx-4.2.so support in our supplied glibc and db4:

EOF
		echo "$LIBDB234_DEPS"
		cat << EOF

Please resolve this issue before running Owl upgrade procedure again.

You can try to remove the problematic packages from the system with:

	# chroot $ROOT /bin/rpm -e $LIBDB234_DEPS

This command will fail if other packages depend on those requiring the
old versions of libdb.  If so, remove those other packages in a similar
manner as well, then try again.
EOF
		log "Found non-Owl packages which depend on old libdb"
		exit 1
	fi

	setup_rpm

	log "Rebuilding RPM database"
# Remove __db.00? files that look like they're pre-NPTL.  The next invocation
# of rpm will recreate the files.
	if [ -f $ROOT/var/lib/rpm/__db.001 -a \
	    "`wc -c < $ROOT/var/lib/rpm/__db.001`" -le 8192 ]; then
		rm -f $ROOT/var/lib/rpm/__db.00?
	fi
	$RPMD $RPM_FLAGS --root $ROOT --rebuilddb || exit 1

# We introduced x86_64 support shortly _after_ Owl 2.0 release, so we do not
# have nor need the backwards compatibility installation support packages on
# this architecture.  In the check below, we assume that we're running with the
# correct personality set (e.g., set to i686 when upgrading a 32-bit system
# while running an x86_64 kernel), which is similarly assumed by RPM anyway.
	if [ "`uname -m`" != x86_64 ]; then
		NEED_FAKE=yes
	else
		NEED_FAKE=no
	fi
else
	setup_rpm

	log "Initializing RPM database"
	mkdir -m 755 -p $ROOT/var/lib/rpm
	$RPMD $RPM_FLAGS --root $ROOT --initdb || exit 1

# XXX: (GM): This is a hack. We are cloning empty database file Packages
# to Providename to shut our RPM during installation.
	cp -a $ROOT/var/lib/rpm/{Packages,Providename} || exit 1
	$RPMD $RPM_FLAGS --root $ROOT --rebuilddb || exit 1

	NEED_FAKE=no
fi

# owl-hier prior to 0.10-owl1 provided /var/tmp as a directory, even though
# owl-setup (the settle program) then offered to optionally make it a symlink
# to /tmp.  owl-hier 0.10-owl1 switched to packaging the symlink right away.
# Unfortunately, RPM can't handle this change on upgrade on its own.  Moreover,
# we can't do it from owl-hier's scriptlets because owl-hier is installed
# before we install the shell.  Hence, we try to remove the directory here.
if [ ! -L $ROOT/var/tmp -a -d $ROOT/var/tmp ]; then
	if mv $ROOT/var/tmp{,-}; then
		ln -s /tmp $ROOT/var/tmp
# If we fail to remove the old /var/tmp directory, have a message printed (the
# error message from rmdir) and leave the directory as /var/tmp-, mode 700.
		rmdir $ROOT/var/tmp- || chmod 700 $ROOT/var/tmp-
	fi
fi

export MAKE_CDROM

export SILO_INSTALL
export SILO_FLAGS

cd $RPMS || exit 1

# Don't install host system specific packages inside a container
if [ -e $ROOT/proc/vz -a ! -e $ROOT/proc/vz/version ]; then
	SKIP_HOST=yes
fi

grep -v ^# $HOME/installorder.conf |
while read PACKAGES; do
	PACKAGES_SUBSET=
	FILES=
	for TOKEN in $PACKAGES; do
		PACKAGE=${TOKEN#[A-Za-z]:}
		TAG=${TOKEN:0:2}
		if [ \( "$TAG" = "D:" -a "$MAKE_CDROM" != yes \) -o \
		    \( "$TAG" = "d:" -a "$MAKE_CDROM" = yes \) -o \
		    \( "$TAG" = "E:" -a "$SKIP_EXTRA" = yes \) -o \
		    \( "$TAG" = "H:" -a "$SKIP_HOST" = yes \) ]; then
			log "Skipping $PACKAGE"
			continue
		fi
		if [ "$PACKAGE" = kernel -a "$KERNEL_FAKE" != no ]; then
			PACKAGE=kernel-fake
		fi
		if [ "$NEED_FAKE" != yes ]; then
			case "$PACKAGE" in
			glibc-compat-fake|libstdc++*-compat|db4-compat-fake)
				log "Skipping $PACKAGE"
				continue
				;;
			esac
		fi
		PACKAGES_SUBSET="$PACKAGES_SUBSET $PACKAGE"
# XXX: When multiple versions of a package are present, this will pick one
# of those, but not always the latest one (not for "-owl9" vs. "-owl10").
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
	mkdir -p $HOME/tmp-work/failures/
	for PACKAGE in $PACKAGES_SUBSET; do
		touch $HOME/tmp-work/failures/$PACKAGE
	done
	log "Failed${PACKAGES_SUBSET}"
done

if [ "$NEED_FAKE" = yes ]; then
	log "Removing installation support packages"
	for PACKAGE in glibc-compat-fake libstdc++-v5-compat db4-compat-fake; do
		if ! $RPM $RPM_FLAGS --root $ROOT -ev $PACKAGE; then
			log "Removal of $PACKAGE failed"
		fi
	done
fi

if [ "$NEED_ARCH_TAG" = yes ]; then
	ARCH="`$RPMQ $RPM_FLAGS --root $ROOT -q --whatprovides --queryformat '%{arch}' kernel`"
	if [ -n "$ARCH" ]; then
		echo "$ARCH" > "$ROOT/.Owl-arch"
	fi
fi

FAILED="`cd $HOME/tmp-work/failures/ 2>/dev/null && echo *`"

log "Removing temporary files"
rm -rf $HOME/tmp-work $ROOT/$HOME/tmp-work

echo "`date '+%Y %b %e %H:%M:%S'`: Finished" >> $HOME/logs/installworld

if [ -n "$FAILED" ]; then
	STATUS=1
	log "Failed to install: $FAILED"
fi

exit $STATUS

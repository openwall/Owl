# $Owl: Owl/packages/rpm/rpm.spec,v 1.78 2010/01/26 17:18:57 solar Exp $

%define WITH_PYTHON 0

%define rpm_version 4.2
%define popt_version 1.8

Summary: The Red Hat package management system.
Name: rpm
Version: %rpm_version
Release: owl21
License: GPL
Group: System Environment/Base
# ftp://ftp.rpm.org/pub/rpm/dist/rpm-4.2.x/rpm-%version.tar.gz
Source0: rpm-%version.tar.bz2
Source1: rpminit
Source2: rpminit.1
Source3: gendiff
Source4: configure-presets
# XXX: Patch0 is only for the case of using glibc with NPTL and is currently
# not applied.
#Patch0: rpm-4.2-owl-pthreads.diff
Patch1: rpm-4.2-owl-lite.diff
Patch2: rpm-4.2-owl-librpmbuild-link.diff
Patch3: rpm-4.2-owl-static-utils.diff
Patch4: rpm-4.2-owl-rpmpopt-search.diff
Patch5: rpm-4.2-owl-elfutils-builtin_expect.diff
Patch6: rpm-4.2-owl-macros.diff
Patch7: rpm-4.2-owl-scripts-file.diff
Patch8: rpm-4.2-owl-tmp-scripts.diff
Patch9: rpm-4.2-owl-brp-scripts.diff
Patch10: rpm-4.2-owl-db-umask.diff
Patch11: rpm-4.2-owl-mtab-message.diff
# Regenerated Owl 1.1 patches
Patch12: rpm-4.2-owl-closeall.diff
Patch14: rpm-4.2-owl-autodeps-symbol-versioning.diff
Patch15: rpm-4.2-owl-autoreq.diff
Patch16: rpm-4.2-owl-buildhost.diff
Patch17: rpm-4.2-owl-popt-sgid.diff
Patch18: rpm-4.2-owl-rpmrc.diff
# End of regenerated Owl 1.1 patches
Patch19: rpm-4.2-owl-vendor-setup.diff
Patch20: rpm-4.2-owl-install-perms.diff
# (GM): This one comes from regenerating config files via new automake
Patch21: rpm-4.2-owl-po-mkinstalldirs.diff
Patch22: rpm-4.2-owl-libtoolize.diff
Patch23: rpm-4.2-owl-drop-tests.diff
Patch24: rpm-4.2-owl-transaction-obsoletes-fix.diff
Patch25: rpm-4.2-owl-db-open.diff
Patch26: rpm-4.2-owl-rpmdb-pthread.diff
Patch27: rpm-4.2-owl-db1-addon.diff
Patch28: rpm-4.2-owl-fix-configure.diff
Patch29: rpm-4.2-owl-chroot-ugid.diff
Patch30: rpm-4.2-owl-rpmal-bounds.diff
Patch31: rpm-4.2-owl-compare-digest.diff
Patch32: rpm-4.2-owl-honor-buildtime.diff
Patch33: rpm-4.2-owl-runScript-umask.diff
Patch34: rpm-4.2-owl-man.diff
Patch35: rpm-4.2-cvs-20030515-parseSpec.diff
Patch36: rpm-4.2-cvs-20050827-check-prereqs.diff
Patch37: rpm-4.2-cvs-20061030-showQueryPackage.diff
Patch38: rpm-4.2-rh-owl-build-tar.diff

PreReq: /sbin/ldconfig
PreReq: sh-utils, fileutils, mktemp, gawk
Requires: findutils, diffutils, gzip
BuildRequires: libtool >= 1.5.2, automake >= 1.8.3, autoconf >= 2.59
BuildRequires: gettext >= 0.14.1
BuildRequires: elfutils-libelf-devel >= 0:0.108-owl3
BuildRoot: /override/%name-%rpm_version

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages.  Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package devel
Summary: Development files for applications which will manipulate RPM packages.
Group: Development/Libraries
Requires: %name = %version-%release, popt

%description devel
This package contains the RPM C library and header files.  These
development files will simplify the process of writing programs which
manipulate RPM packages and databases.  These files are intended to
simplify the process of creating graphical package managers or any
other tools that need an intimate knowledge of RPM packages in order
to function.

%package build
Summary: Scripts and executable programs used to build packages.
Group: Development/Tools
Requires: %name = %version-%release
Requires: file

%description build
This package contains scripts and executable programs that are used to
build packages using RPM.

%if %WITH_PYTHON
%package python
Summary: Python bindings for apps which will manipulate RPM packages.
Group: Development/Libraries
Requires: rpm = %rpm_version
Requires: python

%description python
The rpm-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.
%endif

%package -n popt
Summary: A C library for parsing command line arguments.
Version: %popt_version
Group: Development/Libraries
PreReq: /sbin/ldconfig

%description -n popt
popt is a C library for parsing command line arguments.  popt was
heavily influenced by the getopt() and getopt_long() functions, but it
improves on them by allowing more powerful argument expansion.  popt
can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments.  popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%prep
# RPM 3.0.6 magic: after definition of version for popt the version
# macro is set to the popt version -- but this is not correct.
%define	version	%rpm_version
%setup -q

# XXX: RPM tests have known tmp issues :(
rm -r tests

#patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p0
%patch36 -p0
%patch37 -p0
%patch38 -p1

bzip2 -9k CHANGES

# Replace gendiff with our implementation
install -p -m 755 %_sourcedir/gendiff .

# Remove libelf archive just in case
rm -r elfutils

%build
CC=gcc
CXX=g++
export CC CXX
# Prepare libfmagic archive and save it to the rpmio subdirectory.
# Also, put patchlevel.h to the tools directory (it is needed by rpmfile.c)
pushd file
# We add -DMAGIC=path to configure to make sure that default magic file will
# be searched for in the directory where "file" package stores it (this will
# be unneeded once we separate "file" from "rpm")
CFLAGS="%optflags -DMAGIC='\"/usr/share/magic\"'" \
./configure \
	--host=%_target_platform \
	--build=%_target_platform \
	--target=%_target_platform \
	--program-transform-name=
%__make libfmagic.la
cp -rp .libs libfmagic.la ../rpmio/
cp -p patchlevel.h ../tools/
popd
rm -r file

%define _noVersionedDependencies 1

# XXX legacy requires './' payload prefix to be omitted from RPM packages.
%define _noPayloadPrefix 1

%define __usr            /usr
%define __usrsrc         %__usr/src
%define __var            /var

%ifarch x86_64
%define _lib             lib64
%else
%define _lib             lib
%endif
%define __share          /share
%define __prefix         %__usr
%define __exec_prefix    %__prefix
%define __bindir         %__exec_prefix/bin
%define __sbindir        %__exec_prefix/sbin
%define __libexecdir     %__exec_prefix/%_lib
%define __datadir        %__prefix/share
%define __sysconfdir     /etc
%define __sharedstatedir %__prefix/com
%define __localstatedir  %__var
%define __libdir         %__exec_prefix/%_lib
%define __includedir     %__prefix/include
%define __oldincludedir  /usr/include
%define __infodir        %__datadir/info
%define __mandir         %__datadir/man
%define _rpmlibdir       %__prefix/lib/rpm

# XXX rpm needs functioning nptl for configure tests
unset LD_ASSUME_KERNEL || :
%if %WITH_PYTHON
%define with_python_option "--with-python=%with_python_version"
%else
%define with_python_option "--without-python"
%endif

unset LINGUAS || :
libtoolize --force --copy
for ltmain in */ltmain.sh; do
	rm $ltmain
	ln -s ../ltmain.sh $ltmain
done

# this one is for db/dist/ltmain.sh
for ltmain in */*/ltmain.sh; do
	rm $ltmain
	ln -s ../../ltmain.sh $ltmain
done

aclocal
automake -f
autoconf
# This build does not use %%optflags yet, because
# build with %%optflags produces unusable executables.
ac_cv_header_libelf_h=no ac_cv_header_gelf_h=no \
./configure \
	--host=%_target_platform \
	--build=%_target_platform \
	--target=%_target_platform \
	--program-transform-name= \
	--prefix=%__prefix \
	--sysconfdir=%__sysconfdir \
	--localstatedir=%__localstatedir \
	--infodir=%__infodir \
	--mandir=%__mandir \
	--disable-rpath \
	--without-javaglue \
	%with_python_option \
	--disable-posixmutexes
%__make
# Check whether it works at all
./rpmi --showrc >/dev/null
./rpm --showrc >/dev/null

%install
rm -rf %buildroot

%__make DESTDIR="%buildroot" install

mkdir -p %buildroot%__sysconfdir/rpm
mkdir -p %buildroot%__localstatedir/spool/repackage
mkdir -p %buildroot%__localstatedir/lib/rpm
for dbi in \
    Basenames Conflictname Dirnames Group Installtid Name Packages \
    Providename Provideversion Requirename Requireversion Triggername \
    Filemd5s Pubkeys Sha1header Sigmd5 \
    __db.001 __db.002 __db.003 __db.004 __db.005 __db.006 __db.007 \
    __db.008 __db.009
do
	touch %buildroot%__localstatedir/lib/rpm/$dbi
done

# Fix rpmpopt
ln -s rpmpopt-%rpm_version %buildroot%_rpmlibdir/rpmpopt

# Remove unpackaged files
#
# beecrypt library was linked statically into rpm, we do not need to provide it
rm -r %buildroot%__includedir/beecrypt
rm %buildroot%__libdir/libbeecrypt.*
# these scripts have nothing to do in Owl
rm %buildroot%_rpmlibdir/{Specfile.pm,cpanflute*,rpmdiff*,sql*,tcl*,trpm}
# unneeded crontab, logrotate config, xinetd config
rm %buildroot%_rpmlibdir/rpm.{daily,log,xinetd}
# outdated man pages
rm -r %buildroot%__mandir/{fr,ja,ko,pl,ru,sk}
# .la files
rm %buildroot%__libdir/*.la

# XXX: glibc 2.3.2 update -- this file isn't created
#rm %buildroot%__datadir/locale/locale.alias

install -p -m 755 %_sourcedir/rpminit %buildroot%__bindir/
install -p -m 644 %_sourcedir/rpminit.1 %buildroot%__mandir/man1/
install -p -m 644 %_sourcedir/configure-presets %buildroot%__bindir/

echo "%%defattr(-,root,root)"
platforms="`echo %buildroot%_rpmlibdir/*/macros | sed 's#/macros##g; s#%buildroot%__prefix/lib/##g'`"
for platform in $platforms; do
	echo "%%attr(0755,root,root) %%dir %__prefix/lib/$platform" >> platforms.list
	echo "%%attr(0644,root,root) %%verify(not md5 size mtime) %%config(missingok,noreplace) %__prefix/lib/$platform/macros" >> platforms.list
done

%pre
if [ -f /var/lib/rpm/packages.rpm ]; then
	if [ -f /var/lib/rpm/Packages ]; then
		cat << EOF
You have both /var/lib/rpm/packages.rpm	(db1 format installed packages
headers) and /var/lib/rpm/Packages (db3 format installed package headers).
Let's try to determine which one of these is in use...

EOF

		if [ /var/lib/rpm/Packages -ot /var/lib/rpm/packages.rpm ]; then
			cat << EOF
/var/lib/rpm/Packages is older than /var/lib/rpm/packages.rpm.  We cannot
determine which of these databases is actual.  Please remove (or at least
rename) one of these files, then try installing this package again.
EOF
			exit 1
		fi

		cat << EOF
/var/lib/rpm/Packages is newer than /var/lib/rpm/packages.rpm, perhaps
we've converted db1 format database to db3 format and then proceeded to
use the db3 one.  You'll need to remove the db1 format database files
(/var/lib/rpm/*.rpm) once installation completes.

Install will continue in 10 seconds...
EOF
		sleep 10
	else
		cat << EOF
The old RPM database (db1 format) was found.  Unfortunately, we cannot
automatically convert this database during installation of this
package due to a "chicken and egg" problem.  To convert old RPM database
to the new database format extract "rpmd" binary from this package and
run "rpmd --rebuilddb" manually.
EOF
		exit 1
	fi
fi

%post
/sbin/ldconfig

if [ ! -e %__sysconfdir/rpm/macros -a -e %__sysconfdir/rpmrc -a \
    -f %_rpmlibdir/convertrpmrc.sh ]; then
	sh %_rpmlibdir/convertrpmrc.sh &> /dev/null
fi

# ToDo: (GM): It is good to run "rpmd --rebuilddb" after upgrading rpm, but
# it is not so trivial. Rebuild process has to start _after_ this package is
# installed, so we will have to hack the installation process. One way to
# do this thing can be seen in ALT Linux's rpm.spec, they fire a special
# helper which waits for main RPM process exit and runs specified program.
# For now, we assume that "make installworld" (Owl installation and upgrade
# procedure) does all the dirty work for us. :)

%postun -p /sbin/ldconfig

%post -n popt -p /sbin/ldconfig
%postun -n popt -p /sbin/ldconfig

%files -f platforms.list
%defattr(-,root,root)
%doc CHANGES.bz2 GROUPS RPM-GPG-KEY RPM-PGP-KEY doc/manual/*
/bin/rpm
%dir %__sysconfdir/rpm
%__bindir/gendiff
%__bindir/rpm2cpio
%__bindir/rpmdb
%__bindir/rpme
%__bindir/rpmi
%__bindir/rpmu
%__bindir/rpmgraph
%__bindir/rpminit
%__bindir/rpmquery
%__bindir/rpmsign
%__bindir/rpmverify
%__libdir/librpm-%rpm_version.so
%__libdir/librpmdb-%rpm_version.so
%__libdir/librpmio-%rpm_version.so
%config %__prefix/lib/rpmpopt
%config %__prefix/lib/rpmrc

%dir %__localstatedir/lib/rpm
%ghost %attr(0644,root,root) %verify(not md5 size mtime) %config(missingok,noreplace) %__localstatedir/lib/rpm/*
%dir %__localstatedir/spool/repackage

%dir %_rpmlibdir
%_rpmlibdir/convertrpmrc.sh
%config(missingok,noreplace) %_rpmlibdir/macros
%_rpmlibdir/rpm2cpio.sh
%_rpmlibdir/rpmcache
%_rpmlibdir/rpmdb*
%_rpmlibdir/rpmd
%_rpmlibdir/rpme
%_rpmlibdir/rpmi
%_rpmlibdir/rpmk
%_rpmlibdir/rpmq
%_rpmlibdir/rpmu
%_rpmlibdir/rpmv
%config %_rpmlibdir/rpmpopt*
%config(noreplace) %_rpmlibdir/rpmrc*
%_rpmlibdir/tgpg
%_rpmlibdir/u_pkg.sh

%__mandir/man1/gendiff.1*
%__mandir/man1/rpminit.1*
%__mandir/man8/rpm.8*
%__mandir/man8/rpm2cpio.8*
%__mandir/man8/rpmcache.8*
%__mandir/man8/rpmgraph.8*

%__datadir/locale/*/LC_MESSAGES/rpm.mo

%files build
%defattr(-,root,root)
%__bindir/configure-presets
%__bindir/rpmbuild
%__libdir/librpmbuild-%rpm_version.so
%_rpmlibdir/brp-*
%_rpmlibdir/check-files
%_rpmlibdir/check-prereqs
%_rpmlibdir/config.*
%_rpmlibdir/cross-build
%_rpmlibdir/debugedit
%_rpmlibdir/find-debuginfo.sh
%_rpmlibdir/find-lang.sh
%_rpmlibdir/find-prov*
%_rpmlibdir/find-req*
%_rpmlibdir/get_magic.pl
%_rpmlibdir/getpo.sh
%_rpmlibdir/*.req
%_rpmlibdir/*.prov
%_rpmlibdir/javadeps
%_rpmlibdir/mkinstalldirs
%_rpmlibdir/perldeps.pl
%_rpmlibdir/rpm[bt]
%_rpmlibdir/rpmdeps
%_rpmlibdir/rpmfile
%_rpmlibdir/vpkg-*.sh
%__mandir/man8/rpmbuild.8*
%__mandir/man8/rpmdeps.8*

%files devel
%defattr(-,root,root)
%__includedir/rpm
%__libdir/librpm*.a
%__libdir/librpm.so
%__libdir/librpmbuild.so
%__libdir/librpmdb.so
%__libdir/librpmio.so

%files -n popt
%defattr(-,root,root)
%__libdir/libpopt.so.*
%__datadir/locale/*/LC_MESSAGES/popt.mo
%__mandir/man3/popt.3*

# XXX These may end up in popt-devel but it hardly seems worth the effort now.
%__libdir/libpopt.a
%__libdir/libpopt.so
%__includedir/popt.h

%changelog
* Fri Nov 27 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl21
- Changed default build architecture on i686+ CPUs to i686.

* Wed Sep 09 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl20
- Implemented automated %%check control using --with/--without
check/test switches.

* Fri Aug 21 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl19
- Predefined a bunch of autoconf variables by sourcing new configure-presets
script in %%___build_pre macro, to harden configure checks for security
sensitive functions, and to speedup configure checks for most popular
functions.
- Fixed gendiff to avoid producing changelog diffs with no context.

* Fri Aug 17 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl18
- Changed rpmbuild to pass --wildcards to tar on build from tarball.

* Sun Nov 19 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl17
- Backported upstream fix for potential heap buffer overflow in
showQueryPackage function (CVE-2006-5466).
- Added x86-64 support to rpminit script.

* Sun May 07 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl16
- Removed unused macros: WITH_INCLUDED_GETTEXT, WITH_API_DOCS, and WITH_BZIP2.
- Added a dependency on the file package to rpm-build (find-provides is
using the file utility).

* Tue Apr 04 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl15
- Backported upstream fix to check-prereqs script.
- Corrected specfile to make it build on x86_64.
- Updated rpmrc optflags for x86_64.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl14
- Compressed CHANGES file.

* Sat Dec 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl13
- Corrected build to generate proper values for %%_host, %%_host_alias,
%%_host_cpu and %%_host_vendor macros.

* Wed Dec 21 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl12
- Fixed build to avoid linking of librpmbuild with system librpm.

* Fri Nov 18 2005 Solar Designer <solar-at-owl.openwall.com> 4.2-owl11
- Added public domain statements to the rpminit script and its man page.

* Sat Nov 05 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl10
- Fixed macro files which appeared to be incomplete due to outdated
vendor autodetection code in configure scripts.

* Mon Oct 17 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl9
- Backported fix to nested %if handling.
- Changed package upgrade algorithm to remove old files
on "-U --force" even if package versions match.
- When comparing package versions on -U or -F, take build dates
into account.
- Set umask 022 for install scripts and triggers execution.
- Build debugedit utility with system libelf.
- Applied sparc optflags update from Alexandr Kanevskiy.

* Fri Sep 23 2005 Michail Litvak <mci-at-owl.openwall.com> 4.2-owl8
- Don't package .la files.

* Sat Jun 25 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl7
- Do not use system's libelf even if the library is available during build.

* Sat Apr 02 2005 Solar Designer <solar-at-owl.openwall.com> 4.2-owl6
- Allow unpackaged files and missing docs by default for building legacy
third-party packages (our build environment overrides this for native ones).
- Re-implemented the gendiff script.

* Tue Mar 22 2005 Solar Designer <solar-at-owl.openwall.com> 4.2-owl5
- Updated the default rpmrc to use -march/-mtune as required for gcc 3.4.3+
and to use -pipe with all supported archs.

* Sun Mar 20 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl4
- Fixed a bug with creating and packaging /var/lib/lib/rpm.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl3
- Applied rpmal-bounds patch to avoid going out of array bounds in the
dependency checker.

* Sun Dec 26 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl2
- Applied chroot-ugid patch to not rely on host OS provided NSS modules.

* Tue Nov 02 2004 Solar Designer <solar-at-owl.openwall.com> 4.2-owl1
- Corrected the long text messages for consistency with owl-etc.
- Set Release to -owl1 such that we can make this public.

* Wed Sep 29 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.18
- Added db1 format support into rpmdb
- Fixed configure.ac to use proper AC_CONFIG_HEADERS syntax
- Removed "create" from __dbi_cdb definition in macros.in, because it breaks upgrade logic
- Modified %%pre section to be more friendly to end-user

* Mon May 05 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.17
- Finally fixed the problem with db environment opens inside & outside chroot.

* Mon Mar 22 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.16
- Quick and dirty fix for the problem with installing into a chroot jail
from read-only filesystem. (Discovered by Solar Designer)

* Fri Mar 19 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.15
- Fixed problem during package upgrade with Obsoletes tag pointed to
not installed package
- Removed unneeded PreReqs, added necessary Requires

* Thu Mar 11 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.14
- Fixed permissions during install of packages. Not explictly included
directories (that is, those in the middle of an included pathname) will be
created with mode 755, all files will be created with mode 600 and then
chmod'ed to the specified access rights.

* Wed Mar 10 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.13
- Minor changes to the spec file (exporting CFLAGS, making sure that any
passed value of CFLAGS gets into compilation process).

* Thu Mar 04 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.12
- Changed type of rpmError for errors during opening of /etc/mtab from error
to debug.
- Modified version of Owl RPM3 closeall patch added
- Modified version of Owl RPM3 gendiff patch added
- Regenerated Owl RPM3 patches: autodeps-symbol-versioning, autoreq,
buildhost, popt-sgid, rpmrc
- Added vendor-setup patch to setup our environment (compatible with RH)

* Wed Mar 03 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.11
- Added missing --enable-posixmutexes option to configure

* Fri Feb 20 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.10
- Removed unnecessary verify prefix from rpmmacros and rpmpopt
- Applied style corrections as described by Solar Designer

* Mon Feb 16 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.9
- It seems to be first fully working version of this package and drop-in
replacement for rpm 3.0.6 (except upgrade procedure)
- Applied patch to ignore umask and follow the logical behavior of honoring
permissions settings in the macros.

* Fri Feb 13 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.8
- Fixed issue with platforms directories

* Thu Feb 12 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.7
- Changed macros file to use external dependency generator (internal one
is very ugly :( )
- Minor changes in %_libdir/rpm directory

* Wed Feb 11 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.6
- Fixed brp- scripts

* Tue Feb 10 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.5
- Cleaned up the spec file (to use macros in file sections)
- Added %%config to configuration files
- Fixed permissions on platform directories under %__libdir/rpm/

* Mon Feb 09 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.4
- Making only libelf.a from elfutils, not 'make all' in libelf subdirectory
- Removed dependency on gcc3+ and binutils 2.14.90+

* Thu Feb 05 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.3
- Tested building of this package under rpm 3.0.6 and rebuilding under
rpm 4.2
- Added -DMAGIC option to CFLAGS for configure in file subdirectory to
hardcode correct path to file's magic database in /usr/share
- Linked rpmq, rpmv and rpmdeps to static librpmbuild to avoid rpm-build
dependency from rpm
- Added missing rpmrc, rpmdeps

* Wed Feb 04 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.2
- Moved compilation of libelf.a, libfmagic.so to prep and removed
source trees for elfutils and file (Hope, someday we will package
them independently).
- Solved problem with linking librpm.so.0 into librpmbuild if we're
building on a system with installed rpm 3.x

* Tue Feb 03 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.1
- Updated to version 4.2
- Spec file was heavily reviewed

* Fri Jan 16 2004 Michail Litvak <mci-at-owl.openwall.com> 3.0.6-owl11
- Make /usr/lib/rpm directory owned by this package.

* Fri Dec 12 2003 Solar Designer <solar-at-owl.openwall.com> 3.0.6-owl10
- In brp-strip*, use sed expressions which allow SUID/SGID binaries to get
stripped.

* Sun Dec 07 2003 Solar Designer <solar-at-owl.openwall.com> 3.0.6-owl9
- Don't use a file under /tmp in installplatform script used during builds,
spotted by (GalaxyMaster).

* Tue May 27 2003 Solar Designer <solar-at-owl.openwall.com> 3.0.6-owl8
- Obey AutoReq: false also for dependency on the shell with triggers.

* Thu May 15 2003 Solar Designer <solar-at-owl.openwall.com> 3.0.6-owl7
- Don't call gzerror() after gzclose(), patch from Dmitry V. Levin.

* Wed Apr 30 2003 Solar Designer <solar-at-owl.openwall.com> 3.0.6-owl6
- In popt, handle uses from SGID apps in the same way as from SUID ones.

* Sun Feb 23 2003 Michail Litvak <mci-at-owl.openwall.com>
- Fixed misplaced semicolon in /usr/lib/rpm/macros file
  (Thanks to Oleg Lukashin)

* Fri Jan 17 2003 Solar Designer <solar-at-owl.openwall.com>
- In find-requires, support symbol versioning with package dependencies
for libraries other than glibc (from Dmitry V. Levin of ALT Linux).

* Tue Dec 17 2002 Solar Designer <solar-at-owl.openwall.com>
- Added rpminit, a script to create private RPM package build directories,
and its man page.
- Changed the default rpmrc to use more optimal optflags for our gcc (note
that builds of Owl itself use a different set of optflags anyway).

* Sun Mar 03 2002 Solar Designer <solar-at-owl.openwall.com>
- Support setting the BuildHost tag explicitly rather than only from what
the kernel thinks the system's hostname is.
- Don't package vpkg-provides* (temporary file handling issues, non-Linux).
- Don't package rpmgettext/rpmputtext because of poor quality and no uses
by RPM itself.

* Wed Feb 06 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Jun 12 2001 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- update to 3.0.6 release

* Thu Nov 30 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- disable /usr/src/RPM for security reasons

* Sun Nov 19 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- gendiff fix

* Sun Nov 12 2000 Solar Designer <solar-at-owl.openwall.com>
- Added missing #include's to lib/rpmio.c (it wouldn't build with a
sparc64 kernel).

* Fri Oct 20 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- disabled /usr/share/man autodetection

* Sun Sep 03 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- vendor fix
- FHS
- closeall security fix
- RH 6.2 updates merge

* Sat Aug 05 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- change build target
- /usr/src/redhat -> /usr/src/RPM

* Thu Jul 20 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from official RPM team test rpm.
- disable Python module

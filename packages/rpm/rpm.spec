# $Id: Owl/packages/rpm/rpm.spec,v 1.44 2004/12/26 13:58:48 galaxy Exp $

%define WITH_PYTHON 0
%define WITH_API_DOCS 0
%define WITH_BZIP2 0
%define WITH_INCLUDED_GETTEXT 0

%define rpm_version 4.2
%define popt_version 1.8

Summary: The Red Hat package management system.
Name: rpm
Version: %rpm_version
Release: owl2
License: GPL
Group: System Environment/Base
Source0: ftp://ftp.rpm.org/pub/rpm/dist/rpm-4.2.x/rpm-%version.tar.gz
Source1: rpminit
Source2: rpminit.1
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
Patch13: rpm-4.2-owl-gendiff.diff
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
Patch29: rpm-4.2-owl-chroot_ugid.diff

PreReq: /sbin/ldconfig
PreReq: sh-utils, fileutils, mktemp, gawk
Requires: findutils, diffutils, gzip
BuildRequires: libtool >= 1.5.2, automake >= 1.8.3, autoconf >= 2.59
BuildRequires: gettext >= 0.14.1
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
%patch13 -p1
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

# Prepare libelf archive and save it with headers to the tools subdirectory
pushd elfutils
export CFLAGS="${CFLAGS:-%optflags}"
./configure
%__make AM_CFLAGS="$CFLAGS" -C libelf libelf.a
cp -p libelf/{libelf.a,libelf.h,gelf.h,elf.h} libdwarf/dwarf.h ../tools/
popd
rm -r elfutils

# Prepare libfmagic archive and save it to the rpmio subdirectory.
# Also, put patchlevel.h to the tools directory (it is needed by rpmfile.c)
pushd file
# We add -DMAGIC=path to configure to make sure that default magic file will
# be searched for in the directory where "file" package stores it (this will
# be unneeded once we seperate "file" from "rpm")
export CFLAGS="$CFLAGS -DMAGIC='\"/usr/share/magic\"'"
./configure
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

%define _lib             lib
%define __share          /share
%define __prefix         %__usr
%define __exec_prefix    %__prefix
%define __bindir         %__exec_prefix/bin
%define __sbindir        %__exec_prefix/sbin
%define __libexecdir     %__exec_prefix/%_lib
%define __datadir        %__prefix/share
%define __sysconfdir     /etc
%define __sharedstatedir %__prefix/com
%define __localstatedir  %__var/%_lib
%define __libdir         %__exec_prefix/%_lib
%define __includedir     %__prefix/include
%define __oldincludedir  /usr/include
%define __infodir        %__datadir/info
%define __mandir         %__datadir/man

%build
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
./configure \
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

%install
rm -rf %buildroot

%__make DESTDIR="%buildroot" install

mkdir -p %buildroot%__sysconfdir/rpm
mkdir -p %buildroot%__localstatedir/spool/repackage
mkdir -p %buildroot%__localstatedir/%_lib/rpm
for dbi in \
    Basenames Conflictname Dirnames Group Installtid Name Packages \
    Providename Provideversion Requirename Requireversion Triggername \
    Filemd5s Pubkeys Sha1header Sigmd5 \
    __db.001 __db.002 __db.003 __db.004 __db.005 __db.006 __db.007 \
    __db.008 __db.009
do
	touch %buildroot%__localstatedir/%_lib/rpm/$dbi
done

# Fix rpmpopt
ln -s rpmpopt-%rpm_version %buildroot%__libdir/rpm/rpmpopt

# Remove unpackaged files
#
# beecrypt library was linked statically into rpm, we do not need to provide it
rm -r %buildroot%__includedir/beecrypt
rm %buildroot%__libdir/libbeecrypt.*
# these scripts have nothing to do in Owl
rm %buildroot%__libdir/rpm/{Specfile.pm,cpanflute*,rpmdiff*,sql*,tcl*,trpm}
# unneeded crontab, logrotate config, xinetd config
rm %buildroot%__libdir/rpm/rpm.{daily,log,xinetd}
# outdated man pages
rm -r %buildroot%__mandir/{fr,ja,ko,pl,ru,sk}

# XXX: glibc 2.3.2 update -- this file isn't created
#rm %buildroot%__datadir/locale/locale.alias

install -p -m 755 $RPM_SOURCE_DIR/rpminit %buildroot%__bindir/
install -p -m 644 $RPM_SOURCE_DIR/rpminit.1 %buildroot%__mandir/man1/

echo "%defattr(-,root,root)"
platforms="`echo %buildroot%__libdir/rpm/*/macros | sed -e 's#/macros##g; s#%buildroot%__libdir/##g'`"
for platform in $platforms; do
	echo "%attr(0755,root,root) %dir %__libdir/$platform" >> platforms.list
	echo "%attr(0644,root,root) %verify(not md5 size mtime) %config(missingok,noreplace) %__libdir/$platform/macros" >> platforms.list
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
    -f %__libdir/rpm/convertrpmrc.sh ]; then
	sh %__libdir/rpm/convertrpmrc.sh &> /dev/null
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
%doc RPM-PGP-KEY RPM-GPG-KEY CHANGES GROUPS doc/manual/*
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
%config %__libdir/rpmpopt
%config %__libdir/rpmrc

%dir %__localstatedir/%_lib/rpm
%ghost %attr(0644,root,root) %verify(not md5 size mtime) %config(missingok,noreplace) %__localstatedir/%_lib/rpm/*
%dir %__localstatedir/spool/repackage

%dir %__libdir/rpm
%__libdir/rpm/convertrpmrc.sh
%config(missingok,noreplace) %__libdir/rpm/macros
%__libdir/rpm/rpm2cpio.sh
%__libdir/rpm/rpmcache
%__libdir/rpm/rpmdb*
%__libdir/rpm/rpmd
%__libdir/rpm/rpme
%__libdir/rpm/rpmi
%__libdir/rpm/rpmk
%__libdir/rpm/rpmq
%__libdir/rpm/rpmu
%__libdir/rpm/rpmv
%config %__libdir/rpm/rpmpopt*
%config(noreplace) %__libdir/rpm/rpmrc*
%__libdir/rpm/tgpg
%__libdir/rpm/u_pkg.sh

%__mandir/man1/gendiff.1*
%__mandir/man1/rpminit.1*
%__mandir/man8/rpm.8*
%__mandir/man8/rpm2cpio.8*
%__mandir/man8/rpmcache.8*
%__mandir/man8/rpmgraph.8*

%__datadir/locale/*/LC_MESSAGES/rpm.mo

%files build
%defattr(-,root,root)
%__bindir/rpmbuild
%__libdir/librpmbuild-%rpm_version.so
%__libdir/rpm/brp-*
%__libdir/rpm/check-files
%__libdir/rpm/check-prereqs
%__libdir/rpm/config.*
%__libdir/rpm/cross-build
%__libdir/rpm/debugedit
%__libdir/rpm/find-debuginfo.sh
%__libdir/rpm/find-lang.sh
%__libdir/rpm/find-prov*
%__libdir/rpm/find-req*
%__libdir/rpm/get_magic.pl
%__libdir/rpm/getpo.sh
%__libdir/rpm/*.req
%__libdir/rpm/*.prov
%__libdir/rpm/javadeps
%__libdir/rpm/mkinstalldirs
%__libdir/rpm/perldeps.pl
%__libdir/rpm/rpm[bt]
%__libdir/rpm/rpmdeps
%__libdir/rpm/rpmfile
%__libdir/rpm/vpkg-*.sh
%__mandir/man8/rpmbuild.8*
%__mandir/man8/rpmdeps.8*

%files devel
%defattr(-,root,root)
%__includedir/rpm
%__libdir/librpm*.*a
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
%__libdir/libpopt.*a
%__libdir/libpopt.so
%__includedir/popt.h

%changelog
* Sun Dec 26 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl2
- Applied chroot_ugid patch to not rely on host OS provided NSS modules.

* Tue Nov 02 2004 Solar Designer <solar@owl.openwall.com> 4.2-owl1
- Corrected the long text messages for consistency with owl-etc.
- Set Release to -owl1 such that we can make this public.

* Wed Sep 29 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.18
- Added db1 format support into rpmdb
- Fixed configure.ac to use proper AC_CONFIG_HEADERS syntax
- Removed "create" from __dbi_cdb definition in macros.in, because it breaks upgrade logic
- Modified %%pre section to be more friendly to end-user

* Mon May 05 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.17
- Finally fixed the problem with db environment opens inside & outside chroot.

* Mon Mar 22 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.16
- Quick and dirty fix for the problem with installing into a chroot jail
from read-only filesystem. (Discovered by Solar Designer)

* Fri Mar 19 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.15
- Fixed problem during package upgrade with Obsoletes tag pointed to
not installed package
- Removed unneeded PreReqs, added necessary Requires

* Thu Mar 11 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.14
- Fixed permissions during install of packages. Not explictly included
directories (that is, those in the middle of an included pathname) will be
created with mode 755, all files will be created with mode 600 and then
chmod'ed to the specified access rights.

* Wed Mar 10 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.13
- Minor changes to the spec file (exporting CFLAGS, making sure that any
passed value of CFLAGS gets into compilation process).

* Thu Mar 04 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.12
- Changed type of rpmError for errors during opening of /etc/mtab from error
to debug.
- Modified version of Owl RPM3 closeall patch added
- Modified version of Owl RPM3 gendiff patch added
- Regenerated Owl RPM3 patches: autodeps-symbol-versioning, autoreq,
buildhost, popt-sgid, rpmrc
- Added vendor-setup patch to setup our environment (compatible with RH)

* Wed Mar 03 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.11
- Added missing --enable-posixmutexes option to configure

* Fri Feb 20 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.10
- Removed unnecessary verify prefix from rpmmacros and rpmpopt
- Applied style corrections as described by Solar Designer

* Mon Feb 16 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.9
- It seems to be first fully working version of this package and drop-in
replacement for rpm 3.0.6 (except upgrade procedure)
- Applied patch to ignore umask and follow the logical behavior of honoring
permissions settings in the macros.

* Fri Feb 13 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.8
- Fixed issue with platforms directories

* Thu Feb 12 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.7
- Changed macros file to use external dependency generator (internal one
is very ugly :( )
- Minor changes in %_libdir/rpm directory

* Wed Feb 11 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.6
- Fixed brp- scripts

* Tue Feb 10 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.5
- Cleaned up the spec file (to use macros in file sections)
- Added %config to configuration files
- Fixed permissions on platform directories under %__libdir/rpm/

* Mon Feb 09 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.4
- Making only libelf.a from elfutils, not 'make all' in libelf subdirectory
- Removed dependency on gcc3+ and binutils 2.14.90+

* Thu Feb 05 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.3
- Tested building of this package under rpm 3.0.6 and rebuilding under
rpm 4.2
- Added -DMAGIC option to CFLAGS for configure in file subdirectory to
hardcode correct path to file's magic database in /usr/share
- Linked rpmq, rpmv and rpmdeps to static librpmbuild to avoid rpm-build
dependency from rpm
- Added missing rpmrc, rpmdeps

* Wed Feb 04 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.2
- Moved compilation of libelf.a, libfmagic.so to prep and removed
source trees for elfutils and file (Hope, someday we will package
them independently).
- Solved problem with linking librpm.so.0 into librpmbuild if we're
building on a system with installed rpm 3.x

* Tue Feb 03 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl0.1
- Updated to version 4.2
- Spec file was heavily reviewed

* Fri Jan 16 2004 Michail Litvak <mci@owl.openwall.com> 3.0.6-owl11
- Make /usr/lib/rpm directory owned by this package.

* Fri Dec 12 2003 Solar Designer <solar@owl.openwall.com> 3.0.6-owl10
- In brp-strip*, use sed expressions which allow SUID/SGID binaries to get
stripped.

* Sun Dec 07 2003 Solar Designer <solar@owl.openwall.com> 3.0.6-owl9
- Don't use a file under /tmp in installplatform script used during builds,
spotted by (GalaxyMaster).

* Tue May 27 2003 Solar Designer <solar@owl.openwall.com> 3.0.6-owl8
- Obey AutoReq: false also for dependency on the shell with triggers.

* Thu May 15 2003 Solar Designer <solar@owl.openwall.com> 3.0.6-owl7
- Don't call gzerror() after gzclose(), patch from Dmitry V. Levin.

* Wed Apr 30 2003 Solar Designer <solar@owl.openwall.com> 3.0.6-owl6
- In popt, handle uses from SGID apps in the same way as from SUID ones.

* Sun Feb 23 2003 Michail Litvak <mci@owl.openwall.com>
- Fixed misplaced semicolon in /usr/lib/rpm/macros file
  (Thanks to Oleg Lukashin)

* Fri Jan 17 2003 Solar Designer <solar@owl.openwall.com>
- In find-requires, support symbol versioning with package dependencies
for libraries other than glibc (from Dmitry V. Levin of ALT Linux).

* Tue Dec 17 2002 Solar Designer <solar@owl.openwall.com>
- Added rpminit, a script to create private RPM package build directories,
and its man page.
- Changed the default rpmrc to use more optimal optflags for our gcc (note
that builds of Owl itself use a different set of optflags anyway).

* Sun Mar 03 2002 Solar Designer <solar@owl.openwall.com>
- Support setting the BuildHost tag explicitly rather than only from what
the kernel thinks the system's hostname is.
- Don't package vpkg-provides* (temporary file handling issues, non-Linux).
- Don't package rpmgettext/rpmputtext because of poor quality and no uses
by RPM itself.

* Wed Feb 06 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Jun 12 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- update to 3.0.6 release

* Thu Nov 30 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- disable /usr/src/RPM for security reasons

* Sun Nov 19 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- gendiff fix

* Sun Nov 12 2000 Solar Designer <solar@owl.openwall.com>
- Added missing #include's to lib/rpmio.c (it wouldn't build with a
sparc64 kernel).

* Fri Oct 20 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- disabled /usr/share/man autodetection

* Sun Sep 03 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- vendor fix
- FHS
- closeall security fix
- RH 6.2 updates merge

* Sat Aug 05 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- change build target
- /usr/src/redhat -> /usr/src/RPM

* Thu Jul 20 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from official RPM team test rpm.
- disable Python module

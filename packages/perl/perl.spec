# $Owl: Owl/packages/perl/perl.spec,v 1.50 2006/05/07 04:05:23 galaxy Exp $

%define BUILD_PH 1
%define BUILD_PH_ALL 0

# This controls whether to build/package suidperl.  Your possible use of
# this is at your own risk, -- we do not officially support suidperl.
%define BUILD_SUIDPERL 0

# Build perl with threads support.
%define BUILD_THREADS 1

# Build perl with large files support.
%define BUILD_LARGEFILES 1

# Build a shared library of perl.  For example, this is needed for PostgreSQL
# to use perl as a procedural language.
%define BUILD_DSO_PERL 0

# Whether or not to run tests after build.
%define BUILD_TEST 1

# Set this if you might be running kernel with enabled "Destroy shared
# memory segments not in use" (CONFIG_HARDEN_SHM) configuration option.
%define KERNEL_CONFIG_HARDEN_SHM 1

Summary: The Perl programming language.
Name: perl
Version: 5.8.8
Release: owl1
Epoch: 4
License: GPL
Group: Development/Languages
Source: ftp://ftp.perl.org/pub/CPAN/src/perl-%version.tar.bz2
Patch0: perl-5.8.3-owl-disable-suidperl.diff
Patch1: perl-5.8.8-owl-tmp.diff
Patch2: perl-5.8.3-owl-vitmp.diff
Patch3: perl-5.8.8-owl-CPAN-tools.diff
%if %KERNEL_CONFIG_HARDEN_SHM
Patch10: perl-5.8.8-owl-tests-shm.diff
%endif
Patch20: perl-5.8.8-alt-AnyDBM_File-DB_File.diff
Patch21: perl-5.8.8-alt-MM-uninst.diff
Patch22: perl-5.8.3-alt-deb-perldoc-INC.diff
Patch23: perl-5.8.3-rh-lpthread.diff
Patch24: perl-5.8.3-alt-configure-no-perl.diff
Patch25: perl-5.8.6-alt-File-Copy-preserve.diff
Patch26: perl-5.8.6-alt-pod-vendor-dirs-perlbug34500.diff
Provides: perl(:WITH_PERLIO)
%if %BUILD_THREADS
%define thread_arch -thread-multi
Provides: perl(:WITH_ITHREADS)
Provides: perl(:WITH_THREADS)
%else
%define thread_arch %nil
Provides: perl(:WITHOUT_ITHREADS)
Provides: perl(:WITHOUT_THREADS)
%endif
%if %BUILD_LARGEFILES
Provides: perl(:WITH_LARGEFILES)
%else
Provides: perl(:WITHOUT_LARGEFILES)
%endif
# self requirements which were not detected by our find-provides
Provides: perl(Carp::Heavy), perl(getopts.pl)
Obsoletes: perl-MD5
BuildRequires: gdbm-devel, db4-devel >= 4.3.29, gawk, grep
BuildRequires: rpm >= 4.0.5
BuildRoot: /override/%name-%version

%description
Perl is a high-level programming language with roots in C, sed, awk
and shell scripting.  Perl is good at handling processes and files,
and is especially good at handling text.  Perl's hallmarks are
practicality and efficiency.  While it is used to do a lot of
different things, Perl's most common applications are system
administration utilities and web programming.  A large proportion of
the CGI scripts on the web are written in Perl.  You need the Perl
package installed on your system so that your system can handle Perl
scripts.

%if %BUILD_SUIDPERL
%package suidperl
Summary: Privileged Perl wrapper to support SUID/SGID Perl scripts.
Group: Development/Languages
Requires: %name = %epoch:%version-%release

%description suidperl
This package contains a SUID root Perl executable that is used to handle
SUID/SGID Perl scripts.  An attempt has been made by the Perl developers
to make suidperl safe to be installed on a system and to permit for safe
operation of SUID/SGID Perl scripts.  In reality, however, due to the
complexity of Perl, it is almost certain that the use of SUID/SGID Perl
scripts and possibly even mere installation of suidperl on a system will
introduce security holes.
%endif

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%if %KERNEL_CONFIG_HARDEN_SHM
%patch10 -p1
%endif
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1

find . -name '*.orig' -delete

# Remove files with known temporary file handling issues that we don't
# package or use anyway.
REMOVE_FILES='INSTALL makeaperl.SH perly.fixer ext/SDBM_File/sdbm/grind'
chmod u+w $REMOVE_FILES
rm $REMOVE_FILES
mv MANIFEST MANIFEST.orig
for f in $REMOVE_FILES; do
	echo "^${f}[[:space:]]"
done | sed 's/\./\\./' | grep -vEf - MANIFEST.orig > MANIFEST
# Satisfy a make dependency
touch makeaperl.SH

# Correct library search paths
if [ %_lib != lib ]; then
	sed -i ': start ; s,\([[:space:]"]\(/usr\(/local\)\?\)\?\)/lib\([[:space:]"]\),\1/%_lib\4,g ; t start' Configure
fi

# Perl5 always installs itself to %_prefix/lib/perl5 (fix for x86_64 builds)
%define _libdir %_prefix/lib/perl5

cat > filter_depends.sh <<EOF
#!/bin/sh
%__find_requires $* | grep -vE '(NDBM|perl\(v5\.8\.8\)|perl\(Mac::|perl\(Tk|perl\(VMS::|perl\(FCGI\))'
EOF
chmod +x filter_depends.sh

%define __find_requires	%_builddir/%name-%version/filter_depends.sh

# if we ain't run from 'make buildworld' the buildhost macro is undefined
%{expand: %%define buildhost %{?buildhost:%buildhost}%{?!buildhost:localhost}}

%build
rm -rf %buildroot
%_buildshell Configure \
	-des \
	-O \
	-Dmyuname="`uname -mrs`" \
	-Dnewmyuname="`uname -mrs`" \
	-Dmyhostname=%buildhost \
	-Doptimize="%optflags" \
	-Dcc='%__cc' \
	-Dcccdlflags='-fPIC' \
	-Dinstallprefix=%buildroot%_prefix \
	-Dprefix=%_prefix \
	-Darchname=%_arch-%_os \
	-Dvendorprefix=%_prefix \
	-Dsiteprefix=%_prefix \
	-Dotherlibdirs=%_libdir/%version \
%if %BUILD_SUIDPERL
	-Dd_dosuid \
%else
	-Ud_dosuid \
%endif
%ifarch sparc sparcv9
	-Ud_longdbl \
%endif
	-Dd_semctl_semun \
	-Di_db \
	-Di_ndbm \
	-Di_gdbm \
	-Di_shadow \
	-Dman1dir=%_mandir/man1 \
	-Dman3dir=%_mandir/man3 \
	-Dman3ext=3pm \
%if %BUILD_THREADS
	-Dusethreads \
	-Duseithreads \
%else
	-Uusethreads \
	-Uuseithreads \
%endif
%if %BUILD_LARGEFILES
	-Duselargefiles \
%else
	-Uuselargefiles \
%endif
%if %BUILD_DSO_PERL
	-Duseshrplib \
%else
	-Uuseshrplib \
%endif
	-Uversiononly \
	-Dinc_version_list='5.8.0/%_arch-%_os%thread_arch 5.8.0'

%__make

%if %BUILD_TEST
# Some of the tests might require network access.
%__make test
%endif

%install
rm -rf %buildroot
%__make install
%__mkdir_p %buildroot%_bindir
%__install -m 755 utils/pl2pm %buildroot%_bindir/

%if %BUILD_PH
# Generate *.ph files with a trick.  Is this sick or what?
#
# It is non-obvious whether there's any need to process this many header
# files, especially given that due to a bug on Red Hat Linux only the kernel
# headers were actually processed.  Which means that we don't have to keep
# the whole list for compatibility.  ALT Linux are using just glibc-devel.
#
# It also is non-obvious whether any of this needs to be done during the
# package build at all.

# h2ph happens to overflow an 8 MB stack on Alpha.
ulimit -s 16384

%__make all -f - <<EOF
%if %BUILD_PH_ALL
PKGS	= \$(shell rpm -qa | sed -n 's/\(^.*-devel\)-[0-9.]\+-owl[0-9]\+\$$/\1/p' | sort) \
	  binutils popt
STDH	= \$(filter %_includedir/%%.h, \$(shell rpm -ql \$(PKGS); echo %_includedir/{linux,asm*,scsi}/*.h))
%else
PKGS	= glibc-devel
STDH	= \$(filter %_includedir/%%.h, \$(shell rpm -ql \$(PKGS); echo %_includedir/{linux,asm*}/*.h))
%endif
GCCDIR	= \$(shell gcc --print-file-name include)
GCCH	= \$(filter \$(GCCDIR)/%%.h, \$(shell rpm -ql gcc))

PERLLIB = %buildroot%_libdir/%version
PERL	= %{?BUILD_DSO_PERL:LD_LIBRARY_PATH=\$(PERLLIB)/%_arch-%_os%thread_arch/CORE} PERL5LIB=\$(PERLLIB) %buildroot%_bindir/perl
PHDIR	= \$(PERLLIB)/%_arch-%_os%thread_arch
H2PH	= \$(PERL) %buildroot%_bindir/h2ph -d \$(PHDIR)/

all: std-headers gcc-headers fix-config

std-headers: \$(STDH)
	# PKGS=\$(PKGS)
	# STDH=\$(STDH)
	# H2PH=\$(H2PH)
	cd %_includedir && \$(H2PH) \$(STDH:%_includedir/%%=%%)

gcc-headers: \$(GCCH)
	cd \$(GCCDIR) && \$(H2PH) \$(GCCH:\$(GCCDIR)/%%=%%)

fix-config: \$(PHDIR)/Config.pm
	\$(PERL) -i -p -e "s|%buildroot||g;" \$<
EOF
%endif

# Don't leak information specific to the build system.
# "-f" here because compile.ph appeared here only when we have
# compiled kernel source tree in system.
rm -f %buildroot%_libdir/%version/%_arch-%_os%thread_arch/linux/compile.ph

# Fix the rest of the stuff
find %buildroot%_libdir -name .packlist -o -name perllocal.pod | \
	xargs sed -i 's|%buildroot||g' $packlist

chmod -R u+w %buildroot

%files
%defattr(-,root,root)
%doc Artistic Copying AUTHORS README README.Y2K
%_mandir/*/*
%_libdir
%if !%BUILD_SUIDPERL
%_bindir/*
%else
%_bindir/[^s]*
%_bindir/s2p
%_bindir/splain

%files suidperl
%attr(4711,root,root) %_bindir/sperl%version
%attr(4711,root,root) %_bindir/suidperl
%endif

%changelog
* Sat May 06 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4:5.8.8-owl1
- Fixed perlio.c to use TMPDIR.
- Enabled tests.

* Fri May 05 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4:5.8.8-owl0
- Updated to 5.8.8.
- Introduced the BUILD_DSO_PERL macro to enable/disable building of
libperl.so.
- Removed redundant Provides added at 1:5.8.3-owl2, they were added in RHL
due to their inefficient find-provides script (we have no such limitation).
- Added links and lftp to the CPAN module since lynx is somewhat obsoleted
and we don't package ncftp*.
- Imported a few patches from ALT: disabling perl detection in Configure,
preserving file attributes and timestamps in FileCopy, and searching for
PODs in vendor directories.

* Fri Apr 07 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3:5.8.3-owl13
- Corrected specfile to make it build on x86_64.
- Rebuilt with libdb-4.3.so.

* Thu Jan 12 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3:5.8.3-owl12
- Added several provides for FC and RHEL compatibility.

* Sat Dec 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3:5.8.3-owl11
- Rebuilt with libdb-4.2.so.

* Thu Dec 22 2005 Solar Designer <solar-at-owl.openwall.com> 3:5.8.3-owl10
- Increase the stack size rlimit to 16 MB before h2ph invocations since
h2ph happens to overflow an 8 MB stack on Alpha.

* Wed Dec 21 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3:5.8.3-owl9
- Bumped the Epoch to 3 for FC and RHEL compatibility.
- Updated Sys::Syslog to version 0.08.

* Sun Dec 11 2005 Solar Designer <solar-at-owl.openwall.com> 2:5.8.3-owl8
- Corrected the perl5db.pl patch to obtain the TTY name from ~/.perldbtty$$
rather than from a file under /var/run to allow ordinary users to utilize
that method of notifying Term::Rendezvous of a TTY (patch from David
Eisenstein of Fedora Legacy project).

* Tue Dec 06 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2:5.8.3-owl7
- Backported upstream fix for a potential integer overflow in format
string functionality (CVE-2005-3962).

* Thu Nov 10 2005 Solar Designer <solar-at-owl.openwall.com> 2:5.8.3-owl6
- Corrected the removal of "$SAFEDIR/a.out" in c2ph.PL (fix from Fedora Legacy
pointed out by Pekka Savola).

* Sat Nov 05 2005 Solar Designer <solar-at-owl.openwall.com> 2:5.8.3-owl5
- Bumped the Epoch to 2 for Fedora and RHEL compatibility.

* Sun Feb 06 2005 Solar Designer <solar-at-owl.openwall.com> 1:5.8.3-owl4
- File::Path::rmtree and suidperl PERLIO_DEBUG security fixes.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:5.8.3-owl3
- Removed unneeded BuildRequires for tcsh.
- Reflected Epoch in the %changelog.

* Fri Mar 19 2004 Michail Litvak <mci-at-owl.openwall.com> 1:5.8.3-owl2
- Deal with automatic requires.
- Add some Provides, which were undetected automatically.

* Fri Mar 19 2004 Solar Designer <solar-at-owl.openwall.com> 1:5.8.3-owl1.3
- Dropped the AutoReq: false

* Mon Mar 15 2004 Michail Litvak <mci-at-owl.openwall.com> 1:5.8.3-owl1.2
- Build with threading support to be RH9 compatible.
- Added vendor_perl directory to @INC.

* Thu Feb 19 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:5.8.3-owl1.1
- Temporarily set AutoReq to false

* Sun Jan 25 2004 Solar Designer <solar-at-owl.openwall.com> 1:5.8.3-owl1
- Additional temporary file handling fixes.
- Made building/packaging of suidperl optional and officially unsupported.

* Tue Jan 20 2004 Solar Designer <solar-at-owl.openwall.com> 1:5.8.3-owl0
- Updated to 5.8.3.
- Reviewed all the patches, re-generated those which are to remain, applied
various corrections to the patches and the spec file.

* Thu Dec 25 2003 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:5.8.2-owl0
- Updated to 5.8.2.
- Dropped patches incorporated into mainstream (rh-buildroot, rh-fhs,
rh-installman-man, rh-no-db, rh-prereq, up-owl-glob-bound).
- Dropped owl-getpwent patch due to rewrite of pp_sys.c such that it
no longer uses getspent(3).
- Dropped alt-owl-perldoc-tmp due to rewrite of perldoc.PL (it uses module
Pod::Perldoc, which deals with temporary files via File::Temp).
- Dropped perlcc.PL source (it was a back-port from Perl 5.6.1 to 5.6.0).
- Added patches from ALT Linux perl package.
- Added patch to skip taint tests which use shared memory segments
(they will fail on system with CONFIG_HARDEN_SHM).
- Reviewed Owl patches and corrected some of them to suit the new version.

* Fri Jul 04 2003 Solar Designer <solar-at-owl.openwall.com> 1:5.6.0-owl13
- Corrected the Perl getpwent() to not rely on getspent(3) returning
entries in the same order as getpwent(3) does; this actually makes a
difference with /etc/tcb and likely with non-files password databases.

* Sun Aug 11 2002 Solar Designer <solar-at-owl.openwall.com> 1:5.6.0-owl12
- Back-ported bound checking fixes for File::Glob from Perl 5.8.0.
Thanks to Pavel Kankovsky for the report and to Michael Tokarev for
discussing other possible approaches to fixing this.

* Sun Aug 04 2002 Solar Designer <solar-at-owl.openwall.com>
- Use "rm -f" on compile.ph as it won't exist if the kernel sources under
/usr/src/linux haven't been compiled (reported by Camiel Dobbelaar).

* Thu Jul 18 2002 Solar Designer <solar-at-owl.openwall.com>
- Patched c2ph and lib/ExtUtils/inst to use File::Temp, and the inst to
work with GNU tar.
- Patched lib/dotsh.pl to use a pipe instead of a temporary file (which
used to be created unsafely) and lib/perl5db.pl to not use /tmp/perldbtty$$.
- Applied many fixes to documentation and code comments to not suggest bad
practices on the use of temporary files.

* Tue Jul 16 2002 Solar Designer <solar-at-owl.openwall.com>
- Package File::Temp as needed for the modified perldoc.
- Replaced perlcc with the version that uses File::Temp, from Perl 5.6.1.
- Patched perlbug and s2p to create temporary files with File::Temp, and
perlbug to use vitmp.
- Package some plaintext documentation.
- Only generate *.ph files out of gcc, glibc and kernel headers (but not
SCSI ones) by default.

* Sun Jul 14 2002 Solar Designer <solar-at-owl.openwall.com>
- Corrected the temporary file handling in perldoc (patch from ALT Linux)
and Configure.
- Use the versions of Perl-specific find-{provides,requires} included with
RPM, don't bring our own with this package.
- Only generate *.ph files for packages which are a part of Owl, not other
packages which just happened to be installed on the build system, and make
the line producing STDH out of PKGS actually work (did they ever test this
at Red Hat? same bug in Rawhide, so it seems not).
- Override myuname (to `uname -mrs` rather than `uname -a`) and myhostname
and don't package linux/compile.ph to not leak information specific to the
build system's last kernel compile.

* Thu Feb 07 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Mon Sep 18 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- specify cc=%__cc; continue to let cpp sort itself out
- switch shadow support on (RH bug #8646)

* Wed Sep 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- no mail in suidperl

* Sun Sep 03 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH
- MD5 -> Digest::MD5
- /usr/man/man*
- suidperl default mode 400

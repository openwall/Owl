# $Id: Owl/packages/perl/perl.spec,v 1.24 2004/09/10 07:28:57 galaxy Exp $

%define BUILD_PH 1
%define BUILD_PH_ALL 0

# This controls whether to build/package suidperl.  Your possible use of
# this is at your own risk, -- we do not officially support suidperl.
%define BUILD_SUIDPERL 0

# Build perl with threads support.
%define BUILD_THREADS 1

# Set this if you might be running kernel with enabled "Destroy shared
# memory segments not in use" (CONFIG_HARDEN_SHM) configuration option.
%define KERNEL_CONFIG_HARDEN_SHM 1

Summary: The Perl programming language.
Name: perl
Version: 5.8.3
Release: owl1.4
Epoch: 1
License: GPL
Group: Development/Languages
Source: ftp://ftp.perl.org/pub/CPAN/src/perl-%version.tar.bz2
Patch0: perl-5.8.3-owl-disable-suidperl.diff
Patch1: perl-5.8.3-owl-tmp.diff
Patch2: perl-5.8.3-owl-vitmp.diff
%if %KERNEL_CONFIG_HARDEN_SHM
Patch10: perl-5.8.3-owl-tests-shm.diff
%endif
Patch20: perl-5.8.3-alt-AnyDBM_File-DB_File.diff
Patch21: perl-5.8.3-alt-MM-uninst.diff
Patch22: perl-5.8.3-alt-deb-perldoc-INC.diff
Patch30: perl-5.8.3-rh-lpthread.diff
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
# XXX: RH do this
Provides: perl(abbrev.pl)
Provides: perl(assert.pl)
Provides: perl(bigfloat.pl)
Provides: perl(bigint.pl)
Provides: perl(bigrat.pl)
Provides: perl(bytes_heavy.pl)
Provides: perl(cacheout.pl)
Provides: perl(complete.pl)
Provides: perl(ctime.pl)
Provides: perl(dotsh.pl)
Provides: perl(dumpvar.pl)
Provides: perl(exceptions.pl)
Provides: perl(fastcwd.pl)
Provides: perl(find.pl)
Provides: perl(finddepth.pl)
Provides: perl(flush.pl)
Provides: perl(getcwd.pl)
Provides: perl(getopt.pl)
Provides: perl(getopts.pl)
Provides: perl(hostname.pl)
Provides: perl(importenv.pl)
Provides: perl(look.pl)
Provides: perl(newgetopt.pl)
Provides: perl(open2.pl)
Provides: perl(open3.pl)
Provides: perl(perl5db.pl)
Provides: perl(pwd.pl)
Provides: perl(shellwords.pl)
Provides: perl(stat.pl)
Provides: perl(syslog.pl)
Provides: perl(tainted.pl)
Provides: perl(termcap.pl)
Provides: perl(timelocal.pl)
Provides: perl(utf8_heavy.pl)
Provides: perl(validate.pl)
Obsoletes: perl-MD5
BuildRequires: rpm >= 4.0.5
BuildRequires: gawk, grep, tcsh
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
Requires: %name = %version-%release

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
%if %KERNEL_CONFIG_HARDEN_SHM
%patch10 -p1
%endif
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch30 -p1

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

cat > filter_depends.sh <<EOF
#!/bin/sh
/usr/lib/rpm/find-requires.perl $* | grep -v NDBM | grep -v 'perl(v5.6.0)' | grep -v 'perl(Mac::' | grep -v 'perl(Tk' | grep -v 'perl(VMS::' | grep -v 'perl(FCGI)'
EOF
chmod +x filter_depends.sh

%define __find_requires	%_builddir/%name-%version/filter_depends.sh

%build
rm -rf $RPM_BUILD_ROOT
%_buildshell Configure \
	-des \
	-O \
	-Dmyuname="`uname -mrs`" \
	-Dnewmyuname="`uname -mrs`" \
	-Dmyhostname=%buildhost \
	-Doptimize="$RPM_OPT_FLAGS" \
	-Dcc='%__cc' \
	-Dcccdlflags='-fPIC' \
	-Dinstallprefix=$RPM_BUILD_ROOT%_prefix \
	-Dprefix=%_prefix \
	-Darchname=%_arch-%_os \
	-Dvendorprefix=%_prefix \
	-Dsiteprefix=%_prefix \
	-Dotherlibdirs=/usr/lib/perl5/%version \
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
	-Duselargefiles \
	-Ubincompat5005 \
	-Uversiononly \
	-Dinc_version_list='5.8.0/%_arch-%_os%thread_arch 5.8.0'
%__make

# Some of the tests might create temporary files without due care, some
# others require network access.
#%__make test

%install
rm -rf $RPM_BUILD_ROOT
%__make install
%__mkdir_p $RPM_BUILD_ROOT%_bindir
%__install -m 755 utils/pl2pm $RPM_BUILD_ROOT%_bindir/

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
#
%__make all -f - <<EOF
%if %BUILD_PH_ALL
PKGS	= \$(shell rpm -qa | sed -n 's/\(^.*-devel\)-[0-9.]\+-owl[0-9]\+\$$/\1/p' | sort) \
	  binutils popt pwdb
STDH	= \$(filter %_includedir/%%.h, \$(shell rpm -ql \$(PKGS); echo %_includedir/{linux,asm*,scsi}/*.h))
%else
PKGS	= glibc-devel
STDH	= \$(filter %_includedir/%%.h, \$(shell rpm -ql \$(PKGS); echo %_includedir/{linux,asm*}/*.h))
%endif
GCCDIR	= \$(shell gcc --print-file-name include)
GCCH	= \$(filter \$(GCCDIR)/%%.h, \$(shell rpm -ql gcc))

PERLLIB = \$(RPM_BUILD_ROOT)%_libdir/perl5/%version
PERL	= PERL5LIB=\$(PERLLIB) \$(RPM_BUILD_ROOT)%_bindir/perl
PHDIR	= \$(PERLLIB)/%_arch-%_os%thread_arch
H2PH	= \$(PERL) \$(RPM_BUILD_ROOT)%_bindir/h2ph -d \$(PHDIR)/

all: std-headers gcc-headers fix-config

std-headers: \$(STDH)
	# PKGS=\$(PKGS)
	# STDH=\$(STDH)
	# H2PH=\$(H2PH)
	cd %_includedir && \$(H2PH) \$(STDH:%_includedir/%%=%%)

gcc-headers: \$(GCCH)
	cd \$(GCCDIR) && \$(H2PH) \$(GCCH:\$(GCCDIR)/%%=%%)

fix-config: \$(PHDIR)/Config.pm
	\$(PERL) -i -p -e "s|\$(RPM_BUILD_ROOT)||g;" \$<
EOF
%endif

# Don't leak information specific to the build system.
# "-f" here because compile.ph appeared here only when we have
# compiled kernel source tree in system.
rm -f $RPM_BUILD_ROOT%_libdir/perl5/%version/%_arch-%_os%thread_arch/linux/compile.ph

# Fix the rest of the stuff
find $RPM_BUILD_ROOT%_libdir/perl* -name .packlist -o -name perllocal.pod | \
	xargs ./perl -i -p -e "s|$RPM_BUILD_ROOT||g;" $packlist

%files
%defattr(-,root,root)
%doc Artistic Copying AUTHORS README README.Y2K
%_mandir/*/*
%_libdir/*
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
* Fri Mar 19 2004 Michail Litvak <mci@owl.openwall.com> 5.8.3-owl1.4
- Deal with automatic requires
- Add some Provides, which is undetected automatically.

* Fri Mar 19 2004 Solar Designer <solar@owl.openwall.com> 5.8.3-owl1.3
- Dropped the AutoReq: false

* Mon Mar 15 2004 Michail Litvak <mci@owl.openwall.com> 5.8.3-owl1.2
- Build with threading support to be RH9 compatible.
- Added vendor_perl directory to @INC.

* Thu Feb 19 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 5.8.3-owl1.1
- Temporarily set AutoReq to false

* Sun Jan 25 2004 Solar Designer <solar@owl.openwall.com> 5.8.3-owl1
- Additional temporary file handling fixes.
- Made building/packaging of suidperl optional and officially unsupported.

* Tue Jan 20 2004 Solar Designer <solar@owl.openwall.com> 5.8.3-owl0
- Updated to 5.8.3.
- Reviewed all the patches, re-generated those which are to remain, applied
various corrections to the patches and the spec file.

* Thu Dec 25 2003 (GalaxyMaster) <galaxy@owl.openwall.com> 5.8.2-owl0
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

* Fri Jul 04 2003 Solar Designer <solar@owl.openwall.com> 5.6.0-owl13
- Corrected the Perl getpwent() to not rely on getspent(3) returning
entries in the same order as getpwent(3) does; this actually makes a
difference with /etc/tcb and likely with non-files password databases.

* Sun Aug 11 2002 Solar Designer <solar@owl.openwall.com> 5.6.0-owl12
- Back-ported bound checking fixes for File::Glob from Perl 5.8.0.
Thanks to Pavel Kankovsky for the report and to Michael Tokarev for
discussing other possible approaches to fixing this.

* Sun Aug 04 2002 Solar Designer <solar@owl.openwall.com>
- Use "rm -f" on compile.ph as it won't exist if the kernel sources under
/usr/src/linux haven't been compiled (reported by Camiel Dobbelaar).

* Thu Jul 18 2002 Solar Designer <solar@owl.openwall.com>
- Patched c2ph and lib/ExtUtils/inst to use File::Temp, and the inst to
work with GNU tar.
- Patched lib/dotsh.pl to use a pipe instead of a temporary file (which
used to be created unsafely) and lib/perl5db.pl to not use /tmp/perldbtty$$.
- Applied many fixes to documentation and code comments to not suggest bad
practices on the use of temporary files.

* Tue Jul 16 2002 Solar Designer <solar@owl.openwall.com>
- Package File::Temp as needed for the modified perldoc.
- Replaced perlcc with the version that uses File::Temp, from Perl 5.6.1.
- Patched perlbug and s2p to create temporary files with File::Temp, and
perlbug to use vitmp.
- Package some plaintext documentation.
- Only generate *.ph files out of gcc, glibc and kernel headers (but not
SCSI ones) by default.

* Sun Jul 14 2002 Solar Designer <solar@owl.openwall.com>
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

* Thu Feb 07 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Mon Sep 18 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- specify cc=%__cc; continue to let cpp sort itself out
- switch shadow support on (RH bug #8646)

* Wed Sep 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- no mail in suidperl

* Sun Sep 03 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- MD5 -> Digest::MD5
- /usr/man/man*
- suidperl default mode 400

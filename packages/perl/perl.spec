# $Id: Owl/packages/perl/perl.spec,v 1.16 2003/07/04 16:13:08 solar Exp $

%define BUILD_PH 1
%define BUILD_PH_ALL 0

Summary: The Perl programming language.
Name: perl
Version: 5.6.0
Release: owl13
Epoch: 1
License: GPL
Group: Development/Languages
Source0: ftp://ftp.perl.org/pub/CPAN/src/perl-%{version}.tar.gz
Source1: ftp://ftp.perl.org/pub/CPAN/modules/by-module/Digest/Digest-MD5-2.09.tar.gz
Source2: ftp://ftp.perl.org/pub/CPAN/modules/by-module/File/File-Temp-0.12.tar.gz
Source10: perlcc.PL
Patch0: perl-5.6.0-rh-install-man.diff
Patch1: perl-5.6.0-rh-fhs.diff
Patch2: perl-5.6.0-rh-buildroot.diff
Patch3: perl-5.6.0-rh-prereq.diff
Patch4: perl-5.6.0-rh-no-db.diff
Patch5: perl-5.6.0-owl-no-mail.diff
Patch6: perl-5.6.0-owl-disable-suidperl.diff
Patch7: perl-5.6.0-alt-owl-perldoc-tmp.diff
Patch8: perl-5.6.0-owl-tmp.diff
Patch9: perl-5.6.0-owl-vitmp.diff
Patch10: perl-5.6.0-up-owl-glob-bound.diff
Patch11: perl-5.6.0-owl-getpwent.diff
Provides: perl <= %{version}
Obsoletes: perl-MD5
BuildRequires: rpm >= 3.0.5
BuildRequires: gawk, grep, tcsh
BuildRoot: /override/%{name}-%{version}

# Provide Perl-specific find-{provides,requires}.
%define	__find_provides	/usr/lib/rpm/find-provides.perl
%define	__find_requires	/usr/lib/rpm/find-requires.perl

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

%prep
%setup -q
# Remove files with known temporary file handling issues that we don't
# package or use anyway.
REMOVE_FILES='
	INSTALL
	makeaperl.SH perly.fixer
	ext/SDBM_File/sdbm/grind ext/ODBM_File/ODBM_File.xs
	eg/g/gsh eg/g/gcp.man'
rm $REMOVE_FILES
mv MANIFEST MANIFEST.orig
for f in $REMOVE_FILES; do
	echo "^${f}[[:space:]]"
done | sed 's/\./\\./' | grep -vEf - MANIFEST.orig > MANIFEST
# Satisfy a make dependency
touch makeaperl.SH

mkdir modules
tar xzf %SOURCE1 -C modules
tar xzf %SOURCE2 -C modules

rm utils/perlcc.PL
cp $RPM_SOURCE_DIR/perlcc.PL utils/

%patch0 -p1
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

find . -name '*.orig' -print0 | xargs -r0 rm -v --

%build
rm -rf $RPM_BUILD_ROOT
sh Configure \
	-des \
	-O \
	-Dnewmyuname="`uname -mrs`" \
	-Dmyhostname=%{buildhost} \
	-Doptimize="$RPM_OPT_FLAGS" \
	-Dcc='%{__cc}' \
	-Dcccdlflags='-fPIC' \
	-Dinstallprefix=$RPM_BUILD_ROOT%{_prefix} \
	-Dprefix=%{_prefix} \
	-Darchname=%{_arch}-%{_os} \
%ifarch sparc sparcv9
	-Ud_longdbl \
%endif
	-Dd_dosuid \
	-Dd_semctl_semun \
	-Di_db \
	-Di_ndbm \
	-Di_gdbm \
	-Di_shadow \
	-Dman3ext=3pm \
	-Uuselargefiles
make

# Build the modules we have
cd modules
for module in *; do
	cd $module
	../../perl -I../../lib Makefile.PL
	make
	cd ..
done

%install
rm -rf $RPM_BUILD_ROOT

make install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
install -m 755 utils/pl2pm ${RPM_BUILD_ROOT}%{_bindir}/

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
make all -f - <<EOF
%if %BUILD_PH_ALL
PKGS	= \$(shell rpm -qa | sed -n 's/\(^.*-devel\)-[0-9.]\+-owl[0-9]\+\$$/\1/p' | sort) \
	  binutils popt pwdb
STDH	= \$(filter %{_includedir}/%%.h, \$(shell rpm -ql \$(PKGS); echo %{_includedir}/{linux,asm*,scsi}/*.h))
%else
PKGS	= glibc-devel
STDH	= \$(filter %{_includedir}/%%.h, \$(shell rpm -ql \$(PKGS); echo %{_includedir}/{linux,asm*}/*.h))
%endif
GCCDIR	= \$(shell gcc --print-file-name include)
GCCH	= \$(filter \$(GCCDIR)/%%.h, \$(shell rpm -ql gcc))

PERLLIB = \$(RPM_BUILD_ROOT)%{_libdir}/perl5/%{version}
PERL	= PERL5LIB=\$(PERLLIB) \$(RPM_BUILD_ROOT)%{_bindir}/perl
PHDIR	= \$(PERLLIB)/\${RPM_ARCH}-linux
H2PH	= \$(PERL) \$(RPM_BUILD_ROOT)%{_bindir}/h2ph -d \$(PHDIR)/

all: std-headers gcc-headers fix-config

std-headers: \$(STDH)
	# PKGS=\$(PKGS)
	# STDH=\$(STDH)
	cd %{_includedir} && \$(H2PH) \$(STDH:%{_includedir}/%%=%%)

gcc-headers: \$(GCCH)
	cd \$(GCCDIR) && \$(H2PH) \$(GCCH:\$(GCCDIR)/%%=%%)

fix-config: \$(PHDIR)/Config.pm
	\$(PERL) -i -p -e "s|\$(RPM_BUILD_ROOT)||g;" \$<
EOF

# Don't leak information specific to the build system
rm -f $RPM_BUILD_ROOT%{_libdir}/perl5/%{version}/%{_arch}-linux/linux/compile.ph
%endif

# Now pay attention to the extra modules
pushd modules
for module in *; do
	eval $(../perl -V:installarchlib)
	mkdir -p $RPM_BUILD_ROOT/$installarchlib
	make -C $module install
done
popd

# Fix the rest of the stuff
find $RPM_BUILD_ROOT%{_libdir}/perl* -name .packlist -o -name perllocal.pod | \
	xargs ./perl -i -p -e "s|$RPM_BUILD_ROOT||g;" $packlist

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc Artistic Copying AUTHORS README README.Y2K
%{_bindir}/*
%{_libdir}/*
%{_mandir}/*/*

%changelog
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
- specify cc=%{__cc}; continue to let cpp sort itself out
- switch shadow support on (RH bug #8646)

* Wed Sep 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- no mail in suidperl

* Sun Sep 03 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- MD5 -> Digest::MD5
- /usr/man/man*
- suidperl default mode 400

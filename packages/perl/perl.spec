# $Id: Owl/packages/perl/perl.spec,v 1.5 2000/09/18 11:17:56 kad Exp $

Summary: 	The Perl programming language.
Name: 		perl
%define 	perlver 5.6.0
Version: 	%{perlver}
Release: 	9owl
Copyright: 	GPL
Group: 		Development/Languages
Source0:	ftp://ftp.perl.org/pub/perl/CPAN/src/perl-%{perlver}.tar.gz
Source1: 	ftp://ftp.perl.org/pub/CPAN/modules/by-module/MD5/Digest-MD5-2.09.tar.gz
Source2: 	find-provides
Source3: 	find-requires
Patch0: 	perl5.005_02-rh-buildsys.diff
Patch1: 	perl-5.6.0-rh-installman.diff
Patch2: 	perl-5.6.0-rh-nodb.diff
Patch3: 	perl-5.6.0-rh-prereq.diff
Patch4: 	perl-5.6.0-rh-root.diff
Patch5: 	perl-5.6.0-rh-fhs.diff
Patch6: 	perl-5.6.0-rh-buildroot.diff
Patch7:		perl-5.6.0-owl-nomail.diff
Obsoletes: 	perl-MD5
Buildroot: 	/var/rpm-buildroot/%{name}-root
BuildPreReq: 	gawk, grep, tcsh
Epoch: 		1

# ----- Perl module dependencies.
#
# Provide perl-specific find-{provides,requires} until rpm-3.0.4 catches up.
%define	__find_provides	%{SOURCE2}
%define	__find_requires	%{SOURCE3}

# By definition of 'do' (see 'man perlfunc') this package provides all
# versions of perl previous to it.
Provides: perl <= %{version}

# These modules appear to be missing or break assumptions made by the
# dependency analysis tools.  Typical problems include refering to
# CGI::Apache as Apache and having no package line in CPAN::Nox.pm. I
# hope that the perl people fix these to work with our dependency
# engine or give us better dependency tools.
#
# Provides: perl(Apache)
# Provides: perl(ExtUtils::MM_Mac)
# Provides: perl(ExtUtils::XSSymSet)
# Provides: perl(FCGI)
# Provides: perl(LWP::UserAgent)
# Provides: perl(Mac::Files)
# Provides: perl(URI::URL)
# Provides: perl(VMS::Filespec)

%description
Perl is a high-level programming language with roots in C, sed, awk
and shell scripting.  Perl is good at handling processes and files,
and is especially good at handling text.  Perl's hallmarks are
practicality and efficiency.  While it is used to do a lot of
different things, Perl's most common applications are system
administration utilities and web programming.  A large proportion of
the CGI scripts on the web are written in Perl.  You need the perl
package installed on your system so that your system can handle Perl
scripts.

Install this package if you want to program in Perl or enable your
system to handle Perl scripts.

%prep
%setup -q
mkdir modules
tar xzf %{SOURCE1} -C modules
%patch0 -p1 -b .buildsys
%patch1 -p1 -b .instman
%patch2 -p1 -b .nodb
%patch3 -p1 -b .prereq
%patch4 -p1 -b .root
%patch5 -p1 -b .fhs
%patch6 -p1 -b .buildroot
%patch7 -p1 -b .nomail

find . -name \*.orig -exec rm -fv {} \;

%build
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
sh Configure -des -Doptimize="$RPM_OPT_FLAGS" \
        -Dcc='%{__cc}' \
	-Dcccdlflags='-fPIC' \
	-Dinstallprefix=$RPM_BUILD_ROOT%{_prefix} \
	-Dprefix=%{_prefix} \
	-Darchname=%{_arch}-%{_os} \
%ifarch sparc
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
make -f Makefile

# Build the modules we have
MainDir=$(pwd)
cd modules
for module in * ; do 
    cd $module
    $MainDir/perl -I$MainDir/lib Makefile.PL
    make
    cd ..
done
cd $MainDir

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

make install -f Makefile
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
install -m 755 utils/pl2pm ${RPM_BUILD_ROOT}%{_bindir}/pl2pm

# Generate *.ph files with a trick. Is this sick or what ?
make all -f - <<EOF
PKGS	= glibc-devel gdbm-devel gpm-devel libgr-devel libjpeg-devel \
	  libpng-devel libtiff-devel ncurses-devel popt \
	  zlib-devel binutils libelf e2fsprogs-devel pam pwdb \
	  rpm-devel
STDH	= \$(filter %{_includedir}/include/%%, \$(shell rpm -q --queryformat '[%%{FILENAMES}\n]' \$(PKGS)))
STDH	+=\$(wildcard %{_includedir}/linux/*.h) \$(wildcard %{_includedir}/asm/*.h) \
	  \$(wildcard %{_includedir}/scsi/*.h)
GCCDIR	= \$(shell gcc --print-file-name include)
GCCH	= \$(filter \$(GCCDIR)/%%, \$(shell rpm -q --queryformat '[%%{FILEMODES} %%{FILENAMES}\n]' gcc | grep -v ^4 | awk '{print $NF}'))

PERLLIB = \$(RPM_BUILD_ROOT)%{_libdir}/perl5/%{perlver}
PERL	= PERL5LIB=\$(PERLLIB) \$(RPM_BUILD_ROOT)%{_bindir}/perl
PHDIR	= \$(PERLLIB)/\${RPM_ARCH}-linux
H2PH	= \$(PERL) \$(RPM_BUILD_ROOT)%{_bindir}/h2ph -d \$(PHDIR)/

all: std-headers gcc-headers fix-config

std-headers: \$(STDH)
	cd %{_includedir} && \$(H2PH) \$(STDH:%{_includedir}/%%=%%)

gcc-headers: \$(GCCH)
	cd \$(GCCDIR) && \$(H2PH) \$(GCCH:\$(GCCDIR)/%%=%%) || true

fix-config: \$(PHDIR)/Config.pm
	\$(PERL) -i -p -e "s|\$(RPM_BUILD_ROOT)||g;" \$<

EOF

# Now pay attention to the extra modules
MainDir=$(pwd)
pushd modules
for module in * ; do 
    eval $($MainDir/perl '-V:installarchlib')
    mkdir -p $RPM_BUILD_ROOT/$installarchlib
    make -C $module install
done
popd
#cd $MainDir

# fix the rest of the stuff
find $RPM_BUILD_ROOT%{_libdir}/perl* -name .packlist -o -name perllocal.pod | \
xargs ./perl -i -p -e "s|$RPM_BUILD_ROOT||g;" $packlist

chmod 400 $RPM_BUILD_ROOT%{_prefix}/bin/suidperl

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%{_mandir}/*/*

%changelog
* Mon Sep 18 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- specify cc=%{__cc}; continue to let cpp sort itself out
- switch shadow support on (RH bug #8646)

* Wed Sep  6 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- no mail in suidperl

* Sun Sep  3 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- MD5 -> Digest::MD5
- /usr/man/man*
- suidperl default mode 400

* Tue Jul 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- strip buildroot from perl pods (#14040)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jun 21 2000 Preston Brown <pbrown@redhat.com>
- don't require tcsh to install, only to build

* Mon Jun 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild against new db3 package

* Sat Jun 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable 64-bit file support
- change name of package that Perl expects gcc to be in from "egcs" to "gcc"
- move man pages to /usr/share via hints/linux.sh and MM_Unix.pm
- fix problems prefixifying with empty prefixes
- disable long doubles on sparc (they're the same as doubles anyway)
- add an Epoch to make sure we can upgrade from perl-5.00503

* Thu Mar 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.6.0

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Fri Jan 14 2000 Jeff Johnson <jbj@redhat.com>
- add provides for perl modules (from kestes@staff.mail.com).

* Mon Oct 04 1999 Cristian Gafton <gafton@redhat.com>
- fix the %install so that the MD5 module gets actually installed correctly

* Mon Aug 30 1999 Cristian Gafton <gafton@redhat.com>
- make sure the package builds even when we don't have perl installed on the
  system

* Fri Aug 06 1999 Cristian Gafton <gafton@redhat.com>
- merged with perl-MD5
- get rid of the annoying $RPM_BUILD_ROOT paths in the installed tree

* Mon Jul 26 1999 Cristian Gafton <gafton@redhat.com>
- do not link anymore against the system db library (and make each module
  link against it separately, so that we can have Berkeley db1 and db2 mixed
  up)

* Wed Jun 16 1999 Cristian Gafton <gafton@redhat.com>
- use wildcards for files in /usr/bin and /usr/man

* Tue Apr 06 1999 Cristian Gafton <gafton@redhat.com>
- version 5.00503
- make the default man3 install dir be release independent
- try to link against db1 to preserve compatibility with older databases;
  abandoned idea because perl is too broken to allow such an easy change
  (hardcoded names *everywhere* !!!)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Jan 07 1999 Cristian Gafton <gafton@redhat.com>
- guilty of the inlined Makefile in the spec file
- adapted for the arm build

* Wed Sep 09 1998 Preston Brown <pbrown@redhat.com>
- added newer CGI.pm to the build
- changed the version naming scheme around to work with RPM

* Sun Jul 19 1998 Jeff Johnson <jbj@redhat.com>
- attempt to generate *.ph files reproducibly

* Mon Jun 15 1998 Jeff Johnson <jbj@redhat.com>
- update to 5.004_04-m4 (pre-5.005 maintenance release)

* Tue Jun 12 1998 Christopher McCrory <chrismcc@netus.com
- need stdarg.h from gcc shadow to fix "use Sys::Syslog" (problem #635)

* Fri May 08 1998 Cristian Gafton <gafton@redhat.com>
- added a patch to correct the .ph constructs unless defined (foo) to read
  unless(defined(foo))

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Mar 10 1998 Cristian Gafton <gafton@redhat.com>
- fixed strftime problem

* Sun Mar 08 1998 Cristian Gafton <gafton@redhat.com>
- added a patch to fix a security race
- do not use setres[ug]id - those are not implemented on 2.0.3x kernels

* Mon Mar 02 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 5.004_04 - 5.004_01 had some nasty memory leaks.
- fixed the spec file to be version-independent

* Fri Dec 05 1997 Erik Troan <ewt@redhat.com>
- Config.pm wasn't right do to the builtrooting

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- fixed arch-specfic part of spec file

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- updated to perl 5.004_01
- users a build root

* Thu Jun 12 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Apr 22 1997 Erik Troan <ewt@redhat.com>
- Incorporated security patch from Chip Salzenberg <salzench@nielsenmedia.com>

* Fri Feb 07 1997 Erik Troan <ewt@redhat.com>
- Use -Darchname=i386-linux 
- Require csh (for glob)
- Use RPM_ARCH during configuration and installation for arch independence

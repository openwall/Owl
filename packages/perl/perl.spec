# $Id: Owl/packages/perl/perl.spec,v 1.8 2002/02/07 01:49:34 solar Exp $

Summary: The Perl programming language.
Name: perl
Version: 5.6.0
Release: owl9
Epoch: 1
License: GPL
Group: Development/Languages
Source0: ftp://ftp.perl.org/pub/perl/CPAN/src/perl-%{version}.tar.gz
Source1: ftp://ftp.perl.org/pub/CPAN/modules/by-module/MD5/Digest-MD5-2.09.tar.gz
Source2: find-provides
Source3: find-requires
Patch0: perl5.005_02-rh-buildsys.diff
Patch1: perl-5.6.0-rh-installman.diff
Patch2: perl-5.6.0-rh-nodb.diff
Patch3: perl-5.6.0-rh-prereq.diff
Patch4: perl-5.6.0-rh-root.diff
Patch5: perl-5.6.0-rh-fhs.diff
Patch6: perl-5.6.0-rh-buildroot.diff
Patch7: perl-5.6.0-owl-nomail.diff
Provides: perl <= %{version}
Obsoletes: perl-MD5
BuildRequires: gawk, grep, tcsh
BuildRoot: /override/%{name}-%{version}

# ----- Perl module dependencies.
#
# Provide perl-specific find-{provides,requires} until rpm-3.0.4 catches up.
%define	__find_provides	%{SOURCE2}
%define	__find_requires	%{SOURCE3}

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
the CGI scripts on the web are written in Perl.  You need the Perl
package installed on your system so that your system can handle Perl
scripts.

%prep
%setup -q
mkdir modules
tar xzf %{SOURCE1} -C modules
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

find . -name '*.orig' -print0 | xargs -r0 rm -v --

%build
rm -rf $RPM_BUILD_ROOT
sh Configure -des -Doptimize="$RPM_OPT_FLAGS" \
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
MainDir=`pwd`
cd modules
for module in *; do
	cd $module
	$MainDir/perl -I$MainDir/lib Makefile.PL
	make
	cd ..
done

%install
rm -rf $RPM_BUILD_ROOT

make install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
install -m 755 utils/pl2pm ${RPM_BUILD_ROOT}%{_bindir}/

# Generate *.ph files with a trick. Is this sick or what?
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

PERLLIB = \$(RPM_BUILD_ROOT)%{_libdir}/perl5/%{version}
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
MainDir=`pwd`
pushd modules
for module in *; do
	eval $($MainDir/perl '-V:installarchlib')
	mkdir -p $RPM_BUILD_ROOT/$installarchlib
	make -C $module install
done
popd

# fix the rest of the stuff
find $RPM_BUILD_ROOT%{_libdir}/perl* -name .packlist -o -name perllocal.pod | \
	xargs ./perl -i -p -e "s|$RPM_BUILD_ROOT||g;" $packlist

chmod 400 $RPM_BUILD_ROOT%{_prefix}/bin/suidperl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%{_mandir}/*/*

%changelog
* Thu Feb 07 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

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

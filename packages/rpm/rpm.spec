# $Id: Owl/packages/rpm/rpm.spec,v 1.21 2002/02/07 18:07:47 solar Exp $

Summary: The Red Hat package management system.
Name: rpm
Version: 3.0.6
Release: owl1
License: GPL
Group: System Environment/Base
Source: ftp://ftp.rpm.org/pub/rpm/dist/rpm-3.0.x/rpm-%{version}.tar.gz
Patch0: rpm-3.0.6-owl-topdir.diff
Patch1: rpm-3.0.5-owl-bash2.diff
Patch2: rpm-3.0.5-owl-vendor.diff
Patch3: rpm-3.0.5-owl-closeall.diff
Patch4: rpm-3.0.5-owl-includes.diff
Patch5: rpm-3.0.5-owl-gendiff.diff
PreReq: /sbin/ldconfig
PreReq: gawk, fileutils, textutils, sh-utils, mktemp
Requires: popt, bzip2 >= 0.9.0c-2
Conflicts: patch < 2.5
# XXX the libio interface is incompatible in glibc 2.2
Conflicts: glibc >= 2.1.90
BuildRequires: bzip2 >= 0.9.0c-2
BuildRoot: /override/%{name}-%{version}

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages.  Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package devel
Summary: Development files for applications which will manipulate RPM packages.
Group: Development/Libraries
Requires: rpm = %{version}-%{release}, popt

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
Requires: rpm = %{version}-%{release}

%description build
This package contains scripts and executable programs that are used to
build packages using RPM.

%package -n popt
Summary: A C library for parsing command line arguments.
Version: 1.5.1
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
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%define _noVersionedDependencies 1

# XXX legacy requires './' payload prefix to be omitted from RPM packages.
%define _noPayloadPrefix 1
%define __prefix /usr

# Not yet.
#%define __share /share
%define __share %{nil}

%define __mandir %{__prefix}%{__share}/man

%build
unset LINGUAS || :
autoconf
automake
CFLAGS="$RPM_OPT_FLAGS" ./configure \
	--prefix=%{__prefix} \
	--sysconfdir=/etc \
	--localstatedir=/var \
	--infodir='${prefix}%{__share}/info' \
	--mandir='${prefix}%{__share}/man' \
	--build=%{_arch}-unknown-linux
make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR="$RPM_BUILD_ROOT" install
mkdir -p $RPM_BUILD_ROOT/etc/rpm

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/bin/rpm --initdb
if [ ! -e /etc/rpm/macros -a -e /etc/rpmrc -a -f %{__prefix}/lib/rpm/convertrpmrc.sh ]; then
	sh %{__prefix}/lib/rpm/convertrpmrc.sh &> /dev/null
fi

%postun -p /sbin/ldconfig

%post -n popt -p /sbin/ldconfig
%postun -n popt -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc RPM-PGP-KEY RPM-GPG-KEY CHANGES GROUPS doc/manual/*
/bin/rpm
%dir /etc/rpm
%{__prefix}/bin/rpm2cpio
%{__prefix}/bin/gendiff
%{__prefix}/lib/librpm.so.*
%{__prefix}/lib/librpmbuild.so.*

%{__prefix}/lib/rpm/brp-*
%{__prefix}/lib/rpm/config.guess
%{__prefix}/lib/rpm/config.sub
%{__prefix}/lib/rpm/convertrpmrc.sh
%{__prefix}/lib/rpm/find-prov.pl
%{__prefix}/lib/rpm/find-provides
%{__prefix}/lib/rpm/find-req.pl
%{__prefix}/lib/rpm/find-requires
%{__prefix}/lib/rpm/macros
%{__prefix}/lib/rpm/mkinstalldirs
%{__prefix}/lib/rpm/rpmpopt
%{__prefix}/lib/rpm/rpmrc
%{__prefix}/lib/rpm/vpkg-provides.sh
%{__prefix}/lib/rpm/vpkg-provides2.sh

%ifarch %ix86
%{__prefix}/lib/rpm/i*86*
%endif
%ifarch alpha alphaev5 alphaev56 alphapca56 alphaev6 alphaev67
%{__prefix}/lib/rpm/alpha*
%endif
%ifarch sparc sparcv9 sparc64
%{__prefix}/lib/rpm/sparc*
%endif
%ifarch ia64
%{__prefix}/lib/rpm/ia64*
%endif
%ifarch powerpc ppc
%{__prefix}/lib/rpm/ppc*
%endif

# Disabled.
#%dir %{__prefix}/src/RPM
#%dir %{__prefix}/src/RPM/BUILD
#%dir %{__prefix}/src/RPM/SPECS
#%dir %{__prefix}/src/RPM/SOURCES
#%dir %{__prefix}/src/RPM/SRPMS
#%dir %{__prefix}/src/RPM/RPMS
#%{__prefix}/src/RPM/RPMS/*

%{__prefix}/*/locale/*/LC_MESSAGES/rpm.mo
%{__mandir}/man[18]/*.[18]*
%lang(pl) %{__mandir}/pl/man[18]/*.[18]*
%lang(ru) %{__mandir}/ru/man[18]/*.[18]*
%lang(sk) %{__mandir}/sk/man[18]/*.[18]*

%files build
%defattr(-,root,root)
%{__prefix}/lib/rpm/check-prereqs
%{__prefix}/lib/rpm/cpanflute
%{__prefix}/lib/rpm/find-lang.sh
%{__prefix}/lib/rpm/find-provides.perl
%{__prefix}/lib/rpm/find-requires.perl
%{__prefix}/lib/rpm/get_magic.pl
%{__prefix}/lib/rpm/getpo.sh
%{__prefix}/lib/rpm/http.req
%{__prefix}/lib/rpm/magic.prov
%{__prefix}/lib/rpm/magic.req
%{__prefix}/lib/rpm/perl.prov
%{__prefix}/lib/rpm/perl.req
%{__prefix}/lib/rpm/rpmdiff
%{__prefix}/lib/rpm/rpmdiff.cgi
%{__prefix}/lib/rpm/rpmgettext
%{__prefix}/lib/rpm/rpmputtext
%{__prefix}/lib/rpm/u_pkg.sh

%files devel
%defattr(-,root,root)
%{__prefix}/include/rpm
%{__prefix}/lib/librpm.a
%{__prefix}/lib/librpm.la
%{__prefix}/lib/librpm.so
%{__prefix}/lib/librpmbuild.a
%{__prefix}/lib/librpmbuild.la
%{__prefix}/lib/librpmbuild.so

%files -n popt
%defattr(-,root,root)
%{__prefix}/lib/libpopt.so.*
%{__prefix}/*/locale/*/LC_MESSAGES/popt.mo
%{__mandir}/man3/popt.3*

# XXX These may end up in popt-devel but it hardly seems worth the effort now.
%{__prefix}/lib/libpopt.a
%{__prefix}/lib/libpopt.la
%{__prefix}/lib/libpopt.so
%{__prefix}/include/popt.h

%changelog
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

* Sun Sep  3 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- vendor fix
- FHS
- closeall security fix
- RH 6.2 updates merge

* Sat Aug  5 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- change build target
- /usr/src/redhat -> /usr/src/RPM

* Thu Jul 20 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from official RPM team test rpm.
- disable Python module

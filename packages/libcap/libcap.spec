# $Id: Owl/packages/libcap/libcap.spec,v 1.5 2003/11/10 00:00:19 solar Exp $

Summary: Library for getting and setting POSIX.1e capabilities.
Name: libcap
Version: 1.10
Release: owl2
License: GPL
Group: System Environment/Libraries
URL: http://www.kernel.org/pub/linux/libs/security/linux-privs/
Source0: ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.2/%name-%version.tar.bz2
Source1: ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.2/capfaq-0.2.txt
Patch0: libcap-1.10-alt-cap_free.diff
Patch1: libcap-1.10-alt-bound.diff
Patch2: libcap-1.10-alt-userland.diff
Patch3: libcap-1.10-alt-warnings.diff
Patch4: libcap-1.10-rh-alt-makenames.diff
Patch5: libcap-1.10-alt-Makefile.diff
BuildRoot: /override/%name-%version

%description
This is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package utils
Summary: Utilities for getting and setting POSIX.1e capabilities.
Group: System Environment/Base
Requires: %name = %version-%release

%description utils
This packages contains utilities for getting and setting POSIX.1e
(formerly POSIX 6) draft 15 capabilities.

%package devel
Summary: The development library, header files, and documentation for libcap.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
The development library, header files, and documentation for building
applications dealing with POSIX.1e (formerly POSIX 6) draft 15
capabilities.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
install -p -m 644 $RPM_SOURCE_DIR/capfaq-0.2.txt .

%{expand:%%define optflags %optflags -Wall}

%build
make COPTFLAG="$RPM_OPT_FLAGS -D_GNU_SOURCE" DEBUG= LDFLAGS= WARNINGS=

%install
rm -rf $RPM_BUILD_ROOT
make install FAKEROOT=$RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/lib/*.so.*

%files utils
%defattr(-,root,root)
/sbin/*

%files devel
%defattr(-,root,root)
%doc README CHANGELOG *.txt pgp.keys.asc doc/capability.notes
%doc progs/*.c
/lib/*.so
%_includedir/sys/*.h
# man-pages package currently has newer versions of the section 2 pages.
%_mandir/man3/*

%changelog
* Thu Nov 06 2003 Dmitry V. Levin <ldv@owl.openwall.com> 1.10-owl2
- Do not override capget and capset symbols defined in glibc.
- Build the shared library with -fPIC.

* Sun Oct 26 2003 Solar Designer <solar@owl.openwall.com> 1.10-owl1
- Re-worked the spec file to make it suitable for inclusion in Owl.

* Sat Oct 11 2003 Simon B <simonb@owl.openwall.com> 1.10-owl0.1
- Initial revision, based on a spec file from ALT Linux.

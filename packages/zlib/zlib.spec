# $Id: Owl/packages/zlib/zlib.spec,v 1.1.2.1 2002/03/07 18:22:10 solar Exp $

Summary: The zlib compression and decompression library.
Name: zlib
Version: 1.1.3
Release: 12owl
License: BSD
Group: System Environment/Libraries
URL: http://www.gzip.org/zlib/
Source: ftp://ftp.info-zip.org/pub/infozip/zlib/zlib-%{version}.tar.gz
Patch0: zlib-1.1.3-rh-glibc.diff
Patch1: zlib-1.1.3-mark-inflate-error-handling.diff
PreReq: /sbin/ldconfig
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
The zlib compression library provides in-memory compression and
decompression functions, including integrity checks of the
uncompressed data.  This version of the library supports only one
compression method (deflation), but other algorithms may be added
later, which will have the same stream interface.  The zlib library is
used by many different system programs.

%package devel
Summary: Header files and libraries for developing apps which will use zlib.
Group: Development/Libraries
Requires: zlib

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --shared --prefix=%{_prefix}
make
# now build the static lib
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}

CFLAGS="$RPM_OPT_FLAGS" ./configure --shared --prefix=%{_prefix}
make install prefix=${RPM_BUILD_ROOT}%{_prefix}

CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix}
make install prefix=${RPM_BUILD_ROOT}%{_prefix}

install -m 644 zutil.h ${RPM_BUILD_ROOT}%{_includedir}/zutil.h
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3
install -m 644 zlib.3 ${RPM_BUILD_ROOT}%{_mandir}/man3

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README
%{_libdir}/libz.so.*

%files devel
%defattr(-,root,root)
%doc ChangeLog algorithm.txt
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/zlib.3*

%changelog
* Thu Mar 07 2002 Solar Designer <solar@owl.openwall.com>
- Error handling fixes for inflate from Mark Adler.
- Enforce some of our new spec file conventions (from -current).

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

# $Id: Owl/packages/zlib/zlib.spec,v 1.9 2004/11/23 22:40:50 mci Exp $

Summary: The zlib compression and decompression library.
Name: zlib
Version: 1.1.4
Release: owl3
License: BSD
Group: System Environment/Libraries
URL: http://www.gzip.org/zlib/
Source: ftp://ftp.info-zip.org/pub/infozip/zlib/zlib-%version.tar.bz2
Patch0: zlib-1.1.4-owl-gzprintf-bound.diff
Patch1: zlib-1.1.4-alt-gzio.diff
PreReq: /sbin/ldconfig
Prefix: %_prefix
BuildRoot: /override/%name-%version

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

%{expand:%%define optflags %optflags -Wall}

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --shared --prefix=%_prefix
make
# now build the static lib
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%_prefix
make

%install
rm -rf %buildroot
mkdir -p %buildroot%_prefix

CFLAGS="$RPM_OPT_FLAGS" ./configure --shared --prefix=%_prefix
make install prefix=%buildroot%_prefix

CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%_prefix
make install prefix=%buildroot%_prefix

install -m 644 zutil.h %buildroot%_includedir/
mkdir -p %buildroot%_mandir/man3
install -m 644 zlib.3 %buildroot%_mandir/man3/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README
%_libdir/libz.so.*

%files devel
%defattr(-,root,root)
%doc ChangeLog algorithm.txt
%_libdir/*.a
%_libdir/*.so
%_includedir/*
%_mandir/man3/zlib.3*

%changelog
* Thu May 15 2003 Solar Designer <solar@owl.openwall.com> 1.1.4-owl3
- Do safer memory (de)allocation in gzio and gzerror() in particular,
patch from Dmitry V. Levin, originally for ALT Linux.

* Tue Feb 25 2003 Solar Designer <solar@owl.openwall.com>
- Patched gzprintf() to use vsnprintf() and handle possible truncation,
thanks to Bugtraq postings by Crazy Einstein, Richard Kettlewell, and
Carlo Marcelo Arenas Belon.

* Wed Mar 13 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 1.1.4.
- Build with -Wall.

* Mon Feb 11 2002 Solar Designer <solar@owl.openwall.com>
- Error handling fixes for inflate from Mark Adler.

* Sat Feb 02 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

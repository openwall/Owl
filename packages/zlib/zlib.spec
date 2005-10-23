# $Id: Owl/packages/zlib/zlib.spec,v 1.10 2005/10/23 21:37:54 ldv Exp $

Summary: The zlib compression and decompression library.
Name: zlib
Version: 1.2.3
Release: owl1
License: BSD
Group: System Environment/Libraries
URL: http://www.zlib.net/
Source: %url/zlib-%version.tar.bz2
Patch0: zlib-1.2.3-alt-gzio-gzwrite-z_err.diff
Patch1: zlib-1.2.3-alt-gzio-gzerror.diff
Patch2: zlib-1.2.3-alt-gzio-gzread-transparent.diff
Patch3: zlib-1.2.3-alt-versioning.diff
Patch4: zlib-1.2.3-rh-make-test.diff
PreReq: /sbin/ldconfig
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
The zlib compression library provides in-memory compression and
decompression functions, including integrity checks of the uncompressed
data.  This version of the library supports only one compression method
(deflation), but other algorithms may be added later, which will have
the same stream interface.  The zlib library is used by many different
system programs.

%package devel
Summary: Header files and libraries for developing apps which will use zlib.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
The zlib-devel package contains the header files and libraries needed to
develop programs that use the zlib compression and decompression library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
fgrep -B999 @ zlib.h >License

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags} -Wall}

%build
# first build and test static zlib
CFLAGS="%optflags" ./configure --prefix=%_prefix
! grep -wE 'NO_vsnprintf|HAS_vsprintf_void|HAS_vsnprintf_void|NO_snprintf|HAS_sprintf_void|HAS_snprintf_void' Makefile
%__make
%__make test
rm -f *.s *.o

# next build and test shared zlib
CFLAGS="%optflags -fPIC" ./configure --prefix=%_prefix --shared
! grep -wE 'NO_vsnprintf|HAS_vsprintf_void|HAS_vsnprintf_void|NO_snprintf|HAS_sprintf_void|HAS_snprintf_void' Makefile
%__make
%__make test

bzip2 -9fk ChangeLog FAQ algorithm.txt

%install
rm -rf %buildroot
mkdir -p %buildroot{%_libdir,%_includedir,%_mandir/man3}

cp -a libz.* %buildroot%_libdir/
install -p -m644 zlib.h zconf.h %buildroot%_includedir/
install -p -m644 zlib.3 %buildroot%_mandir/man3/

%define docdir %_docdir/%name-%version
mkdir -p %buildroot%docdir
install -p -m644 License README {FAQ,ChangeLog,algorithm.txt}.bz2 \
	example.c minigzip.c %buildroot%docdir/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%_libdir/libz.so.*
%dir %docdir
%docdir/License
%docdir/README

%files devel
%defattr(-,root,root)
%_libdir/*.a
%_libdir/*.so
%_includedir/*
%_mandir/man?/*
%dir %docdir
%docdir/*.c
%docdir/*.bz2

%changelog
* Sun Oct 23 2005 Dmitry V. Levin <ldv@owl.openwall.com> 1.2.3-owl1
- Updated to 1.2.3.
- Imported a bunch of patches from ALT's zlib-1.2.3-alt2 package,
including versioning for exported symbols added after zlib-1.1.4.
- Reviewed Owl patches, removed obsolete ones.
- Updated URL per Mark Adler suggestion.

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

# $Id: Owl/packages/zlib/zlib.spec,v 1.1 2000/08/09 00:51:27 kad Exp $

Summary: The zlib compression and decompression library.
Name: 		zlib
Version: 	1.1.3
Release: 	11owl
Group: 		System Environment/Libraries
Source: 	ftp://ftp.info-zip.org/pub/infozip/zlib/zlib-%{version}.tar.gz
Patch0: 	zlib-1.1.3-rh-glibc.diff
URL: 		http://www.info-zip.org/pub/infozip/zlib/
Copyright: 	BSD
Prefix: 	%{_prefix}
BuildRoot: 	/var/rpm-buildroot/%{name}-root

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

Install the zlib-devel package if you want to develop applications that
will use the zlib library.

%prep
%setup -q
%patch0 -p1 -b .glibc

%build


CFLAGS="$RPM_OPT_FLAGS" ./configure --shared --prefix=%{_prefix}
make
# now build the static lib
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix}
make

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}

CFLAGS="$RPM_OPT_FLAGS" ./configure --shared --prefix=%{_prefix}
make install prefix=${RPM_BUILD_ROOT}%{_prefix}

CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix}
make install prefix=${RPM_BUILD_ROOT}%{_prefix}

install -m644 zutil.h ${RPM_BUILD_ROOT}%{_includedir}/zutil.h
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3
install -m644 zlib.3 ${RPM_BUILD_ROOT}%{_mandir}/man3

%clean
rm -rf ${RPM_BUILD_ROOT}

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
* Sun Aug  6 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul 02 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Tue Jun 13 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging to build on solaris2.5.1.

* Wed Jun 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_mandir} and %%{_tmppath}

* Fri May 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- updated URL and source location
- moved README to main package

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man page.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- link against glibc

* Mon Jul 27 1998 Jeff Johnson <jbj@redhat.com>
- upgrade to 1.1.3

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.1.2
- buildroot

* Tue Oct 07 1997 Donnie Barnes <djb@redhat.com>
- added URL tag (down at the moment so it may not be correct)
- made zlib-devel require zlib

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

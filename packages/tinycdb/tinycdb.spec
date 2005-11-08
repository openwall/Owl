# $Id: Owl/packages/tinycdb/tinycdb.spec,v 1.2 2005/11/08 01:47:12 ldv Exp $

Name: tinycdb
Version: 0.75
Release: owl1

Summary: Shared library and command line tool for managing constant databases.
License: GPL/LGPL
Group: System Environment/Libraries
URL: http://www.corpit.ru/mjt/tinycdb.html

Source: ftp://ftp.corpit.ru/pub/tinycdb/tinycdb_%version.tar.gz

Patch0: tinycdb-0.75-alt-progname.diff
Patch1: tinycdb-0.75-alt-warnings.diff
Patch2: tinycdb-0.75-alt-doc.diff
Patch3: tinycdb-0.75-alt-Makefile.diff

BuildRoot: /override/%name-%version

%description
tinycdb is a small, fast and reliable utility set and subroutine library
for creating and reading constant databases.  The database structure is
tuned for fast reading:
+ Successful lookups take normally just two disk accesses.
+ Unsuccessful lookups take only one disk access.
+ Small disk space and memory size requirements; a database uses 2048
  bytes for the header and 24 bytes per record.
+ Maximum database size is 4GB; individual record size is not
  otherwise limited.
+ Portable file format.
+ Fast creation of new databases.
+ No locking, updates are atomical.

This package contains tinycdb shared library and command line tool for
managing constant databases.

%package devel
Summary: Development files for the tinycdb library.
License: LGPL
Group: System Environment/Libraries
Requires: %name = %version-%release

%description devel
tinycdb is a small, fast and reliable utility set and subroutine
library for creating and reading constant databases.

This package contains tinycdb development libraries and header files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%__make CFLAGS="%optflags -Wall -W -D_GNU_SOURCE"
%__make check

%install
rm -rf %buildroot
%makeinstall

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%_bindir/*
%_mandir/man1/*
%_libdir/libcdb.so.*
%doc ChangeLog NEWS

%files devel
%defattr(-,root,root)
%_libdir/libcdb.a
%_libdir/libcdb.so
%_mandir/man[35]/*
%_includedir/*

%changelog
* Mon Nov 07 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.75-owl1
- Initial build for Openwall GNU/*/Linux, based on ALT package.

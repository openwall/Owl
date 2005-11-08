# $Id: Owl/packages/pcre/pcre.spec,v 1.1 2005/11/08 01:32:02 ldv Exp $

Name: pcre
Version: 6.4
Release: owl1

Summary: Perl-compatible regular expression library.
License: BSD
Group: System Environment/Libraries
URL: http://www.pcre.org/

Source0: ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-%version.tar.bz2
Source1: pcre-config.1
Source2: zpcregrep

Patch0: pcre-6.3-deb-pcreposix.diff
Patch1: pcre-6.3-deb-pcregrep.diff
Patch2: pcre-6.3-deb-pcretest.diff
Patch3: pcre-6.3-alt-Makefile.diff
Patch4: pcre-6.4-owl-testdata.diff
Patch5: pcre-5.0-rh-libdir.diff

BuildRequires: autoconf, automake, libtool, sed >= 4.1.1

BuildRoot: /override/%name-%version

%description
The PCRE library is a set of functions that implement regular expression
pattern matching using the same syntax and semantics as Perl, with
just a few differences.  The current implementation of PCRE corresponds
approximately with Perl 5.8.

This package contains PCRE shared libraries, pcregrep - a grep with
Perl-compatible regular expressions, and pcretest - a program for testing
Perl-compatible regular expressions.

%package devel
Summary: Development files for the Perl-compatible regular expression library.
Group: System Environment/Libraries
Requires: %name = %version-%release

%description devel
The PCRE library is a set of functions that implement regular expression
pattern matching using the same syntax and semantics as Perl, with
just a few differences.  The current implementation of PCRE corresponds
approximately with Perl 5.8.

This package contains PCRE development libraries and header files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# Fix configure.in; bundled one is broken.
sed -i '/^AC_LIBTOOL_WIN32_DLL/ d;s/AM_PROG_LIBTOOL/AC_PROG_LIBTOOL/' configure.in

%build
# Regenerate configure script; bundled one is broken.
aclocal --force
libtoolize --force
autoconf --force

%configure --includedir=%_includedir/pcre --disable-cpp --enable-utf8
%__make
bzip2 -9fk ChangeLog
%__make check

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot

install -pm644 %_sourcedir/pcre-config.1 %buildroot%_mandir/man1/
install -pm755 %_sourcedir/zpcregrep %buildroot%_bindir/
ln -s pcregrep.1.gz %buildroot%_mandir/man1/zpcregrep.1.gz

rm -f %buildroot%_libdir/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%_bindir/*pcregrep
%_bindir/pcretest
%_libdir/*.so.*
%_mandir/man1/*pcregrep.*
%_mandir/man1/pcretest.*
%doc AUTHORS ChangeLog.bz2 LICENCE NEWS README

%files devel
%defattr(-,root,root)
%_bindir/pcre-config
%_libdir/*.a
%_libdir/*.so
%_libdir/pkgconfig/*
%_includedir/pcre
%_mandir/man1/pcre-config.*
%_mandir/man3/*

%changelog
* Mon Nov 07 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 6.4-owl1
- Initial build for Openwall GNU/*/Linux, based on ALT package.

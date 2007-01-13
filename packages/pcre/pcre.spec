# $Owl: Owl/packages/pcre/pcre.spec,v 1.6 2007/01/13 02:28:12 galaxy Exp $

Summary: Perl-compatible regular expression library.
Name: pcre
Version: 7.0
Release: owl1
License: BSD
Group: System Environment/Libraries
URL: http://www.pcre.org
Source0: ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-%version.tar.bz2
Source1: pcre-config.1
Patch0: pcre-6.6-deb-alt-shlib.diff
Patch1: pcre-6.3-deb-pcretest.diff
Patch2: pcre-6.4-owl-testdata.diff
Patch3: pcre-6.6-rh-multilib.diff
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

bzip2 -9fk ChangeLog

# Fix configure.in; bundled one is broken.
sed -i '/^AC_LIBTOOL_WIN32_DLL/ d' configure.ac

%build
# Regenerate configure script; bundled one is broken.
aclocal --force
libtoolize --force
autoconf --force

%configure --includedir=%_includedir/pcre --disable-cpp --enable-utf8
%__make
%__make check

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot

# Relocate shared libraries from %_libdir/ to /%_lib/.
mkdir %buildroot/%_lib
for f in %buildroot%_libdir/*.so; do
	t=`objdump -p "$f" |awk '/SONAME/ {print $2}'`
	[ -n "$t" ]
	ln -sf ../../%_lib/"$t" "$f"
done
mv %buildroot%_libdir/*.so.* %buildroot/%_lib/

install -pm644 %_sourcedir/pcre-config.1 %buildroot%_mandir/man1/

rm %buildroot%_bindir/pcregrep
rm %buildroot%_mandir/man1/pcregrep.*
rm %buildroot%_libdir/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%_bindir/pcretest
/%_lib/*.so.*
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
* Sat Jan 13 2007 (GalaxyMaster) <galaxy-at-owl.openwall.com> 7.0-owl1
- Updated to 7.0.

* Tue Nov 14 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 6.7-owl1
- Updated to 6.7.
- Relocated the compression of ChangeLog to the %%prep section.

* Wed Nov 30 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 6.4-owl2
- Relocated shared libraries from %_libdir/ to /%_lib/.
- Moved pcregrep to grep package.

* Mon Nov 07 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 6.4-owl1
- Initial build for Openwall GNU/*/Linux, based on ALT package.

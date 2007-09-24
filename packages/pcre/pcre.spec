# $Owl: Owl/packages/pcre/pcre.spec,v 1.8 2007/09/24 23:03:35 ldv Exp $

Summary: Perl-compatible regular expression library.
Name: pcre
Version: 7.4
Release: owl1
License: BSD-style
Group: System Environment/Libraries
URL: http://www.pcre.org
Source0: ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-%version.tar.bz2
Source1: pcre-config.1
Patch0: pcre-7.4-deb-pcreposix.diff
Patch1: pcre-7.4-deb-pcretest.diff
Patch2: pcre-7.4-rh-multilib.diff
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

%build
# Replace with autoreconf after toolchain update.
%undefine __libtoolize

%define docdir %_docdir/%name-%version
%configure --includedir=%_includedir/pcre --docdir=%docdir \
	--disable-cpp --enable-utf8
%__make
%__make check

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot

# Relocate shared libraries from %_libdir/ to /%_lib/.
mkdir %buildroot/%_lib
for f in %buildroot%_libdir/*.so; do
	t=`objdump -p "$f" |awk '$1=="SONAME"{print $2}'`
	[ -n "$t" ]
	ln -sf ../../%_lib/"$t" "$f"
done
mv %buildroot%_libdir/*.so.* %buildroot/%_lib/

install -pm644 %_sourcedir/pcre-config.1 %buildroot%_mandir/man1/
bzip2 -9 %buildroot%docdir/ChangeLog
install -pm644 HACKING pcredemo.c %buildroot%docdir/

rm %buildroot%_bindir/pcregrep
rm %buildroot%_mandir/man1/pcregrep.*
rm %buildroot%_libdir/*.la
rm -r %buildroot%docdir/{README,html,*.txt}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%_bindir/pcretest
/%_lib/*.so.*
%_mandir/man1/pcretest.*
%dir %docdir
%docdir/AUTHORS
%docdir/COPYING
%docdir/ChangeLog.bz2
%docdir/LICENCE
%docdir/NEWS

%files devel
%defattr(-,root,root)
%_bindir/pcre-config
%_libdir/*.a
%_libdir/*.so
%_libdir/pkgconfig/*
%_includedir/pcre
%_mandir/man1/pcre-config.*
%_mandir/man3/*
%dir %docdir
%docdir/HACKING
%docdir/*.c

%changelog
* Mon Sep 24 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 7.4-owl1
- Updated to 7.4.

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

# $Owl: Owl/packages/pcre/pcre.spec,v 1.11 2009/05/27 17:22:50 ldv Exp $

%{?!BUILD_CPP: %define BUILD_CPP 0}

Summary: Perl-compatible regular expression library.
Name: pcre
Version: 7.9
Release: owl1
License: BSD-style
Group: System Environment/Libraries
URL: http://www.pcre.org
Source0: ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-%version.tar.bz2
Source1: pcre-config.1
Patch0: pcre-7.9-deb-pcreposix.diff
Patch1: pcre-7.9-deb-pcretest.diff
Patch2: pcre-7.4-rh-multilib.diff
BuildRequires: autoconf, automake, libtool, sed >= 4.1.1
%if %BUILD_CPP
BuildRequires: gcc-c++
%endif
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
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
The PCRE library is a set of functions that implement regular expression
pattern matching using the same syntax and semantics as Perl, with
just a few differences.  The current implementation of PCRE corresponds
approximately with Perl 5.8.

This package contains PCRE development libraries and header files.

%package -n libpcrecpp
Summary: Perl-compatible regular expressions C++ wrapper shared library.
Group: System Environment/Libraries
Requires: %name = %version-%release

%description -n libpcrecpp
The PCRE library is a set of functions that implement regular expression
pattern matching using the same syntax and semantics as Perl, with
just a few differences.  The current implementation of PCRE corresponds
approximately with Perl 5.8.

This package contains PCRE C++ wrapper shared library.

%package -n libpcrecpp-devel
Summary: Perl-compatible regular expressions C++ wrapper development files.
Group: Development/Libraries
Requires: libpcrecpp = %version-%release, %name-devel = %version-%release

%description -n libpcrecpp-devel
The PCRE library is a set of functions that implement regular expression
pattern matching using the same syntax and semantics as Perl, with
just a few differences.  The current implementation of PCRE corresponds
approximately with Perl 5.8.

This package contains PCRE C++ wrapper development library and header files.

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
	--enable-utf8 --enable-unicode-properties \
%if %BUILD_CPP
	--enable-cpp
%else
	--disable-cpp
%endif
%__make
%__make check

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot

# Relocate shared libraries from %_libdir/ to /%_lib/.
mkdir %buildroot/%_lib
for f in %buildroot%_libdir/libpcre{,posix}.so; do
	t=`objdump -p "$f" |awk '$1=="SONAME"{print $2}'`
	[ -n "$t" ]
	ln -sf ../../%_lib/"$t" "$f"
done
mv %buildroot%_libdir/libpcre{,posix}.so.* %buildroot/%_lib/

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
/%_lib/libpcre.so.*
/%_lib/libpcreposix.so.*
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
%_libdir/libpcre.so
%_libdir/libpcreposix.so
%_libdir/libpcre.a
%_libdir/libpcreposix.a
%_libdir/pkgconfig/libpcre.pc
%_includedir/pcre
%_mandir/man1/pcre-config.*
%_mandir/man3/*
%if %BUILD_CPP
%exclude %_includedir/pcre/pcrecpp*.h
%exclude %_includedir/pcre/pcre_*.h
%exclude %_mandir/man3/pcrecpp.*
%endif
%dir %docdir
%docdir/HACKING
%docdir/*.c

%if %BUILD_CPP
%files -n libpcrecpp
%_libdir/libpcrecpp.so.*

%files -n libpcrecpp-devel
%_libdir/libpcrecpp.so
%_libdir/libpcrecpp.a
%dir %_includedir/pcre
%_includedir/pcre/pcrecpp*.h
%_includedir/pcre/pcre_*.h
%_libdir/pkgconfig/libpcrecpp.pc
%_mandir/man3/pcrecpp.*
%endif

%changelog
* Wed May 27 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 7.9-owl1
- Updated to 7.9.

* Wed Feb 13 2008 Dmitry V. Levin <ldv-at-owl.openwall.com> 7.6-owl1
- Updated to 7.6.

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

# $Owl: Owl/packages/mpfr/mpfr.spec,v 1.1 2011/10/21 17:03:41 segoon Exp $

Summary: A C library for multiple-precision floating-point computations.
Name: mpfr
Version: 3.0.1
Release: owl1
License: LGPLv3+ and GPLv3+ and GFDL
Group: System Environment/Libraries
URL: http://www.mpfr.org/
Source0: http://www.mpfr.org/mpfr-current/%name-%version.tar.xz
# Signature: http://www.mpfr.org/mpfr-current/mpfr-%version.tar.xz.asc
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: gmp >= 4.2.1
%ifarch x86_64 s390x sparc64 ppc64
Provides: libmpfr.so.1()(64bit)
%else
Provides: libmpfr.so.1
%endif
BuildRequires: autoconf libtool gmp-devel
BuildRoot: /override/%name-%version

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and 
also has a well-defined semantics. It copies the good ideas from the 
ANSI/IEEE-754 standard for double-precision floating-point arithmetic 
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%package devel
Summary: Development tools A C library for mpfr library.
Group: Development/Libraries
Requires: %name = %version-%release
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: gmp-devel

%description devel
Header files and documentation for using the MPFR 
multiple-precision floating-point library in applications.

If you want to develop applications which will use the MPFR library,
you'll need to install the mpfr-devel package.  You'll also need to
install the mpfr package.

%prep
%setup -q

%build
%configure --disable-assert
%__make

%install
rm -rf %buildroot

#iconv  -f iso-8859-1 -t utf-8 mpfr.info >mpfr.info.aux
#mv mpfr.info.aux mpfr.info

%__make install DESTDIR=%buildroot
cd ..
mkdir %buildroot/%_docdir/%name-%version
mv %buildroot/%_docdir/%name/ %buildroot/%_docdir/%name-%version/
ln -s libmpfr.so.4.0.0 %buildroot%_libdir/libmpfr.so.1
ln -s libmpfr.so.4.0.0 %buildroot%_libdir/libmpfr.so.1.2.2

%check
%__make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %_infodir/mpfr.info.gz %_infodir/dir || :

%preun devel
if [ "$1" -eq 0 ]; then
	/sbin/install-info --delete %_infodir/mpfr.info.gz %_infodir/dir || :
fi

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LESSER NEWS README
%_libdir/libmpfr.so.*
%exclude %_libdir/libmpfr.la
%exclude %_libdir/libmpfr.a
%exclude %_infodir/dir

%files devel
%defattr(-,root,root,-)
%_libdir/libmpfr.so
%_includedir/*.h
%_infodir/mpfr.info*

%changelog
* Fri Oct 21 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 3.0.1-owl1
- Initial import from Fedora.

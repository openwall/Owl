# $Owl: Owl/packages/libmpc/libmpc.spec,v 1.1 2011/10/21 17:04:48 segoon Exp $

Summary: C library for multiple precision complex arithmetic.
Name: libmpc
Version: 0.9
Release: owl1
License: LGPLv2+
Group: Development/Tools
URL: http://www.multiprecision.org/
Source0: mpc-%version.tar.xz
# http://www.multiprecision.org/mpc/download/mpc-%version.tar.gz
# Signature: http://www.multiprecision.org/mpc/download/mpc-%version.tar.gz.asc
BuildRequires: gmp-devel >= 4.3.2
BuildRequires: mpfr-devel >= 2.4.2
BuildRequires: texinfo
BuildRoot: /override/%name-%version

%description
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as Mpfr.

%package devel
Summary: Header and shared development libraries for MPC.
Group: Development/Libraries
Requires: %name = %version-%release
Requires: mpfr-devel gmp-devel

%description devel
Header files and shared object symlinks for MPC is a C library.

%prep
%setup -q -n mpc-%version

%build
export EGREP=egrep
%configure
%__make

%check
%__make check

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %_infodir/mpc.info.gz %_infodir/dir || :

%preun devel
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/mpc.info.gz %_infodir/dir || :
fi

%files
%defattr(-,root,root,-)
%doc README NEWS COPYING.LIB
%_libdir/libmpc.so.*
%exclude %_libdir/libmpc.la
%exclude %_libdir/libmpc.a
%exclude %_infodir/dir

%files devel
%defattr(-,root,root,-)
%_libdir/libmpc.so
%_includedir/mpc.h
%_infodir/*.info*

%changelog
* Fri Oct 21 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 0.9-owl1
- Initial import from Fedora.


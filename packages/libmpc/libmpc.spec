# $Owl: Owl/packages/libmpc/libmpc.spec,v 1.6 2015/01/11 23:53:15 solar Exp $

Summary: C library for multiple precision complex arithmetic.
Name: libmpc
Version: 1.0.2
Release: owl1
License: LGPLv2+
Group: Development/Tools
URL: http://www.multiprecision.org
Source0: mpc-%version.tar.xz
# http://www.multiprecision.org/mpc/download/mpc-%version.tar.gz
# Signature: http://www.multiprecision.org/mpc/download/mpc-%version.tar.gz.sig
BuildRequires: autoconf >= 2.61
BuildRequires: gmp-devel >= 4.3.2
BuildRequires: mpfr-devel >= 2.4.2
BuildRequires: texinfo
BuildRoot: /override/%name-%version

%description
MPC is a C library for the arithmetic of complex numbers with arbitrarily high
precision and correct rounding of the result.  It is built upon and follows the
same principles as MPFR.

%package devel
Summary: Development files for the MPC library.
Group: Development/Libraries
Requires: %name = %version-%release
Requires: mpfr-devel gmp-devel
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description devel
Header files, static library, and documentation for using the MPC library in
applications.

%prep
%setup -q -n mpc-%version

autoreconf -fis

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
%doc README NEWS COPYING.LESSER
%_libdir/libmpc.so.*
%exclude %_libdir/libmpc.la
%exclude %_libdir/libmpc.a

%files devel
%defattr(-,root,root,-)
%_libdir/libmpc.so
%_libdir/libmpc.a
%_includedir/mpc.h
%_infodir/*.info*
%exclude %_infodir/dir

%changelog
* Thu Jan 23 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.0.2-owl1
- Updated to 1.0.2.

* Fri Oct 21 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 0.9-owl1
- Initial import from Fedora.

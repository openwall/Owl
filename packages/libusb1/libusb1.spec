# $Owl: Owl/packages/libusb1/libusb1.spec,v 1.2.2.2 2011/09/07 07:43:14 solar Exp $

Summary: A library for accessing USB devices.
Name: libusb1
Version: 1.0.8
Release: owl1
License: LGPLv2+
Group: System Environment/Libraries
URL: http://libusb.wiki.sourceforge.net/Libusb1.0
Source0: http://downloads.sourceforge.net/libusb/libusb-%version.tar.bz2
BuildRoot: /override/%name-%version

%description
This package provides a way for applications to access USB devices.  Note that
this library is not compatible with the original libusb-0.1 series.

%package devel
Summary: Development files for libusb.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
This package contains the header files, libraries, and documentation needed to
develop applications that use libusb1.

%prep
%setup -q -n libusb-%version

%build
%configure
%__make

%install
rm -rf %buildroot
make install DESTDIR=%buildroot
rm -f %buildroot%_libdir/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README NEWS ChangeLog
%_libdir/*.so.*

%files devel
%defattr(-,root,root)
%doc examples/*.c
%_includedir/*
%_libdir/*.a
%_libdir/*.so
%exclude %_libdir/pkgconfig/libusb-1.0.pc

%changelog
* Thu Jan 27 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.0.8-owl1
- Initial import from Fedora.
- Updated to 1.0.8.

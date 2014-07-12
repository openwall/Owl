# $Owl: Owl/packages/libusb-compat/libusb-compat.spec,v 1.3 2014/07/12 14:09:27 galaxy Exp $

Summary: A library which allows userspace access to USB devices.
Name: libusb-compat
Version: 0.1.3
Release: owl2
License: LGPLv2+
Group: System Environment/Libraries
URL: http://www.libusb.org/wiki/LibusbCompat0.1
Source0: http://downloads.sourceforge.net/project/libusb/libusb-compat-0.1/libusb-compat-%version/libusb-compat-%version.tar.bz2
Patch0: libusb-compat-0.1.3-owl-configure.diff
Requires: libusb1
Provides: libusb
BuildRequires: libtool >= 2.4.2
BuildRequires: libusb1-devel
BuildRoot: /override/%name-%version

%description
A compatibility layer allowing applications written for libusb-0.1 to work
with libusb-1.0. libusb-compat-0.1 attempts to look, feel, smell and walk
like libusb-0.1.

%package devel
Summary: Development files for libusb-compat.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
This package contains the header files, libraries and documentation needed to
develop applications that use libusb-compat.

%prep
%setup -q
%patch0 -p1
autoreconf -fis -I m4

%build
# Workaround - we have no pkg-config yet
export LIBUSB_1_0_CFLAGS=-I%_includedir/libusb-1.0/
export LIBUSB_1_0_LIBS=-lusb-1.0
%configure
%__make

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%_libdir/libusb-0.1.so.*
%exclude %_libdir/libusb.la

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog INSTALL LICENSE NEWS README
%_bindir/libusb-config
%_includedir/usb.h
%_libdir/libusb.so
%_libdir/pkgconfig/libusb.pc
%_libdir/libusb.a

%changelog
* Sun Jun 29 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.1.3-owl2
- Regenerated the configure patch since it was fuzzy.
- Enforced the regeneration of autotools scripts.

* Sat Feb 05 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 0.1.3-owl1
- Initial import of Jan Vcelak's spec:
http://jvcelak.fedorapeople.org/libusb-compat/

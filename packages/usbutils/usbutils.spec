Summary: Linux USB utilities
Name: usbutils
Version: 001
Release: owl1
License: GPLv2+
Group: Applications/System
URL: http://www.linux-usb.org/
Source: http://www.kernel.org/pub/linux/utils/usb/usbutils/%name-%version.tar.bz2
# Source: http://downloads.sourceforge.net/linux-usb/%name-%version.tar.bz2
Patch0: usbutils-001-owl-lftp.diff
BuildRequires: libusb1-devel
BuildRoot: /override/%name-%version

%description 
This package contains the lsusb utility for inspecting the devices
connected to the USB bus. It shows a representation of the devices that
are currently plugged in, showing the topology of the USB bus. It also
displays information on each individual device on the bus.

More information can be found at the Linux USB web site:
http://www.linux-usb.org/

%prep
%setup -q
%patch0 -p1
# autoreconf

%build
# Workaround - we have no pkg-config yet
export LIBUSB_CFLAGS=-I%_includedir/libusb-1.0/
export LIBUSB_LIBS=-lusb-1.0
%configure
%__make

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot INSTALL="install -p"

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%_mandir/man1/*
%_mandir/man8/*
%_sbindir/update-usbids.sh
%_bindir/*
%_datadir/usb.ids.gz
%exclude %_datadir/usb.ids
%exclude %_datadir/pkgconfig/usbutils.pc

%changelog
* Thu Jan 27 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 001-owl1
- Initial import from Fedora.
- Updated to 001.
- Fixed update-usbids.sh to gzip the database and use lftp.

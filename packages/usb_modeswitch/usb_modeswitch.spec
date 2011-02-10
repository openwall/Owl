# $Owl: Owl/packages/usb_modeswitch/usb_modeswitch.spec,v 1.2 2011/02/10 17:36:08 solar Exp $

%define source_name	usb-modeswitch

Summary: USB Modeswitch gets 4G cards in operational mode.
Name: usb_modeswitch
Version: 1.1.6
Release: owl1
License: GPLv2+
Group: Applications/System
URL: http://www.draisberghof.de/usb_modeswitch/
Source0: http://www.draisberghof.de/%name/%source_name-%version.tar.bz2
Patch0: usb_modeswitch-1.1.6-owl-fixes.diff
Requires: usb_modeswitch-data
BuildRequires: libusb1-devel
BuildRoot: /override/%name-%version

%description
USB Modeswitch brings up your datacard into operational mode. When plugged
in they identify themselves as cdrom and present some non-Linux compatible
installation files. This tool deactivates this cdrom-devices and enables
the real communication device. It supports most devices built and
sold by Huawei, T-Mobile, Vodafone, Option, ZTE, Novatel.

%prep
%setup -q -n %source_name-%version
%patch0 -p1

%build
%__make

%install
rm -rf %buildroot
mkdir -p %buildroot%_sbindir
mkdir -p %buildroot%_mandir/man1

install -p -m 755 usb_modeswitch %buildroot%_sbindir/
install -m 644 usb_modeswitch.1 %buildroot%_datadir/man/man1

%files
%defattr(-,root,root,-)
%_sbindir/usb_modeswitch
%_mandir/man1/usb_modeswitch.1.gz
%doc COPYING README ChangeLog device_reference.txt 

%changelog
* Sat Feb 05 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.1.6-owl1
- Initial import from Fedora.
- Added owl-warnings patch to fix memory leak.

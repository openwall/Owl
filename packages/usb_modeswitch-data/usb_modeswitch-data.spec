# $Owl: Owl/packages/usb_modeswitch-data/usb_modeswitch-data.spec,v 1.1 2011/02/05 18:21:28 segoon Exp $

%define source_name	usb-modeswitch-data

Summary: USB Modeswitch gets 4G cards in operational mode.
Name: usb_modeswitch-data
Version: 20101222
Release: owl1
License: GPLv2+
Group: Applications/System
URL: http://www.draisberghof.de/usb_modeswitch/
Source0: http://www.draisberghof.de/%name/%source_name-%version.tar.bz2
Requires: usb_modeswitch >= 1.1.2
BuildRoot: /override/%name-%version

%description
USB Modeswitch brings up your datacard into operational mode. When plugged
in they identify themselves as cdrom and present some non-Linux compatible
installation files. This tool deactivates this cdrom-devices and enables
the real communication device. It supports most devices built and
sold by Huawei, T-Mobile, Vodafone, Option, ZTE, Novatel.

This package contains the data files needed for usb_modeswitch to function.

%prep
%setup -q -n %source_name-%version

%install
rm -rf %buildroot
mkdir -p %buildroot%_sysconfdir/usb_modeswitch.d/
install -p -m 644  usb_modeswitch.d/* %buildroot%_sysconfdir/usb_modeswitch.d/

%files
%defattr(-,root,root,-)
%_sysconfdir/usb_modeswitch.d/
%doc ChangeLog COPYING README

%changelog
* Sat Feb 05 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 20101222-owl1
- Initial import from Fedora.

# $Owl: Owl/packages/usb_modeswitch-data/usb_modeswitch-data.spec,v 1.2.2.2 2011/09/07 07:44:22 solar Exp $

%define source_name	usb-modeswitch-data

Summary: Data files needed for usb_modeswitch.
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
USB_ModeSwitch is a mode switching tool for controlling "flip flop" (multiple
device) USB gear.

This package contains the data files needed for usb_modeswitch to function.

%prep
%setup -q -n %source_name-%version

%install
rm -rf %buildroot
mkdir -p %buildroot%_sysconfdir/usb_modeswitch.d/
install -p -m 644 usb_modeswitch.d/* %buildroot%_sysconfdir/usb_modeswitch.d/

%files
%defattr(-,root,root,-)
%_sysconfdir/usb_modeswitch.d/
%doc ChangeLog COPYING README

%changelog
* Sat Feb 05 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 20101222-owl1
- Initial import from Fedora.

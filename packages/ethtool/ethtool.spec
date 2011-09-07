# $Owl: Owl/packages/ethtool/ethtool.spec,v 1.3.2.2 2011/09/07 07:42:10 solar Exp $

Summary: Utility for controlling network drivers and hardware.
Name: ethtool
Version: 2.6.37
Release: owl1
Epoch: 2
License: GPLv2
Group: Applications/System
URL: http://www.kernel.org/pub/software/network/ethtool/
# URL: http://sourceforge.net/projects/gkernel/
Source: http://www.kernel.org/pub/software/network/%name/%name-%version.tar.bz2
# Signature: http://www.kernel.org/pub/software/network/%name/%name-%version.tar.bz2.sign
BuildRequires: automake, autoconf
BuildRoot: /override/%name-%version

%description
ethtool is the standard Linux utility for controlling network drivers and
hardware, particularly for wired Ethernet devices.  It can be used to:

* Get identification and diagnostic information
* Get extended device statistics
* Control speed, duplex, autonegotiation, and flow control for Ethernet devices
* Control checksum offload and other hardware offload features
* Control DMA ring sizes and interrupt moderation
* Control receive queue selection for multiqueue devices
* Upgrade firmware in flash memory

Most features are dependent on support in the specific driver.  See the manual
page for full information.

%prep
%setup -q

%build
%configure
%__make

%install
rm -rf %buildroot
%__make DESTDIR=%buildroot INSTALL='install -p' install

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING LICENSE NEWS README
%_sbindir/%name
%_mandir/man8/%name.8*

%changelog
* Thu Jan 27 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2:2.6.37-owl1
- Initial import from Fedora.
- Updated to 2.6.37.

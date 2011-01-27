Summary: Ethernet settings tool for PCI ethernet cards
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

BuildRequires:	automake, autoconf
BuildRoot: /override/%name-%version

%description
This utility allows querying and changing settings such as speed,
port, autonegotiation, PCI locations and checksum offload on many
network devices, especially of ethernet devices.

%prep
%setup -q

%build
%configure
%__make

%install
rm -rf %buildroot
%__make DESTDIR=%buildroot INSTALL='install -p' install

%clean
rm -rf %buildroot

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING LICENSE NEWS README
%_sbindir/%name
%_mandir/man8/%name.8*

%changelog
* Thu Jan 27 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.37-owl1
- Initial import from Fedora.
- Updated to 2.6.37.

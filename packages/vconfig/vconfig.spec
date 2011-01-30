# $Owl: Owl/packages/vconfig/vconfig.spec,v 1.3 2011/01/30 17:00:20 solar Exp $

Summary: Linux 802.1q VLAN configuration utility.
Name: vconfig
Version: 1.9
Release: owl1
License: GPLv2+
Group: System Environment/Base
URL: http://www.candelatech.com/~greear/vlan.html
Source: http://www.candelatech.com/~greear/vlan/vlan.%version.tar.gz
BuildRoot: /override/%name-%version

%description
This package contains the user mode program to add and remove 802.1q VLAN
virtual devices from Ethernet devices.  A typical application for a VLAN
enabled box is a single wire firewall, router, or load balancer.

%prep
%setup -q -n vlan
rm macvlan_config* vconfig vconfig.o

%{expand:%%define optflags %optflags -Wall -D_GNU_SOURCE}

%build
%__make clean
rm vconfig
%__make STRIP=/bin/true CCFLAGS="%optflags" vconfig
rm -rf contrib/

%install
rm -rf %buildroot
%__install -D -m755 vconfig %buildroot%_sbindir/vconfig
%__install -D -m644 vconfig.8 %buildroot%_mandir/man8/vconfig.8

%files
%defattr(-,root,root,0755)
%doc CHANGELOG README vlan.html vlan_test.pl
%attr(700,root,root) %_sbindir/vconfig
%_mandir/man8/vconfig.8*

%changelog
* Sun Jan 30 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.9-owl1
- Initial import from Fedora.

# $Id: Owl/packages/net-tools/net-tools.spec,v 1.11 2005/10/23 16:58:11 galaxy Exp $

Summary: The basic tools for setting up networking.
Name: net-tools
Version: 1.60
Release: owl1
License: GPL
Group: System Environment/Base
Source0: http://www.tazenda.demon.co.uk/phil/net-tools/net-tools-%version.tar.bz2
Source1: net-tools-1.57-config.h
Source2: net-tools-1.57-config.make
Patch0: net-tools-1.57-owl-fixes.diff
Patch1: net-tools-1.60-owl-x25_address.diff
BuildRoot: /override/%name-%version

%description
The net-tools package contains the basic tools needed for setting up
networking: ethers, route and others.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

cp %_sourcedir/net-tools-1.57-config.h config.h
cp %_sourcedir/net-tools-1.57-config.make config.make

%build
%__make CC="%__cc" COPTS="%optflags -D_GNU_SOURCE -Wall"

%install
rm -rf %buildroot
mkdir -p %buildroot/{bin,sbin}
mkdir -p %buildroot%_mandir/man{1,5,8}

%__make BASEDIR=%buildroot mandir=%_mandir install

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot%_datadir/locale/cs/LC_MESSAGES/net-tools.mo
rm %buildroot%_datadir/locale/de/LC_MESSAGES/net-tools.mo
rm %buildroot%_datadir/locale/et_EE/LC_MESSAGES/net-tools.mo
rm %buildroot%_datadir/locale/fr/LC_MESSAGES/net-tools.mo
rm %buildroot%_datadir/locale/pt_BR/LC_MESSAGES/net-tools.mo
rm %buildroot%_mandir/de_DE/man1/dnsdomainname.1*
rm %buildroot%_mandir/de_DE/man1/domainname.1*
rm %buildroot%_mandir/de_DE/man1/hostname.1*
rm %buildroot%_mandir/de_DE/man1/nisdomainname.1*
rm %buildroot%_mandir/de_DE/man1/ypdomainname.1*
rm %buildroot%_mandir/de_DE/man5/ethers.5*
rm %buildroot%_mandir/de_DE/man8/arp.8*
rm %buildroot%_mandir/de_DE/man8/ifconfig.8*
rm %buildroot%_mandir/de_DE/man8/netstat.8*
rm %buildroot%_mandir/de_DE/man8/plipconfig.8*
rm %buildroot%_mandir/de_DE/man8/rarp.8*
rm %buildroot%_mandir/de_DE/man8/route.8*
rm %buildroot%_mandir/de_DE/man8/slattach.8*
rm %buildroot%_mandir/fr_FR/man1/dnsdomainname.1*
rm %buildroot%_mandir/fr_FR/man1/domainname.1*
rm %buildroot%_mandir/fr_FR/man1/hostname.1*
rm %buildroot%_mandir/fr_FR/man1/nisdomainname.1*
rm %buildroot%_mandir/fr_FR/man1/ypdomainname.1*
rm %buildroot%_mandir/fr_FR/man5/ethers.5*
rm %buildroot%_mandir/fr_FR/man8/arp.8*
rm %buildroot%_mandir/fr_FR/man8/ifconfig.8*
rm %buildroot%_mandir/fr_FR/man8/netstat.8*
rm %buildroot%_mandir/fr_FR/man8/plipconfig.8*
rm %buildroot%_mandir/fr_FR/man8/rarp.8*
rm %buildroot%_mandir/fr_FR/man8/route.8*
rm %buildroot%_mandir/fr_FR/man8/slattach.8*
rm %buildroot%_mandir/pt_BR/man1/dnsdomainname.1*
rm %buildroot%_mandir/pt_BR/man1/domainname.1*
rm %buildroot%_mandir/pt_BR/man1/hostname.1*
rm %buildroot%_mandir/pt_BR/man1/nisdomainname.1*
rm %buildroot%_mandir/pt_BR/man1/ypdomainname.1*
rm %buildroot%_mandir/pt_BR/man8/arp.8*
rm %buildroot%_mandir/pt_BR/man8/ifconfig.8*
rm %buildroot%_mandir/pt_BR/man8/netstat.8*
rm %buildroot%_mandir/pt_BR/man8/rarp.8*
rm %buildroot%_mandir/pt_BR/man8/route.8*

%files
%defattr(-,root,root)
/bin/dnsdomainname
/bin/domainname
/bin/hostname
/bin/netstat
/bin/nisdomainname
/bin/ypdomainname
/sbin/arp
/sbin/ifconfig
/sbin/ipmaddr
/sbin/iptunnel
/sbin/mii-tool
/sbin/plipconfig
/sbin/rarp
/sbin/route
/sbin/slattach
/sbin/nameif
%_mandir/man[158]/*

%changelog
* Tue Jun 14 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 1.60-owl1
- Updated to 1.60.
- Dropped obsoleted -rh-fhs patch.
- Added a hack to build this package against kernel 2.6.

* Fri Jan 07 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 1.57-owl3
- Added a fix to the "label at end of compound statement" issue.

* Sun Nov 28 2004 Michail Litvak <mci@owl.openwall.com> 1.57-owl2
- Fixed building with 2.4.28 kernel.

* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com> 1.57-owl1
- Enforce our new spec file conventions

* Thu Sep 07 2000 Solar Designer <solar@owl.openwall.com>
- Use RPM_OPT_FLAGS.

* Wed Aug 09 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- upgrade to 1.57

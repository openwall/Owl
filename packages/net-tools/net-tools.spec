# $Id: Owl/packages/net-tools/net-tools.spec,v 1.4 2002/02/06 18:45:35 solar Exp $

Summary: The basic tools for setting up networking.
Name: net-tools
Version: 1.57
Release: owl1
License: GPL
Group: System Environment/Base
Source0: http://www.tazenda.demon.co.uk/phil/net-tools/net-tools-%{version}.tar.bz2
Source1: net-tools-1.57-config.h
Source2: net-tools-1.57-config.make
Patch0: net-tools-1.56-rh-fhs.diff
BuildRoot: /override/%{name}-%{version}

%description
The net-tools package contains the basic tools needed for setting up
networking: ethers, route and others.

%prep
%setup -q
%patch0 -p1

cp $RPM_SOURCE_DIR/net-tools-1.57-config.h config.h
cp $RPM_SOURCE_DIR/net-tools-1.57-config.make config.make

%build
make COPTS="$RPM_OPT_FLAGS -D_GNU_SOURCE -Wall"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{bin,sbin}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{1,5,8}

make BASEDIR=$RPM_BUILD_ROOT mandir=%{_mandir} install

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_mandir}/man[158]/*

%changelog
* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Thu Sep 07 2000 Solar Designer <solar@owl.openwall.com>
- Use RPM_OPT_FLAGS.

* Wed Aug 09 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- upgrade to 1.57

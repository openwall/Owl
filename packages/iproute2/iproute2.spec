# $Id: Owl/packages/iproute2/iproute2.spec,v 1.4 2001/12/29 00:17:41 mci Exp $

%define snapshot ss010824

Summary: Enhanced IP routing and network devices configuration tools.
Name: iproute2
Version: 2.4.7
Release: 3owl
License: GPL
Group: Applications/System
Source0: ftp://ftp.inr.ac.ru/ip-routing/%name-%version-now-%snapshot.tar.gz
Patch0: iproute2-2.4.7-rh-config.diff
Patch1: iproute2-2.4.7-rh-promisc-allmulti.diff
Patch2: iproute2-2.4.7-pld-owl-ll_types_proto.diff
Provides: iproute = %{version}
Obsoletes: iproute
BuildRoot: /override/%{name}-%{version}

%description
Linux 2.2 maintains compatibility with the basic configuration utilities of
the network (ifconfig, route) but a new utility is required to exploit the new
characteristics and features of the kernel, such as policy routing, fast NAT
and packet scheduling.  This package includes the new utilities
(ip, tc, rtmon, rtacct).

%prep
%setup -q -n %name
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make KERNEL_INCLUDE=/usr/include \
    CCOPTS="$RPM_OPT_FLAGS -D_GNU_SOURCE -O2 -Wstrict-prototypes -Wall -Werror"

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT{/sbin,%{_sbindir},/etc/iproute2,%{_mandir}/man3}

install -p -m 755 ip/{ip,ifcfg,rtmon} tc/tc $RPM_BUILD_ROOT/sbin
install -p -m 755 ip/rtacct $RPM_BUILD_ROOT%{_sbindir}
install -p -m 644 etc/iproute2/* $RPM_BUILD_ROOT/etc/iproute2

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/sbin/*
%dir /etc/iproute2
%doc README* RELNOTES doc/*.tex examples
%attr(644,root,root) %config(noreplace) /etc/iproute2/*
%{_sbindir}/*

%changelog
* Tue Dec 28 2001 Michail Litvak <mci@owl.openwall.com>
- spec-file based on RH's

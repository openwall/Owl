# $Id: Owl/packages/iproute2/iproute2.spec,v 1.6 2002/02/12 07:34:13 mci Exp $

Summary: Enhanced IP routing and network devices configuration tools.
Name: iproute2
Version: 2.4.7
%define snapshot ss010824
Release: owl3
License: GPL
Group: Applications/System
Source0: ftp://ftp.inr.ac.ru/ip-routing/%name-%version-now-%snapshot.tar.gz
Source1: %name-%version-%snapshot-ps.tar.gz
Source2: ip.8
Source3: tc.8
Source4: tc-htb.8
Source5: tc-pbfifo.8
Source6: tc-pfifo_fast.8
Source7: tc-prio.8
Source8: tc-red.8
Source9: tc-sfq.8
Source10: tc-tbf.8
Source11: tc-cbq.8
Patch0: iproute2-2.4.7-rh-config.diff
Patch1: iproute2-2.4.7-rh-promisc-allmulti.diff
Patch2: iproute2-2.4.7-pld-owl-ll_types_proto.diff
Provides: iproute = %{version}
Obsoletes: iproute
BuildRoot: /override/%{name}-%{version}

%description
Linux 2.2+ maintains compatibility with the basic configuration utilities
of the network (ifconfig, route) but a new utility is required to exploit
the new characteristics and features of the kernel, such as policy
routing, fast NAT and packet scheduling.  This package includes the new
utilities (ip, tc, rtmon, rtacct).

%prep
%setup -q -n %name -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{expand:%%define optflags %optflags -Wall -Wstrict-prototypes}

%build
make \
	KERNEL_INCLUDE=/usr/include \
	CCOPTS="$RPM_OPT_FLAGS -D_GNU_SOURCE"

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT{/sbin,%{_sbindir},/etc/iproute2,%{_mandir}/man8}

install -m 755 ip/{ip,ifcfg,rtmon} tc/tc $RPM_BUILD_ROOT/sbin/
install -m 755 ip/rtacct $RPM_BUILD_ROOT%{_sbindir}/
install -m 644 etc/iproute2/* $RPM_BUILD_ROOT/etc/iproute2/
install -m 644 $RPM_SOURCE_DIR/ip.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 $RPM_SOURCE_DIR/tc.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 $RPM_SOURCE_DIR/tc-htb.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 $RPM_SOURCE_DIR/tc-pbfifo.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 $RPM_SOURCE_DIR/tc-pfifo_fast.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 $RPM_SOURCE_DIR/tc-prio.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 $RPM_SOURCE_DIR/tc-red.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 $RPM_SOURCE_DIR/tc-sfq.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 $RPM_SOURCE_DIR/tc-tbf.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 $RPM_SOURCE_DIR/tc-cbq.8 $RPM_BUILD_ROOT/%{_mandir}/man8/

gzip -9nf iproute2-ps/*.ps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README* RELNOTES examples iproute2-ps/*.ps*
%dir /etc/iproute2
%attr(644,root,root) %config(noreplace) /etc/iproute2/*
/sbin/*
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Mon Feb 11 2002 Michail Litvak <mci@owl.openwall.com>
- add manpages
- add PostScript documentation

* Thu Feb 07 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Dec 28 2001 Michail Litvak <mci@owl.openwall.com>
- spec-file based on RH's

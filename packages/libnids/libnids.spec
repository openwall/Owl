# $Id: Owl/packages/libnids/libnids.spec,v 1.2 2002/02/04 15:39:12 mci Exp $

Summary: NIDS E-component
Name: libnids
Version: 1.16
Release: owl1
Epoch: 1
License: GPL
Group: Libraries
Source: http://www.packetfactory.net/Projects/Libnids/dist/%{name}-%{version}.tar.gz
URL: http://www.packetfactory.net/Projects/Libnids/
Patch0: %{name}-%{version}-pld-conf.diff
Patch1: %{name}-%{version}-owl-pcap062.diff
BuildRequires: autoconf, libpcap-devel, libnet-devel
BuildRoot: /override/%{name}-%{version}

%description
libnids is an implementation of an E-component of Network Intrusion
Detection System.  It emulates the IP stack of Linux 2.0.x.  libnids
offers IP defragmentation, TCP stream assembly and TCP port scan
detection.

%package devel
Summary: Header files and development documentation for libnids
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
Header files and development documentation for libnids.

%prep
%setup -q
%patch0 -p1
%patch1 -p0

%build
autoconf
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	install_prefix=$RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%doc CHANGES README CREDITS MISC doc/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*.h
%{_mandir}/man3/*
%{_libdir}/lib*.a

%changelog
* Mon Feb 04 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Tue Apr 17 2001 Solar Designer <solar@owl.openwall.com>
- Minor spec file cleanups.

* Wed Apr 11 2001 Rafal Wojtczuk <nergal@owl.openwall.com>
- adapted pld specs
- patch to enable usage of libpcap-0.6.2 "any" device
- -Wl,-soname adjusted

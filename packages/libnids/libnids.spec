# $Id: Owl/packages/libnids/libnids.spec,v 1.8 2003/10/18 14:42:37 solar Exp $

Summary: NIDS E-component.
Name: libnids
Version: 1.18
Release: owl1
Epoch: 1
License: GPL
Group: System Environment/Libraries
URL: http://libnids.sourceforge.net
Source: %{name}-%{version}.tar.gz
PreReq: /sbin/ldconfig
BuildRequires: autoconf, libpcap-devel, libnet-devel
BuildRoot: /override/%{name}-%{version}

%description
libnids is an implementation of an E-component of Network Intrusion
Detection System.  It emulates the IP stack of Linux 2.0.x.  libnids
offers IP defragmentation, TCP stream assembly, and TCP port scan
detection.

%package devel
Summary: Development libraries, header files, and documentation for libnids.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development libraries, header files, and documentation for libnids.

%prep
%setup -q

%build
autoconf
%configure --enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install install_prefix=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

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
* Wed Oct 15 2003 Rafal Wojtczuk <nergal@owl.openwall.com> 1.18-owl1
- updated to 1.18

* Tue Dec 17 2002 Rafal Wojtczuk <nergal@owl.openwall.com> 1.17-owl2
- switched soname to libnids.1.xx because of binary incompatibility between
versions

* Fri Dec 13 2002 Rafal Wojtczuk <nergal@owl.openwall.com>
- updated to 1.17

* Mon Feb 04 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Tue Apr 17 2001 Solar Designer <solar@owl.openwall.com>
- Minor spec file cleanups.

* Wed Apr 11 2001 Rafal Wojtczuk <nergal@owl.openwall.com>
- adapted pld specs
- patch to enable usage of libpcap-0.6.2 "any" device
- -Wl,-soname adjusted

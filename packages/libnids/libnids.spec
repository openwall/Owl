# $Id: Owl/packages/libnids/libnids.spec,v 1.1 2001/04/17 03:38:46 solar Exp $

Summary:	NIDS E-component
Name:		libnids
Version:	1.16
Release:	1owl
Epoch:		1
License:	GPL
Group:		Libraries
Source0:	http://www.packetfactory.net/Projects/Libnids/dist/%{name}-%{version}.tar.gz
Patch0:		%{name}-%{version}-pld-conf.diff
Patch1:		%{name}-%{version}-owl-pcap062.diff
URL:		http://www.packetfactory.net/Projects/Libnids/
BuildRequires:	autoconf
BuildRequires:	libpcap-devel
BuildRequires:	libnet-devel
BuildRoot:	/var/rpm-buildroot/%{name}-%{version}

%description
libnids is an implementation of an E-component of Network Intrusion
Detection System.  It emulates the IP stack of Linux 2.0.x.  libnids
offers IP defragmentation, TCP stream assembly and TCP port scan
detection.

%package devel
Summary:	Header files and development documentation for libnids
Group:		Development/Libraries
Requires:	%{name} = %{version}

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
* Tue Apr 17 2001 Solar Designer <solar@owl.openwall.com>
- Minor spec file cleanups.

* Wed Apr 11 2001 Rafal Wojtczuk <nergal@owl.openwall.com>
- adapted pld specs
- patch to enable usage of libpcap-0.6.2 "any" device
- -Wl,-soname adjusted

* Tue Dec 19 2000 PLD Team <pld-list@pld.org.pl>
All persons listed below can be reached at <cvs_login>@pld.org.pl

Revision 1.8  2000/12/19 02:45:51  kloczek
- added autoconf to BuildRequires,
- cosmetics in %install.

Revision 1.7  2000/12/18 20:29:55  areq
- updated to 1.16

Revision 1.6  2000/11/20 17:55:26  misiek
don't duplicate patches

Revision 1.5  2000/11/20 17:24:27  baggins
- release 3

Revision 1.4  2000/11/20 17:24:10  baggins
- added system-libs patch
- lect configure find libpcap

Revision 1.3  2000/11/20 12:51:36  baggins
- release 2
- let configure find libnet

Revision 1.2  2000/11/02 12:17:14  kloczek
- spec adapterized,
- do not compress man pages.

Revision 1.1  2000/11/02 09:05:52  misiek
new spec

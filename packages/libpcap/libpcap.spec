# $Id: Owl/packages/libpcap/libpcap.spec,v 1.3 2002/02/04 17:33:52 solar Exp $

Summary: Network packet capture library.
Name: libpcap
Version: 0.6.2
Release: owl1
Epoch: 2
License: GPL
Group: System Environment/Libraries
Source: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
Patch0: libpcap-0.6.2-pld-shared.diff
BuildRequires: flex, bison
BuildRoot: /override/%{name}-%{version}

%description
libpcap is a system-independent interface for user-level packet
capture.  libpcap provides a portable framework for low-level network
monitoring.  Applications include network statistics collection,
security monitoring, network debugging, etc.  libpcap has
system-independent API that is used by several applications, including
tcpdump and arpwatch.

%package devel
Summary: Header files and development documentation for libpcap.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Header files and development documentation for libpcap.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
%configure \
	--with-pcap=linux \
	--enable-ipv6
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_includedir}/net
mkdir -p ${RPM_BUILD_ROOT}{%{_libdir},%{_mandir}/man3}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGES CREDITS
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*.h
%{_includedir}/net/*.h
%{_mandir}/man*/*
%{_libdir}/lib*.a

%changelog
* Mon Feb 04 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Tue Apr 17 2001 Solar Designer <solar@owl.openwall.com>
- Minor spec file cleanups.
- Removed non-English descriptions (we don't have them in other packages).

* Wed Apr 11 2001 Rafal Wojtczuk <nergal@owl.openwall.com>
- Imported from PLD, adjusted naming conventions
- removed unnecesary info about few patches
- replaced ipv6 patches with ANK patch.

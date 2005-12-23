# $Owl: Owl/packages/libnids/libnids.spec,v 1.19 2005/12/23 01:29:03 solar Exp $

Summary: NIDS E-component.
Name: libnids
Version: 1.20
Release: owl1
Epoch: 1
License: GPL
Group: System Environment/Libraries
URL: http://libnids.sourceforge.net
Source: %name-%version.tar.gz
PreReq: /sbin/ldconfig
BuildRequires: libpcap-devel, libnet-devel >= 1:1.1
BuildRoot: /override/%name-%version

%description
libnids is an implementation of an E-component of Network Intrusion
Detection System.  It emulates the IP stack of Linux 2.0.x.  libnids
offers IP defragmentation, TCP stream assembly, and TCP port scan
detection.

%package devel
Summary: Development libraries, header files, and documentation for libnids.
Group: Development/Libraries
Requires: %name = %epoch:%version-%release

%description devel
This package contains development libraries and C header files needed for
building applications which use libnids, as well as documentation on libnids.

%prep
%setup -q

%build
%configure --enable-shared
%__make

%install
rm -rf %buildroot
%makeinstall

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%_libdir/libnids.so.*

%files devel
%defattr(-,root,root)
%doc doc README CHANGES CREDITS MISC
%_mandir/man3/*
%_includedir/*.h
%_libdir/libnids.so
%_libdir/libnids.a

%changelog
* Fri Dec 23 2005 Solar Designer <solar-at-owl.openwall.com> 1:1.20-owl1
- Updated to 1.20.

* Tue Dec 13 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:1.19-owl2
- Corrected interpackage dependencies.

* Fri Jul 30 2004 Rafal Wojtczuk <nergal-at-owl.openwall.com> 1:1.19-owl1
- updated to 1.19

* Wed Feb 18 2004 Solar Designer <solar-at-owl.openwall.com> 1:1.18-owl2
- Replaced the Prism patch with a version from Nergal; the previous patch
broke things for (at least) PPP interfaces.

* Mon Feb 16 2004 Simon Baker <simonb-at-owl.openwall.com>
- Added prism wireless capabilities patch from Snax <snax at shmoo.com>

* Wed Oct 15 2003 Rafal Wojtczuk <nergal-at-owl.openwall.com> 1:1.18-owl1
- updated to 1.18

* Tue Dec 17 2002 Rafal Wojtczuk <nergal-at-owl.openwall.com> 1:1.17-owl2
- switched soname to libnids.1.xx because of binary incompatibility between
versions

* Fri Dec 13 2002 Rafal Wojtczuk <nergal-at-owl.openwall.com>
- updated to 1.17

* Mon Feb 04 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Tue Apr 17 2001 Solar Designer <solar-at-owl.openwall.com>
- Minor spec file cleanups.

* Wed Apr 11 2001 Rafal Wojtczuk <nergal-at-owl.openwall.com>
- adapted pld specs
- patch to enable usage of libpcap-0.6.2 "any" device
- -Wl,-soname adjusted

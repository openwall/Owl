# $Id: Owl/packages/libpcap/libpcap.spec,v 1.1 2001/04/17 03:38:46 solar Exp $

Summary:	libpcap provides promiscuous mode access to network interfaces
Name:		libpcap
Version:	0.6.2
Release:	1owl
Epoch:		2
License:	GPL
Group:		Libraries
Source0:	http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
Patch0:		%{name}-%{version}-pld-shared.diff
BuildRequires:	flex
BuildRequires:	bison
BuildRoot:	/var/rpm-buildroot/%{name}-%{version}

%description
libpcap is a system-independent interface for user-level packet
capture.  libpcap provides a portable framework for low-level network
monitoring.  Applications include network statistics collection,
security monitoring, network debugging, etc.  libpcap has
system-independent API that is used by several applications, including
tcpdump and arpwatch.

%package devel
Summary:	Header files and development documentation for libpcap
Group:		Development/Libraries
Requires:	%{name} = %{version}

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
install -d $RPM_BUILD_ROOT%{_includedir}/net \
	$RPM_BUILD_ROOT{%{_libdir},%{_mandir}/man3}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
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
* Tue Apr 17 2001 Solar Designer <solar@owl.openwall.com>
- Minor spec file cleanups.
- Removed non-English descriptions (we don't have them in other packages).

* Wed Apr 11 2001 Rafal Wojtczuk <nergal@owl.openwall.com>
- Imported from PLD, adjusted naming conventions

* Wed Feb 07 2001 PLD Team <pld-list@pld.org.pl>
All persons listed below can be reached at <cvs_login>@pld.org.pl

Revision 1.37  2001/02/07 21:49:41  misiek
0.6.2

Revision 1.36  2001/01/12 15:02:01  misiek
latest official release 0.6.1

Revision 1.35  2001/01/07 12:37:20  misiek
3.6 cvs prerelease. Changed versioning number scheme.

Revision 1.34  2000/12/17 12:19:43  misiek
updated to cvs20001217

Revision 1.33  2000/12/02 21:40:58  misiek
updated to cvs20001202

Revision 1.32  2000/11/03 09:12:24  kloczek
- use new rpm automation.

Revision 1.31  2000/11/02 09:27:24  misiek
updated to cvs version as official stable is broken

Revision 1.30  2000/08/27 21:02:14  kloczek
- release 2.

Revision 1.29  2000/08/26 00:05:20  mis
- removed /usr/include/net dir, it's in glibc-devel

Revision 1.28  2000/08/01 10:55:30  zagrodzki
- updated to 0.5.2

Revision 1.27  2000/07/14 13:30:40  wiget
0.5

Revision 1.26  2000/06/09 07:54:44  kloczek
- more %%{__make} macros.

Revision 1.25  2000/06/09 07:23:24  kloczek
- added using %%{__make} macro.

Revision 1.24  2000/05/23 21:25:52  kloczek
- release 21 (for allow upgrade from RH 6.2),
- spec adapterized.

Revision 1.23  2000/05/07 13:10:57  kloczek
- release 19.

Revision 1.22  2000/04/14 08:55:00  qboosh
- added flex and bison to BuildRequires:

Revision 1.21  2000/04/01 11:14:52  zagrodzki
- changed all BuildRoot definitons
- removed all applnkdir defs
- changed some prereqs/requires
- removed duplicate empty lines

Revision 1.20  2000/03/28 16:54:40  baggins
- translated kloczkish into english

Revision 1.19  2000/01/23 09:46:02  kloczek
- added missing %%date macro.

Revision 1.18  2000/01/23 09:39:44  kloczek
- fixed %changelog.

Revision 1.17  2000/01/23 09:36:47  kloczek
- release 18,
- updated Patch0 to ss991029,
- adapter(ized).

Revision 1.16  1999/11/29 20:26:15  wiget
- added %%defattr

Revision 1.15  1999/11/27 03:07:10  kloczek
- release 3,
- added patch for building and installing srared libpcap (based on Debian),
- added static and devel subpackages,
- added scanner and IFF_LOOPBACK patches (from Debian).

Revision 1.14  1999/08/19 11:50:28  kloczek
- release 2.

Revision 1.13  1999/08/12 11:19:04  misiek
includes moved to up directory

* Sat Jul 03 1999 Arkadiusz Mi¶kiewicz <misiek@pld.org.pl>
  [0.4-1]
- removed unnecesary info about few patches
- replaced ipv6 patches with ANK patch.

* Sun Mar 14 1999 Micha³ Kuratczyk <kura@pld.org.pl>
  [0.4a6-6]
- removed man group from man pages
- fixed Summary(pl)
- minor changes

* Tue Feb 16 1999 Artur Frysiak <wiget@usa.net>
  [0.4a6-5d]
- initial release for PLD

# $Id: Owl/packages/libpcap/libpcap.spec,v 1.13 2004/02/19 16:24:45 mci Exp $

Summary: Network packet capture library.
Name: libpcap
Version: 0.8.1
Release: owl2
Epoch: 2
License: GPL
Group: System Environment/Libraries
URL: http://www.tcpdump.org
Source: http://www.tcpdump.org/release/%name-%version.tar.gz
Patch0: libpcap-0.8.1-pld-shared.diff
Patch1: libpcap-0.8.1-nmap-alt-owl-linux-honor-timeout.diff
Patch2: libpcap-0.8.1-owl-align.diff
PreReq: /sbin/ldconfig
BuildRequires: flex, bison
BuildRoot: /override/%name-%version

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
Requires: %name = %version-%release

%description devel
Header files and development documentation for libpcap.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure \
	--with-pcap=linux \
	--enable-ipv6
%__make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%_libdir,%_mandir/man3}

%__make install \
	DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%_includedir/net
ln -s ../pcap-bpf.h $RPM_BUILD_ROOT%_includedir/net/bpf.h

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README CHANGES CREDITS
%attr(755,root,root) %_libdir/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %_libdir/lib*.so
%_includedir/*.h
%_includedir/net/*.h
%_mandir/man*/*
%_libdir/lib*.a

%changelog
* Thu Feb 19 2004 Michail Litvak <mci@owl.openwall.com> 2:0.8.1-owl2
- Updated -nmap-alt-owl-linux-honor-timeout.diff patch.

* Fri Feb 13 2004 Michail Litvak <mci@owl.openwall.com> 2:0.8.1-owl1
- 0.8.1
- provide %_includedir/net/bpf.h for compatibility.

* Mon Dec 15 2003 Solar Designer <solar@owl.openwall.com> 2:0.6.2-owl5
- Avoid unaligned accesses in bpf_filter.c unless we're positive the
architecture can handle them.

* Mon Jun 02 2003 Solar Designer <solar@owl.openwall.com> 2:0.6.2-owl4
- Corrected the timeout handling patch to do it in the packet receive
loop rather than only once before the loop and to return on timeout.

* Mon Jun 02 2003 Solar Designer <solar@owl.openwall.com> 2:0.6.2-owl3
- Added a patch for timeout handling on Linux from Nmap with minor
modifications by ALT Linux team.
- Added URL.

* Mon Sep 16 2002 Michail Litvak <mci@owl.openwall.com> 2:0.6.2-owl2
- Back-ported a possible buffer overflow fix from the CVS; This fixes
a bug wherein "live_open_new()" wasn't making the buffer size the maximum
of "enough to hold packets of the MTU obtained from the socket" and
"the snapshot length" (for some reason, "recvfrom()" was copying more data
than the MTU obtained from the socket). Thanks to Pavel Kankovsky.

* Mon Feb 04 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Tue Apr 17 2001 Solar Designer <solar@owl.openwall.com>
- Minor spec file cleanups.
- Removed non-English descriptions (we don't have them in other packages).

* Wed Apr 11 2001 Rafal Wojtczuk <nergal@owl.openwall.com>
- Imported from PLD, adjusted naming conventions
- removed unnecesary info about few patches
- replaced ipv6 patches with ANK patch.

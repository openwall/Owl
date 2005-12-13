# $Owl: Owl/packages/libpcap/libpcap.spec,v 1.20 2005/12/13 13:17:26 ldv Exp $

Summary: Network packet capture library.
Name: libpcap
Version: 0.9.4
Release: owl2
Epoch: 14
License: BSD
Group: System Environment/Libraries
URL: http://www.tcpdump.org
Source0: http://www.tcpdump.org/release/libpcap-%version.tar.gz
Source1: libpcap.map
Patch0: libpcap-0.9.4-nmap-alt-owl-linux-honor-timeout.diff
Patch1: libpcap-0.9.4-owl-align.diff
Patch2: libpcap-0.9.4-owl-static.diff
Patch3: libpcap-0.9.4-rh-ppp.diff
Patch4: libpcap-0.9.4-deb-man.diff
PreReq: /sbin/ldconfig
%define soname libpcap.so.0
%define compat_sonames libpcap.so.0.8.2 libpcap.so.0.8.3 libpcap.so.0.9.4
# Additional provides for better binary compatibility with Fedora.
Provides: %compat_sonames
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
Requires: %name = %epoch:%version-%release

%description devel
Header files and development documentation for libpcap.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
install -pm644 %_sourcedir/libpcap.map .
bzip2 -9k CHANGES

%build
%configure \
	--with-pcap=linux \
	--enable-ipv6
# First build shared,
%__make CCOPT="%optflags -fPIC `getconf LFS_CFLAGS`"
mkdir shared
gcc -shared -o shared/libpcap.so.%version \
	-Wl,-soname,%soname -Wl,--version-script,libpcap.map \
	-Wl,-whole-archive,libpcap.a,-no-whole-archive

# then static.
%__make clean
%__make CCOPT="%optflags `getconf LFS_CFLAGS`"

%install
rm -rf %buildroot
%makeinstall

install -pm644 shared/libpcap.so.%version %buildroot%_libdir/
for n in %soname %compat_sonames libpcap.so.1 libpcap.so; do
	[ -f %buildroot%_libdir/$n ] ||
		ln -s libpcap.so.%version %buildroot%_libdir/$n
done

mkdir -p %buildroot%_includedir/net
ln -s ../pcap-bpf.h %buildroot%_includedir/net/bpf.h

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,755)
%doc CHANGES.bz2 CREDITS LICENSE README
%_libdir/lib*.so.*

%files devel
%defattr(-,root,root,755)
%_libdir/lib*.so
%_includedir/*.h
%_includedir/net/*.h
%_mandir/man*/*
%_libdir/lib*.a

%changelog
* Tue Dec 13 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 14:0.9.4-owl2
- Corrected interpackage dependencies.

* Fri Nov 18 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 14:0.9.4-owl1
- Updated to 0.9.4.
- Reworked shared and static libraries build method.
- Restricted list of global symbols exported by the library.

* Thu Nov 10 2005 Solar Designer <solar-at-owl.openwall.com> 14:0.8.1-owl4
- Bumped the Epoch to 14 (yuck) for Fedora and RHEL compatibility.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2:0.8.1-owl3
- Fixed orphaned %_libdir/libpcap.so.0 produced in %post.

* Thu Feb 19 2004 Michail Litvak <mci-at-owl.openwall.com> 2:0.8.1-owl2
- Updated -nmap-alt-owl-linux-honor-timeout.diff patch.

* Fri Feb 13 2004 Michail Litvak <mci-at-owl.openwall.com> 2:0.8.1-owl1
- 0.8.1
- provide %_includedir/net/bpf.h for compatibility.

* Mon Dec 15 2003 Solar Designer <solar-at-owl.openwall.com> 2:0.6.2-owl5
- Avoid unaligned accesses in bpf_filter.c unless we're positive the
architecture can handle them.

* Mon Jun 02 2003 Solar Designer <solar-at-owl.openwall.com> 2:0.6.2-owl4
- Corrected the timeout handling patch to do it in the packet receive
loop rather than only once before the loop and to return on timeout.

* Mon Jun 02 2003 Solar Designer <solar-at-owl.openwall.com> 2:0.6.2-owl3
- Added a patch for timeout handling on Linux from Nmap with minor
modifications by ALT Linux team.
- Added URL.

* Mon Sep 16 2002 Michail Litvak <mci-at-owl.openwall.com> 2:0.6.2-owl2
- Back-ported a possible buffer overflow fix from the CVS; This fixes
a bug wherein "live_open_new()" wasn't making the buffer size the maximum
of "enough to hold packets of the MTU obtained from the socket" and
"the snapshot length" (for some reason, "recvfrom()" was copying more data
than the MTU obtained from the socket). Thanks to Pavel Kankovsky.

* Mon Feb 04 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Tue Apr 17 2001 Solar Designer <solar-at-owl.openwall.com>
- Minor spec file cleanups.
- Removed non-English descriptions (we don't have them in other packages).

* Wed Apr 11 2001 Rafal Wojtczuk <nergal-at-owl.openwall.com>
- Imported from PLD, adjusted naming conventions
- removed unnecesary info about few patches
- replaced ipv6 patches with ANK patch.

# $Owl: Owl/packages/libnet/libnet.spec,v 1.14 2005/12/13 13:17:26 ldv Exp $

Summary: "libpwrite" Network Routine Library.
Name: libnet
Version: 1.0.2a
Release: owl5
Epoch: 1
License: BSD
Group: System Environment/Libraries
URL: http://www.packetfactory.net/libnet/
Source: http://www.packetfactory.net/libnet/dist/%name-%version.tar.gz
Patch0: libnet-1.0.2a-pld-shared.diff
Patch1: libnet-1.0.2a-owl-alpha-targets.diff
PreReq: /sbin/ldconfig
BuildRequires: libpcap-devel, autoconf
BuildRoot: /override/%name-%version

%description
The Network Library provides a simple API for commonly used low-level
network functions (mainly packet injection).  Using libnet, it is easy
to build and write arbitrary network packets.  It provides a portable
framework for low-level network packet writing and handling (use
libnet in conjunction with libpcap and you can write some really cool
stuff).  libnet includes packet creation at the IP layer and at the
link layer as well as a host of supplementary and complementary
functionality.

%package devel
Summary: Header files and development documentation for libnet.
Group: Development/Libraries
Requires: %name = %epoch:%version-%release

%description devel
Header files and development documentation for libnet.

%prep
%setup -q -n Libnet-%version
%patch0 -p1
%patch1 -p1

%build
aclocal
autoconf
%configure --with-pf_packet=yes
%__make CFLAGS="%optflags"

%install
rm -rf %buildroot

%__make install \
	DESTDIR=%buildroot \
	MAN_PREFIX=%_mandir/man3

pushd %buildroot%_libdir
ln -sf libnet.so.*.* libnet.so
# XXX: (GM): we have to find a universal way to do the following:
ln -sf libnet.so.*.* libnet.so.1
popd
ln -sf libnet.so %buildroot%_libdir/libpwrite

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %_libdir/lib*.so.*
%attr(755,root,root) %_libdir/libpwrite

%files devel
%defattr(644,root,root,755)
%doc doc README
%attr(755,root,root) %_libdir/lib*.so
%attr(755,root,root) %_bindir/*
%_includedir/*.h
%_includedir/libnet
%_mandir/man*/*
%_libdir/lib*.a

%changelog
* Tue Dec 13 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:1.0.2a-owl5
- Corrected interpackage dependencies.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:1.0.2a-owl4
- Fixed orphaned %_libdir/libnet.so.1 created by %post.

* Mon Feb 16 2004 Michail Litvak <mci-at-owl.openwall.com> 1:1.0.2a-owl3
- Correctly install documentation from doc/ subdirectory.

* Mon Feb 04 2002 Michail Litvak <mci-at-owl.openwall.com> 1:1.0.2a-owl2
- Enforce our new spec file conventions

* Sun Jun 17 2001 Solar Designer <solar-at-owl.openwall.com>
- Support alpha* targets other than plain alpha (don't even try to check
for unaligned accesses when building for an Alpha).

* Tue Apr 17 2001 Solar Designer <solar-at-owl.openwall.com>
- Minor spec file cleanups.

* Wed Apr 11 2001 Rafal Wojtczuk <nergal-at-owl.openwall.com>
- adapted pld package to libnet version 1.0.2a
- -Wl,-soname adjusted

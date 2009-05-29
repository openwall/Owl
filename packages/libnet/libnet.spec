# $Owl: Owl/packages/libnet/libnet.spec,v 1.21 2009/05/29 14:23:42 solar Exp $

Summary: A library for portable packet creation and injection.
Name: libnet
Version: 1.1.3
%define extra -RC-01
Release: owl0.2
Epoch: 1
License: BSD
Group: System Environment/Libraries
URL: http://www.packetfactory.net/libnet/
Source: %name-%version%extra-stripped-for-owl-1.tar.bz2
# The following subdirectories and files have been removed from the tarball:
# win32 include/win32 sample/win32 src/libnet_link_win32.c src/.libs
# and files matching the shell pattern .#* anywhere in the tree, as well as
# CVS directories anywhere in the tree,
# and a README-stripped file has been added.
# The size reduced from 1.1 MB to 300 KB.
# Source: http://www.packetfactory.net/libnet/dist/%name-%version%extra.tar.gz
Patch0: libnet-1.0.2a-owl-alpha-targets.diff
PreReq: /sbin/ldconfig
BuildRequires: libpcap-devel, autoconf
BuildRoot: /override/%name-%version

%description
Libnet is an API to help with the construction and handling of network
packets.  It provides a portable framework for low-level network
packet writing and handling (use libnet in conjunction with libpcap and
you can write some really cool stuff).  Libnet includes packet creation
at the IP layer and at the link layer as well as a host of supplementary
and complementary functionality.

%package devel
Summary: Development libraries, header files, and documentation for libnet.
Group: Development/Libraries
Requires: %name = %epoch:%version-%release

%description devel
This package contains development libraries and C header files needed for
building applications which use libnet, as well as documentation on libnet.

%prep
%setup -q -n libnet
%patch0 -p1
rm -rf doc/CVS # Remove this directory if present, but don't complain if not
rm -r doc/{man,libnet.doxygen.conf}
bzip2 -9 doc/CHANGELOG

%build
aclocal
autoconf
export ac_cv_libnet_linux_procfs=yes \
%configure
%__make

%install
rm -rf %buildroot
%makeinstall

# Don't package .la files.
rm %buildroot%_libdir/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%_libdir/libnet.so.*

%files devel
%defattr(-,root,root)
%doc doc/* README
%_bindir/libnet-config
%_includedir/libnet.h
%_includedir/libnet
%_libdir/libnet.so
%_libdir/libnet.a

%changelog
* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:1.1.3-owl0.2
- Compressed CHANGELOG file.

* Fri Dec 23 2005 Solar Designer <solar-at-owl.openwall.com> 1:1.1.3-owl0.1
- Updated to 1.1.3-RC-01.

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

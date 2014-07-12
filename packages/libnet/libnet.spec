# $Owl: Owl/packages/libnet/libnet.spec,v 1.23 2014/07/12 13:54:08 galaxy Exp $

%define ver 1.2
%define extra rc3

Summary: A library for portable packet creation and injection.
Name: libnet
Version: %ver%{?extra}
Release: owl1
Epoch: 1
License: BSD
Group: System Environment/Libraries
URL: http://www.sourceforge.net/projects/libnet-dev/
Source: http://downloads.sourceforge.net/libnet-dev/%name-%ver%{?extra:-%extra}.tar.gz
#Patch0: libnet-1.0.2a-owl-alpha-targets.diff
BuildRequires: libpcap-devel, autoconf >= 2.69
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
%setup -q -n %name-%ver%{?extra:-%extra}
#patch0 -p1
#rm -r doc/{man,libnet.doxygen.conf}
bzip2 -9fk doc/CHANGELOG

%build
autoreconf -fis
%configure \
	--enable-shared \
	--disable-static \
#

%__make

%install
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'
%makeinstall

# Don't package .la files.
rm -- '%buildroot%_libdir'/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(0644,root,root,0755)
%_libdir/libnet.so.*

%files devel
%defattr(0644,root,root,0755)
%doc doc/{C,D,P,R,T}* doc/MIGRATION README
%attr(0755,root,root) %_bindir/libnet-config
%_includedir/libnet.h
%_includedir/libnet
%_libdir/libnet.so
%_mandir/man3/libnet*.3*

%changelog
* Mon Jun 16 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:1.2rc3-owl1
- Updated to 1.2-rc3.
- Dropped the deprecated PreReq tag.

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

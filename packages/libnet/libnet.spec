# $Id: Owl/packages/libnet/libnet.spec,v 1.2 2001/06/17 03:44:10 solar Exp $

Summary:	"libpwrite" Network Routine Library
Name:		libnet
Version:	1.0.2a
Release:	2owl
Epoch:		1
License:	BSD
Group:		Libraries
Source0:	http://www.packetfactory.net/libnet/dist/%{name}-%{version}.tar.gz
Patch0:		libnet-1.0.2a-pld-shared.diff
Patch1:		libnet-1.0.2a-owl-alpha-targets.diff
URL:		http://www.packetfactory.net/libnet/
BuildRequires:	libpcap-devel, autoconf
BuildRoot:	/var/rpm-buildroot/%{name}-%{version}

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
Summary:	Header files and development documentation for libnet
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files and development documentation for libnet.

%prep
%setup -q -n Libnet-%{version}
%patch0 -p1
%patch1 -p1

%build
aclocal
autoconf
%configure \
	--with-pf_packet=yes
%{__make} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	MAN_PREFIX=%{_mandir}/man3

pushd $RPM_BUILD_ROOT%{_libdir}
ln -sf libnet.so.*.* libnet.so
popd
ln -sf libnet.so $RPM_BUILD_ROOT%{_libdir}/libpwrite

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/libpwrite

%files devel
%defattr(644,root,root,755)
%doc doc/* README
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_bindir}/*
%{_includedir}/*.h
%{_includedir}/libnet
%{_mandir}/man*/*
%{_libdir}/lib*.a

%changelog
* Sun Jun 17 2001 Solar Designer <solar@owl.openwall.com>
- Support alpha* targets other than plain alpha (don't even try to check
for unaligned accesses when building for an Alpha).

* Tue Apr 17 2001 Solar Designer <solar@owl.openwall.com>
- Minor spec file cleanups.

* Wed Apr 11 2001 Rafal Wojtczuk <nergal@owl.openwall.com>
- adapted pld package to libnet version 1.0.2a
- -Wl,-soname adjusted

* Mon Nov 20 2000 PLD Team <pld-list@pld.org.pl>
All persons listed below can be reached at <cvs_login>@pld.org.pl

Revision 1.13  2000/11/20 17:02:41  baggins
- release 3
- fixed .so link

Revision 1.12  2000/11/20 12:49:03  baggins
- release 2
- use RPM_OPT_FLAGS

Revision 1.11  2000/11/02 13:38:17  kloczek
- spec adapterized,
- do not compress man pages.

Revision 1.10  2000/11/02 08:33:31  misiek
new spec

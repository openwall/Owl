# $Id: Owl/packages/traceroute/traceroute.spec,v 1.1 2001/03/06 17:05:39 solar Exp $

Summary: Traces the route taken by packets over a TCP/IP network.
Name: traceroute
Version: 1.4a12
Release: 1owl
Copyright: BSD
Group: Applications/Internet
Source0: ftp://ftp.ee.lbl.gov/traceroute-%{version}.tar.gz
Source1: traceroute.control
Patch0: traceroute-1.4a12-owl-install-no-root.diff
Patch1: traceroute-1.4a12-owl-tim-chris-fixes.diff
Patch2: traceroute-1.4a12-owl-force-linux.diff
Prefix: %{_prefix}
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: owl-control < 2.0

%description
The traceroute utility displays the route used by IP packets on their
way to a specified network (or Internet) host.  traceroute is used as
a network debugging tool.  If you're having network connectivity
problems, traceroute will show you where the trouble is coming from
along the route.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8

make DESTDIR=${RPM_BUILD_ROOT} install install-man

strip $RPM_BUILD_ROOT%{_sbindir}/* || :

mkdir -p $RPM_BUILD_ROOT/etc/control.d/facilities
install -m 700 %{SOURCE1} $RPM_BUILD_ROOT/etc/control.d/facilities/traceroute

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(4711,root,root)	%{_sbindir}/traceroute
%{_mandir}/man8/*
/etc/control.d/facilities/traceroute

%changelog
* Tue Mar 06 2001 Solar Designer <solar@owl.openwall.com>
- Reviewed many patches in other distributions, concluded that only some
of the security fixes by Tim Robbins and Chris Evans are still relevant.
- Produced a patch with the above fixes and some more (in particular, to
restrict the allowed source addresses to those on external interfaces).
- Patched configure to force the use of /proc/net/route even if it can't
be accessed at compile time.
- Wrote traceroute.control.
- Based this spec file on Red Hat's.

# $Id: Owl/packages/traceroute/traceroute.spec,v 1.6 2002/11/03 03:14:29 solar Exp $

Summary: Traces the route taken by packets over a TCP/IP network.
Name: traceroute
Version: 1.4a12
Release: owl5
License: BSD
Group: Applications/Internet
Source0: ftp://ftp.ee.lbl.gov/traceroute-%{version}.tar.gz
Source1: traceroute.control
Patch0: traceroute-1.4a12-owl-install-no-root.diff
Patch1: traceroute-1.4a12-owl-tim-chris-fixes.diff
Patch2: traceroute-1.4a12-owl-force-linux.diff
Patch3: traceroute-1.4a12-owl-sockaddr-vs-sockaddr_in.diff
Patch4: traceroute-1.4a12-rh-unaligned.diff
Prefix: %{_prefix}
Requires: owl-control >= 0.4, owl-control < 2.0
BuildRoot: /override/%{name}-%{version}

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
%patch3 -p1
%patch4 -p1

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8

make DESTDIR=${RPM_BUILD_ROOT} install install-man

mkdir -p $RPM_BUILD_ROOT/etc/control.d/facilities
install -m 700 %{SOURCE1} $RPM_BUILD_ROOT/etc/control.d/facilities/traceroute

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ $1 -ge 2 ]; then
	/usr/sbin/control-dump traceroute
fi

%post
if [ $1 -ge 2 ]; then
	/usr/sbin/control-restore traceroute
else
	/usr/sbin/control traceroute public
fi

%files
%defattr(-,root,root)
%attr(700,root,root) %{_sbindir}/traceroute
%{_mandir}/man8/*
/etc/control.d/facilities/traceroute

%changelog
* Sun Nov 03 2002 Solar Designer <solar@owl.openwall.com>
- Dump/restore the owl-control setting for traceroute on package upgrades.
- Keep traceroute at mode 700 ("restricted") in the package, but default
it to "public" in %post when the package is first installed.  This avoids
a race and fail-open behavior.

* Sun Jul 07 2002 Solar Designer <solar@owl.openwall.com>
- Use struct sockaddr_in everywhere rather than cast struct sockaddr's as
the latter may have different alignment requirements.

* Mon Apr 01 2002 Solar Designer <solar@owl.openwall.com>
- Imported Red Hat's patch for proper use of the unaligned *outdata
structure; this really was still needed on 64-bit architectures.

* Mon Feb 04 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Mar 08 2001 Solar Designer <solar@owl.openwall.com>
- Use bind(2) for the actual source address restriction (but leave the loop
such that the right source address is tried in case of multiple A records).
- Disallow non-loopback destinations for the case of "-i lo" as well.

* Tue Mar 06 2001 Solar Designer <solar@owl.openwall.com>
- Reviewed many patches in other distributions, concluded that only some
of the security fixes by Tim Robbins and Chris Evans are still relevant.
- Produced a patch with the above fixes and some more (in particular, to
restrict the allowed source addresses to those on external interfaces).
- Patched configure to force the use of /proc/net/route even if it can't
be accessed at compile time.
- Wrote traceroute.control.
- Based this spec file on Red Hat's.

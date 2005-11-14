# $Id: Owl/packages/traceroute/traceroute.spec,v 1.13 2005/11/14 15:25:30 ldv Exp $

Summary: Traces the route taken by packets over a TCP/IP network.
Name: traceroute
Version: 1.0.3
Release: owl1
Epoch: 1
License: GPL
Group: Applications/Internet
URL: http://rechner.lst.de/~okir/traceroute/
Source: ftp://ftp.lst.de/pub/people/okir/traceroute/traceroute-%version.tar.bz2
Patch0: traceroute-1.0.3-rh-compat.diff
Patch1: traceroute-1.0.3-alt-fixes.diff
Patch2: traceroute-1.0.3-alt-src_port.diff
# due to traceroute6
Conflicts: iputils < 0:ss020927-owl4
BuildRoot: /override/%name-%version

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
%__make CCOPTS="%optflags -W"

%install
rm -rf %buildroot
install -pD -m755 traceroute %buildroot/bin/traceroute
install -pD -m644 traceroute.1 %buildroot%_mandir/man8/traceroute.8
ln -s traceroute %buildroot/bin/traceroute6
ln -s traceroute.8.gz %buildroot%_mandir/man8/traceroute6.8.gz
# Backwards compatibility symlinks.
mkdir -p %buildroot%_sbindir
ln -s ../../bin/traceroute %buildroot%_sbindir/
ln -s ../../bin/traceroute %buildroot%_sbindir/traceroute6

%files
%defattr(-,root,root)
/bin/traceroute*
%_sbindir/traceroute*
%_mandir/man8/*

%changelog
* Mon Nov 14 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:1.0.3-owl1
- Replaced with traceroute written by Olaf Kirch.
- Imported patch from Fedora for better backwards compatibility.
- Imported ALT patches which add -P option to specify UDP source port
and fix compilation warnings.
- Relocated traceroute binaries to /bin/ and added symlinks to old
/usr/sbin/ place for backwards compatibility.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.4a12-owl6
- Removed verify checks for traceroute binary since we are using control
to configure its permissions and group owner.
- Cleaned up the spec.

* Sun Nov 03 2002 Solar Designer <solar-at-owl.openwall.com> 1.4a12-owl5
- Dump/restore the owl-control setting for traceroute on package upgrades.
- Keep traceroute at mode 700 ("restricted") in the package, but default
it to "public" in %post when the package is first installed.  This avoids
a race and fail-open behavior.

* Sun Jul 07 2002 Solar Designer <solar-at-owl.openwall.com>
- Use struct sockaddr_in everywhere rather than cast struct sockaddr's as
the latter may have different alignment requirements.

* Mon Apr 01 2002 Solar Designer <solar-at-owl.openwall.com>
- Imported Red Hat's patch for proper use of the unaligned *outdata
structure; this really was still needed on 64-bit architectures.

* Mon Feb 04 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Mar 08 2001 Solar Designer <solar-at-owl.openwall.com>
- Use bind(2) for the actual source address restriction (but leave the loop
such that the right source address is tried in case of multiple A records).
- Disallow non-loopback destinations for the case of "-i lo" as well.

* Tue Mar 06 2001 Solar Designer <solar-at-owl.openwall.com>
- Reviewed many patches in other distributions, concluded that only some
of the security fixes by Tim Robbins and Chris Evans are still relevant.
- Produced a patch with the above fixes and some more (in particular, to
restrict the allowed source addresses to those on external interfaces).
- Patched configure to force the use of /proc/net/route even if it can't
be accessed at compile time.
- Wrote traceroute.control.
- Based this spec file on Red Hat's.

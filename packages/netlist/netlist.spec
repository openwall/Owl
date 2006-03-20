# $Owl: Owl/packages/netlist/Attic/netlist.spec,v 1.13 2006/03/20 00:45:18 ldv Exp $

Summary: A program to list active Internet connections and sockets.
Name: netlist
Version: 2.0
Release: owl4
License: distributable
Group: System Environment/Base
URL: http://www.openwall.com/linux/
Source: ftp://ftp.openwall.com/pub/patches/linux/contrib/netlist-%version.tar.gz
Patch: netlist-2.0-alt-scan_proc_table.diff
BuildRoot: /override/%name-%version

%description
When run by a non-privileged user, netlist lists active Internet
connections and listening sockets of that user.

When run by root or a user with group access privileges for /proc,
netlist lists all active TCP, UDP, and raw sockets on the system.

netlist was created to oppose restrictive tendencies in security.  Your
use of netlist must be in accordance with this intent.  Please see the
LICENSE for information on this and other licensing conditions.

%prep
%setup -q
%patch -p1

%build
%__make CFLAGS="-c -Wall %optflags"

%install
rm -rf %buildroot
make install DESTDIR=%buildroot BINDIR=%_bindir MANDIR=%_mandir

%post
grep -q '^proc:[^:]*:110:' /etc/group && \
	chgrp proc %_bindir/netlist && chmod 2711 %_bindir/netlist

%files
%defattr(-,root,root)
%doc LICENSE
%verify(not mode group) %_bindir/netlist
%_mandir/man1/netlist.1*

%changelog
* Sun Mar 19 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.0-owl4
- Updated /proc scanner for 2.6.x kernels.

* Mon Jun 02 2003 Solar Designer <solar-at-owl.openwall.com> 2.0-owl3
- Removed verify checks for size and group owner due to %post.
- Cleaned up the spec.

* Mon Jun 02 2003 Solar Designer <solar-at-owl.openwall.com> 2.0-owl2
- Added URL.

* Wed Feb 06 2002 Michail Litvak <mci-at-owl.openwall.com> 2.0-owl1
- Enforce our new spec file conventions

* Wed Nov 07 2001 Solar Designer <solar-at-owl.openwall.com>
- Wrote the man page, Makefile, and this spec file.

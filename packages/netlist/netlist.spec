Summary: A program to list active Internet connections and sockets.
Name: netlist
Version: 2.0
Release: 1owl
License: distributable
Group: System Environment/Base
Source: netlist-%version.tar.gz
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

%build
make CFLAGS="-c -Wall $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT BINDIR=%_bindir MANDIR=%_mandir

%clean
rm -rf $RPM_BUILD_ROOT

%post
grep -q '^proc:[^:]*:110:' /etc/group && \
	chgrp proc %_bindir/netlist && chmod 2711 %_bindir/netlist

%files
%defattr(-,root,root)
%doc LICENSE
/usr/bin/netlist
%_mandir/man1/netlist.1*

%changelog
* Wed Nov 07 2001 Solar Designer <solar@owl.openwall.com>
- Wrote the man page, Makefile, and this spec file.

# $Id: Owl/packages/termcap/termcap.spec,v 1.4 2004/11/23 22:40:49 mci Exp $

Summary: The terminal feature database used by certain applications.
Name: termcap
Version: 11.0.1
Release: owl1
License: public domain
Group: System Environment/Base
Source: http://www.tuxedo.org/~esr/terminfo/termtypes.tc.gz
BuildArchitectures: noarch
BuildRoot: /override/%name-%version

%description
The termcap package provides the /etc/termcap file.  /etc/termcap is a
database which defines the capabilities of various terminals and
terminal emulators.  Certain programs use the /etc/termcap file to
access various features of terminals (the bell, colors, and graphics,
etc.).

%prep
mkdir -p %buildroot/etc
zcat $RPM_SOURCE_DIR/termtypes.tc.gz > %buildroot/etc/termcap

%files
%config %attr(0644,root,root) /etc/termcap

%changelog
* Mon Feb 04 2002 Solar Designer <solar@owl.openwall.com> 11.0.1-owl1
- Enforce our new spec file conventions.

* Tue Aug 08 2000 Solar Designer <solar@owl.openwall.com>
- Based this spec file on one from RH, updated to 11.0.1, removed all
of the RH patches for now.
- Added %attr.

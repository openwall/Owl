# $Id: Owl/packages/termcap/termcap.spec,v 1.1 2000/08/07 23:02:20 solar Exp $

Summary: The terminal feature database used by certain applications.
Name: termcap
Version: 11.0.1
Release: 1owl
Copyright: none
Group: System Environment/Base
Source: http://www.tuxedo.org/~esr/terminfo/termtypes.tc.gz
Buildroot: /var/rpm-buildroot/%{name}-%{version}
BuildArchitectures: noarch

%description
The termcap package provides the /etc/termcap file.  /etc/termcap is a
database which defines the capabilities of various terminals and
terminal emulators.  Certain programs use the /etc/termcap file to
access various features of terminals (the bell, colors, and graphics,
etc.).

%prep
mkdir -p $RPM_BUILD_ROOT/etc
zcat $RPM_SOURCE_DIR/termtypes.tc.gz > $RPM_BUILD_ROOT/etc/termcap

%clean
rm -rf $RPM_BUILD_ROOT

%files
%config %attr(0644,root,root) /etc/termcap

%changelog
* Tue Aug 08 2000 Solar Designer <solar@owl.openwall.com>
- Based this spec file on one from RH, updated to 11.0.1, removed all
of the RH patches for now.
- Added %attr.

# $Id: Owl/packages/owl-control/owl-control.spec,v 1.7 2002/11/03 01:24:35 solar Exp $

Summary: A set of scripts to control installed system facilities.
Name: owl-control
Version: 0.4
Release: owl1
License: public domain
Group: System Environment/Base
Source0: functions
Source1: control
Source2: control-dump
Source3: control-restore
Requires: /bin/sh, /dev/null, sh-utils, fileutils, findutils
Requires: sed, grep, mktemp
BuildArchitectures: noarch
BuildRoot: /override/%{name}-%{version}

%description
The scripts included in this package provide a common interface to
control system facilities provided by a number of other packages.
This is intended for use primarily by packages which are providing
a facility that can potentially be dangerous to system security,
to let you enable, disable, or configure the facility independently
from package installation.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{/etc/control.d/facilities,%{_sbindir}}
cp $RPM_SOURCE_DIR/functions $RPM_BUILD_ROOT/etc/control.d/
cp $RPM_SOURCE_DIR/control{,-dump,-restore} $RPM_BUILD_ROOT%{_sbindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0700,root,root)
%dir /etc/control.d
%dir /etc/control.d/facilities
%attr(0600,root,root) /etc/control.d/functions
%{_sbindir}/control*

%changelog
* Sun Nov 03 2002 Solar Designer <solar@owl.openwall.com>
- Imported some of the ALT Linux updates, including (modified versions of)
the control-dump and control-restore scripts.
- Install the scripts into %{_sbindir} directly, no more symlinks.

* Sun Jul 07 2002 Solar Designer <solar@owl.openwall.com>
- Use grep -q in the provided shell functions.

* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Nov 22 2000 Solar Designer <solar@owl.openwall.com>
- Support extended regexp's in control_subst().

* Fri Aug 11 2000 Solar Designer <solar@owl.openwall.com>
- Various important changes to the provided shell functions.
- Wrote the package description.
- Moved the symlink: /sbin/control is now /usr/sbin/control.

* Thu Aug 10 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

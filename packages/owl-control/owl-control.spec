# $Id: Owl/packages/owl-control/owl-control.spec,v 1.3 2000/11/22 17:04:26 solar Exp $

Summary: A set of scripts to control installed system facilities.
Name: owl-control
Version: 0.2
Release: 1owl
Copyright: public domain
Group: System Environment/Base
Source0: control
Source1: functions
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: /bin/sh, /dev/null, sh-utils, fileutils, findutils
Requires: sed, grep, mktemp
BuildArchitectures: noarch

%description
The scripts included in this package provide a common interface to
control system facilities provided by a number of other packages.
This is intended for use primarily by packages which are providing
a facility that can potentially be dangerous to system security,
to let you enable, disable, or configure the facility independently
from package installation.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{etc/control.d/facilities,usr/sbin}
cp $RPM_SOURCE_DIR/control $RPM_BUILD_ROOT/etc
cp $RPM_SOURCE_DIR/functions $RPM_BUILD_ROOT/etc/control.d
ln -s /etc/control $RPM_BUILD_ROOT/usr/sbin/control

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0700,root,root)
/etc/control
/usr/sbin/control
%dir /etc/control.d
%dir /etc/control.d/facilities
%attr(0600,root,root) /etc/control.d/functions

%changelog
* Wed Nov 22 2000 Solar Designer <solar@owl.openwall.com>
- Support extended regexp's in control_subst().

* Fri Aug 11 2000 Solar Designer <solar@owl.openwall.com>
- Various important changes to the provided shell functions.
- Wrote the package description.
- Moved the symlink: /sbin/control is now /usr/sbin/control.

* Thu Aug 10 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

# $Id: Owl/packages/owl-control/owl-control.spec,v 1.1 2000/08/10 07:33:15 solar Exp $

Summary: A set of scripts to control installed system facilities.
Name: owl-control
Version: 0.0
Release: 1owl
Copyright: public domain
Group: System Environment/Base
Source0: control
Source1: functions
Buildroot: /var/rpm-buildroot/%{name}-%{version}
BuildArchitectures: noarch

%description
A set of scripts to control installed system facilities.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{etc/control.d/facilities,sbin}
cp $RPM_SOURCE_DIR/control $RPM_BUILD_ROOT/etc
cp $RPM_SOURCE_DIR/functions $RPM_BUILD_ROOT/etc/control.d
ln -s /etc/control $RPM_BUILD_ROOT/sbin/control

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0700,root,root)
/etc/control
/sbin/control
%dir /etc/control.d
%dir /etc/control.d/facilities
%attr(0600,root,root) /etc/control.d/functions

%changelog
* Thu Aug 10 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

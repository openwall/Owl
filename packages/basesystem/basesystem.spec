# $Id: Owl/packages/basesystem/basesystem.spec,v 1.1 2000/08/01 23:54:55 solar Exp $

Summary: Initial set of configuration files and directory hierarchy
Name: basesystem
Version: 0.0
Release: 1owl
Copyright: public domain
Group: System Environment/Base
Prereq: owl-etc owl-hier
Buildroot: /var/rpm-buildroot/%{name}-%{version}
BuildArchitectures: noarch

%description
This package combines owl-etc and owl-hier, and exists primarily for
RH compatibility.

%changelog
* Wed Aug 02 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

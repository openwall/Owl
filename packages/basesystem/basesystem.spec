# $Id: Owl/packages/basesystem/basesystem.spec,v 1.3 2000/12/20 18:54:35 solar Exp $

Summary: Initial set of configuration files and directory hierarchy
Name: basesystem
Version: 99.0
Release: 1owl
Copyright: public domain
Group: System Environment/Base
Prereq: owl-etc owl-hier
Buildroot: /var/rpm-buildroot/%{name}-%{version}
BuildArchitectures: noarch

%description
This package combines owl-etc and owl-hier, and exists primarily for
RH compatibility.

%files

%changelog
* Wed Dec 20 2000 Solar Designer <solar@owl.openwall.com>
- Set version to 99.0 so that we can cleanly replace Red Hat's package.

* Wed Aug 02 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

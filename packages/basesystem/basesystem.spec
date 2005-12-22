# $Owl: Owl/packages/basesystem/basesystem.spec,v 1.8 2005/12/22 03:57:32 solar Exp $

Summary: Initial set of configuration files and directory hierarchy.
Name: basesystem
Version: 99.0
Release: owl1
License: public domain
Group: System Environment/Base
PreReq: owl-etc, owl-hier
BuildArchitectures: noarch
BuildRoot: /override/%name-%version

%description
This package combines owl-etc and owl-hier, and exists primarily for
Red Hat Linux compatibility.

%install
rm -rf %buildroot

%files

%changelog
* Thu Jan 24 2002 Solar Designer <solar-at-owl.openwall.com> 99.0-owl1
- Enforce our new spec file conventions.

* Wed Dec 20 2000 Solar Designer <solar-at-owl.openwall.com>
- Set version to 99.0 so that we can cleanly replace Red Hat's package.

* Wed Aug 02 2000 Solar Designer <solar-at-owl.openwall.com>
- Initial version.

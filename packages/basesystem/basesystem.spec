# $Owl: Owl/packages/basesystem/basesystem.spec,v 1.10 2014/07/12 14:08:09 galaxy Exp $

Summary: Initial set of configuration files and directory hierarchy.
Name: basesystem
Version: 99.0
Release: owl2
License: public domain
Group: System Environment/Base
Requires: owl-etc, owl-hier
BuildArchitectures: noarch
BuildRoot: /override/%name-%version

%description
This package combines owl-etc and owl-hier, and exists primarily for
Red Hat Linux compatibility.

%install
rm -rf %buildroot
exit 0

%files

%changelog
* Mon Jun 30 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 99.0-owl2
- Replaced the deprecated PreReq tag with Requires.

* Thu Jan 24 2002 Solar Designer <solar-at-owl.openwall.com> 99.0-owl1
- Enforce our new spec file conventions.

* Wed Dec 20 2000 Solar Designer <solar-at-owl.openwall.com>
- Set version to 99.0 so that we can cleanly replace Red Hat's package.

* Wed Aug 02 2000 Solar Designer <solar-at-owl.openwall.com>
- Initial version.

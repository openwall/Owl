# $Id: Owl/packages/mtree/mtree.spec,v 1.11 2005/01/14 03:27:52 galaxy Exp $

Summary: Map a directory hierarchy.
Name: mtree
Version: 3.1
Release: owl3
License: BSD
Group: System Environment/Base
Source: mtree-%version-20020728.tar.bz2
Patch0: mtree-3.1-owl-linux.diff
Patch1: mtree-3.1-owl-fixes.diff
Requires: openssl
BuildRequires: openssl-devel
BuildRoot: /override/%name-%version

%description
The utility mtree compares the file hierarchy rooted in the current
directory against a specification read from the standard input.
Messages are written to the standard output for any files whose
characteristics do not match the specification, or which are
missing from either the file hierarchy or the specification.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
CFLAGS="-c $RPM_OPT_FLAGS" %__make CC="%__cc" LDFLAGS="-lcrypto"

%install
rm -rf %buildroot
mkdir -p %buildroot{%_sbindir,%_mandir/man8}
install -m 755 usr.sbin/mtree/mtree %buildroot%_sbindir/
install -m 644 usr.sbin/mtree/mtree.8 %buildroot%_mandir/man8/

%files
%defattr(-,root,root)
%_sbindir/mtree
%_mandir/man8/mtree.8*

%changelog
* Fri Jan 07 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 3.1-owl3
- Made use of %__cc macro
- Added gcc343-fixes patch to deal with "label at end of compound statment"
issue.

* Sun Dec 25 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 3.1-owl2
- Bumped up release to satisfy dependency resolver (fix for openssl
upgrading issue.

* Sun Jul 28 2002 Solar Designer <solar@owl.openwall.com> 3.1-owl1
- Updated to version from current OpenBSD (post-3.1).

* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Apr 26 2001 Solar Designer <solar@owl.openwall.com>
- New release number for upgrades after building against OpenSSL 0.9.6a.

* Sun Jul 23 2000 Solar Designer <solar@owl.openwall.com>
- Updated to version from OpenBSD 2.7.

* Sat Jul 22 2000 Solar Designer <solar@owl.openwall.com>
- Ported mtree from OpenBSD, wrote initial version of this spec file.

# $Id: Owl/packages/mtree/mtree.spec,v 1.18 2005/10/24 03:06:27 solar Exp $

Summary: Map a directory hierarchy.
Name: mtree
Version: 3.7.20050808
Release: owl1
License: BSD
Group: System Environment/Base
Source: mtree-%version.tar.bz2
Patch0: mtree-3.7.20050808-freebsd-owl-vis.diff
Patch1: mtree-3.7.20050808-owl-fixes.diff
Patch2: mtree-3.7.20050808-owl-linux.diff
Requires: openssl
BuildRequires: openssl-devel >= 0.9.7g-owl1
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
%patch2 -p1

%build
CFLAGS="%optflags" %__make

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
* Mon Aug 08 2005 Solar Designer <solar-at-owl.openwall.com> 3.7.20050808-owl1
- Updated to version from current OpenBSD (post-3.7).
- Added VIS_GLOB support into *vis(), originally by phk of FreeBSD.
- Fixed a number of bugs in mtree spec file creation and parsing, including
with processing of filenames starting with the hash character ('#') or
containing glob(3) wildcard characters, of comment lines ending with a
backslash ('\\'), and of files not ending with a linefeed; the fixes are
generic and need to be fed back to *BSDs.

* Sat Jun 25 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.1-owl4
- Rebuilt with libcrypto.so.5.

* Fri Jan 07 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.1-owl3
- Made use of %__cc macro
- Added a patch to deal with "label at end of compound statement" issue.

* Sun Dec 25 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.1-owl2
- Bumped up release to satisfy dependency resolver (fix for openssl
upgrading issue).

* Sun Jul 28 2002 Solar Designer <solar-at-owl.openwall.com> 3.1-owl1
- Updated to version from current OpenBSD (post-3.1).

* Wed Feb 06 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Apr 26 2001 Solar Designer <solar-at-owl.openwall.com>
- New release number for upgrades after building against OpenSSL 0.9.6a.

* Sun Jul 23 2000 Solar Designer <solar-at-owl.openwall.com>
- Updated to version from OpenBSD 2.7.

* Sat Jul 22 2000 Solar Designer <solar-at-owl.openwall.com>
- Ported mtree from OpenBSD, wrote initial version of this spec file.

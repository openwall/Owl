# $Id: Owl/packages/mktemp/mktemp.spec,v 1.9 2003/10/30 21:15:46 solar Exp $

Summary: A small utility for safely making temporary files.
Name: mktemp
Version: 1.5
Release: owl1
Epoch: 1
License: BSD
Group: System Environment/Base
URL: http://www.mktemp.org
Source: ftp://ftp.mktemp.org/pub/mktemp/mktemp-%version.tar.gz
BuildRoot: /override/%name-%version

%description
mktemp is an utility to be used by shell scripts and other programs to
safely create and use temporary files in directories writable by other
users (such as in /tmp).

%prep
%setup -q

%build
%define _bindir /bin
%configure --with-man --with-random=/dev/urandom
make

%install
%makeinstall

%files
%defattr(-,root,root)
%doc LICENSE README RELEASE_NOTES
%_bindir/mktemp
%_mandir/man1/mktemp.*

%changelog
* Wed Apr 02 2003 Solar Designer <solar@owl.openwall.com> 1:1.5-owl1
- Updated to 1.5.

* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Nov 13 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 1.4 release.

* Thu Oct 04 2001 Solar Designer <solar@owl.openwall.com>
- Updated to a pre-1.4 (uses $TMPDIR and a hard-coded template by default).

* Tue Oct 02 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 1.3.1 (built-in $TMPDIR support).

* Fri Jun 29 2001 Solar Designer <solar@owl.openwall.com>
- Packaged the portable mktemp, now that Todd Miller maintains it in
addition to the OpenBSD-specific version. :-)

* Tue Aug 08 2000 Solar Designer <solar@owl.openwall.com>
- Updated to version from OpenBSD 2.7.
- Added __attribute__ ((format ...)) to err() and "%s" to errx().
- Added %defattr.

* Fri Jul 07 2000 Solar Designer <solar@owl.openwall.com>
- Imported from RH, and fixed for arbitrary buildroot.

# $Id: Owl/packages/mktemp/mktemp.spec,v 1.7 2002/02/06 17:02:51 mci Exp $

Summary: A small utility for safely making temporary files.
Name: mktemp
Version: 1.4
Release: owl1
Epoch: 1
License: BSD
Group: System Environment/Base
URL: http://www.courtesan.com/mktemp/
Source: ftp://ftp.courtesan.com/pub/mktemp/mktemp-%{version}.tar.gz
BuildRoot: /override/%{name}-%{version}

%description
The mktemp utility takes a given filename template and overwrites a
portion of it to create a unique filename.  This allows shell scripts
and other programs to safely create and use temporary files under /tmp.

%prep
%setup -q

%build
%define _bindir /bin
%configure --with-man --with-random=/dev/urandom
make

%install
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE README RELEASE_NOTES
%_bindir/mktemp
%_mandir/man1/mktemp.*

%changelog
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

# $Id: Owl/packages/mktemp/mktemp.spec,v 1.3 2001/06/28 23:32:26 solar Exp $

Summary: A small utility for safely making /tmp files.
Name: mktemp
Epoch: 1
Version: 1.2
Release: 1owl
Copyright: BSD
Group: System Environment/Base
Source: ftp://ftp.courtesan.com/pub/mktemp/mktemp-%{version}.tar.gz
URL: http://www.courtesan.com/mktemp/
Buildroot: /var/rpm-buildroot/%{name}-%{version}

%description
The mktemp utility takes a given file name template and overwrites a
portion of it to create a unique file name.  This allows shell scripts
and other programs to safely create and use /tmp files.

Install the mktemp package if you need to use shell scripts or other
programs which will create and use unique /tmp files.

%prep
%setup

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
* Fri Jun 29 2001 Solar Designer <solar@owl.openwall.com>
- Packaged the portable mktemp, now that Todd Miller maintains it in
addition to the OpenBSD-specific version. :-)

* Tue Aug 08 2000 Solar Designer <solar@owl.openwall.com>
- Updated to version from OpenBSD 2.7.
- Added __attribute__ ((format ...)) to err() and "%s" to errx().
- Added %defattr.

* Fri Jul 07 2000 Solar Designer <solar@owl.openwall.com>
- Imported from RH, and fixed for arbitrary buildroot.

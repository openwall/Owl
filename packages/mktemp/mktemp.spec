# $Id: Owl/packages/mktemp/mktemp.spec,v 1.2 2000/08/07 22:18:14 solar Exp $

Summary: A small utility for safely making /tmp files.
Name: mktemp
Version: 2.7
Release: 1owl
Copyright: BSD
Group: System Environment/Base
Source: mktemp-%{version}.tar.gz
Patch0: mktemp-2.7-rh-owl-linux.diff
Url: http://www.openbsd.org/
Buildroot: /var/rpm-buildroot/%{name}-%{version}

%description
The mktemp utility takes a given file name template and overwrites a
portion of it to create a unique file name.  This allows shell scripts
and other programs to safely create and use /tmp files.

Install the mktemp package if you need to use shell scripts or other
programs which will create and use unique /tmp files.

%prep
%setup
%patch -p1

%build
make -C usr.bin/mktemp CFLAGS="-c $RPM_OPT_FLAGS"

%install
mkdir -p $RPM_BUILD_ROOT/bin $RPM_BUILD_ROOT/usr/man/man1
make -C usr.bin/mktemp FAKEROOT="$RPM_BUILD_ROOT" install
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/mktemp.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/bin/mktemp
/usr/man/man1/mktemp.*

%changelog
* Tue Aug 08 2000 Solar Designer <solar@owl.openwall.com>
- Updated to version from OpenBSD 2.7.
- Added __attribute__ ((format ...)) to err() and "%s" to errx().
- Added %defattr.

* Fri Jul 07 2000 Solar Designer <solar@owl.openwall.com>
- Imported from RH, and fixed for arbitrary buildroot.

# $Id: Owl/packages/mtree/mtree.spec,v 1.2 2000/07/23 17:39:03 solar Exp $

Summary: Map a directory hierarchy
Name: mtree
Version: 2.7
Release: 1owl
Copyright: BSD
Group: System Environment/Base
Source: mtree-%{version}.tar.gz
Patch: mtree-%{version}-owl-linux.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: openssl
BuildPreReq: openssl-devel

%description
The utility mtree compares the file hierarchy rooted in the current
directory against a specification read from the standard input.
Messages are written to the standard output for any files whose
characteristics do not match the specification, or which are
missing from either the file hierarchy or the specification.

%prep
%setup -q
%patch -p1

%build
make -C usr.sbin/mtree CFLAGS="-c -I. $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/sbin $RPM_BUILD_ROOT/usr/man/man8
install -m 755 usr.sbin/mtree/mtree $RPM_BUILD_ROOT/usr/sbin/
install -m 644 usr.sbin/mtree/mtree.8 $RPM_BUILD_ROOT/usr/man/man8/
gzip -9nf $RPM_BUILD_ROOT/usr/man/man8/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/sbin/mtree
/usr/man/man8/mtree.8*

%changelog
* Sun Jul 23 2000 Solar Designer <solar@owl.openwall.com>
- Updated to version from OpenBSD 2.7.

* Sat Jul 22 2000 Solar Designer <solar@owl.openwall.com>
- Ported mtree from OpenBSD, wrote initial version of this spec file.

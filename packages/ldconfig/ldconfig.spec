# $Id: Owl/packages/ldconfig/Attic/ldconfig.spec,v 1.4 2000/11/30 20:02:19 solar Exp $

%define reldate 1999-07-31

Summary: 	Creates a shared library cache and maintains symlinks for ld.so.
Name: 		ldconfig
Version: 	1.9.10
Release: 	2owl
Copyright: 	GPL
Group: 		System Environment/Base
Source: 	ftp://ftp.valinux.com/pub/support/hjl/glibc/ldconfig-%{reldate}.tar.gz
Exclusiveos: 	Linux
Patch0: 	ldconfig-1.9.10-rh-help.diff
Patch1: 	ldconfig-1.9.10-owl-not_in_glibc.diff
Prereq: 	basesystem
Buildroot: 	/var/rpm-buildroot/%{name}-root

%description
Ldconfig is a basic system program which determines run-time link
bindings between ld.so and shared libraries. Ldconfig scans a running
system and sets up the symbolic links that are used to load shared
libraries properly. It also creates a cache (/etc/ld.so.cache) which
speeds the loading of programs which use shared libraries.

%prep
%setup -q -n ldconfig-%{reldate}
%patch0 -p0
%patch1 -p0

%build
rm -f ldconfig
gcc -s -o ldconfig $RPM_OPT_FLAGS -static ldconfig.c

%install
mkdir -p $RPM_BUILD_ROOT/{sbin,etc}
install -s -m 755 ldconfig $RPM_BUILD_ROOT/sbin/ldconfig
touch $RPM_BUILD_ROOT/etc/ld.so.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README
/sbin/ldconfig
%attr(600,root,root) %ghost /etc/ld.so.conf

%changelog
* Sat Oct 28 2000 Solar Designer <solar@owl.openwall.com>
- Create an empty /etc/ld.so.conf, so that its permissions are set here.

* Sun Sep 10 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
- new release from HJL's site
- import help patch from RH
- not in glibc patch

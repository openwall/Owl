# $Id: Owl/packages/kernel/kernel.spec,v 1.3 2000/10/28 19:23:30 solar Exp $

Summary: Fake Linux kernel package for RH compatibility
Name: kernel
Version: 2.2.999fake
Release: 1owl
Copyright: public domain
Group: System Environment/Base
Prereq: basesystem
Buildroot: /var/rpm-buildroot/%{name}-%{version}
BuildArchitectures: noarch

%package headers
Summary: Symlinks for the Linux kernel header files
Group: Development/System
Prereq: basesystem

%description
This package exists for RH compatibility only.  It doesn't provide an
actual Linux kernel, but satisfies package dependencies.

%description headers
This package exists primarily for RH compatibility.  It provides only
the symlinks to Linux kernel header files, not the actual files.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/include
cd $RPM_BUILD_ROOT
ln -s /usr/src/linux/include/{linux,asm} usr/include/

%files

%files headers
%defattr(-,root,root)
/usr/include/linux
/usr/include/asm

%changelog
* Sat Oct 28 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

# $Id: Owl/packages/kernel/kernel.spec,v 1.4 2000/11/16 11:53:27 solar Exp $

Summary: Fake Linux kernel package for RH compatibility
Name: kernel
Version: 2.2.999fake
Release: 2owl
Copyright: public domain
Group: System Environment/Base
Source0: BuildASM-sparc.sh
Prereq: basesystem
ExclusiveOS: Linux
BuildArchitectures: noarch
Buildroot: /var/rpm-buildroot/%{name}-%{version}

%package headers
Summary: Symlinks for the Linux kernel header files
Group: Development/System
Prereq: basesystem
BuildArchitectures: noarch sparc sparcv9

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
ln -s /usr/src/linux/include/linux usr/include/linux
%ifarch sparc sparcv9
ln -s /usr/src/linux/include/asm-sparc usr/include/asm-sparc
ln -s /usr/src/linux/include/asm-sparc64 usr/include/asm-sparc64
mkdir usr/include/asm
install -m 744 $RPM_SOURCE_DIR/BuildASM-sparc.sh usr/include/asm/BuildASM
usr/include/asm/BuildASM usr/include
%else
ln -s /usr/src/linux/include/asm usr/include/asm
%endif

%files

%files headers
%defattr(-,root,root)
/usr/include/linux
/usr/include/asm

%changelog
* Thu Nov 16 2000 Solar Designer <solar@owl.openwall.com>
- Imported the BuildASM script from RH to produce the magic headers
needed to build 32-bit packages when a sparc64 kernel is installed.

* Sat Oct 28 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

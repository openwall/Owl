# $Id: Owl/packages/kernel/kernel.spec,v 1.11 2003/07/31 15:28:37 solar Exp $

Summary: Fake Linux kernel package for Red Hat Linux compatibility.
Name: kernel
# 2.2.999fake or 2.4.999fake
Version: %(sed -n 's,^#define UTS_RELEASE "\(2\.[2-9]\)\..*$,\1.999fake,p' < /usr/include/linux/version.h)
Release: owl3
License: public domain
Group: System Environment/Base
Source: BuildASM-sparc.sh
PreReq: basesystem
%ifarch sparc sparcv9
BuildArchitectures: %{_arch}
%else
BuildArchitectures: noarch
%endif
BuildRoot: /override/%{name}-%{version}

%description
This package exists for Red Hat Linux compatibility only.  It doesn't
provide an actual Linux kernel, but satisfies package dependencies.

%package headers
Summary: Symlinks for the Linux kernel header files.
Group: Development/System
PreReq: basesystem

%description headers
This package exists primarily for Red Hat Linux compatibility.  It
provides only the symlinks to Linux kernel header files, not the actual
files.

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
%ifarch sparc sparcv9
/usr/include/asm-sparc*

%pre headers
test -L /usr/include/asm && rm -f /usr/include/asm || :
%endif

%changelog
* Thu Jul 31 2003 Solar Designer <solar@owl.openwall.com> 2.2+.x-owl3
- Set this package's version to match the actual kernel headers used
(this is especially important on SPARC).

* Mon Feb 04 2002 Michail Litvak <mci@owl.openwall.com> 2.2.999-owl2
- Enforce our new spec file conventions

* Thu Nov 16 2000 Solar Designer <solar@owl.openwall.com>
- Imported the BuildASM script from RH to produce the magic headers
needed to build 32-bit packages when a sparc64 kernel is installed.

* Sat Oct 28 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

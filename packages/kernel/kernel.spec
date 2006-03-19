# $Owl: Owl/packages/kernel/kernel.spec,v 1.20 2006/03/19 22:37:33 solar Exp $

Summary: Fake Linux kernel package for Red Hat Linux compatibility.
Name: kernel
Version: %(sed -n 's,^#define UTS_RELEASE "\(2\.[2-9]\.[0-9]\+\).*$,\1fake,p' < %_includedir/linux/version.h)
Release: owl5
License: public domain
Group: System Environment/Base
Source: BuildASM-sparc.sh
PreReq: basesystem
Provides: kernel-drm = 4.1.0
Provides: kernel-drm = 4.2.0
Provides: kernel-drm = 4.2.99.3
Provides: kernel-drm = 4.3.0
%ifarch sparc sparcv9
BuildArchitectures: %_arch
%else
BuildArchitectures: noarch
%endif
BuildRoot: /override/%name-%version

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
rm -rf %buildroot
mkdir -p %buildroot%_includedir
cd %buildroot
ln -s ../src/linux/include/linux .%_includedir/linux
%ifarch sparc sparcv9
ln -s ../src/linux/include/asm-sparc .%_includedir/asm-sparc
ln -s ../src/linux/include/asm-sparc64 .%_includedir/asm-sparc64
mkdir .%_includedir/asm
install -pm744 %_sourcedir/BuildASM-sparc.sh .%_includedir/asm/BuildASM
.%_includedir/asm/BuildASM .%_includedir
%else
ln -s ../src/linux/include/asm .%_includedir/asm
%endif

%files

%files headers
%defattr(-,root,root)
%_includedir/linux
%_includedir/asm
%ifarch sparc sparcv9
%_includedir/asm-sparc*

%pre headers
test -L %_includedir/asm && rm -f %_includedir/asm || :
%endif

%changelog
* Sun Mar 12 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.4.x-owl5
- Made %_includedir/* symlinks relative.

* Sat Mar 13 2004 Michail Litvak <mci-at-owl.openwall.com> 2.2+.x-owl4
- Provide kernel-drm for compatibility with RH.

* Thu Jul 31 2003 Solar Designer <solar-at-owl.openwall.com> 2.2+.x-owl3
- Set this package's version to match the actual kernel headers used
(this is especially important on SPARC).

* Mon Feb 04 2002 Michail Litvak <mci-at-owl.openwall.com> 2.2.999-owl2
- Enforce our new spec file conventions

* Thu Nov 16 2000 Solar Designer <solar-at-owl.openwall.com>
- Imported the BuildASM script from RH to produce the magic headers
needed to build 32-bit packages when a sparc64 kernel is installed.

* Sat Oct 28 2000 Solar Designer <solar-at-owl.openwall.com>
- Initial version.

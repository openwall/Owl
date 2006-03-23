# $Owl: Owl/packages/setarch/setarch.spec,v 1.6 2006/03/23 00:14:36 ldv Exp $

Summary: Personality setter.
Name: setarch
Version: 1.9
Release: owl1
License: GPL
Group: System Environment/Kernel
Source: %name-%version.tar.gz
Patch: setarch-1.9-owl-fixes.diff
%ifarch sparc sparcv9 sparc64
Provides: sparc32
Obsoletes: sparc32
%endif
ExclusiveArch: %ix86 x86_64 sparc sparcv9 sparc64 ppc ppc64 mips mips64 ia64 s390 s390x
BuildRoot: /override/%name-%version

%description
This utility tells the kernel to report a different architecture than
the current one, then runs a program in that environment.  It can also
set various personality flags.

%prep
%setup -q
%patch -p1

%build
%__cc -o setarch setarch.c %optflags

%install
rm -rf %buildroot
mkdir -p %buildroot%_bindir %buildroot%_mandir/man8
install -pm644 setarch.8 %buildroot%_mandir/man8/
install -m755 setarch %buildroot%_bindir/

LINKS="linux32 linux64"
%ifarch %ix86 x86_64
LINKS="$LINKS i386 x86_64"
%endif
%ifarch sparc sparcv9 sparc64
LINKS="$LINKS sparc sparc64 sparc32"
%endif
%ifarch ppc ppc64
LINKS="$LINKS ppc ppc64 ppc32"
%endif
%ifarch mips mips64
LINKS="$LINKS mips mips64 mips32"
%endif
%ifarch ia64
LINKS="$LINKS i386 ia64"
%endif
%ifarch s390 s390x
LINKS="$LINKS s390 s390x"
%endif
for i in $LINKS; do
	ln -s setarch %buildroot%_bindir/$i
	echo '.so man8/setarch.8' > %buildroot%_mandir/man8/$i.8
done

%files
%defattr(-,root,root)
%_bindir/*
%_mandir/man8/*

%changelog
* Thu Mar 23 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.9-owl1
- Updated to 1.9.
- Cleaned up setarch error handling.

* Thu Oct 20 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.8-owl1
- Minor specfile cleanup.

* Tue Oct 18 2005 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- Initial build for Openwall GNU/*/Linux, based on RH package.
- fix sparc32 alias.

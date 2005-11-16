# $Owl: Owl/packages/setarch/setarch.spec,v 1.3 2005/11/16 13:31:51 solar Exp $

Summary: Personality setter.
Name: setarch
Version: 1.8
Release: owl1
License: GPL
Group: System Environment/Kernel
Source: %name-%version.tar.gz
Patch: setarch-1.8-owl-sparc32-alias.diff
%ifarch sparc sparcv9 sparc64
Provides: sparc32
Obsoletes: sparc32
%endif
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
install -p -m644 setarch.8 %buildroot%_mandir/man8/
install -m755 setarch %buildroot%_bindir/

LINKS="linux32"
%ifarch s390 s390x
LINKS="$LINKS s390 s390x"
%endif
%ifarch %ix86 x86_64
LINKS="$LINKS i386 x86_64"
%endif
%ifarch ppc ppc64
LINKS="$LINKS ppc ppc64 ppc32"
%endif
%ifarch sparc sparc64
LINKS="$LINKS sparc sparc64 sparc32"
%endif
%ifarch ia64
LINKS="$LINKS i386 ia64"
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
* Thu Oct 20 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.8-owl1
- Minor specfile cleanup.

* Tue Oct 18 2005 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- Initial build for Openwall GNU/*/Linux, based on RH package.
- fix sparc32 alias.

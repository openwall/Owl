# $Id: Owl/packages/dev86/dev86.spec,v 1.19 2005/07/03 20:55:27 mci Exp $

Summary: A real mode 80x86 assembler and linker.
Name: dev86
Version: 0.16.17
Release: owl1
License: GPL
Group: Development/Languages
Source: http://www.cix.co.uk/~mayday/dev86/Dev86src-%version.tar.gz
Patch0: dev86-0.16.17-rh-install-no-root.diff
Patch1: dev86-0.16.17-owl-kinclude.diff
Patch2: dev86-0.16.17-owl-warnings.diff
Patch3: dev86-0.16.17-owl-Makefile.diff
Patch4: dev86-0.16.17-owl-optflags.diff
Obsoletes: bin86
ExclusiveArch: %ix86
BuildRoot: /override/%name-%version

%description
The dev86 package provides an assembler and linker for real mode 80x86
instructions.  You'll need to have this package installed in order to
build programs that run in real mode, including LILO and the kernel's
bootstrapping code, from their sources.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%{expand:%%define optflags %optflags -fno-strict-aliasing -fno-builtin-exp2 -Wall}

%build
%__make \
	CC="%__cc" \
	PREFIX="%_prefix" \
	BINDIR="%_bindir" \
	LIBPRE="%_prefix" \
	LIBDIR="%_libdir/bcc" \
	MANDIR="%_mandir" \
	ELKSSRC=.. \
	<<!FooBar!
5
quit
!FooBar!

%install
rm -rf %buildroot

%__make install \
	DIST="%buildroot" \
	DISTPRE="%buildroot%_prefix"

# Build and install dis88
%__make install-other \
	DIST="%buildroot" \
	MANDIR="%_mandir"

pushd %buildroot%_bindir
rm nm86 size86
ln -s objdump86 nm86
ln -s objdump86 size86
popd

mv bootblocks/README README.bootblocks
mv copt/README README.copt
mv dis88/README README.dis88
mv elksemu/README README.elksemu
mv unproto/README README.unproto
mv bin86/README-0.4 README.bin86-0.4
mv bin86/README README.bin86
mv bin86/ChangeLog ChangeLog.bin86

%files
%defattr(-,root,root)
%doc README MAGIC Contributors README.bootblocks README.copt README.dis88
%doc README.elksemu README.unproto README.bin86-0.4 README.bin86 ChangeLog.bin86
%dir %_libdir/bcc
%_bindir/bcc
%_bindir/as86
%_bindir/ar86
%_bindir/ld86
%_bindir/objdump86
%_bindir/nm86
%_bindir/size86
%_bindir/dis86
%_bindir/makeboot
%_bindir/elksemu
%_libdir/bcc/*
%_mandir/man1/*

%changelog
* Thu Jun 30 2005 Michail Litvak <mci@owl.openwall.com> 0.16.17-owl1
- 0.16.17
- Dropped outdated patches, updated -owl-warnings patch.

* Tue Jun 28 2005 Dmitry V. Levin <ldv@owl.openwall.com> 0.16.0-owl7
- Build this package without optimizations based on strict aliasing rules.

* Sun Jan 09 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 0.16.0-owl6
- Made use of %%__make and %%__cc macros.
- Added build of dis86 (it seems like we forgot it).
- Optimized package build by issuing optflags to all compile stages which
use gcc.
- Cleaned up the spec.

* Fri Feb 27 2004 Michail Litvak <mci@owl.openwall.com> 0.16.0-owl5
- Patch to fix errno.h usage (from RH).
- add ar86 to file list.

* Sun Feb 15 2004 Michail Litvak <mci@owl.openwall.com> 0.16.0-owl4
- Correctly install documentation files from subdirectories
(rename dir/README to README.dir)

* Mon Feb 09 2004 Michail Litvak <mci@owl.openwall.com> 0.16.0-owl3
- Use rpm macros instead just paths.

* Thu Mar 20 2002 Michail Litvak <mci@owl.openwall.com> 0.16.0-owl2
- fixes to build with -Wall without warnings

* Thu Mar 14 2002 Michail Litvak <mci@owl.openwall.com>
- 0.16

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Mon Dec 04 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- optflags fix
- symlink fix

* Sun Nov 19 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- 0.15.4

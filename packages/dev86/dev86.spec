# $Id: Owl/packages/dev86/dev86.spec,v 1.13 2004/03/12 18:09:53 solar Exp $

Summary: A real mode 80x86 assembler and linker.
Name: dev86
Version: 0.16.0
Release: owl5
License: GPL
Group: Development/Languages
Source: http://www.cix.co.uk/~mayday/dev86/Dev86src-%version.tar.gz
Patch0: dev86-0.16.0-rh-install-no-root.diff
Patch1: dev86-0.16.0-rh-no-bcc.diff
Patch2: dev86-0.16.0-rh-paths.diff
Patch3: dev86-0.16.0-rh-errno.diff
Patch4: dev86-0.16.0-owl-kinclude.diff
Patch5: dev86-0.16.0-owl-optflags.diff
Patch6: dev86-0.16.0-owl-warnings.diff
Patch7: dev86-0.16.0-owl-Makefile.diff
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
%patch5 -p1
%patch6 -p1
%patch7 -p1

%{expand:%%define optflags %optflags -Wall}

%build
make <<!FooBar!
5
quit
!FooBar!

%install
rm -rf $RPM_BUILD_ROOT

make DIST=$RPM_BUILD_ROOT MANDIR=%_mandir ELKSSRC=. install

install -m 755 -s $RPM_BUILD_ROOT/lib/elksemu $RPM_BUILD_ROOT%_bindir
rm -rf $RPM_BUILD_ROOT/lib/

pushd $RPM_BUILD_ROOT/usr/bin
rm -f nm86 size86
ln -s objdump86 nm86
ln -s objdump86 size86

# Move header files out of /usr/include and into /usr/lib/bcc/include
mv $RPM_BUILD_ROOT/usr/include $RPM_BUILD_ROOT%_libdir/bcc/
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
%defattr(-,root,root,-)
%doc README MAGIC Contributors README.bootblocks README.copt README.dis88
%doc README.elksemu README.unproto README.bin86-0.4 README.bin86 ChangeLog.bin86
%dir %_libdir/bcc
%dir %_libdir/bcc/i86
%dir %_libdir/bcc/i386
%dir %_libdir/bcc/include
%_bindir/bcc
%_bindir/as86
%_bindir/as86_encap
%_bindir/ar86
%_bindir/ld86
%_bindir/objdump86
%_bindir/nm86
%_bindir/size86
%_libdir/bcc/bcc-cc1
%_libdir/bcc/copt
%_libdir/bcc/unproto
%_libdir/bcc/i86/*
%_libdir/bcc/i386/*
%_libdir/liberror.txt
%_libdir/bcc/include/*
%_bindir/elksemu
%_mandir/man1/*

%changelog
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

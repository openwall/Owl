# $Id: Owl/packages/dev86/dev86.spec,v 1.8 2002/03/20 19:51:12 mci Exp $

Summary: A real mode 80x86 assembler and linker.
Name: dev86
Version: 0.16.0
Release: owl2
License: GPL
Group: Development/Languages
Source: http://www.cix.co.uk/~mayday/Dev86src-%{version}.tar.gz
Patch0: dev86-0.16.0-rh-install-no-root.diff
Patch1: dev86-0.16.0-rh-no-bcc.diff
Patch2: dev86-0.16.0-rh-paths.diff
Patch3: dev86-0.16.0-owl-kinclude.diff
Patch4: dev86-0.16.0-owl-optflags.diff
Patch5: dev86-0.16.0-owl-warnings.diff
Obsoletes: bin86
ExclusiveArch: %ix86
BuildRoot: /override/%{name}-%{version}

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

%build
make <<!FooBar!
5
quit
!FooBar!

%install
rm -rf $RPM_BUILD_ROOT

make DIST=$RPM_BUILD_ROOT MANDIR=${RPM_BUILD_ROOT}/%{_mandir} ELKSSRC=. install

install -m 755 -s ${RPM_BUILD_ROOT}/lib/elksemu ${RPM_BUILD_ROOT}/usr/bin
rm -rf ${RPM_BUILD_ROOT}/lib/

cd ${RPM_BUILD_ROOT}/usr/bin
rm -f nm86 size86
ln -s objdump86 nm86
ln -s objdump86 size86

# move header files out of /usr/include and into /usr/lib/bcc/include
mv ${RPM_BUILD_ROOT}/usr/include ${RPM_BUILD_ROOT}/usr/lib/bcc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README MAGIC Contributors bootblocks/README copt/README dis88/README
%doc elksemu/README unproto/README bin86/README-0.4 bin86/README bin86/ChangeLog
%dir /usr/lib/bcc
%dir /usr/lib/bcc/i86
%dir /usr/lib/bcc/i386
%dir /usr/lib/bcc/include
/usr/bin/bcc
/usr/bin/as86
/usr/bin/as86_encap
/usr/bin/ld86
/usr/bin/objdump86
/usr/bin/nm86
/usr/bin/size86
/usr/lib/bcc/bcc-cc1
/usr/lib/bcc/copt
/usr/lib/bcc/unproto
/usr/lib/bcc/i86/*
/usr/lib/bcc/i386/*
/usr/lib/liberror.txt
/usr/lib/bcc/include/*
/usr/bin/elksemu
/%{_mandir}/man1/*

%changelog
* Thu Mar 20 2002 Michail Litvak <mci@owl.openwall.com>
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

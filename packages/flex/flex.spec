# $Id: Owl/packages/flex/flex.spec,v 1.1 2000/08/09 02:02:16 kad Exp $

Summary: A tool for creating scanners (text pattern recognizers).
Name: 		flex
Version:	2.5.4a
Release: 	11owl
Copyright: 	GPL
Group: 		Development/Tools
Source: 	ftp://ftp.gnu.org/pub/gnu/flex/flex-%{version}.tar.gz
Patch0: 	flex-2.5.4a-rh-skel.diff
Prefix: 	%{_prefix}
BuildRoot: 	/var/rpm-buildroot/%{name}-root

%description
The flex program generates scanners.  Scanners are programs which can
recognize lexical patterns in text.  Flex takes pairs of regular
expressions and C code as input and generates a C source file as
output.  The output file is compiled and linked with a library to
produce an executable.  The executable searches through its input for
occurrences of the regular expressions.  When a match is found, it
executes the corresponding C code.  Flex was designed to work with
both Yacc and Bison, and is used by many programs as part of their
build process.

You should install flex if you are going to use your system for
application development.

%prep
%setup -q -n flex-2.5.4
%patch0 -p1

%build
autoconf
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall mandir=$RPM_BUILD_ROOT/%{_mandir}/man1

( cd ${RPM_BUILD_ROOT}
  strip .%{_prefix}/bin/flex
  ln -sf flex .%{_prefix}/bin/lex
  ln -s flex.1 .%{_mandir}/man1/lex.1
  ln -s flex.1 .%{_mandir}/man1/flex++.1
  ln -s libfl.a .%{_prefix}/lib/libl.a
)

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc COPYING NEWS README
%{_prefix}/bin/lex
%{_prefix}/bin/flex
%{_prefix}/bin/flex++
%{_mandir}/man1/*
%{_prefix}/lib/libl.a
%{_prefix}/lib/libfl.a
%{_prefix}/include/FlexLexer.h

%changelog
* Sun Aug  6 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun  6 2000 Bill Nottingham <notting@redhat.com>
- rebuild, FHS stuff.

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- add a libl.a link to libfl.a

* Wed Aug 25 1999 Jeff Johnson <jbj@redhat.com>
- avoid uninitialized variable warning (Erez Zadok).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0 tree

* Mon Aug 10 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 2.5.4 to 2.5.4a

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Mar 20 1997 Michael Fulbright <msf@redhat.com>
- Updated to v. 2.5.4

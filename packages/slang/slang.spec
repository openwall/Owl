# $Id: Owl/packages/slang/Attic/slang.spec,v 1.1 2000/12/14 20:43:02 kad Exp $

%define version 1.4.2

Summary: 	The shared library for the S-Lang extension language.
Name: 		slang
Version: 	%{version}
Release: 	2owl
Copyright: 	GPL
Group: 		System Environment/Libraries
Source: 	ftp://space.mit.edu/pub/davis/slang/v1.4/slang-%{version}.tar.bz2
Url: 		http://www.s-lang.org/
Buildroot: 	/var/rpm-buildroot/%{name}-root

%description
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package devel
Summary: The static library and header files for development using S-Lang.
Group: Development/Libraries
Requires: slang

%description devel
This package contains the S-Lang extension language static libraries
and header files which you'll need if you want to develop S-Lang based
applications.  Documentation which may help you write S-Lang based
applications is also included.

Install the slang-devel package if you want to develop applications
based on the S-Lang extension language.


%prep
%setup -n slang-%{version} -q

%build
mv autoconf/configure.in .
%configure --includedir=/usr/include/slang
make elf all

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/include/slang

%makeinstall \
  install_lib_dir=$RPM_BUILD_ROOT/usr/lib \
  install_include_dir=$RPM_BUILD_ROOT/usr/include/slang install-elf

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/lib/libslang.so.*

%files devel
%defattr(-,root,root)
%doc doc
/usr/lib/libslang.a
/usr/lib/libslang.so
/usr/include/slang


%changelog
* Thu Dec 14 2000 Alexandr D. Kanevkiy <kad@owl.openwall.com>
- import from RH

* Tue Aug 29 2000 Bill Nottingham <notting@redhat.com>
- update to 1.4.2

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Matt Wilson <msw@redhat.com>
- added defattr

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- rebuild, FHS stuff

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- autoconf fix for ia64

* Mon Apr 24 2000 Bill Nottingham <notting@redhat.com>
- update to 1.4.1

* Wed Mar 29 2000 Bill Nottingham <notting@redhat.com>
- fix background color problem with newt

* Thu Mar  2 2000 Bill Nottingham <notting@redhat.com>
- resurrect for the devel tree

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Wed Oct 21 1998 Bill Nottingham <notting@redhat.com>
- libslang.so goes in -devel

* Sun Jun 07 1998 Prospector System <bugs@redhat.com>

- translations modified for de

* Sat Jun  6 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.2.2 with buildroot.

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 18 1998 Erik Troan <ewt@redhat.com>
- rebuilt to find terminfo in /usr/share

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Mon Sep 1 1997 Donnie Barnes <djb@redhat.com>
- upgraded to 0.99.38 (will it EVER go 1.0???)
- all patches removed (all appear to be in this version)

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

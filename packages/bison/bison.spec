# $Id: Owl/packages/bison/bison.spec,v 1.1 2000/08/09 00:51:27 kad Exp $

Summary: A GNU general-purpose parser generator.
Name: 		bison
Version: 	1.28
Release: 	5owl
Copyright: 	GPL
Group: 		Development/Tools
Source: 	ftp://ftp.gnu.org/pub/gnu/bison/bison-%{version}.tar.gz
Prereq: 	/sbin/install-info
BuildRoot: 	/var/rpm-buildroot/%{name}-root

%description
Bison is a general purpose parser generator which converts a grammar
description for an LALR(1) context-free grammar into a C program to parse
that grammar.  Bison can be used to develop a wide range of language
parsers, from ones used in simple desk calculators to complex programming
languages.  Bison is upwardly compatible with Yacc, so any correctly
written Yacc grammar should work with Bison without any changes.  If
you know Yacc, you shouldn't have any trouble using Bison. You do need
to be very proficient in C programming to be able to use Bison).  Bison 
is only needed on systems that are used for development.

If your system will be used for C development, you should install Bison
since it is used to build many C programs.

%prep
%setup -q

%build
%configure --datadir=%{_libdir}
make LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall datadir=${RPM_BUILD_ROOT}%{_libdir}

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/bison.info*

%post
/sbin/install-info %{_infodir}/bison.info.gz %{_infodir}/dir --entry="* bison: (bison).                        The GNU parser generator."

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/bison.info.gz %{_infodir}/dir --entry="* bison: (bison).                        The GNU parser generator."
fi

%files
%defattr(-,root,root)
%{_mandir}/*/*
%{_libdir}/*
%{_infodir}/bison.info*
%{_bindir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Aug  6 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- fix URL

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- rebuilt in the new build environment
- FHS packaging

* Sat May 27 2000 Ngo Than <than@redhat.de>
- rebuild for 7.0
- put man pages and info files to correct place

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com> 
- rebuild to gzip man page.

* Fri Jul 16 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.28.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Mon Mar  8 1999 Jeff Johnson <jbj@redhat.com>
- configure with datadir=/usr/lib (#1386).

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- updated text in spec file.
- update to 1.27

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- built for Manhattan
- added build root

* Wed Oct 15 1997 Donnie Barnes <djb@redhat.com>
- various spec file cleanups

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc


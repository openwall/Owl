# $Id: Owl/packages/bison/bison.spec,v 1.13 2003/10/29 18:37:48 solar Exp $

Summary: A GNU general-purpose parser generator.
Name: bison
Version: 1.35
Release: owl2
License: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/bison/bison-%version.tar.bz2
Patch0: bison-1.30-owl-tmp.diff
PreReq: /sbin/install-info
BuildRequires: mktemp >= 1:1.3.1
BuildRoot: /override/%name-%version

%description
Bison is a general purpose parser generator which converts a grammar
description for an LALR(1) context-free grammar into a C program to parse
that grammar.  Bison can be used to develop a wide range of language
parsers, from ones used in simple desk calculators to complex programming
languages.  Bison is upwardly compatible with Yacc, so any correctly
written Yacc grammar should work with Bison without any changes.  If
you know Yacc, you shouldn't have any trouble using Bison.  You do need
to be very proficient in C programming to be able to program with Bison.

%prep
%setup -q
%patch0 -p1

%{expand:%%define optflags %optflags -Wall}

%build
%configure --datadir=%_libdir
make LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall datadir=$RPM_BUILD_ROOT%_libdir

%post
/sbin/install-info %_infodir/bison.info.gz %_infodir/dir \
	--entry="* bison: (bison).                               The GNU parser generator."

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/bison.info.gz %_infodir/dir \
		--entry="* bison: (bison).                               The GNU parser generator."
fi

%files
%defattr(-,root,root)
%_mandir/*/*
%_libdir/*
%_infodir/bison.info*
%_bindir/*

%changelog
* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com> 1.35-owl2
- Deal with info dir entries such that the menu looks pretty.

* Tue Jun 11 2002 Michail Litvak <mci@owl.openwall.com>
- 1.35

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 1.32.

* Fri Dec 21 2001 Solar Designer <solar@owl.openwall.com>
- Corrected the dependency on mktemp(1) (it's only needed for builds).

* Thu Nov 08 2001 Solar Designer <solar@owl.openwall.com>
- Build with -Wall (surprisingly the code was clean enough already).

* Mon Nov 05 2001 Michail Litvak <mci@owl.openwall.com>
- 1.30
- Patch for configure to use mktemp in a fail-close way

* Wed Jan 03 2001 Solar Designer <solar@owl.openwall.com>
- Patch to create temporary files safely.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- fix URL

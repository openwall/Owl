# $Owl: Owl/packages/bison/bison.spec,v 1.29 2006/09/18 23:30:54 ldv Exp $

%define BUILD_TEST 0

Summary: A GNU general-purpose parser generator.
Name: bison
Version: 2.3
Release: owl1
License: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/bison/
Source: ftp://ftp.gnu.org/gnu/bison/bison-%version.tar.bz2
Patch0: bison-2.0-owl-info.diff
PreReq: /sbin/install-info
BuildRequires: mktemp >= 1:1.3.1
BuildRequires: glibc >= 0:2.2
BuildRequires: automake, autoconf
BuildRequires: rpm-build >= 0:4
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
bzip2 -9k NEWS

%{expand:%%define optflags %optflags -Wall}

%build
%configure
%__make
%if %BUILD_TEST
%__make check
%endif

%install
rm -rf %buildroot
%makeinstall

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/bison.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/bison.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS NEWS.bz2 THANKS
%_mandir/*/*
%_datadir/aclocal/*
%_datadir/bison
%_datadir/locale/*/LC_MESSAGES/bison*.mo
%_infodir/bison.info*
%_bindir/*
%_libdir/liby.a

%changelog
* Tue Sep 19 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.3-owl1
- Updated to 2.3.

* Tue Jun 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.1-owl1
- Updated to 2.1.

* Wed Apr 27 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.0-owl1
- Adjusted post-/pre- scriptlets to not use an explicit compression suffix.

* Mon Apr 04 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.0-owl0
- Updated to 2.0.
- Dropped -tmp patch; regenerate configure instead.
- Added optional testsuite.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.35-owl4
- Fixed package filelist to include files which belong to this package only.
- Use %%_datadir for data, not %%_libdir.

* Sat Sep 11 2004 Solar Designer <solar-at-owl.openwall.com> 1.35-owl3
- Use RPM's exclude macro on info dir file.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 1.35-owl2
- Deal with info dir entries such that the menu looks pretty.

* Tue Jun 11 2002 Michail Litvak <mci-at-owl.openwall.com>
- 1.35

* Thu Jan 24 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 1.32.

* Fri Dec 21 2001 Solar Designer <solar-at-owl.openwall.com>
- Corrected the dependency on mktemp(1) (it's only needed for builds).

* Thu Nov 08 2001 Solar Designer <solar-at-owl.openwall.com>
- Build with -Wall (surprisingly the code was clean enough already).

* Mon Nov 05 2001 Michail Litvak <mci-at-owl.openwall.com>
- 1.30
- Patch for configure to use mktemp in a fail-close way

* Wed Jan 03 2001 Solar Designer <solar-at-owl.openwall.com>
- Patch to create temporary files safely.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH
- fix URL

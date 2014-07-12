# $Owl: Owl/packages/bison/bison.spec,v 1.37 2014/07/12 13:48:50 galaxy Exp $

Summary: A GNU general-purpose parser generator.
Name: bison
Version: 3.0.2
Release: owl1
License: GPLv3+
Group: Development/Tools
URL: http://www.gnu.org/software/bison/
Source: ftp://ftp.gnu.org/gnu/bison/bison-%version.tar.xz
# Signature: ftp://ftp.gnu.org/gnu/bison/bison-%version.tar.xz.sig
Patch0: %name-3.0.2-owl-no-man-regen.diff
Patch1: %name-3.0.2-owl-info.diff
Requires(post,preun): /sbin/install-info
BuildRequires: m4 >= 1.4.6
BuildRequires: gettext >= 0.19.1
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
%patch1 -p1
bzip2 -9k NEWS

gettextize -f -q --symlink
rm lib/gettext.h
ln -s '%_datadir/gettext/gettext.h' lib/gettext.h
aclocal --force -I m4
autoreconf -fis -I m4

%{expand:%%define optflags %optflags -Wall}

%build
%configure \
	--disable-rpath \
#

%__make

%check
%__make check

%install
rm -rf %buildroot
%makeinstall

%find_lang %name || :
%find_lang %name-runtime || :
echo '%%defattr(0644,root,root,0755)' > '%name.lst'
for f in '%name'{,-runtime}.lang ; do
	grep -vE '^\s*$' "$f" >> '%name.lst'
done

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/bison.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/bison.info %_infodir/dir
fi

%files -f %name.lst
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING NEWS.bz2 THANKS
%attr(0755,root,root) %_bindir/bison
%attr(0755,root,root) %_bindir/yacc
%_mandir/man1/bison.1*
%_mandir/man1/yacc.1*
%_datadir/aclocal/bison*.m4
%_datadir/bison
%_infodir/bison.info*
%_libdir/liby.a

%changelog
* Thu Jun 19 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.0.2-owl1
- Updated to 3.0.2.
- Replaced the deprecated PreReq tag with Requires(post,preun).

* Wed Aug 18 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.4.3-owl1
- Updated to 2.4.3.
- Fixed compiler warnings.

* Sun Aug 16 2009 Michail Litvak <mci-at-owl.openwall.com> 2.4.1-owl1
- Updated to 2.4.1.

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

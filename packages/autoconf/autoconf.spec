# $Owl: Owl/packages/autoconf/autoconf.spec,v 1.16 2014/07/12 13:47:09 galaxy Exp $

Summary: A GNU tool for automatically configuring source code.
Name: autoconf
Version: 2.69
Release: owl1
License: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/autoconf/autoconf-%version.tar.xz
Patch0: %name-2.69-owl-awk.diff
Patch1: %name-2.69-owl-tmp.diff
Patch2: %name-2.69-alt-_AC_PATH_X_XMKMF.diff
Patch3: %name-2.59-alt-AC_PROG_CXXCPP.diff
Patch4: %name-2.69-alt-AC_LANG_FUNC_LINK_TRY_GCC_BUILTIN.diff
Patch5: %name-2.69-alt-sanitize.diff
Patch6: %name-2.69-alt-tools.diff
Patch7: %name-2.69-alt-tests.diff
Patch8: %name-2.69-alt-up-doc-updates.diff
Patch9: %name-2.69-owl-skip-test-209.diff
Requires(pre): /sbin/install-info
Requires: gawk, m4 >= 1.4.17, perl, textutils
Requires: mktemp >= 1:1.3.1
BuildArchitectures: noarch
BuildRequires: sed, m4 >= 1.4.17, texinfo
BuildRoot: /override/%name-%version

%description
Autoconf is a tool for producing shell scripts that automatically
configure software source code packages to adapt to many kinds of
Unix-like systems.  The configuration scripts produced by Autoconf
are independent of Autoconf when they are run, so their users do not
need to have Autoconf.  Using Autoconf, programmers can create
portable and configurable software.

%prep
%setup -q
%patch0 -p1 -b .awk
%patch1 -p1 -b .tmp
%patch2 -p1 -b .AC_PATH
%patch3 -p1 -b .AC_PROG
%patch4 -p1 -b .AC_LANG
%patch5 -p1 -b .sanitize
%patch6 -p1 -b .tools
%patch7 -p1 -b .tests
%patch8 -p1 -b .doc-updates
%patch9 -p1 -b .skip-test-209

%build
%configure
%__make

%install
rm -rf %buildroot
mkdir -p %buildroot%_infodir

%makeinstall

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm %buildroot%_infodir/standards*

# Remove unpackaged files
rm %buildroot%_infodir/dir

%check
%__make check

%post
/sbin/install-info %_infodir/autoconf.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/autoconf.info %_infodir/dir
fi

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %_bindir/*
%_infodir/*.info*
%_datadir/autoconf
%_mandir/man1/*

%changelog
* Sat Jun 14 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.69-owl1
- Updated to 2.69.
- Regenerated the -owl-awk patch.
- Regenerated and enhanced (by including install-sh) the -owl-tmp patch.
- Dropped the accepted RH patch.
- Updated ALT Linux patches from http://git.altlinux.org/gears/a/autoconf_2.60.git and introduced some more.
- Introduced the testsuite in the %%check section.

* Mon Jun 26 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.59-owl3
- Imported autoconf macros patches from autoconf-2.59-alt5 package.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.59-owl2
- Corrected info files installation.

* Sat Sep 11 2004 Solar Designer <solar-at-owl.openwall.com> 2.59-owl1
- Make it official, and do not use RPM's exclude macro on info dir file just
yet to avoid introducing additional chicken-egg problems.

* Wed Feb 25 2004 Michail Litvak <mci-at-owl.openwall.com> 2.59-owl0.1
- 2.59
- Patch to use mktemp in a fail-close way.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 2.13-owl10
- Deal with info dir entries such that the menu looks pretty.

* Thu Jan 24 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.
- Based the new package description on the texinfo documentation.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import spec from RH
- fix URL

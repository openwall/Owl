# $Owl: Owl/packages/autoconf/autoconf.spec,v 1.15 2006/06/26 22:13:35 ldv Exp $

Summary: A GNU tool for automatically configuring source code.
Name: autoconf
Version: 2.59
Release: owl3
License: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/autoconf/autoconf-%version.tar.bz2
Patch0: autoconf-2.59-owl-awk.diff
Patch1: autoconf-2.59-owl-tmp.diff
Patch2: autoconf-2.59-alt-warnings.diff
Patch3: autoconf-2.59-alt-_AC_PATH_X_XMKMF.diff
Patch4: autoconf-2.59-alt-AC_PROG_CXXCPP.diff
Patch5: autoconf-2.59-alt-AC_LANG_FUNC_LINK_TRY_GCC_BUILTIN.diff
Patch6: autoconf-2.59-rh-_AC_PATH_X_DIRECT.diff
PreReq: /sbin/install-info
Requires: gawk, m4, mktemp, perl, textutils
Requires: mktemp >= 1:1.3.1
BuildArchitectures: noarch
BuildRequires: sed, m4, texinfo
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

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

%post
/sbin/install-info %_infodir/autoconf.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/autoconf.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%_bindir/*
%_infodir/*.info*
%_datadir/autoconf
%_mandir/man1/*

%changelog
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

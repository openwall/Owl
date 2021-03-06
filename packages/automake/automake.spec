# $Owl: Owl/packages/automake/automake.spec,v 1.21 2014/07/12 13:48:12 galaxy Exp $

%define api_version 1.14

Summary: A GNU tool for automatically creating Makefiles.
Name: automake
Version: %{api_version}.1
Release: owl1
License: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/automake/
Source: ftp://ftp.gnu.org/gnu/automake/automake-%version.tar.xz
Patch0: %name-1.14-owl-info.diff
Patch1: %name-1.14-owl-tmp.diff
Requires(post,preun): /sbin/install-info
Requires: perl
BuildRequires: autoconf >= 2.65
BuildRequires: texinfo >= 4.8
BuildArchitectures: noarch
BuildRoot: /override/%name-%version

%description
Automake is a tool for creating GNU Standards-compliant Makefiles from
template files.

%prep
%setup -q
%patch0 -p1 -b .info
%patch1 -p1 -b .tmp

# There is a known issue with the following 2 tests, they fail to run with
# the recent versions of flex when linked against libfl.so.  If we link
# them against libfl.a, they are OK, so let's apply this as a temporary
# workaround here.  We are patching it here since the lib directory is
# architecture dependent and it would require a non-trivial patch.
sed -i 's,^[[:space:]]*./configure,LEXLIB="%_libdir/libfl.a" &,' \
	t/lex-{clean,depend}-cxx.sh

bzip2 -9k ChangeLog NEWS

%build
%configure
%__make

%check
%{expand:%%{!?_with_test: %%{!?_without_test: %%global _without_test --without-test}}}
%__make check

%install
rm -rf -- '%buildroot'
%makeinstall

mkdir -p '%buildroot%_datadir/aclocal'

# suppress the dependencies generation for tap-driver.pl since it uses
# TAP::Parser which we do not currently provide.
chmod 0644 '%buildroot%_datadir/automake-%api_version/tap-driver.pl'

# Remove unpackaged files
rm -- '%buildroot%_infodir/dir'
rm -- '%buildroot%_docdir/%name/'amhello*.tar.*

%post
/sbin/install-info '%_infodir/automake.info' '%_infodir/dir'

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete '%_infodir/automake.info' '%_infodir/dir'
fi

%files
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING ChangeLog.bz2 NEWS.bz2 README THANKS
%attr(0755,root,root) %_bindir/*
%_infodir/*.info*
%dir %_datadir/automake-%api_version
%_datadir/automake-%api_version/Automake
%_datadir/automake-%api_version/am
%_datadir/automake-%api_version/COPYING
%_datadir/automake-%api_version/INSTALL
%_datadir/automake-%api_version/texinfo.tex
%attr(0755,root,root) %_datadir/automake-%api_version/ar-lib
%attr(0755,root,root) %_datadir/automake-%api_version/compile
%attr(0755,root,root) %_datadir/automake-%api_version/config.guess
%attr(0755,root,root) %_datadir/automake-%api_version/config.sub
%attr(0755,root,root) %_datadir/automake-%api_version/depcomp
%attr(0755,root,root) %_datadir/automake-%api_version/install-sh
%attr(0755,root,root) %_datadir/automake-%api_version/mdate-sh
%attr(0755,root,root) %_datadir/automake-%api_version/missing
%attr(0755,root,root) %_datadir/automake-%api_version/mkinstalldirs
%attr(0755,root,root) %_datadir/automake-%api_version/py-compile
%attr(0755,root,root) %_datadir/automake-%api_version/tap-driver.pl
%attr(0755,root,root) %_datadir/automake-%api_version/tap-driver.sh
%attr(0755,root,root) %_datadir/automake-%api_version/test-driver
%attr(0755,root,root) %_datadir/automake-%api_version/ylwrap
%_datadir/aclocal-%api_version
%dir %_datadir/aclocal
%_datadir/aclocal/README
%_mandir/man1/aclocal*.1*
%_mandir/man1/automake*.1*

%changelog
* Sun Jun 15 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.14.1-owl1
- Updated to 1.14.1.
- Replaced the deprecated PreReq tag with Requires(post,preun).

* Sun Aug 30 2009 Solar Designer <solar-at-owl.openwall.com> 1.9.6-owl2
- Allow for overriding BUILD_TEST without having to edit this spec file.

* Tue Jun 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.9.6-owl1
- Updated to 1.9.6.

* Thu May 26 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.9.5-owl2
- Fixed temporary directory handling issue in texinfo documentation
examples.
- Corrected info files installation.

* Wed Mar 30 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.9.5-owl1
- Updated to 1.9.5.
- Added texinfo >= 4.8 to BuildRequires.
- Changed make to %%__make in the spec file.
- Removed INSTALL from documentation since it isn't needed there.
- Compressed ChangeLog to save some space.
- Added optional testsuite.

* Sat Sep 11 2004 Solar Designer <solar-at-owl.openwall.com> 1.8.3-owl1
- Make it official, and do not use RPM's exclude macro on info dir file just
yet to avoid introducing additional chicken-egg problems.

* Tue Mar 09 2004 Michail Litvak <mci-at-owl.openwall.com> 1.8.3-owl0.1
- 1.8.3 (fixes a vulnerability discovered by Stefan Nordhausen).

* Wed Feb 25 2004 Michail Litvak <mci-at-owl.openwall.com> 1.8.2-owl0.1
- 1.8.2
- spec cleanups.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 1.4-owl9
- Deal with info dir entries such that the menu looks pretty.

* Thu Jan 24 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.
- Based the new package description on the texinfo documentation.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH
- fix URL

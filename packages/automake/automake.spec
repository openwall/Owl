# $Id: Owl/packages/automake/automake.spec,v 1.11 2005/04/19 03:05:02 galaxy Exp $

%define BUILD_TEST 0

%define api_version 1.9

Summary: A GNU tool for automatically creating Makefiles.
Name: automake
Version: %{api_version}.5
Release: owl1
License: GPL
Group: Development/Tools
URL: http://sourceware.cygnus.com/automake/
Source: ftp://ftp.gnu.org/gnu/automake/automake-%version.tar.bz2
Patch0: automake-1.9.5-owl-info.diff
PreReq: /sbin/install-info
Requires: perl
BuildRequires: autoconf >= 2.59
BuildRequires: texinfo >= 4.8
BuildArchitectures: noarch
BuildRoot: /override/%name-%version

%description
Automake is a tool for creating GNU Standards-compliant Makefiles from
template files.

%prep
%setup -q
%patch0 -p1

%build
%configure
%__make
%if %BUILD_TEST
%__make check
%endif

%install
rm -rf %buildroot
%makeinstall

bzip2 -9f ChangeLog

mkdir -p %buildroot%_datadir/aclocal

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/automake.info.gz %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/automake.info.gz %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog.bz2 NEWS README THANKS TODO
%_bindir/*
%_infodir/*.info*
%_datadir/automake-%api_version
%_datadir/aclocal-%api_version
%dir %_datadir/aclocal

%changelog
* Wed Mar 30 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 1.9.5-owl1
- Updated to 1.9.5.
- Added texinfo >= 4.8 to BuildRequires.
- Changed make to %%__make in the spec file.
- Removed INSTALL from documentation since it isn't needed there.
- Compressed ChangeLog to save some space.
- Added optional testsuite.

* Sat Sep 11 2004 Solar Designer <solar@owl.openwall.com> 1.8.3-owl1
- Make it official, and do not use RPM's exclude macro on info dir file just
yet to avoid introducing additional chicken-egg problems.

* Tue Mar 09 2004 Michail Litvak <mci@owl.openwall.com> 1.8.3-owl0.1
- 1.8.3 (fixes a vulnerability discovered by Stefan Nordhausen).

* Wed Feb 25 2004 Michail Litvak <mci@owl.openwall.com> 1.8.2-owl0.1
- 1.8.2
- spec cleanups.

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com> 1.4-owl9
- Deal with info dir entries such that the menu looks pretty.

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.
- Based the new package description on the texinfo documentation.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- fix URL

# $Id: Owl/packages/automake/automake.spec,v 1.9 2004/11/02 02:32:02 solar Exp $

%define api_version 1.8

Summary: A GNU tool for automatically creating Makefiles.
Name: automake
Version: %{api_version}.3
Release: owl1
License: GPL
Group: Development/Tools
URL: http://sourceware.cygnus.com/automake/
Source: ftp://ftp.gnu.org/gnu/automake/automake-%version.tar.bz2
Patch0: automake-1.8.2-owl-info.diff
PreReq: /sbin/install-info
Requires: perl
BuildRequires: autoconf >= 2.59
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
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

mkdir -p $RPM_BUILD_ROOT%_datadir/aclocal

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
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%_bindir/*
%_infodir/*.info*
%_datadir/automake-%api_version
%_datadir/aclocal-%api_version
%dir %_datadir/aclocal

%changelog
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

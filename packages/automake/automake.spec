# $Id: Owl/packages/automake/automake.spec,v 1.4 2002/08/26 15:05:43 mci Exp $

Summary: A GNU tool for automatically creating Makefiles.
Name: automake
Version: 1.4
Release: owl9
License: GPL
Group: Development/Tools
URL: http://sourceware.cygnus.com/automake/
Source: ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.gz
Patch0: automake-1.4-rh-copytosourcedir.diff
Patch1: automake-1.4-owl-info.diff
PreReq: /sbin/install-info
Requires: perl
BuildArchitectures: noarch
BuildRoot: /override/%{name}-%{version}

%description
Automake is a tool for creating GNU Standards-compliant Makefiles from
template files.

%prep
%setup -q
%patch0 -p0
%patch1 -p1

%build
rm automake.info
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/automake.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/automake.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%{_bindir}/*
%{_infodir}/*.info*
%{_datadir}/automake
%{_datadir}/aclocal

%changelog
* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.
- Based the new package description on the texinfo documentation.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- fix URL

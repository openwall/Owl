# $Id: Owl/packages/automake/automake.spec,v 1.3 2002/02/04 17:13:23 solar Exp $

Summary: A GNU tool for automatically creating Makefiles.
Name: automake
Version: 1.4
Release: owl8
License: GPL
Group: Development/Tools
URL: http://sourceware.cygnus.com/automake/
Source: ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.gz
Patch: automake-1.4-rh-copytosourcedir.diff
PreReq: /sbin/install-info
Requires: perl
BuildArchitectures: noarch
BuildRoot: /override/%{name}-%{version}

%description
Automake is a tool for creating GNU Standards-compliant Makefiles from
template files.

%prep
%setup -q
%patch -p0

%build
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
* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.
- Based the new package description on the texinfo documentation.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- fix URL

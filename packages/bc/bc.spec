# $Id: Owl/packages/bc/bc.spec,v 1.5 2002/08/26 15:08:05 mci Exp $

Summary: GNU's bc (a numeric processing language) and dc (a calculator).
Name: bc
Version: 1.06
Release: owl3
License: GPL
Group: Applications/Engineering
Source: ftp://ftp.gnu.org/gnu/bc/bc-%{version}.tar.gz
Patch0: bc-1.06-owl-info.diff
Patch1: bc-1.06-owl-functions-fix.diff
PreReq: /sbin/install-info, grep
Prefix: %{_prefix}
BuildRequires: texinfo, readline-devel
BuildRoot: /override/%{name}-%{version}

%description
The bc package includes bc and dc.  bc implements a numeric processing
language with interactive execution of statements.  dc is a stack-based
calculator.  Both bc and dc support arbitrary precision arithmetic.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm doc/*.info
makeinfo
%configure --with-readline
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/bc.info.gz %{_infodir}/dir
/sbin/install-info %{_infodir}/dc.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/bc.info.gz %{_infodir}/dir
	/sbin/install-info --delete %{_infodir}/dc.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
/usr/bin/dc
/usr/bin/bc
%{_mandir}/*/*
%{_infodir}/*.info*

%changelog
* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Install the info dir entry for bc as well.
- Enforce our new spec file conventions.
- Wrote a cleaner package description.

* Thu Dec 07 2000 Solar Designer <solar@owl.openwall.com>
- Fixed a bug in the loading of functions (this affected primarily the
built-in math library).

* Mon Nov 21 2000 Michail Litvak <mci@owl.openwall.com>
- Updated to 1.06 version
- added patch to avoid creation of dir file

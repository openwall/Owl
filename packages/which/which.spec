# $Id: Owl/packages/which/which.spec,v 1.4 2002/02/03 00:18:04 solar Exp $

Summary: Displays where a particular program in your path is located.
Name: which
Version: 2.12
Release: owl2
License: GPL
Group: Applications/System
Source0: ftp://ftp.gnu.org/gnu/which/%{name}-%{version}.tar.gz
Source1: which-2.sh
Source2: which-2.csh
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
The which command shows the full pathname of a specified program, if
the specified program is in your PATH.

%prep
%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -m 755 $RPM_SOURCE_DIR/which-2.{sh,csh} $RPM_BUILD_ROOT/etc/profile.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc EXAMPLES README
%{_bindir}/*
%config /etc/profile.d/which-2.*
%{_mandir}/*/*

%changelog
* Sat Feb 02 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Nov 19 2000 Michail Litvak <mci@owl.openwall.com>
- Imported from RH.
- update to 2.12

# $Id: Owl/packages/hdparm/hdparm.spec,v 1.6 2002/02/04 06:50:08 solar Exp $

Summary: A utility for displaying and/or setting hard disk parameters.
Name: hdparm
Version: 4.1
Release: owl4
License: BSD
Group: Applications/System
Source: http://www.ibiblio.org/pub/Linux/system/hardware/%{name}-%{version}.tar.gz
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
hdparm - get/set hard disk parameters for IDE drives.

%prep
%setup -q

%build
sed -e "s/-O2/$RPM_OPT_FLAGS/g" < Makefile > Makefile.optflags
make -f Makefile.optflags

%install
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8
install -c -s -m 755 hdparm $RPM_BUILD_ROOT/sbin/hdparm
install -c -m 644 hdparm.8 $RPM_BUILD_ROOT/%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc hdparm.lsm Changelog
/sbin/hdparm
%{_mandir}/man8/hdparm.8*

%changelog
* Sun Feb 03 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Sat Mar 31 2001 Michail Litvak <mci@owl.openwall.com>
- description fix

* Wed Mar 28 2001 Michail Litvak <mci@owl.openwall.com>
- use sed instead of perl
- removed old RH changelog

* Tue Mar 27 2001 Michail Litvak <mci@owl.openwall.com>
- Import spec from RH.
- version 4.1

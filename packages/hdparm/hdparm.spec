# $Id: Owl/packages/hdparm/hdparm.spec,v 1.2 2001/03/28 10:42:56 mci Exp $

Summary: A utility for displaying and/or setting hard disk parameters.
Name: hdparm
Version: 4.1
Release: 2owl
Copyright: BSD
Group: Applications/System
Source: http://www.ibiblio.org/pub/Linux/system/hardware/%{name}-%{version}.tar.gz
Prefix: %{_prefix}
Buildroot: /var/rpm-buildroot/%{name}-root

%description
hdparm - get/set hard disk parameters for Linux IDE drives.

%prep
%setup -q

%build
sed -e "s/-O2/$RPM_OPT_FLAGS/g" <Makefile >Makefile.optflags
make -f Makefile.optflags

%install
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT/usr/doc
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
* Wed Mar 28 2001  Michail Litvak <mci@owl.openwall.com>
- use sed instead perl
- removed old RH changelog

* Tue Mar 27 2001 Michail Litvak <mci@owl.openwall.com>
- Import spec from RH.
- version 4.1

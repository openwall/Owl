# $Id: Owl/packages/hdparm/hdparm.spec,v 1.10 2003/01/07 23:19:01 mci Exp $

Summary: A utility for displaying and/or setting hard disk parameters.
Name: hdparm
Version: 5.3
Release: owl1
License: BSD
Group: Applications/System
Source: http://www.ibiblio.org/pub/Linux/system/hardware/%{name}-%{version}.tar.gz
Patch: hdparm-5.3-owl-warnings.diff
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
hdparm - get/set hard disk parameters for IDE drives.

%prep
%setup -q
%patch -p1

%{expand:%%define optflags %optflags -Wall}

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
install -s -m 755 hdparm $RPM_BUILD_ROOT/sbin/
install -m 644 hdparm.8 $RPM_BUILD_ROOT%{_mandir}/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc hdparm.lsm Changelog README.acoustic
/sbin/hdparm
%{_mandir}/man8/hdparm.8*

%changelog
* Wed Jan 08 2003 Michail Litvak <mci@owl.openwall.com>
- 5.3
- Updated -warnings.diff.

* Tue Nov 05 2002 Solar Designer <solar@owl.openwall.com>
- Package README.acoustic.

* Mon Nov 04 2002 Michail Litvak <mci@owl.openwall.com>
- 5.2
- Fixed building with -Wall

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

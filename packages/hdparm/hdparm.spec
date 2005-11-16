# $Owl: Owl/packages/hdparm/hdparm.spec,v 1.17 2005/11/16 13:11:14 solar Exp $

Summary: A utility for displaying and/or setting hard disk parameters.
Name: hdparm
Version: 5.8
Release: owl1
License: BSD
Group: Applications/System
Source: http://www.ibiblio.org/pub/Linux/system/hardware/%name-%version.tar.gz
Patch0: hdparm-5.3-owl-warnings.diff
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
hdparm - get/set hard disk parameters for IDE drives.

%prep
%setup -q
%patch0 -p1

%{expand:%%define optflags %optflags -Wall}

%build
make CC=gcc CFLAGS="%optflags"

%install
mkdir -p %buildroot/sbin
mkdir -p %buildroot%_mandir/man8
install -s -m 755 hdparm %buildroot/sbin/
install -m 644 hdparm.8 %buildroot%_mandir/man8/

%files
%defattr(-,root,root)
%doc hdparm.lsm Changelog README.acoustic
/sbin/hdparm
%_mandir/man8/hdparm.8*

%changelog
* Sun Nov 28 2004 Michail Litvak <mci-at-owl.openwall.com> 5.8-owl1
- 5.8

* Wed Jan 08 2003 Michail Litvak <mci-at-owl.openwall.com> 5.3-owl1
- 5.3
- Updated -warnings.diff.

* Tue Nov 05 2002 Solar Designer <solar-at-owl.openwall.com>
- Package README.acoustic.

* Mon Nov 04 2002 Michail Litvak <mci-at-owl.openwall.com>
- 5.2
- Fixed building with -Wall

* Sun Feb 03 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Sat Mar 31 2001 Michail Litvak <mci-at-owl.openwall.com>
- description fix

* Wed Mar 28 2001 Michail Litvak <mci-at-owl.openwall.com>
- use sed instead of perl
- removed old RH changelog

* Tue Mar 27 2001 Michail Litvak <mci-at-owl.openwall.com>
- Import spec from RH.
- version 4.1

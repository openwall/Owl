# $Owl: Owl/packages/hdparm/hdparm.spec,v 1.21 2008/01/04 00:42:32 ldv Exp $

Summary: An utility for displaying and/or setting hard disk parameters.
Name: hdparm
Version: 7.7
Release: owl1
License: BSD-style
Group: Applications/System
URL: http://sourceforge.net/projects/hdparm/
Source: http://prdownloads.sourceforge.net/hdparm/hdparm-%version.tar.gz
Patch: hdparm-7.7-owl-Makefile.diff
BuildRoot: /override/%name-%version

%description
hdparm utility provides a command line interface to various hard disk
ioctls supported by the Linux SATA/PATA/SAS "libata" subsystem and the
older IDE driver subsystem.

%prep
%setup -q
%patch -p1

%build
CFLAGS="%optflags" %__make CC="%__cc" LDFLAGS=

%install
rm -rf %buildroot
install -D -m755 hdparm %buildroot/sbin/hdparm
install -pD -m644 hdparm.8 %buildroot%_mandir/man8/hdparm.8

%files
%defattr(-,root,root)
%doc hdparm.lsm Changelog LICENSE.TXT README.acoustic
/sbin/hdparm
%_mandir/man8/hdparm.8*

%changelog
* Fri Jan 04 2008 Dmitry V. Levin <ldv-at-owl.openwall.com> 7.7-owl1
- Updated to 7.7.

* Mon Jun 12 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 6.6-owl1
- Updated to 6.6.
- Corrected build to keep upstream compiler options.
- Added URL.

* Sun Dec 25 2005 Michail Litvak <mci-at-owl.openwall.com> 6.3-owl1
- 6.3

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

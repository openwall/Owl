# $Id: Owl/packages/owl-setup/owl-setup.spec,v 1.44 2005/10/26 16:48:49 croco Exp $

Summary: Owl configuration tool.
Name: owl-setup
Version: 0.27
Release: owl1
License: relaxed BSD and (L)GPL-compatible; libraries under LGPL
Group: System Environment/Base
Source: setup-%version.tar.gz
Requires: e2fsprogs, kbd, util-linux
Conflicts: setuptool
BuildRequires: ncurses-devel, cdk-devel
BuildRoot: /override/%name-%version

%description
This is the installation and configuration tool for Owl.

%prep
%setup -q -n setup-%version

%{expand:%%define optflags %optflags -Wall}

%build
CXXFLAGS="%optflags" %__make

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot SBINDIR=%_sbindir

%files
%defattr(-,root,root)
%_sbindir/*

%changelog
* Wed Oct 26 2005 Croco <croco-at-owl.openwall.com> 0.27-owl1
- ncurses-based interface is now able to use colors

* Fri Sep 23 2005 Croco <croco-at-owl.openwall.com> 0.26-owl1
- bug with injectCDKxxx worked around
- scanning fstab for standard entries added; the default entries are
  reformatted to match those in the default fstab
- config module reworked (install root is now a variable)
- scanning the base system for the network settings implemented
- the settle's main menu now doesn't display completion status for
  'shellout', 'exit' and 'reboot' items.
- ncurses-based interface is now enabled (but the dumb is still used by
  default)

* Wed Sep 21 2005 Croco <croco-at-owl.openwall.com> 0.25-owl1
- careful handling of /etc/hosts added
- timezone and keyb. layout in the dumb interface made case insensitive 

* Mon Sep 19 2005 Croco <croco-at-owl.openwall.com> 0.24-owl1
- UTC/local hw clock handled; creation of /etc/sysconfig/clock implemented
- lots of fixes to the ncurses-based interface

* Mon Sep 19 2005 Croco <croco-at-owl.openwall.com> 0.23-owl1
- ext3 is now offered as the default
- removed some unclear dirty workarounds with creating mountpoints
- mountpoints themselves are now forced to be 0700, not 0755

* Mon Sep 12 2005 Croco <croco-at-owl.openwall.com> 0.22-owl1
- Enforce the proper permissions on files created by the installer (regardless
of umask).
- An ncurses-based user interface has been implemented (but not yet enabled).

* Mon Aug 08 2005 Solar Designer <solar-at-owl.openwall.com> 0.21-owl1
- Revised the user interface messages and applied various bugfixes.

* Wed Aug 03 2005 Solar Designer <solar-at-owl.openwall.com> 0.20-owl1
- Replaced with Croco's new installer.

* Mon Oct 20 2003 Solar Designer <solar-at-owl.openwall.com> 0.14-owl1
- Corrected the path to loadkeys(1) (it broke with the move from console-tools
to kbd).

* Thu May 29 2003 Solar Designer <solar-at-owl.openwall.com> 0.13-owl1
- write_to=tcb

* Thu Apr 17 2003 Solar Designer <solar-at-owl.openwall.com> 0.12-owl1
- Use /lib/kbd, not /usr/lib/kbd.

* Fri Oct 04 2002 Michail Litvak <mci-at-owl.openwall.com>
- Support for LILO boot loader configuration.

* Fri Sep 06 2002 Michail Litvak <mci-at-owl.openwall.com>
- Support for keyboard layout configuration
  (thanks to Matthias Schmidt <schmidt at giessen.ccc.de>)
- fix code indenting

* Sun Jul 07 2002 Solar Designer <solar-at-owl.openwall.com>
- Use grep -q in mkfstab.

* Thu May 23 2002 Solar Designer <solar-at-owl.openwall.com>
- No longer set the obsolete FORWARD_IPV4 option.

* Mon Mar 18 2002 Solar Designer <solar-at-owl.openwall.com>
- Fixed a typo in netcfg introduced with a recent update which prevented
the line with primary hostname from being actually written to /etc/hosts.

* Thu Feb 07 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Nov 16 2001 Solar Designer <solar-at-owl.openwall.com>
- Use pam_tcb.

* Tue Oct 09 2001 Michail Litvak <mci-at-owl.openwall.com>
- configure network interface and gateway separately

* Sun Sep 30 2001 Michail Litvak <mci-at-owl.openwall.com>
- don't check gateway presence for network=yes
- don't write localhost with non-local IP to /etc/hosts

* Wed Jul 25 2001 Michail Litvak <mci-at-owl.openwall.com>
- add --cr-wrap option in netcfg to fix broken
  displaying (cause - changes in new dialog version)
- fix bug in mkfstab, now it is possible to add unlisted partitions
  and properly set their type

* Sat Jun 23 2001 Solar Designer <solar-at-owl.openwall.com>
- Grammar/spelling fix for a netcfg message.
- Ensure the newly created /etc/resolv.conf and /etc/hosts are mode 644.

* Wed Jun 06 2001 Michail Litvak <mci-at-owl.openwall.com>
- write domain into resolv.conf

* Tue Dec 26 2000 Michail Litvak <mci-at-owl.openwall.com>
- Initial version.

# $Owl: Owl/packages/owl-setup/owl-setup.spec,v 1.67 2006/04/19 21:10:56 croco Exp $

Summary: Owl configuration tool.
Name: owl-setup
Version: 1.1.2
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
%__make install DESTDIR=%buildroot SBINDIR=%_sbindir MANDIR=%_mandir

%files
%defattr(-,root,root)
%_sbindir/*
%_mandir/man8/setup.8*
%_mandir/man8/settle.8*

%changelog
* Wed Apr 20 2006 Croco <croco-at-owl.openwall.com> 1.1.2-owl1
- quick search string displaying added to ncurses item lists

* Mon Apr 10 2006 Croco <croco-at-owl.openwall.com> 1.1.1-owl1
- manual pages for both settle and setup created
- general cancellable progress indicators implemented in both interfaces
- 'install kernel headers' is now done with a fancy progress indicator
- quick search implemented in scroll list selections
- 'blind' input within iface_dumb changed to display nothing at all
- PAM service name moved into the config.* module
- several cosmetic fixes

* Sat Mar 25 2006 Croco <croco-at-owl.openwall.com> 1.1.0-owl1
- ru2 keymap workaround created
- backspace hack replaced with manual echo in the dumb interface
- talking to PAM when setting root passwd implemented
- waiting for a key after installing packages & kernel headers implemented

* Sun Feb 12 2006 Solar Designer <solar-at-owl.openwall.com> 1.0.1-owl1
- Updated the "vi newbie" notice to suggest ":qa!" to quit VIM such that both
the help and the fstab windows are closed.

* Tue Feb 07 2006 Solar Designer <solar-at-owl.openwall.com> 1.0-owl1
- Disable x86-specific menu options in "settle" when building for non-x86.
- Use keyboard layouts from /lib/kbd/keymaps/sun on SPARC.

* Fri Feb 03 2006 Croco <croco-at-owl.openwall.com> 0.35-owl1
- VMIN/VTIME worked around for bloody suns
- ip4areas replaced with the version 0.3.1 which might run better on 64-bit
- added some workarounds for non-x86 architectures
- changed vim command line to display help window on the start
- fixed help (invalid cmdline) message for setup
- added chmod after creating the '/var' directory

* Tue Jan 24 2006 Croco <croco-at-owl.openwall.com> 0.34-owl1
- tmpfs fstab entry fixed
- fixed a problem with /var/tmp->/tmp symlink in case there's no /var yet
- the "Run mkswap?" question now defaults to YES
- 'installing headers' now run /bin/cp in verbose mode
- screen is now forced to get clear on exit from ncurses-faced programs
- newbie notice added before launching vi on /etc/fstab

* Fri Jan 06 2006 Croco <croco-at-owl.openwall.com> 0.33-owl1
- sorting criteria for kbd/tz selection fine tuned

* Mon Jan 04 2006 Croco <croco-at-owl.openwall.com> 0.32-owl1
- ncurses interface fixed to allow multiline prompts for string queries
  and to omit blank lines atop a menu if there's no caption
- partition selection dialog now offers to use an unlisted partition
- two fixes to the 'install kernel headers' feature

* Mon Jan 04 2006 Croco <croco-at-owl.openwall.com> 0.31-owl1
- install kernel headers feature added
- timezone and keyboard item lists are now alphabetically sorted
- tmpfs is now offered for /tmp

* Mon Jan 02 2006 Croco <croco-at-owl.openwall.com> 0.30-owl1
- checking whether the /etc/localtime is UTC added
- ncurses interface is now enabled by default
- command line is now parsed using getopt(3) and the code is now in a 
  separated module

* Sat Dec 10 2005 Croco <croco-at-owl.openwall.com> 0.29-owl1
- Automatic curses-incapable terminal detection added
- color scheme changed for ncurses interface
- fixed the bug with 'select your boot device' notice
- changed the settle's quit message to reflect full path of mount points

* Thu Dec 08 2005 Solar Designer <solar-at-owl.openwall.com> 0.28-owl1
- Fixed an infinite recursion bug in scan_net_config().

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

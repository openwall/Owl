# $Id: Owl/packages/owl-setup/owl-setup.spec,v 1.25 2004/11/23 22:40:47 mci Exp $

Summary: Owl configuration tool.
Name: owl-setup
Version: 0.14
Release: owl1
License: mostly public domain, passwdlg is under GPL
Group: System Environment/Base
Source0: Makefile
Source1: passwdlg.c
Source2: setup.pam
Source3: owl-setup.conf
Source4: owl-setup
Source5: mkfstab
Source6: netcfg
Source10: README
Requires: bash >= 2.0, sh-utils, util-linux, sed, mktemp
Requires: dialog
Requires: tcb, kbd
Requires: owl-startup
Conflicts: setuptool
BuildRoot: /override/%name-%version

%description
This is a configuration tool to initially setup fstab, networking,
root password, and timezone.  This is a temporary solution and will
be replaced with a more consistent and reliable tool in the future.

%prep
%setup -n owl-setup -c -T
cp $RPM_SOURCE_DIR/{Makefile,passwdlg.c,README} .
chmod 644 README

%build
make CFLAGS="$RPM_OPT_FLAGS -Wall"

%install
rm -rf %buildroot
mkdir -p %buildroot/{etc/pam.d,usr/lib/owl-setup,usr/sbin}
install -m 600 $RPM_SOURCE_DIR/owl-setup.conf %buildroot/etc/
install -m 700 passwdlg %buildroot/usr/lib/owl-setup/
install -m 600 $RPM_SOURCE_DIR/setup.pam %buildroot/etc/pam.d/setup
install -m 700 $RPM_SOURCE_DIR/owl-setup %buildroot/usr/lib/owl-setup/
install -m 700 $RPM_SOURCE_DIR/mkfstab %buildroot/usr/lib/owl-setup/
install -m 700 $RPM_SOURCE_DIR/netcfg %buildroot/usr/lib/owl-setup/
install -m 644 $RPM_SOURCE_DIR/README %buildroot/usr/lib/owl-setup/
ln -s ../../usr/lib/owl-setup/owl-setup %buildroot/usr/sbin/setup

%files
%defattr(-,root,root)
%doc README
%config /etc/pam.d/setup
%config /etc/owl-setup.conf
/usr/lib/owl-setup
/usr/sbin/setup

%changelog
* Mon Oct 20 2003 Solar Designer <solar@owl.openwall.com> 0.14-owl1
- Corrected the path to loadkeys(1) (it broke with the move from console-tools
to kbd).

* Thu May 29 2003 Solar Designer <solar@owl.openwall.com> 0.13-owl1
- write_to=tcb

* Thu Apr 17 2003 Solar Designer <solar@owl.openwall.com> 0.12-owl1
- Use /lib/kbd, not /usr/lib/kbd.

* Fri Oct 04 2002 Michail Litvak <mci@owl.openwall.com>
- Support for LILO boot loader configuration.

* Fri Sep 06 2002 Michail Litvak <mci@owl.openwall.com>
- Support for keyboard layout configuration
  (thanks to Matthias Schmidt <schmidt@giessen.ccc.de>)
- fix code indenting

* Sun Jul 07 2002 Solar Designer <solar@owl.openwall.com>
- Use grep -q in mkfstab.

* Thu May 23 2002 Solar Designer <solar@owl.openwall.com>
- No longer set the obsolete FORWARD_IPV4 option.

* Mon Mar 18 2002 Solar Designer <solar@owl.openwall.com>
- Fixed a typo in netcfg introduced with a recent update which prevented
the line with primary hostname from being actually written to /etc/hosts.

* Thu Feb 07 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Nov 16 2001 Solar Designer <solar@owl.openwall.com>
- Use pam_tcb.

* Tue Oct 09 2001 Michail Litvak <mci@owl.openwall.com>
- configure network interface and gateway separately

* Sun Sep 30 2001 Michail Litvak <mci@owl.openwall.com>
- don't check gateway presence for network=yes
- don't write localhost with non-local IP to /etc/hosts

* Wed Jul 25 2001 Michail Litvak <mci@owl.openwall.com>
- add --cr-wrap option in netcfg to fix broken
  displaying (cause - changes in new dialog version)
- fix bug in mkfstab, now it is possible to add unlisted partitions
  and properly set their type

* Sat Jun 23 2001 Solar Designer <solar@owl.openwall.com>
- Grammar/spelling fix for a netcfg message.
- Ensure the newly created /etc/resolv.conf and /etc/hosts are mode 644.

* Wed Jun 06 2001 Michail Litvak <mci@owl.openwall.com>
- write domain into resolv.conf

* Tue Dec 26 2000 Michail Litvak <mci@owl.openwall.com>
- Initial version.

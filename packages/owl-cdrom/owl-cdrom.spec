# $Owl: Owl/packages/owl-cdrom/owl-cdrom.spec,v 1.56 2010/07/25 00:11:58 solar Exp $

Summary: Directory hierarchy changes and files needed for bootable CD-ROMs.
Name: owl-cdrom
Version: 1.11
Release: owl1
License: public domain
Group: System Environment/Base
Source0: rc.ramdisk
Source1: welcome-cdrom.sh
Source10: lilo.conf
Source11: floppy-update.sh
Source12: message
Requires: owl-startup >= 0.15-owl1
ExclusiveArch: %ix86 x86_64
BuildRoot: /override/%name-%version

%description
This package applies directory hierarchy changes and provides additional
startup scripts needed for Owl bootable CD-ROMs.

%install
rm -rf %buildroot
mkdir -p %buildroot/{etc/{rc,profile}.d,boot,rom,ram,owl}

cd %buildroot
touch .Owl-CD-ROM
install -m 700 %_sourcedir/rc.ramdisk etc/rc.d/
install -m 755 %_sourcedir/welcome-cdrom.sh etc/profile.d/
install -m 600 %_sourcedir/lilo.conf etc/lilo.conf.bootcd
install -m 700 %_sourcedir/floppy-update.sh boot/
install -m 600 %_sourcedir/message boot/
ln -s ../rom/{dev,etc,home,root,tmp,var,world} ram/

%pre
if [ "$MAKE_CDROM" != yes ]; then
	echo "Please set \"MAKE_CDROM=yes\" if you know what you're doing"
	exit 1
fi

%post
set -e

chmod 755 /
chown root:root /

for DIR in dev etc home root tmp var vz; do
	test -d /$DIR -a ! -e /rom/$DIR
	mv /$DIR /rom/
	ln -s ram/$DIR /
done

test -d /usr/src/world -a ! -e /rom/world
mv /usr/src/world /rom/
ln -s ../../ram/world /usr/src/

%preun
set -e

if [ $1 -eq 0 ]; then
	for DIR in dev etc home root tmp var; do
		test -L /$DIR -a -d /rom/$DIR
		rm /$DIR
		mv /rom/$DIR /
	done

	test -L /usr/src/world -a -d /rom/world
	rm /usr/src/world
	mv /rom/world /usr/src/
fi

%files
%defattr(-,root,root)
/.Owl-CD-ROM
%config /etc/rc.d/rc.ramdisk
%config /etc/profile.d/welcome-cdrom.sh
%config /etc/lilo.conf.bootcd
/boot/floppy-update.sh
/boot/message
%dir /rom
/ram
%dir /owl

%changelog
* Sat Jul 24 2010 Solar Designer <solar-at-owl.openwall.com> 1.11-owl1
- Dropped most LILO boot targets, leaving only two: "normal" and "rescue"
(new names for what was previously known as "autodetect" and "custom").
- Reduced the LILO menu timeout from 60 to 5 seconds.
- Updated the boot menu message to reflect the changes to the menu items.
- Increased the rootdelay= setting from 10 to 30 seconds now that its
meaning is slightly different with our magic root=/dev/cdrom setting (it's
the maximum number of 1-second retries, not an initial delay anymore).
- Revised welcome-cdrom.sh in numerous ways: don't bother looking for kernel
sources (they won't be found in a separate "top level" directory anymore),
refer to the source code tree without calling it "userland" (now that it
contains the kernel as well), provide simpler and more correct instructions
for setting a Cyrillic font (now via a shell alias), use highlighting of
command names (instead of double-quotes) when outputting to a terminal, set
LC_CTYPE=en_US by default (sufficient for browsing the German and French
documentation translations).

* Wed Jul 21 2010 Solar Designer <solar-at-owl.openwall.com> 1.10-owl1
- Added a new LILO boot target called "autodetect" (making use of the new
"root=/dev/cdrom" feature of our kernel patch) and made it the default.

* Mon Jul 19 2010 Solar Designer <solar-at-owl.openwall.com> 1.9-owl1
- Updated for RPM'ed kernel.

* Mon Mar 22 2010 Solar Designer <solar-at-owl.openwall.com> 1.8-owl1
- Updated the configs for 2.6.18-164.15.1.el5.028stab068.5-owl1.
- Use rootdelay=10 with the non-ide label to allow for booting off USB devices.

* Mon Nov 23 2009 Solar Designer <solar-at-owl.openwall.com> 1.7-owl1
- Updated for 2.6/OpenVZ kernels.
- Don't automatically copy /etc/vz/dists (which is a bit large) to /ram.
- Move /vz to /ram.

* Fri May 29 2009 Solar Designer <solar-at-owl.openwall.com> 1.6-owl1
- Disabled the USB EHCI driver in dot-config*, because it resulted in a lockup
on boot at least on Samsung Q45 laptops.
- Switched to the non-alternative USB UHCI driver.
- Install the kernel config file as /boot/config, not /boot/.config, to make it
more visible.

* Wed May 27 2009 Solar Designer <solar-at-owl.openwall.com> 1.5-owl1
- Added menu-title and menu-scheme settings to lilo.conf.

* Sun May 24 2009 Solar Designer <solar-at-owl.openwall.com> 1.4-owl1
- Updated to Linux 2.4.37.1-ow1.
- In dot-config* files enabled SCSI generic support (as needed for CD/DVD
recording), UDF filesystem support (read-only), more SATA and NIC drivers,
CONFIG_HARDEN_VM86 and CONFIG_HARDEN_PAGE0 (as introduced with recent
-ow patches).
- Partially sync'ed dot-config-x86_64 to the plain x86 dot-config.
- Use tmpfs instead of a fixed-size RAM disk filesystem.
- When copying files to /ram, order them by inode number to hopefully
reduce the number and/or distance of CD drive seeks (suggested by
Willy Tarreau).
- Added a new LILO label called "custom", which gives the user full
control over kernel parameters.

* Sat Jul 05 2008 Solar Designer <solar-at-owl.openwall.com> 1.3-owl1
- Install lilo.conf as lilo.conf.bootcd to not conflict with the ghost
from our updated lilo package.

* Fri Jun 01 2007 Solar Designer <solar-at-owl.openwall.com> 1.2-owl1
- In dot-config for plain x86, enabled more IDE chipset drivers (ALI15X3,
PDC202XX_OLD, PDC202XX_NEW, SVWKS, SIS5513, VIA82CXXX), RAID controller
drivers (CONFIG_BLK_DEV_3W_XXXX_RAID, CONFIG_SCSI_DPT_I2O), SCSI emulation
and SATA support (CONFIG_BLK_DEV_IDESCSI, CONFIG_SCSI_SATA), SATA drivers
for AHCI and ICH (CONFIG_SCSI_SATA_AHCI, CONFIG_SCSI_ATA_PIIX), USB and
HID support (CONFIG_USB, EHCI_HCD, UHCI_ALT, OHCI, HID, HIDINPUT;
CONFIG_INPUT, KEYBDEV, MOUSEDEV), USB storage support (CONFIG_USB_STORAGE),
NFS v3 client (CONFIG_NFS_V3).
- In lilo.conf, renamed the "scsi" option to "non-ide" as it should also
work for USB drives.

* Thu Oct 26 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.1-owl1
- Changed floppy geometry from 1.44Mb to 2.88Mb floppy.
- Removed explicit loopback device specification.
- Updated dot-config, added dot-config-x86_64.

* Sun Feb 12 2006 Solar Designer <solar-at-owl.openwall.com> 1.0-owl1
- Updated the suggested "setfont ..." command in welcome-cdrom.sh to apply to
our current version of kbd.

* Thu Sep 22 2005 Solar Designer <solar-at-owl.openwall.com> 0.15-owl1
- Updated lilo.conf according to suggestions from John Coffman: added
"backup=/dev/null", "geometric", "el-torito-bootable-CD", removed "install=..."
since its syntax changed and the file is now linked into LILO anyway.
- Moved the common "read-only" and "append=..." options to the global list.

* Tue Sep 13 2005 Solar Designer <solar-at-owl.openwall.com> 0.14-owl1
- Updated the message in welcome-cdrom.sh for the new owl-setup.
- Install /boot/.config as world-readable.
- Allow for LILO to be built with no external /boot/boot* files.

* Sun Jul 03 2005 Solar Designer <solar-at-owl.openwall.com> 0.13-owl1
- Updated to Linux 2.4.31-ow1, dropped support for old 10 Mbps Intel Ethernet
cards.

* Sun Mar 06 2005 Solar Designer <solar-at-owl.openwall.com> 0.12-owl1
- Updated to Linux 2.4.29-ow1, dropped support for parallel ports, SCSI tape
drives, PPP, SLIP, and NFS server to make the kernel still fit on a floppy
when built with the new gcc (3.4.3).
- Have LILO display a message explaining that it's the controller for the
CD-ROM device that is being requested in the boot menu.

* Sun Apr 18 2004 Solar Designer <solar-at-owl.openwall.com> 0.11-owl1
- Updated to Linux 2.4.26-ow1.
- Include the Broadcom Tigon3 Gigabit Ethernet driver and the BusLogic
SCSI controller driver (the latter is apparently needed under VMware).
- Dropped support for IrDA to make room for the above.

* Thu Feb 05 2004 Solar Designer <solar-at-owl.openwall.com> 0.10-owl1
- In lilo.conf, pass the "rootfstype=iso9660" kernel option to get rid of
the ugly error message resulting from the kernel trying FAT first; thanks
to Nergal for the suggestion.

* Fri Dec 19 2003 Solar Designer <solar-at-owl.openwall.com> 0.9-owl1
- Linux 2.4.23-ow1 + cryptoloop (w/ AES compiled in).
- Support Silicon Image SATA controllers (CONFIG_BLK_DEV_SIIMAGE).

* Tue Oct 21 2003 Solar Designer <solar-at-owl.openwall.com> 0.8-owl1
- Switch to using the new SYM53C8XX driver which supports the whole range
of PCI SCSI controllers from NCR / Symbios Logic SCSI-2 to new LSI Logic
Ultra-160 ones.

* Mon Oct 20 2003 Solar Designer <solar-at-owl.openwall.com> 0.7-owl1
- In the "welcome" script, report the Owl version from /.Owl-CD-ROM,
correctly locate documentation when multiple branches are available, and
explain how to set Cyrillic font.

* Sun Oct 19 2003 Solar Designer <solar-at-owl.openwall.com> 0.6-owl1
- Updated .config for Linux 2.4.22-ow1, require at least a Pentium (need
TSC, and math emulation for older CPUs which could be missing a coprocessor
is too big), dropped PCMCIA and USB support to make the kernel with certain
more relevant 2.4.x-specific features (e.g., ext3fs) still fit on a 1.44 MB
"floppy".

* Tue Sep 10 2002 Solar Designer <solar-at-owl.openwall.com> 0.5-owl1
- Build the CD kernels with SMP, it is always possible to disable SMP
with "nosmp" on the kernel command line.
- In the "welcome" script, explicitly tell ls to list entries by lines
instead of by columns (-x) and ignore CVS directories (-I CVS).

* Thu Aug 22 2002 Solar Designer <solar-at-owl.openwall.com>
- Added a "welcome" script to introduce the user to directory locations.
- Updated .config for Linux 2.2.21-ow1.

* Sat Jun 22 2002 Solar Designer <solar-at-owl.openwall.com>
- Style change with plural form of abbreviations (CD-ROM's -> CD-ROMs).

* Tue Apr 02 2002 Solar Designer <solar-at-owl.openwall.com>
- Marked this package x86-specific because at this stage it really is.

* Wed Feb 06 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Mon Nov 26 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated .config for Linux 2.2.20-ow1.

* Wed Oct 03 2001 Solar Designer <solar-at-owl.openwall.com>
- Create an inode per 1024 bytes on the ramdisk or we would get out of
inodes with a 4 MB ramdisk.
- The timeout for root device choice is now 1 minute, not 5 seconds as
the default choice will very often be wrong.

* Sat Sep 15 2001 Solar Designer <solar-at-owl.openwall.com>
- Packaged lilo.conf, .config, and a script to create or update floppy
images for use with CD-ROMs.
- Move /usr/src/world to /ram such that "make installworld" may create
its symlinks and write to its log file.

* Sat Jul 28 2001 Solar Designer <solar-at-owl.openwall.com>
- Require CDROM=yes such that this package isn't installed by mistake.

* Fri Jul 27 2001 Solar Designer <solar-at-owl.openwall.com>
- Initial version.

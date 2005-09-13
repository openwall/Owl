# $Id: Owl/packages/owl-cdrom/owl-cdrom.spec,v 1.31 2005/09/13 14:27:45 solar Exp $

Summary: Directory hierarchy changes and files needed for bootable CD-ROMs.
Name: owl-cdrom
Version: 0.14
Release: owl1
License: public domain
Group: System Environment/Base
Source0: rc.ramdisk
Source1: welcome-cdrom.sh
Source10: lilo.conf
Source11: dot-config
Source12: floppy-update.sh
Source13: message
Requires: owl-startup >= 0.15-owl1
ExclusiveArch: %ix86
BuildRoot: /override/%name-%version

%description
This package applies directory hierarchy changes and provides additional
startup scripts needed for Owl bootable CD-ROMs.

%install
rm -rf %buildroot
mkdir -p %buildroot/{etc/{rc,profile}.d,boot,rom,ram,owl}

cd %buildroot
touch .Owl-CD-ROM
install -m 700 $RPM_SOURCE_DIR/rc.ramdisk etc/rc.d/
install -m 755 $RPM_SOURCE_DIR/welcome-cdrom.sh etc/profile.d/
install -m 600 $RPM_SOURCE_DIR/lilo.conf etc/
install -m 644 $RPM_SOURCE_DIR/dot-config boot/.config
install -m 700 $RPM_SOURCE_DIR/floppy-update.sh boot/
install -m 600 $RPM_SOURCE_DIR/message boot/
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

for DIR in dev etc home root tmp var; do
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
%config /etc/lilo.conf
%config /boot/.config
/boot/floppy-update.sh
/boot/message
%dir /rom
/ram
%dir /owl

%changelog
* Tue Sep 13 2005 Solar Designer <solar@owl.openwall.com> 0.14-owl1
- Updated the message in welcome-cdrom.sh for the new owl-setup.
- Install /boot/.config as world-readable.

* Sun Jul 03 2005 Solar Designer <solar@owl.openwall.com> 0.13-owl1
- Updated to Linux 2.4.31-ow1, dropped support for old 10 Mbps Intel Ethernet
cards.

* Sun Mar 06 2005 Solar Designer <solar@owl.openwall.com> 0.12-owl1
- Updated to Linux 2.4.29-ow1, dropped support for parallel ports, SCSI tape
drives, PPP, SLIP, and NFS server to make the kernel still fit on a floppy
when built with the new gcc (3.4.3).
- Have LILO display a message explaining that it's the controller for the
CD-ROM device that is being requested in the boot menu.

* Sun Apr 18 2004 Solar Designer <solar@owl.openwall.com> 0.11-owl1
- Updated to Linux 2.4.26-ow1.
- Include the Broadcom Tigon3 Gigabit Ethernet driver and the BusLogic
SCSI controller driver (the latter is apparently needed under VMWare).
- Dropped support for IrDA to make room for the above.

* Thu Feb 05 2004 Solar Designer <solar@owl.openwall.com> 0.10-owl1
- In lilo.conf, pass the "rootfstype=iso9660" kernel option to get rid of
the ugly error message resulting from the kernel trying FAT first; thanks
to Nergal for the suggestion.

* Fri Dec 19 2003 Solar Designer <solar@owl.openwall.com> 0.9-owl1
- Linux 2.4.23-ow1 + cryptoloop (w/ AES compiled in).
- Support Silicon Image SATA controllers (CONFIG_BLK_DEV_SIIMAGE).

* Tue Oct 21 2003 Solar Designer <solar@owl.openwall.com> 0.8-owl1
- Switch to using the new SYM53C8XX driver which supports the whole range
of PCI SCSI controllers from NCR / Symbios Logic SCSI-2 to new LSI Logic
Ultra-160 ones.

* Mon Oct 20 2003 Solar Designer <solar@owl.openwall.com> 0.7-owl1
- In the "welcome" script, report the Owl version from /.Owl-CD-ROM,
correctly locate documentation when multiple branches are available, and
explain how to set Cyrillic font.

* Sun Oct 19 2003 Solar Designer <solar@owl.openwall.com> 0.6-owl1
- Updated .config for Linux 2.4.22-ow1, require at least a Pentium (need
TSC, and math emulation for older CPUs which could be missing a coprocessor
is too big), dropped PCMCIA and USB support to make the kernel with certain
more relevant 2.4.x-specific features (e.g., ext3fs) still fit on a 1.44 MB
"floppy".

* Tue Sep 10 2002 Solar Designer <solar@owl.openwall.com> 0.5-owl1
- Build the CD kernels with SMP, it is always possible to disable SMP
with "nosmp" on the kernel command line.
- In the "welcome" script, explicitly tell ls to list entries by lines
instead of by columns (-x) and ignore CVS directories (-I CVS).

* Thu Aug 22 2002 Solar Designer <solar@owl.openwall.com>
- Added a "welcome" script to introduce the user to directory locations.
- Updated .config for Linux 2.2.21-ow1.

* Sat Jun 22 2002 Solar Designer <solar@owl.openwall.com>
- Style change with plural form of abbreviations (CD-ROM's -> CD-ROMs).

* Tue Apr 02 2002 Solar Designer <solar@owl.openwall.com>
- Marked this package x86-specific because at this stage it really is.

* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Mon Nov 26 2001 Solar Designer <solar@owl.openwall.com>
- Updated .config for Linux 2.2.20-ow1.

* Wed Oct 03 2001 Solar Designer <solar@owl.openwall.com>
- Create an inode per 1024 bytes on the ramdisk or we would get out of
inodes with a 4 MB ramdisk.
- The timeout for root device choice is now 1 minute, not 5 seconds as
the default choice will very often be wrong.

* Sat Sep 15 2001 Solar Designer <solar@owl.openwall.com>
- Packaged lilo.conf, .config, and a script to create or update floppy
images for use with CD-ROMs.
- Move /usr/src/world to /ram such that "make installworld" may create
its symlinks and write to its log file.

* Sat Jul 28 2001 Solar Designer <solar@owl.openwall.com>
- Require CDROM=yes such that this package isn't installed by mistake.

* Fri Jul 27 2001 Solar Designer <solar@owl.openwall.com>
- Initial version.

# $Owl: Owl/packages/syslinux/syslinux.spec,v 1.1 2011/10/27 11:20:39 segoon Exp $

Summary: Simple kernel loader which boots from a FAT filesystem.
Name: syslinux
Version: 4.04
Release: owl1
License: GPLv2+
Group: Applications/System
URL: http://syslinux.zytor.com/wiki/index.php/The_Syslinux_Project
Source0: http://www.kernel.org/pub/linux/utils/boot/syslinux/%name-%version.tar.xz
# Signature: https://www.kernel.org/pub/linux/utils/boot/syslinux/%name-%version.tar.sign
ExclusiveArch: %ix86 x86_64
BuildRoot: /override/%name-%version

# NOTE: extlinux belongs in /sbin, not in /usr/sbin, since it is typically
# a system bootloader, and may be necessary for system recovery.
%define _sbindir /sbin


%description
SYSLINUX is a suite of bootloaders, currently supporting DOS FAT
filesystems, Linux ext2/ext3 filesystems (EXTLINUX), PXE network boots
(PXELINUX), or ISO 9660 CD-ROMs (ISOLINUX).  It also includes a tool,
MEMDISK, which loads legacy operating systems from these media.

%package perl
Summary: Syslinux tools written in perl.
Group: Applications/System

%description perl
Syslinux tools written in perl

%package devel
Summary: Headers and libraries for syslinux development.
Group: Development/Libraries

%description devel
Headers and libraries for syslinux development.

%package extlinux
Summary: The EXTLINUX bootloader, for booting the local system.
Group: System/Boot
Requires: syslinux

%description extlinux
The EXTLINUX bootloader, for booting the local system, as well as all
the SYSLINUX/PXELINUX modules in /boot.

%package tftpboot
Summary: SYSLINUX modules in /tftpboot, available for network booting.
Group: Applications/Internet
Requires: syslinux

%description tftpboot
All the SYSLINUX/PXELINUX modules directly available for network
booting in the /tftpboot directory.

%prep
%setup -q -n syslinux-%version

%build
OPTFLAGS="-g -Os -Werror -Wno-unused -finline-limit=2000"
%__make installer OPTFLAGS="$OPTFLAGS"
%__make -C sample tidy

%install
%__make install-all \
	INSTALLROOT=%buildroot BINDIR=%_bindir SBINDIR=%_sbindir \
	LIBDIR=%_prefix/lib DATADIR=%_datadir \
	MANDIR=%_mandir INCDIR=%_includedir \
	TFTPBOOT=/tftpboot EXTLINUXDIR=/boot/extlinux \
	INSTALL_BIN=linux/syslinux

mkdir -p %buildroot/%_docdir/%name-%version/sample
install -m 644 sample/sample.* %buildroot/%_docdir/%name-%version/sample/
mkdir -p %buildroot/etc
cd %buildroot/etc && ln -s ../boot/extlinux/extlinux.conf .

%files
%defattr(-,root,root)
%doc NEWS README* COPYING 
%doc doc/* 
%doc sample
%_mandir/man1/gethostip*
%_mandir/man1/syslinux*
%_mandir/man1/extlinux*
%_bindir/gethostip
%_bindir/isohybrid
%_bindir/memdiskfind
%_bindir/syslinux
%dir %_datadir/syslinux
%_datadir/syslinux/*.com
%_datadir/syslinux/*.exe
%_datadir/syslinux/*.c32
%_datadir/syslinux/*.bin
%_datadir/syslinux/*.0
%_datadir/syslinux/memdisk
%dir %_datadir/syslinux/dosutil
%_datadir/syslinux/dosutil/*
%exclude %_datadir/syslinux/diag/handoff.bin
%exclude %_datadir/syslinux/diag/geodspms.img.xz
%exclude %_datadir/syslinux/diag/geodsp1s.img.xz

%files perl
%defattr(-,root,root)
%_mandir/man1/lss16toppm*
%_mandir/man1/ppmtolss16*
%_mandir/man1/syslinux2ansi*
%_bindir/keytab-lilo
%_bindir/lss16toppm
%_bindir/md5pass
%_bindir/mkdiskimage
%_bindir/ppmtolss16
%_bindir/pxelinux-options
%_bindir/sha1pass
%_bindir/syslinux2ansi
%_bindir/isohybrid.pl

%files devel
%defattr(-,root,root)
%dir %_datadir/syslinux/com32
%_datadir/syslinux/com32

%files extlinux
%_sbindir/extlinux
/boot/extlinux
%config /etc/extlinux.conf

%files tftpboot
/tftpboot

%post extlinux
echo -n 'Checking whether extlinux was installed ... '
if [ -f /boot/extlinux/extlinux.conf ]; then
	echo 'yes, updating:'
	extlinux --update /boot/extlinux
else
	echo 'NOT installed, skipping'
fi

%changelog
* Thu Oct 27 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 4.04-owl1
- Initial import from Fedora.
- Packaged linux/syslinux instead of mtools/syslinux.

# $Owl: Owl/packages/syslinux/syslinux.spec,v 1.9 2012/05/08 20:51:11 solar Exp $

Summary: A collection of boot loaders for the Linux operating system.
Name: syslinux
Version: 4.05
Release: owl1
License: GPLv2+
Group: Applications/System
URL: http://www.syslinux.org
Source0: http://www.kernel.org/pub/linux/utils/boot/syslinux/%name-%version.tar.xz
# Signature: https://www.kernel.org/pub/linux/utils/boot/syslinux/%name-%version.tar.sign
ExclusiveArch: %ix86 x86_64
BuildRoot: /override/%name-%version

# extlinux belongs in /sbin, not in /usr/sbin, since it is typically
# a system bootloader, and may be necessary for system recovery.
%define _sbindir /sbin

%description
SYSLINUX is a collection of boot loaders for the Linux operating system, which
work from Linux ext2/3/4, btrfs, and DOS FAT filesystems (EXTLINUX), from
network servers using PXE firmware (PXELINUX), or from CD/DVD discs (ISOLINUX).
It also includes a tool, MEMDISK, which loads legacy operating systems from
these media.

%package perl
Summary: Syslinux tools written in Perl.
Group: Applications/System

%description perl
Syslinux tools written in Perl.

%package devel
Summary: Headers and libraries for Syslinux development.
Group: Development/Libraries

%description devel
Headers and libraries for Syslinux development.

%package extlinux
Summary: The EXTLINUX bootloader, for booting the local system.
Group: System Environment/Base
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
%__make clean

%build
OPTFLAGS="%optflags -Werror -Wno-unused -finline-limit=2000"
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
install -pm 644 sample/sample.* %buildroot/%_docdir/%name-%version/sample/
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
%_bindir/lss16toppm
%_bindir/mkdiskimage
%_bindir/ppmtolss16
%_bindir/pxelinux-options
%_bindir/syslinux2ansi
%_bindir/isohybrid.pl
# Packaging of keytab-lilo is disabled because the LILO package provides a
# program of the same name on Owl.
%exclude %_bindir/keytab-lilo
# The below two are disabled because they depend on perl(Crypt::PasswdMD5) and
# perl(Digest::SHA1), which are not part of Owl.
%exclude %_bindir/md5pass
%exclude %_bindir/sha1pass

%files devel
%defattr(-,root,root)
%_datadir/syslinux/com32

%files extlinux
%defattr(-,root,root)
%_sbindir/extlinux
/boot/extlinux
%config /etc/extlinux.conf

%files tftpboot
%defattr(-,root,root)
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
* Tue May 08 2012 Solar Designer <solar-at-owl.openwall.com> 4.05-owl1
- Updated to 4.05.

* Tue May 08 2012 Solar Designer <solar-at-owl.openwall.com> 4.04-owl3
- Disabled packaging of keytab-lilo because the LILO package provides a program
of the same name on Owl.
- Disabled packaging of md5pass and sha1pass because they depend on
perl(Crypt::PasswdMD5) and perl(Digest::SHA1), which are not part of Owl.

* Sat Oct 29 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 4.04-owl2
- Remove precompiled object files in %prep.

* Thu Oct 27 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 4.04-owl1
- Initial import from Fedora.
- Packaged linux/syslinux instead of mtools/syslinux.

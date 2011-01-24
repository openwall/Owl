# $Owl: Owl/packages/lilo/lilo.spec,v 1.33 2011/01/24 05:36:21 solar Exp $

%define BUILD_EXTERNAL_SUPPORT 0

Summary: The boot loader for Linux and other operating systems.
Name: lilo
Version: 23.1
Release: owl3
License: MIT
Group: System Environment/Base
URL: http://lilo.alioth.debian.org/
Source0: http://lilo.alioth.debian.org/ftp/upstream/sources/%name-%version.tar.gz
Source1: keytab-lilo.c
Patch0: lilo-23.1-owl-Makefile.diff
Patch1: lilo-23.1-alt-owl-fixes.diff
Patch2: lilo-23.1-owl-tmp.diff
Patch3: lilo-23.1-deb-owl-man.diff
Patch4: lilo-23.1-up-bios-int-15-fn-e820.diff
BuildRequires: coreutils, dev86
ExclusiveArch: %ix86 x86_64
BuildRoot: /override/%name-%version

%description
LILO (LInux LOader) is a basic system program which boots your Linux
system.  LILO loads the Linux kernel from a floppy or a hard drive,
boots the kernel and passes control of the system to the kernel.  LILO
can also boot other operating systems.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# filename collision of README and readme/README
mv readme/README{,2}
bzip2 -9k readme/README2

%{expand: %%define optflags %optflags -Wall -Wno-long-long -pedantic}

%build
%__make all \
	CFG_DIR=%_sysconfdir \
	BOOT_DIR=/boot \
	CC=%__cc OPT="%optflags -Wall" \
	CONFIG="-DBDATA -DDSECS=3 -DEVMS -DIGNORECASE -DLVM -DNOKEYBOARD \
		-DONE_SHOT -DPASS160 -DREISERFS -DREWRITE_TABLE -DSOLO_CHAIN \
		-DVERSION -DVIRTUAL -DMDPRAID -DDEVMAPPER -DNO_FS"

%__cc %optflags -Wall -s -o keytab-lilo %_sourcedir/keytab-lilo.c

%install
rm -rf %buildroot
mkdir -p %buildroot/usr/bin
mkdir -p %buildroot%_mandir
%__make install \
	DESTDIR=%buildroot \
	CFG_DIR=%_sysconfdir \
	BOOT_DIR=/boot \
	SBIN_DIR=/sbin \
	USRSBIN_DIR=%_sbindir \
	MAN_DIR=%_mandir

install -m 755 keytab-lilo %buildroot%_bindir/

# Create a sample lilo.conf file
mkdir -p -m755 %buildroot%_sysconfdir
cat << EOF > %buildroot%_sysconfdir/lilo.conf.sample
boot=/dev/sda
root=/dev/sda2
read-only
lba32
prompt
timeout=50
menu-title="Openwall GNU/*/Linux boot menu"
menu-scheme=kw:Wb:kw:kw

image=/boot/vmlinuz
	label=linux
EOF

# Touch the ghost
touch %buildroot%_sysconfdir/lilo.conf

# Remove unpackaged files
%if %BUILD_EXTERNAL_SUPPORT
rm %buildroot/boot/mbr.b
%endif

%post
echo -n 'Checking whether LILO was installed ... '
if [ -f %_sysconfdir/lilo.conf ] && /sbin/lilo -q >/dev/null; then
	echo 'yes'
	echo -n '+ testing whether we can update the bootloader ... '
	if ! /sbin/lilo -t >/dev/null; then
		cat << EOF

WARNING: there are some issues during running 'lilo -t', hence this script
WILL NOT update the current bootloader, do it manually!
EOF
	else
		echo 'seems we can, updating:'
		/sbin/lilo -v
	fi
else
	echo 'NOT installed, skipping'
fi

%files
%defattr(-,root,root)
%doc README
%doc readme/README{2.bz2,.bitmaps,.common.problems,.raid1,.nokeyboard,.volumeID}
%doc CHANGELOG NEWS TODO
%doc sample/*.conf
%doc COPYING readme/INCOMPAT QuickInst
%doc %_sysconfdir/lilo.conf.sample
%attr(600,root,root) %verify(not md5 mtime size) %ghost %_sysconfdir/lilo.conf
%attr(755,root,root) %_bindir/keytab-lilo
%if %BUILD_EXTERNAL_SUPPORT
/boot/boot*
/boot/chain.b
/boot/os2_d.b
%endif
%attr(700,root,root) /sbin/lilo
%attr(700,root,root) /usr/sbin/mkrescue
%exclude /etc/kernel/*
%exclude /etc/initramfs/post-update.d/runlilo
%exclude /etc/lilo.conf_example
%_mandir/*/*

%changelog
* Tue Jan 18 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 23.1-owl1
- Updated to 23.1.
- Enabled -Wall, updated all patches.
- Reverted upstream patch (up-bios-int15-fn-e820).

* Mon Jul 19 2010 Solar Designer <solar-at-owl.openwall.com> 22.8-owl3
- In the sample config file, call the kernel image vmlinuz, not bzImage, for
consistency with our RPM'ed kernels.

* Wed May 27 2009 Solar Designer <solar-at-owl.openwall.com> 22.8-owl2
- Added menu-title and menu-scheme settings to the sample lilo.conf.

* Thu Apr 17 2008 (GalaxyMaster) <galaxy-at-owl.openwall.com> 22.8-owl1
- Updated to 22.8.
- Re-generated the Makefile patch (replaced all 'make' with '$(MAKE)',
disabled installation of keytab-lilo.pl).
- Enhanced the %%post script, enabled verbosity during the boot loader
installation (this should help to troubleshoot automatic upgrades if
there are some issues).
- Enforced attributes in the %%files section.
- Re-generated the alt-owl-fixes patch.
- Dropped the owl-no-fs patch (it was accepted upstream).

* Sat Feb 04 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 22.7.1-owl2
- Compressed CHANGES and README files.

* Fri Oct 21 2005 Solar Designer <solar-at-owl.openwall.com> 22.7.1-owl1
- Updated to 22.7.1.
- Patched second.S to not use the FS register since it appears to be clobbered
by some BIOSes.
- Dropped known-buggy and questionable changes.
- Do package the mkrescue script (we were already packaging its man page),
but have it patched for safe temporary file handling.

* Mon Jun 13 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 22.7-owl1
- Updated to 22.7.
- Added a fix for a typo in the geometry.c file.
- Added the %%BUILD_EXTERNAL_SUPPORT macro to control the creation of
/boot/* files, if this macro is set to 0 (default) then files will be
compiled into the LILO bootloader.
- Regenerated patches against new version.

* Thu Feb 14 2002 Michail Litvak <mci-at-owl.openwall.com> 22.1-owl1
- 22.1
- removed non-actual patches
- added patches from ALT Linux and Debian

* Tue Feb 05 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Mon Jul 23 2001 Solar Designer <solar-at-owl.openwall.com>
- Use RPM_OPT_FLAGS.

* Mon Dec 11 2000 Solar Designer <solar-at-owl.openwall.com>
- Run lilo in %post in case the (physical) location of /boot/boot.b or
whatever else LILO depends on has changed with our upgrade.

* Mon Dec 04 2000 Solar Designer <solar-at-owl.openwall.com>
- No longer require mkinitrd.

* Sun Nov 19 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- 21.6
- import from RH

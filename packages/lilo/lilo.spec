# $Id: Owl/packages/lilo/lilo.spec,v 1.17 2005/07/07 13:27:44 solar Exp $

%define BUILD_EXTERNAL_SUPPORT 0

Summary: The boot loader for Linux and other operating systems.
Name: lilo
Version: 22.7
Release: owl1
License: MIT
Group: System Environment/Base
Source0: ftp://sunsite.unc.edu/pub/Linux/system/boot/lilo/%name-%version.src.tar.gz
Source1: keytab-lilo.c
Patch0: lilo-22.7-owl-Makefile.diff
Patch1: lilo-22.7-mdk-part.diff
Patch2: lilo-22.7-alt-owl-fixes.diff
Patch3: lilo-22.7-alt-owl-getopt.diff
Patch4: lilo-22.7-deb-owl-man.diff
Patch5: lilo-22.7-owl-PAGE_SIZE.diff
BuildRequires: coreutils, dev86
ExclusiveArch: %ix86
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
%patch5 -p1

%{expand: %%define optflags %optflags -Wall -Wno-long-long -pedantic}

%build
# XXX: Do we need the DOS version of LILO and its diagnostic disk? -- (GM)
%__make lilo \
	CC="%__cc" OPT="%optflags -Wall" \
	CFG_DIR="%_sysconfdir" \
	BOOT_DIR="/boot"

%__cc %optflags -Wall -s -o keytab-lilo %_sourcedir/keytab-lilo.c

%install
rm -rf %buildroot
mkdir -p %buildroot/usr/bin
mkdir -p %buildroot%_mandir
%__make install \
	ROOT=%buildroot \
	CFG_DIR="%_sysconfdir" \
	BOOT_DIR="/boot" \
	SBIN_DIR="/sbin" \
	USRSBIN_DIR="%_sbindir" \
	MAN_DIR=%_mandir

install -m 755 keytab-lilo %buildroot%_bindir/

# Remove unpackaged files
%if %BUILD_EXTERNAL_SUPPORT
rm %buildroot/boot/mbr.b
%endif
rm %buildroot/sbin/mkrescue
rm %buildroot%_sbindir/keytab-lilo.pl

%post
test -f /etc/lilo.conf && /sbin/lilo || :

%files
%defattr(-,root,root)
%doc README README.bitmaps README.common.problems README.raid1
%doc CHANGES COPYING INCOMPAT QuickInst
%doc doc
%_bindir/keytab-lilo
%if %BUILD_EXTERNAL_SUPPORT
/boot/boot*
/boot/chain.b
/boot/os2_d.b
%endif
/sbin/lilo
%_mandir/*/*

%changelog
* Mon Jun 13 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 22.7-owl1
- Updated to 22.7.
- Added a fix for a typo in the geometry.c file.
- Added the %%BUILD_EXTERNAL_SUPPORT macro to control the creation of
/boot/* files, if this macro is set to 0 (default) then files will be
compiled into the LILO bootloader.
- Regenerated patches against new version.

* Wed Jan 12 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 22.1-owl2
- Added PAGE_SIZE patch to use getpagesize() from unistd.h.
- Cleaned up the spec.

* Thu Feb 14 2002 Michail Litvak <mci@owl.openwall.com> 22.1-owl1
- 22.1
- removed non-actual patches
- added patches from ALT Linux and Debian

* Tue Feb 05 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Mon Jul 23 2001 Solar Designer <solar@owl.openwall.com>
- Use RPM_OPT_FLAGS.

* Mon Dec 11 2000 Solar Designer <solar@owl.openwall.com>
- Run lilo in %post in case the (physical) location of /boot/boot.b or
whatever else LILO depends on has changed with our upgrade.

* Mon Dec 04 2000 Solar Designer <solar@owl.openwall.com>
- No longer require mkinitrd.

* Sun Nov 19 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- 21.6
- import from RH

# $Id: Owl/packages/util-linux/util-linux.spec,v 1.15 2001/11/12 01:57:59 solar Exp $

%define BUILD_MOUNT 1
%define BUILD_LOSETUP 1
%define BUILD_CRYPTO 1

Summary: A collection of basic system utilities.
Name: util-linux
%define base_version 2.10r
%define crypto_version 2.2.18.3
%if %BUILD_CRYPTO
Version: %{base_version}.%{crypto_version}
%else
Version: %{base_version}
%endif
Release: 4owl
License: distributable
Group: System Environment/Base
Source0: ftp://ftp.kernel.org/pub/linux/utils/util-linux/util-linux-%{base_version}.tar.bz2
Source1: mount.control
Source2: write.control
Patch0: util-linux-2.10r-owl-MCONFIG.diff
Patch1: util-linux-2.10r-owl-Makefiles.diff
Patch2: util-linux-2.10r-owl-write.diff
Patch3: util-linux-2.10r-owl-alpha-hwclock-usage.diff
Patch4: util-linux-2.10r-rh-locale-overflow.diff
Patch10: util-linux-2.10r-%{crypto_version}-int.diff
Patch11: util-linux-2.10r-%{crypto_version}-int-owl-fixes.diff
Requires: owl-control < 2.0
Obsoletes: fdisk tunelp
%ifarch sparc alpha
Obsoletes: clock
%endif
BuildRoot: /override/%{name}-%{version}

%description
The util-linux package contains a wide variety of low-level system
utilities that are necessary for a Linux system to function.

%if %BUILD_MOUNT
%package -n mount
Summary: Programs for mounting and unmounting filesystems.
Group: System Environment/Base

%description -n mount
The mount package contains the mount, umount, swapon and swapoff
programs.  Accessible files on your system are arranged in one big
tree or hierarchy.  These files can be spread out over several
devices.  The mount command attaches a filesystem on some device to
your system's file tree.  The umount command detaches a filesystem
from the tree.  swapon and swapoff, respectively, specify and disable
devices and files for paging and swapping.
%endif

%if %BUILD_LOSETUP
%package -n losetup
Summary: Programs for setting up and configuring loopback devices.
Group: System Environment/Base

%description -n losetup
Linux supports a special block device called the loop device, which maps
a normal file onto a virtual block device.  This allows for the file to
be used as a "virtual file system".  losetup is used to associate loop
devices with regular files or block devices, to detach loop devices and
to query the status of a loop device.
%endif

%prep
%setup -q -n %{name}-%{base_version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%if %BUILD_CRYPTO
%patch10 -p1
%patch11 -p1
%endif

%build
unset LINGUAS || :
./configure
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{bin,sbin}
mkdir -p $RPM_BUILD_ROOT/usr/{bin,info,lib,man/man1,man/man6,man/man8,sbin}

make install DESTDIR=$RPM_BUILD_ROOT

ln -sf hwclock $RPM_BUILD_ROOT/sbin/clock

# We do not want dependencies on csh
chmod 644 $RPM_BUILD_ROOT/usr/share/misc/getopt/*

mkdir -p $RPM_BUILD_ROOT/etc/control.d/facilities
cd $RPM_BUILD_ROOT/etc/control.d/facilities

install -m 700 ${RPM_SOURCE_DIR}/mount.control mount
install -m 700 ${RPM_SOURCE_DIR}/write.control write

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/share/locale/*/LC_MESSAGES/*
/sbin/clock
/sbin/hwclock
/usr/man/man8/hwclock.8*

/usr/sbin/tunelp
/usr/man/man8/tunelp.8*

/sbin/fdisk
%ifarch %ix86 alpha armv4l
/sbin/cfdisk
%endif

%ifarch %ix86 alpha
/sbin/fsck.minix
/sbin/mkfs.minix
%endif

/sbin/mkfs
/sbin/mkswap

/usr/bin/fdformat
/usr/bin/setfdprm
%config /etc/fdprm

/usr/man/man8/fdformat.8*
/usr/man/man8/mkswap.8*
/usr/man/man8/setfdprm.8*

/usr/bin/ddate
/usr/man/man1/ddate.1*

/bin/kill
/usr/bin/cal
/usr/bin/logger
/usr/bin/look
/usr/bin/mcookie
/usr/bin/namei
/usr/bin/script
/usr/bin/setterm
/usr/bin/whereis
%attr(2711,root,tty) /usr/bin/write
/usr/bin/getopt
/usr/man/man1/cal.1*
/usr/man/man1/kill.1*
/usr/man/man1/logger.1*
/usr/man/man1/look.1*
/usr/man/man1/mcookie.1*
/usr/man/man1/namei.1*
/usr/man/man1/script.1*
/usr/man/man1/setterm.1*
/usr/man/man1/whereis.1*
/usr/man/man1/write.1*
/usr/man/man1/getopt.1*

/usr/share/misc/getopt

/bin/dmesg

/sbin/ctrlaltdel
/sbin/kbdrate
/bin/arch
/usr/bin/ipcrm
/usr/bin/ipcs
/usr/bin/renice
/usr/sbin/readprofile
/usr/bin/setsid
%ifarch %ix86 alpha armv4l
/usr/bin/cytune
%endif

/usr/man/man1/arch.1*
/usr/man/man1/readprofile.1*
%ifarch %ix86 alpha armv4l
/usr/man/man8/cytune.8*
%endif
/usr/man/man8/ctrlaltdel.8*
/usr/man/man8/dmesg.8*
/usr/man/man8/ipcrm.8*
/usr/man/man8/ipcs.8*
/usr/man/man8/kbdrate.8*
/usr/man/man8/renice.8*
/usr/man/man8/setsid.8*

%ifarch %ix86
/usr/sbin/rdev
/usr/sbin/ramsize
/usr/sbin/rootflags
/usr/sbin/swapdev
/usr/sbin/vidmode
/usr/man/man8/rdev.8*
/usr/man/man8/ramsize.8*
/usr/man/man8/rootflags.8*
/usr/man/man8/swapdev.8*
/usr/man/man8/vidmode.8*
%endif

/usr/info/ipc.info.gz

/usr/bin/col
/usr/bin/colcrt
/usr/bin/colrm
/usr/bin/column
/usr/bin/hexdump
/usr/bin/rename
/usr/bin/rev
/usr/bin/ul

/usr/man/man1/col.1*
/usr/man/man1/colcrt.1*
/usr/man/man1/colrm.1*
/usr/man/man1/column.1*
/usr/man/man1/hexdump.1*
/usr/man/man1/rename.1*
/usr/man/man1/rev.1*
/usr/man/man1/ul.1*

/bin/more
/usr/man/man1/more.1*
/usr/share/misc/more.help

%ifarch %ix86 alpha
/usr/man/man8/fsck.minix.8*
/usr/man/man8/mkfs.minix.8*
/usr/man/man8/mkfs.8*
%endif

/usr/man/man8/fdisk.8*

%ifarch %ix86 alpha armv4l
/usr/man/man8/cfdisk.8*
%endif

%doc */README.*

%ifarch %ix86 alpha
/sbin/sfdisk
/usr/man/man8/sfdisk.8*
%doc fdisk/sfdisk.examples
%endif

/etc/control.d/facilities/write

%if %BUILD_MOUNT
%files -n mount
%defattr(-,root,root)
%attr(700,root,root) /bin/mount
%attr(700,root,root) /bin/umount
/sbin/swapon
/sbin/swapoff
/usr/man/man5/fstab.5*
/usr/man/man5/nfs.5*
/usr/man/man8/mount.8*
/usr/man/man8/swapoff.8*
/usr/man/man8/swapon.8*
/usr/man/man8/umount.8*
/etc/control.d/facilities/mount
%endif

%if %BUILD_LOSETUP
%files -n losetup
%defattr(-,root,root)
/sbin/losetup
/usr/man/man8/losetup.8*
%endif

%changelog
* Mon Nov 12 2001 Solar Designer <solar@owl.openwall.com>
- newgrp is now built from shadow-utils, for gshadow support.
- Dropped the support for building of chsh, chfn, vipw, vigr, and newgrp
entirely (including owl-control files and a security patch, which may be
restored from the CVS if needed) as it's not going to be updated.

* Wed Apr 18 2001 Solar Designer <solar@owl.openwall.com>
- Added crypto code from the international kernel patch (2.2.18.3), with
minor changes.
- Corrected the Alpha-specific hwclock(8) usage information (the options
are case-sensitive).

* Sun Jan 28 2001 Solar Designer <solar@owl.openwall.com>
- Reviewed the changes made in 2.10r, updated the write patch accordingly.
- More improvements to the write patch (prompt/prefix with usernames).
- optflags are now passed correctly.
- newgrp is no longer installed SUID by default (it's owl-control'able).

* Tue Jan 23 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- 2.10r

* Fri Dec 29 2000 Solar Designer <solar@owl.openwall.com>
- Dirty hack for builds with Linux 2.2.18 headers.

* Wed Dec 13 2000 Solar Designer <solar@owl.openwall.com>
- Use the ix86 macro.

* Sat Aug 26 2000 Solar Designer <solar@owl.openwall.com>
- chsh, chfn, vipw, and vigr are now built from shadow-utils, which
uses libpwdb-compatible locking.

* Wed Aug 16 2000 Solar Designer <solar@owl.openwall.com>
- owl-control support for chsh, chfn, newgrp, write, and mount/umount.

* Wed Aug 02 2000 Solar Designer <solar@owl.openwall.com>
- Disabled locale support in write(1) entirely for security reasons
(dangerous printf formats, control characters, anonymous messages).
- Removed the dependency on kernel as we may not have the kernel in
an RPM package.
- mount and losetup are now packaged here.

* Tue Jul 18 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- locale come back

* Thu Jul 13 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file from RH, and changed it heavily.
- Updated one of the RH patches for 2.10h, removed the rest.
- Removed login as we use one from SimplePAMApps.
- Added two security patches.

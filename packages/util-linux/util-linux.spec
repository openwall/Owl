# $Id: Owl/packages/util-linux/util-linux.spec,v 1.11 2001/01/23 20:41:01 kad Exp $

%define BUILD_MOUNT	'yes'
%define BUILD_LOSETUP	'yes'
%define BUILD_CHSH_CHFN	'no'
%define BUILD_VIPW_VIGR	'no'

Summary: A collection of basic system utilities.
Name: util-linux
Version: 2.10r
Release: 1owl
Copyright: distributable
Group: System Environment/Base
Source0: ftp://ftp.kernel.org/pub/linux/utils/util-linux/util-linux-%{version}.tar.bz2
Source1: chsh-chfn.pam
Source2: chsh-chfn.control
Source3: mount.control
Source4: newgrp.control
Source5: write.control
Patch0: util-linux-2.10h-owl-MCONFIG.diff
Patch1: util-linux-2.10r-owl-Makefiles.diff
Patch2: util-linux-2.10r-owl-restrict-locale.diff
Patch3: util-linux-2.10r-owl-write.diff
Patch4: util-linux-2.10r-rh-locale-overflow.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: owl-control < 2.0
Obsoletes: fdisk tunelp
%ifarch sparc alpha
Obsoletes: clock
%endif

%description
The util-linux package contains a large variety of low-level system
utilities that are necessary for a Linux system to function.

%if "%{BUILD_MOUNT}"=="'yes'"
%package -n mount
Summary: Programs for mounting and unmounting filesystems.
Group: System Environment/Base

%description -n mount
The mount package contains the mount, umount, swapon and swapoff
programs.  Accessible files on your system are arranged in one big
tree or hierarchy.  These files can be spread out over several
devices.  The mount command attaches a filesystem on some device to
your system's file tree.  The umount command detaches a filesystem
from the tree.  Swapon and swapoff, respectively, specify and disable
devices and files for paging and swapping.
%endif

%if "%{BUILD_LOSETUP}"=="'yes'"
%package -n losetup
Summary: Programs for setting up and configuring loopback devices.
Group: System Environment/Base

%description -n losetup
Linux supports a special block device called the loop device, which maps
a normal file onto a virtual block device.  This allows for the file to
be used as a "virtual file system".  Losetup is used to associate loop
devices with regular files or block devices, to detach loop devices and
to query the status of a loop device.
%endif

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
unset LINGUAS || :
./configure
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{bin,sbin,etc/pam.d}
mkdir -p $RPM_BUILD_ROOT/usr/{bin,info,lib,man/man1,man/man6,man/man8,sbin}

make install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf $RPM_BUILD_ROOT/usr/info/ipc.info
gzip -9nf $RPM_BUILD_ROOT/usr/man/man*/*

for i in /usr/bin/chfn /usr/bin/chsh /usr/bin/newgrp ; do
	strip $RPM_BUILD_ROOT/$i
done

strip $RPM_BUILD_ROOT/sbin/fdisk || :

rm -f $RPM_BUILD_ROOT/sbin/clock
ln -s hwclock $RPM_BUILD_ROOT/sbin/clock

# We do not want dependencies on csh
chmod 644 $RPM_BUILD_ROOT/usr/share/misc/getopt/*

%if "%{BUILD_CHSH_CHFN}"=="'yes'"
install -m 600 ${RPM_SOURCE_DIR}/chsh-chfn.pam $RPM_BUILD_ROOT/etc/pam.d/chsh
install -m 600 ${RPM_SOURCE_DIR}/chsh-chfn.pam $RPM_BUILD_ROOT/etc/pam.d/chfn
%endif

mkdir -p $RPM_BUILD_ROOT/etc/control.d/facilities
cd $RPM_BUILD_ROOT/etc/control.d/facilities

install -m 700 ${RPM_SOURCE_DIR}/mount.control mount
install -m 700 ${RPM_SOURCE_DIR}/newgrp.control newgrp
install -m 700 ${RPM_SOURCE_DIR}/write.control write

%if "%{BUILD_CHSH_CHFN}"=="'yes'"
install -m 700 ${RPM_SOURCE_DIR}/chsh-chfn.control chsh
sed 's,/usr/bin/chsh,/usr/bin/chfn,' < chsh > chfn
chmod 700 chfn
%endif

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

%if "%{BUILD_CHSH_CHFN}"=="'yes'"
%config /etc/pam.d/chfn
%config /etc/pam.d/chsh
%endif

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

%attr(4711,root,root)	/usr/bin/newgrp
/usr/man/man1/newgrp.1*

%if "%{BUILD_CHSH_CHFN}"=="'yes'"
%attr(700,root,root)	/usr/bin/chfn
%attr(700,root,root)	/usr/bin/chsh
/usr/man/man1/chfn.1*
/usr/man/man1/chsh.1*
%endif

%if "%{BUILD_VIPW_VIGR}"=="'yes'"
%attr(700,root,root)	/usr/sbin/vipw
%attr(700,root,root)	/usr/sbin/vigr
/usr/man/man8/vipw.8*
/usr/man/man8/vigr.8*
%endif

/bin/kill
/usr/bin/cal
/usr/bin/logger
/usr/bin/look
/usr/bin/mcookie
/usr/bin/namei
/usr/bin/script
/usr/bin/setterm
/usr/bin/whereis
%attr(2711,root,tty)	/usr/bin/write
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

%if "%{BUILD_CHSH_CHFN}"=="'yes'"
/etc/control.d/facilities/chsh
/etc/control.d/facilities/chfn
%endif
/etc/control.d/facilities/newgrp
/etc/control.d/facilities/write

%if "%{BUILD_MOUNT}"=="'yes'"
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

%if "%{BUILD_LOSETUP}"=="'yes'"
%files -n losetup
%defattr(-,root,root)
/sbin/losetup
/usr/man/man8/losetup.8*
%endif

%changelog
* Tue Jan 23 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- 2.10r

* Fri Dec 29 2000 Solar Designer <solar@owl.openwall.com>
- Dirty hack for builds with Linux 2.2.18 headers.

* Wed Dec 13 2000 Solar Designer <solar@owl.openwall.com>
- i386 -> %ix86.

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

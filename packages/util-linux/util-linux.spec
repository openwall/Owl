# $Owl: Owl/packages/util-linux/util-linux.spec,v 1.54 2014/07/12 14:19:34 galaxy Exp $

%define BUILD_MOUNT 1
%define BUILD_LOSETUP 1
%define BUILD_CRYPTO 1

Summary: A collection of basic system utilities.
Name: util-linux
Version: 2.11z
Release: owl18
License: distributable
Group: System Environment/Base
Source0: ftp://ftp.kernel.org/pub/linux/utils/util-linux/util-linux-%version.tar.bz2
Source1: mount.control
Source2: write.control
Source3: nologin.c
Source4: nologin.8
Patch0: util-linux-2.11z-owl-MCONFIG.diff
Patch1: util-linux-2.11z-owl-Makefile.diff
Patch2: util-linux-2.11z-owl-write.diff
Patch3: util-linux-2.11z-owl-mtab-umask.diff
Patch4: util-linux-2.11z-owl-warnings.diff
Patch5: util-linux-2.12q-up-20050910-remount.diff
Patch6: util-linux-2.11z-owl-llseek.diff
Patch7: util-linux-2.11z-owl-blockdev.diff
Patch8: util-linux-2.11z-up-elvtune.diff
Patch9: util-linux-2.11z-owl-cytune.diff
Patch10: util-linux-2.11z-owl-hwclock.diff
Patch11: util-linux-2.11z-up-pivot_root.diff
Patch12: util-linux-2.11z-owl-_syscall5.diff
Patch13: util-linux-2.11z-owl-minix.diff
Patch14: util-linux-2.11z-owl-ext2_llseek.diff
%if %BUILD_CRYPTO
Patch100: util-linux-2.11z-crypto-v3.diff.bz2
%endif
Requires(post,preun): /sbin/install-info
Requires(pre,post): owl-control >= 0.4, owl-control < 2.0
Obsoletes: fdisk, tunelp
%ifarch sparc alpha
Obsoletes: clock
%endif
BuildRequires: pam-devel, ncurses-devel, zlib-devel, gettext, sed
BuildRoot: /override/%name-%version

%description
The util-linux package contains a wide variety of low-level system
utilities that are necessary for a Linux system to function.

%if %BUILD_MOUNT
%package -n mount
Summary: Programs for mounting and unmounting filesystems.
Group: System Environment/Base
Requires(pre,post): owl-control >= 0.4, owl-control < 2.0

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
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%ifarch %ix86 x86_64
%patch13 -p1
%endif
%patch14 -p1
%if %BUILD_CRYPTO
%patch100 -p1
%endif

%build
unset LINGUAS || :
CC="%__cc" \
CFLAGS="%optflags -Wno-strict-aliasing" \
./configure

echo 'LIBCURSES+= -ltinfo' >> make_include
%__make RPM_OPT_FLAGS="%optflags -Wno-strict-aliasing"
%__cc %optflags -static -nostartfiles -Dmain=_start -Dexit=_exit \
	%_sourcedir/nologin.c -o nologin

%install
rm -rf %buildroot

%__make install DESTDIR=%buildroot MAN_DIR=%_mandir INFO_DIR=%_infodir
install -pm755 nologin %buildroot/sbin/
install -pm644 %_sourcedir/nologin.8 %buildroot%_mandir/man8/

ln -sf hwclock %buildroot/sbin/clock

# We do not want dependencies on csh
chmod 644 %buildroot/usr/share/misc/getopt/*

mkdir -p %buildroot/etc/control.d/facilities
cd %buildroot/etc/control.d/facilities

install -m 700 %_sourcedir/mount.control mount
install -m 700 %_sourcedir/write.control write

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot/sbin/agetty
rm %buildroot/sbin/mkfs.bfs
rm %buildroot/sbin/pivot_root
rm %buildroot%_bindir/chfn
rm %buildroot%_bindir/chsh
rm %buildroot%_bindir/newgrp
rm %buildroot%_bindir/raw
rm %buildroot%_sbindir/vipw
rm %buildroot%_sbindir/vigr
rm %buildroot%_mandir/man1/chfn.1*
rm %buildroot%_mandir/man1/chsh.1*
rm %buildroot%_mandir/man1/newgrp.1*
rm %buildroot%_mandir/man8/agetty.8*
rm %buildroot%_mandir/man8/mkfs.bfs.8*
rm %buildroot%_mandir/man8/pivot_root.8*
rm %buildroot%_mandir/man8/raw.8*
rm %buildroot%_mandir/man8/vigr.8*
rm %buildroot%_mandir/man8/vipw.8*

%pre
if [ $1 -ge 2 ]; then
	%_sbindir/control-dump write
fi

%post
if [ $1 -ge 2 ]; then
	%_sbindir/control-restore write
else
	%_sbindir/control write public
fi
/sbin/install-info %_infodir/ipc.info %_infodir/dir \
	--entry="* ipc: (ipc).                                   System V IPC."

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/ipc.info %_infodir/dir \
		--entry="* ipc: (ipc).                                   System V IPC."
fi

%if %BUILD_MOUNT
%pre -n mount
if [ $1 -ge 2 ]; then
	%_sbindir/control-dump mount
fi

%post -n mount
if [ $1 -ge 2 ]; then
	%_sbindir/control-restore mount
fi
%endif

%files
%defattr(-,root,root)
%_datadir/locale/*/LC_MESSAGES/*
/sbin/clock
/sbin/hwclock
%_mandir/man8/hwclock.8*

%_sbindir/tunelp
%_mandir/man8/tunelp.8*

/sbin/fdisk
%ifarch %ix86 x86_64 alpha alphaev5 alphaev56 alphapca56 alphaev6 alphaev67
/sbin/cfdisk
%endif

/sbin/mkfs
/sbin/mkswap
/sbin/fsck.cramfs
/sbin/mkfs.cramfs
/sbin/blockdev
/sbin/elvtune

%_bindir/fdformat
%_bindir/setfdprm
%config /etc/fdprm
%_bindir/isosize

%_mandir/man8/fdformat.8*
%_mandir/man8/mkswap.8*
%_mandir/man8/setfdprm.8*
%_mandir/man8/isosize.8*

/sbin/nologin
%_mandir/man8/nologin.8*

%_bindir/ddate
%_mandir/man1/ddate.1*

/bin/kill
%_bindir/cal
%_bindir/logger
%_bindir/look
%_bindir/mcookie
%_bindir/namei
%_bindir/script
%_bindir/setterm
%_bindir/whereis
%attr(700,root,root) %verify(not mode group) %_bindir/write
%_bindir/getopt
%_mandir/man1/cal.1*
%_mandir/man1/kill.1*
%_mandir/man1/logger.1*
%_mandir/man1/look.1*
%_mandir/man1/mcookie.1*
%_mandir/man1/namei.1*
%_mandir/man1/script.1*
%_mandir/man1/setterm.1*
%_mandir/man1/whereis.1*
%_mandir/man1/write.1*
%_mandir/man1/getopt.1*

%_datadir/misc/getopt

/bin/dmesg

/sbin/ctrlaltdel
/bin/arch
%_bindir/ipcrm
%_bindir/ipcs
%_bindir/renice
%_sbindir/readprofile
%_bindir/setsid
%ifarch %ix86 x86_64 alpha alphaev5 alphaev56 alphapca56 alphaev6 alphaev67 sparc sparcv9
%_bindir/cytune
%endif

%_mandir/man1/arch.1*
%_mandir/man1/readprofile.1*
%ifarch %ix86 x86_64 alpha alphaev5 alphaev56 alphapca56 alphaev6 alphaev67 sparc sparcv9
%_mandir/man8/cytune.8*
%endif
%_mandir/man8/ctrlaltdel.8*
%_mandir/man8/dmesg.8*
%_mandir/man8/ipcrm.8*
%_mandir/man8/ipcs.8*
%_mandir/man8/renice.8*
%_mandir/man8/setsid.8*

%_sbindir/rdev
%_mandir/man8/rdev.8*
%ifarch %ix86
%_sbindir/ramsize
%_sbindir/rootflags
%_sbindir/vidmode
%_mandir/man8/ramsize.8*
%_mandir/man8/rootflags.8*
%_mandir/man8/vidmode.8*
%endif

%_infodir/ipc.info.gz

%_bindir/col
%_bindir/colcrt
%_bindir/colrm
%_bindir/column
%_bindir/hexdump
%_bindir/rename
%_bindir/rev
%_bindir/ul
%_bindir/pg
%_bindir/line

%_mandir/man1/col.1*
%_mandir/man1/colcrt.1*
%_mandir/man1/colrm.1*
%_mandir/man1/column.1*
%_mandir/man1/hexdump.1*
%_mandir/man1/rename.1*
%_mandir/man1/rev.1*
%_mandir/man1/ul.1*
%_mandir/man1/pg.1*
%_mandir/man1/line.1*

/bin/more
%_mandir/man1/more.1*

%_mandir/man8/mkfs.8*
%_mandir/man8/elvtune.8*
%_mandir/man8/blockdev.8*

%_mandir/man8/fdisk.8*

%ifarch %ix86 x86_64 alpha alphaev5 alphaev56 alphapca56 alphaev6 alphaev67
%_mandir/man8/cfdisk.8*
%endif

%doc */README.*

%ifarch %ix86 x86_64 alpha alphaev5 alphaev56 alphapca56 alphaev6 alphaev67
/sbin/sfdisk
%_mandir/man8/sfdisk.8*
%doc fdisk/sfdisk.examples
%endif

# sln comes from glibc-utils
%_mandir/man8/sln.8*

/etc/control.d/facilities/write

%if %BUILD_MOUNT
%files -n mount
%defattr(-,root,root)
%attr(700,root,root) %verify(not mode) /bin/mount
%attr(700,root,root) %verify(not mode) /bin/umount
/sbin/swapon
/sbin/swapoff
%_mandir/man5/fstab.5*
%_mandir/man5/nfs.5*
%_mandir/man8/mount.8*
%_mandir/man8/swapoff.8*
%_mandir/man8/swapon.8*
%_mandir/man8/umount.8*
/etc/control.d/facilities/mount
%endif

%if %BUILD_LOSETUP
%files -n losetup
%defattr(-,root,root)
/sbin/losetup
%_mandir/man8/losetup.8*
%endif

%changelog
* Sun Jun 29 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.11z-owl18
- Replaced the deprecated PreReq tag with the corresponding Requires() tags.
- Regenerated the hwclock patch since it was fuzzy.

* Sun Jul 22 2012 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.11z-owl17
- Added -ltinfo into LDFLAGS to fix build error under binutils >= 2.21.
- Used plain lseek(2) instead of ext2_llseek().

* Sat Feb 18 2012 Solar Designer <solar-at-owl.openwall.com> 2.11z-owl16
- Build and package %_sbindir/rdev also on x86_64 and non-x86 since part of its
functionality is not arch-specific and it is required by hdparm's wiper.sh.

* Tue Sep 13 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.11z-owl15
- Disable fsck.minix and mkfs.minix compilation.  They are not used
nowadays and fail to build with gcc 4.6.1.

* Mon Nov 23 2009 Solar Designer <solar-at-owl.openwall.com> 2.11z-owl14
- In sys-utils/cytune.c, #define __iomem before including <linux/cyclades.h>.
This is needed for building with our current kernel headers on x86_64.

* Fri Nov 20 2009 Solar Designer <solar-at-owl.openwall.com> 2.11z-owl13
- Temporarily #define __KERNEL__ when including <linux/unistd.h> in places
where the definition of _syscall5() is needed for _llseek().

* Sun Sep 20 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.11z-owl12
- Fixed build with linux kernel 2.6.x headers.

* Tue Apr 11 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.11z-owl11
- Corrected specfile to make it build on x86_64.
- Fixed x86_64 support in hwclock.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.11z-owl10
- Corrected info files installation.

* Mon Jan 09 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.11z-owl9
- Added support for build with linux 2.6.x headers.

* Sat Dec 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.11z-owl8
- Packaged nologin.

* Fri Nov 11 2005 Solar Designer <solar-at-owl.openwall.com> 2.11z-owl7
- Corrected the uses of llseek() to avoid miscompilation with recent gcc.
- Do package the sln(8) man page.

* Tue Oct 18 2005 Alexandr D. Kanevskiy <kad-at-owl.openwall.com> 2.11z-owl6
- Also package /sbin/fsck.minix, /sbin/mkfs.minix, and /usr/bin/cytune for
sparc and sparcv9 architectures.

* Tue Sep 13 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.11z-owl5
- Backported upstream fix to umount, to avoid unintentional grant of
privileges by "umount -r".

* Tue Jun 28 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.11z-owl4
- Corrected the source code to not break C strict aliasing rules.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.11z-owl3
- Supplied %%__cc to make.
- Removed verify checks for files under the "control" utility.
- Cleaned up the spec.

* Fri Nov 07 2003 Michail Litvak <mci-at-owl.openwall.com> 2.11z-owl2
- Replaced crypto code from international crypto patch (2.2.18.3) to
unified util-linux crypto patch by Jari Ruusu.

* Mon Apr 14 2003 Michail Litvak <mci-at-owl.openwall.com> 2.11z.2.2.18.3-owl1
- 2.11z
- minor spec file cleanups.

* Sun Nov 03 2002 Solar Designer <solar-at-owl.openwall.com>
- Dump/restore the owl-control settings for mount and write on package
upgrades.
- Keep write at mode 700 ("restricted") in the package, but default
it to "public" in %post when the package is first installed.  This avoids
a race and fail-open behavior.

* Sat Oct 12 2002 Solar Designer <solar-at-owl.openwall.com>
- Use umask 077 when creating mtab files (to be chmod'ed later) to avoid
the race pointed out by Olaf Kirch of SuSE.

* Mon Feb 04 2002 Solar Designer <solar-at-owl.openwall.com>
- Install the info dir entry for ipc.
- Enforce our new spec file conventions.

* Mon Nov 12 2001 Solar Designer <solar-at-owl.openwall.com>
- newgrp is now built from shadow-utils, for gshadow support.
- Dropped the support for building of chsh, chfn, vipw, vigr, and newgrp
entirely (including owl-control files and a security patch, which may be
restored from the CVS if needed) as it's not going to be updated.

* Wed Apr 18 2001 Solar Designer <solar-at-owl.openwall.com>
- Added crypto code from the international kernel patch (2.2.18.3), with
minor changes.
- Corrected the Alpha-specific hwclock(8) usage information (the options
are case-sensitive).

* Sun Jan 28 2001 Solar Designer <solar-at-owl.openwall.com>
- Reviewed the changes made in 2.10r, updated the write patch accordingly.
- More improvements to the write patch (prompt/prefix with usernames).
- optflags are now passed correctly.
- newgrp is no longer installed SUID by default (it's owl-control'able).

* Tue Jan 23 2001 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- 2.10r

* Fri Dec 29 2000 Solar Designer <solar-at-owl.openwall.com>
- Dirty hack for builds with Linux 2.2.18 headers.

* Wed Dec 13 2000 Solar Designer <solar-at-owl.openwall.com>
- Use the ix86 macro.

* Sat Aug 26 2000 Solar Designer <solar-at-owl.openwall.com>
- chsh, chfn, vipw, and vigr are now built from shadow-utils, which
uses libpwdb-compatible locking.

* Wed Aug 16 2000 Solar Designer <solar-at-owl.openwall.com>
- owl-control support for chsh, chfn, newgrp, write, and mount/umount.

* Wed Aug 02 2000 Solar Designer <solar-at-owl.openwall.com>
- Disabled locale support in write(1) entirely for security reasons
(dangerous printf formats, control characters, anonymous messages).
- Removed the dependency on kernel as we may not have the kernel in
an RPM package.
- mount and losetup are now packaged here.

* Tue Jul 18 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- locale come back

* Thu Jul 13 2000 Solar Designer <solar-at-owl.openwall.com>
- Imported this spec file from RH, and changed it heavily.
- Updated one of the RH patches for 2.10h, removed the rest.
- Removed login as we use one from SimplePAMApps.
- Added two security patches.

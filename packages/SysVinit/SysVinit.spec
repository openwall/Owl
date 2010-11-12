# $Owl: Owl/packages/SysVinit/SysVinit.spec,v 1.29 2010/11/12 16:52:16 segoon Exp $

Summary: Programs which control basic system processes.
Name: SysVinit
Version: 2.88dsf
Release: owl1
License: GPL
Group: System Environment/Base
Source: http://download.savannah.gnu.org/releases/sysvinit/sysvinit-%version.tar.bz2
# Signature: http://download.savannah.gnu.org/releases/sysvinit/sysvinit-%version.tar.bz2.sig
Patch0: sysvinit-2.88-alt-progname.diff
Patch1: sysvinit-2.88-alt-umask.diff
Patch2: sysvinit-2.88-alt-owl-start-stop-daemon.diff
Patch3: sysvinit-2.86-owl-mount_proc-single-mount.diff
Patch4: sysvinit-2.85-owl-multiline-string-fix.diff
Patch5: sysvinit-2.88-rh-alt-owl-pidof.diff
Patch6: sysvinit-2.86-owl-initcmd_setenv.diff
Patch7: sysvinit-2.86-deb-killall-sched.diff
Patch8: sysvinit-2.88-alt-signedness.diff
Patch9: sysvinit-2.88-alt-wur.diff
Patch10: sysvinit-2.88-deb-init-selinux.diff
Patch11: sysvinit-2.88-suse-SETSIG.diff
Requires: /sbin/sulogin
BuildRoot: /override/%name-%version

%description
The SysVinit package contains a group of programs that control the
very basic functions of your system.  SysVinit includes the init
program, the first program started by the Linux kernel when the
system boots.  init then controls the startup, running and shutdown
of all other programs.

%prep
%setup -q -n sysvinit-%version
rm man/sulogin.8
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

%{expand:%%define optflags %optflags -Wall -D_GNU_SOURCE}

%build
%__make -C src CC="%__cc" CFLAGS="%optflags" LDFLAGS="-static" init
%__make -C src CC="%__cc" CFLAGS="%optflags" LDFLAGS= DISTRO=Owl
%__make -C src CC="%__cc" CFLAGS="%optflags" LDFLAGS= bootlogd
cd contrib
%__cc start-stop-daemon.c -o start-stop-daemon -s %optflags

%install
rm -rf %buildroot
mkdir -p %buildroot/{dev,bin,sbin,%_bindir,%_mandir/man{1,5,8}}
mkdir -p %buildroot%_includedir

%__make -C src install \
	DISTRO=Owl \
	ROOT=%buildroot \
	MANDIR=%_mandir \
	BIN_OWNER=`id -nu` \
	BIN_GROUP=`id -ng`

install -m 700 src/bootlogd %buildroot/sbin/
install -m 700 contrib/start-stop-daemon %buildroot/sbin/

mkfifo -m 600 %buildroot/dev/initctl

# We would like to package pidof in /sbin
rm %buildroot/bin/pidof
rmdir %buildroot/bin
ln -sf killall5 %buildroot/sbin/pidof

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot%_includedir/initreq.h

%pre
# This is tricky.  We don't want to let RPM remove the only link to the
# old init as that would actually leave it pending for delete on process
# termination.  That delete is a filesystem write operation meaning that
# the root filesystem would need to stay mounted read/write.  But we
# absolutely want to be able to remount it read-only during shutdown,
# possibly with the old init still alive!
if [ -e /sbin/init -a ! -e /sbin/.init-working ]; then
	ln /sbin/init /sbin/.init-working
fi

%post
# If /proc is mounted and /sbin/.init-working is running, tell init to
# invoke the replaced version of itself.
if /sbin/pidof /sbin/.init-working &> /dev/null; then
	/sbin/telinit u
	sleep 1
# If /sbin/.init-working is no longer running, remove it.
	if ! /sbin/pidof /sbin/.init-working &> /dev/null; then
		rm -f /sbin/.init-working
	fi
fi

%files
%defattr(-,root,root)
# XXX: v2.88dsf includes misnamed .lsm - segoon
#%doc doc/sysvinit-%version.lsm
%doc doc/sysvinit-2.86.lsm
%doc contrib/start-stop-daemon.README doc/bootlogd.README COPYING
%defattr(0700,root,root)
/sbin/halt
/sbin/init
/sbin/poweroff
/sbin/reboot
/sbin/shutdown
/sbin/telinit
/sbin/fstab-decode
/sbin/bootlogd
%defattr(0755,root,root)
/sbin/killall5
/sbin/pidof
/sbin/runlevel
/sbin/start-stop-daemon
%_bindir/last
%_bindir/lastb
%_bindir/mesg
%attr(0700,root,tty) %_bindir/wall
%attr(0644,root,root) %_mandir/man*/*
%attr(0600,root,root) /dev/initctl

%changelog
* Fri Nov 12 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.88dsf-owl1
- Updated to 2.88dsf.
- Updated all the patches.
- Dropped owl-save-env patch (fixed in upstream).
- Imported deb-killall-sched, alt-signedness, alt-wur, deb-init-selinux,
suse-SETSIG patches.

* Sun Nov 19 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.86-owl2
- Merged ALT's patch for start-stop-daemon to recognize deleted
executables when kernel adds "(deleted) " name prefix in addition to
already recognized case when kernel adds " (deleted)" name suffix.

* Mon Oct 24 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.86-owl1
- Updated to 2.86, dropped patches which were included upstream.
- Adjusted make command according to Makefile of the new version.
- Fixed handling of extra environment variables to deny altering of
INIT_VERSION.
- Fixed the re-exec part to save environment on init reload.
- Fixed compilation warnings.

* Fri Jan 07 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.85-owl5
- Cleaned up the spec.
- Removed "-s" from LDFLAGS since we are using brp- scripts.
- Using %%__cc macros to specify C compiler.
- Fixed multiline string in start-stop-daemon.c to satisfy GCC 3.4.3.

* Sun Apr 27 2003 Solar Designer <solar-at-owl.openwall.com> 2.85-owl4
- Wrote a new implementation of sulogin which is now packaged separately,
so don't package sulogin here.
- Don't mount /proc in pidof, and mount it as "proc" rather than "none"
in killall5 such that umount and others can reasonably refer to it in
error messages.
- Have start-stop-daemon and pidof recognize deleted executables that
were previously renamed to *-RPMDELETE (this is how RPM 3.0.x replaces
files).
- Actually start the new init on package upgrades, with "telinit u".

* Thu Apr 24 2003 Solar Designer <solar-at-owl.openwall.com> 2.85-owl3
- Fixed a bug in yesterday's update to start-stop-daemon's executable file
matching, thanks to Dmitry V. Levin.
- On package upgrades, make a hard link to (the old) /sbin/init instead of
renaming it.

* Wed Apr 23 2003 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.85 (which includes most of our old patches plus quite a few
from ALT Linux).
- Added more patches from ALT and Red Hat Linux, including for executable
file path matching in start-stop-daemon and pidof(8), with minor changes.

* Wed Feb 13 2002 Solar Designer <solar-at-owl.openwall.com>
- Don't unlink the old /sbin/init on package upgrades as that would actually
leave it pending for delete on process termination and prevent remounting
the filesystem read-only during shutdown.
- Link init statically to avoid the same problem with glibc upgrades where
the old libc would remain pending for delete until the very end preventing
the remount.

* Tue Feb 05 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Wed May 30 2001 Solar Designer <solar-at-owl.openwall.com>
- Ensure the umask is no less restrictive than 022 when starting programs
from init and start-stop-daemon.

* Sun Dec 10 2000 Solar Designer <solar-at-owl.openwall.com>
- Use getpass(3) in sulogin; the old code was unreliable.
- Updated the sulogin man page (no fallback).

* Fri Dec 01 2000 Solar Designer <solar-at-owl.openwall.com>
- Relaxed permissions on start-stop-daemon to 755 for status checks.
- Removed the packaging of utmpdump as it is unsafe on untrusted files.

* Wed Aug 09 2000 Solar Designer <solar-at-owl.openwall.com>
- Added building of bootlogd and start-stop-daemon.

* Tue Aug 08 2000 Solar Designer <solar-at-owl.openwall.com>
- Imported this spec file from RH, changed it in various ways.
- Removed the RH patches.
- Added the initial set of Owl patches.

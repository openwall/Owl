# $Id: Owl/packages/SysVinit/SysVinit.spec,v 1.17 2003/04/27 03:07:08 solar Exp $

Summary: Programs which control basic system processes.
Name: SysVinit
Version: 2.85
Release: owl4
License: GPL
Group: System Environment/Base
Source: ftp://ftp.cistron.nl/pub/people/miquels/sysvinit/sysvinit-%{version}.tar.gz
Patch0: sysvinit-2.85-owl-Makefile.diff
Patch1: sysvinit-2.85-owl-wall-longjmp-clobbering.diff
Patch2: sysvinit-2.85-owl-format.diff
Patch3: sysvinit-2.85-alt-progname-umask.diff
Patch4: sysvinit-2.85-alt-owl-start-stop-daemon.diff
Patch5: sysvinit-2.85-alt-owl-bootlogd.diff
Patch6: sysvinit-2.85-owl-mount-path.diff
Patch7: sysvinit-2.85-owl-typos.diff
Patch8: sysvinit-2.85-rh-alt-pidof.diff
Patch9: sysvinit-2.85-rh-alt-owl-shutdown-log.diff
Requires: /sbin/sulogin
BuildRoot: /override/%{name}-%{version}

%description
The SysVinit package contains a group of programs that control the
very basic functions of your system.  SysVinit includes the init
program, the first program started by the Linux kernel when the
system boots.  init then controls the startup, running and shutdown
of all other programs.

%prep
%setup -q -n sysvinit-%{version}
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

%{expand:%%define optflags %optflags -Wall -D_GNU_SOURCE}

%build
make -C src CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s -static" init
make -C src CFLAGS="$RPM_OPT_FLAGS" DISTRO=Owl
make -C src CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s -lutil" bootlogd
cd contrib
gcc start-stop-daemon.c -o start-stop-daemon -s $RPM_OPT_FLAGS

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{dev,sbin,usr/bin,%{_mandir}/man{1,5,8}}
mkdir -p $RPM_BUILD_ROOT/usr/include

make -C src install \
	DISTRO=Owl \
	ROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir} \
	BIN_OWNER=`id -nu` \
	BIN_GROUP=`id -ng`

install -m 700 src/bootlogd $RPM_BUILD_ROOT/sbin/
install -m 700 contrib/start-stop-daemon $RPM_BUILD_ROOT/sbin/

mkfifo -m 600 $RPM_BUILD_ROOT/dev/initctl
ln -sf killall5 $RPM_BUILD_ROOT/sbin/pidof

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# This is tricky.  We don't want to let RPM remove the only link to the
# old init as that would actually leave it pending for delete on process
# termination.  That delete is a filesystem write operation meaning that
# the root filesystem would need to stay mounted read/write.  But we
# absolutely want to be able to remount it read-only during shutdown,
# with the init still alive!
if [ -e /sbin/init -a ! -e /sbin/.init-working ]; then
	ln /sbin/init /sbin/.init-working
fi

%files
%defattr(-,root,root)
%doc doc/sysvinit-%{version}.lsm
%doc contrib/start-stop-daemon.README doc/bootlogd.README
%defattr(0700,root,root)
/sbin/halt
/sbin/init
/sbin/poweroff
/sbin/reboot
/sbin/shutdown
/sbin/telinit
/sbin/bootlogd
%defattr(0755,root,root)
/sbin/killall5
/sbin/pidof
/sbin/runlevel
/sbin/start-stop-daemon
/usr/bin/last
/usr/bin/lastb
/usr/bin/mesg
%attr(0700,root,tty) /usr/bin/wall
%attr(0644,root,root) %{_mandir}/man*/*
%attr(0600,root,root) /dev/initctl

%changelog
* Sun Apr 27 2003 Solar Designer <solar@owl.openwall.com> 2.85-owl4
- Wrote a new implementation of sulogin which is now packaged separately,
so don't package sulogin here.

* Thu Apr 24 2003 Solar Designer <solar@owl.openwall.com> 2.85-owl3
- Fixed a bug in yesterday's update to start-stop-daemon's executable file
matching, thanks to Dmitry V. Levin.
- On package upgrades, make a hard link to (the old) /sbin/init instead of
renaming it.

* Wed Apr 23 2003 Solar Designer <solar@owl.openwall.com>
- Updated to 2.85 (which includes most of our old patches plus quite a few
from ALT Linux).
- Added more patches from ALT and Red Hat Linux, including for executable
file path matching in start-stop-daemon and pidof(8), with minor changes.

* Wed Feb 13 2002 Solar Designer <solar@owl.openwall.com>
- Don't unlink the old /sbin/init on package upgrades as that would actually
leave it pending for delete on process termination and prevent remounting
the filesystem read-only during shutdown.
- Link init statically to avoid the same problem with glibc upgrades where
the old libc would remain pending for delete until the very end preventing
the remount.

* Tue Feb 05 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Wed May 30 2001 Solar Designer <solar@owl.openwall.com>
- Ensure the umask is no less restrictive than 022 when starting programs
from init and start-stop-daemon.

* Sun Dec 10 2000 Solar Designer <solar@owl.openwall.com>
- Use getpass(3) in sulogin; the old code was unreliable.
- Updated the sulogin man page (no fallback).

* Fri Dec 01 2000 Solar Designer <solar@owl.openwall.com>
- Relaxed permissions on start-stop-daemon to 755 for status checks.
- Removed the packaging of utmpdump as it is unsafe on untrusted files.

* Wed Aug 09 2000 Solar Designer <solar@owl.openwall.com>
- Added building of bootlogd and start-stop-daemon.

* Tue Aug 08 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file from RH, changed it in various ways.
- Removed the RH patches.
- Added the initial set of Owl patches.

# $Id: Owl/packages/SysVinit/SysVinit.spec,v 1.11 2002/02/13 00:14:45 solar Exp $

Summary: Programs which control basic system processes.
Name: SysVinit
Version: 2.78
Release: owl12
License: GPL
Group: System Environment/Base
Source: ftp://ftp.cistron.nl/pub/people/miquels/sysvinit/sysvinit-%{version}.tar.gz
Patch0: sysvinit-2.78-owl-bound-format.diff
Patch1: sysvinit-2.78-owl-sulogin.diff
Patch2: sysvinit-2.78-owl-umask.diff
BuildRoot: /override/%{name}-%{version}

%description
The SysVinit package contains a group of processes that control
the very basic functions of your system.  SysVinit includes the init
program, the first program started by the Linux kernel when the
system boots.  init then controls the startup, running and shutdown
of all other programs.

%prep
%setup -q -n sysvinit-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{expand:%%define optflags %optflags -Wall}

%build
make -C src CC=gcc CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s -static" init
make -C src CC=gcc CFLAGS="$RPM_OPT_FLAGS"
make -C src CC=gcc CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s -lutil" bootlogd
cd contrib
gcc start-stop-daemon.c -o start-stop-daemon -s $RPM_OPT_FLAGS

%install
rm -rf $RPM_BUILD_ROOT
for I in sbin usr/bin usr/share/man/man{1,3,5,8} etc var/run dev; do
	mkdir -p $RPM_BUILD_ROOT/$I
done
make -C src ROOT=$RPM_BUILD_ROOT BIN_OWNER=`id -nu` BIN_GROUP=`id -ng` install

install -m 700 src/bootlogd $RPM_BUILD_ROOT/sbin
install -m 700 contrib/start-stop-daemon $RPM_BUILD_ROOT/sbin

mkfifo -m 600 $RPM_BUILD_ROOT/dev/initctl
ln -sf killall5 $RPM_BUILD_ROOT/sbin/pidof

chmod 755 $RPM_BUILD_ROOT/usr/bin/utmpdump

mv $RPM_BUILD_ROOT/usr/share/man $RPM_BUILD_ROOT/usr/man

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# This is tricky.  We don't want to let RPM unlink the old init as that
# would actually leave it pending for delete on process termination.
# That delete is a filesystem write operation meaning that the root
# filesystem would need to stay mounted read/write.  But we absolutely
# want to be able to remount it read-only during shutdown, with the
# init still alive!
if [ -e /sbin/init -a ! -e /sbin/.init-working ]; then
	mv /sbin/init /sbin/.init-working
fi

%files
%defattr(-,root,root)
%doc doc/Propaganda doc/Install
%doc doc/sysvinit-%{version}.lsm contrib/start-stop-daemon.README
%doc doc/bootlogd.README
%defattr(0700,root,root)
/sbin/halt
/sbin/init
/sbin/poweroff
/sbin/reboot
/sbin/shutdown
/sbin/sulogin
/sbin/telinit
/sbin/bootlogd
%defattr(0755,root,root)
/sbin/start-stop-daemon
/sbin/killall5
/sbin/pidof
/sbin/runlevel
/usr/bin/last
/usr/bin/lastb
/usr/bin/mesg
%attr(0700,root,tty) /usr/bin/wall
%attr(0644,root,root) /usr/man/*/*
%attr(0600,root,root) /dev/initctl

%changelog
* Wed Feb 13 2002 Solar Designer <solar@owl.openwall.com>
- Don't unlink the old init(8) on package upgrades as that would actually
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

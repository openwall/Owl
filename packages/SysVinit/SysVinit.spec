# $Id: Owl/packages/SysVinit/SysVinit.spec,v 1.1 2000/08/08 04:37:29 solar Exp $

Summary: Programs which control basic system processes.
Name: SysVinit
Version: 2.78
Release: 6owl
Copyright: GPL
Group: System Environment/Base
Source: ftp://ftp.cistron.nl/pub/people/miquels/sysvinit/sysvinit-%{version}.tar.gz
Patch0: sysvinit-2.78-owl-bound-format.diff
Patch1: sysvinit-2.78-owl-sulogin.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}

%description
The SysVinit package contains a group of processes that control 
the very basic functions of your system.  SysVinit includes the init 
program, the first program started by the Linux kernel when the 
system boots.  Init then controls the startup, running and shutdown
of all other programs.

%prep
%setup -q -n sysvinit-%{version}
%patch0 -p1
%patch1 -p1

%build
make -C src CC=gcc CFLAGS="-Wall $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
for I in sbin usr/bin usr/share/man/man{1,3,5,8} etc var/run dev; do
	mkdir -p $RPM_BUILD_ROOT/$I
done
make -C src ROOT=$RPM_BUILD_ROOT BIN_OWNER=`id -nu` BIN_GROUP=`id -ng` install

# If this already exists, just do nothing (the ||: part)
mknod --mode=0600 $RPM_BUILD_ROOT/dev/initctl p ||:
ln -snf killall5 $RPM_BUILD_ROOT/sbin/pidof

chmod 755 $RPM_BUILD_ROOT/usr/bin/utmpdump

mv $RPM_BUILD_ROOT/usr/share/man $RPM_BUILD_ROOT/usr/man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/Propaganda doc/changelog doc/Install
%doc doc/sysvinit-%{version}.lsm contrib/start-stop-daemon.* 
%defattr(0700,root,root)
/sbin/halt
/sbin/init
/sbin/killall5
/sbin/poweroff
/sbin/reboot
/sbin/shutdown
/sbin/sulogin
/sbin/telinit
%defattr(0755,root,root)
/sbin/pidof
/sbin/runlevel
/usr/bin/last
/usr/bin/lastb
/usr/bin/mesg
/usr/bin/utmpdump
%attr(0700,root,tty) /usr/bin/wall
%attr(0644,root,root) /usr/man/*/*
%attr(0600,root,root) /dev/initctl

%changelog
* Tue Aug 08 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file from RH, changed it in various ways.
- Removed the RH patches.
- Added the initial set of Owl patches.

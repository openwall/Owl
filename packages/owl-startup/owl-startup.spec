# $Id: Owl/packages/owl-startup/owl-startup.spec,v 1.21 2001/11/22 04:42:48 solar Exp $

Summary: Startup scripts.
Name: owl-startup
Version: 0.10
Release: 1owl
License: GPL
Group: System Environment/Base
Source0: initscripts-5.00.tar.gz
Source1: inittab
Source2: rc.sysinit
Source3: rc
Source4: functions
Source5: halt
Source6: single
Source7: clock
PreReq: /sbin/chkconfig
Requires: SysVinit, /sbin/start-stop-daemon
Requires: bash >= 2.0, sh-utils
Requires: mingetty, e2fsprogs >= 1.15, util-linux, net-tools
Requires: gawk, sed, mktemp
Provides: initscripts
Obsoletes: initscripts
BuildRoot: /override/%{name}-%{version}

%description
The scripts used to boot your system, change runlevels, and shut the
system down cleanly.

%prep
%setup -q -n initscripts-5.00

%build
make -C src CFLAGS="$RPM_OPT_FLAGS" usleep ipcalc

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/{rc.d/{rc{0,1,2,3,4,5,6}.d,init.d},profile.d}
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig/network-scripts
mkdir -p $RPM_BUILD_ROOT/{bin,sbin,usr/man/man1,var/{log,run}}

install -m 755 src/{usleep,ipcalc} $RPM_BUILD_ROOT/bin/
install -m 644 src/{usleep.1,ipcalc.1} $RPM_BUILD_ROOT/usr/man/man1/

install -m 755 lang.*sh $RPM_BUILD_ROOT/etc/profile.d/
install -m 700 rc.d/init.d/{random,network,netfs} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/
install -m 700 sysconfig/network-scripts/* \
	$RPM_BUILD_ROOT/etc/sysconfig/network-scripts/
mv $RPM_BUILD_ROOT/etc/sysconfig/network-scripts/if{up,down} \
	$RPM_BUILD_ROOT/sbin/
ln -s /sbin/if{up,down} $RPM_BUILD_ROOT/etc/sysconfig/network-scripts/

mkdir redhat
mv sysconfig.txt sysvinitfiles redhat

cd $RPM_BUILD_ROOT

install -m 600 $RPM_SOURCE_DIR/inittab etc/
install -m 700 $RPM_SOURCE_DIR/rc.sysinit etc/rc.d/
install -m 700 $RPM_SOURCE_DIR/rc etc/rc.d/
install -m 644 $RPM_SOURCE_DIR/functions etc/rc.d/init.d/
install -m 700 $RPM_SOURCE_DIR/{halt,single,clock} etc/rc.d/init.d/
install -m 700 /dev/null etc/rc.d/rc.local

ln -s ../init.d/halt etc/rc.d/rc0.d/S01halt
ln -s ../init.d/halt etc/rc.d/rc6.d/S01reboot

ln -s ../init.d/single etc/rc.d/rc1.d/S99single

ln -s ../rc.local etc/rc.d/rc2.d/S99local
ln -s ../rc.local etc/rc.d/rc3.d/S99local
ln -s ../rc.local etc/rc.d/rc5.d/S99local

touch var/log/wtmp var/run/utmp

mkdir -p var/run/netreport

%post
for f in /var/log/wtmp /var/run/utmp; do
	test -e $f && continue || :
	touch $f
	chown root.utmp $f && chmod 664 $f
done

if [ ! -e /var/log/lastlog ]; then
	touch /var/log/lastlog
	chown root.root /var/log/lastlog && chmod 644 /var/log/lastlog
fi

/sbin/chkconfig --add random
/sbin/chkconfig --add network
/sbin/chkconfig --add netfs

%preun
if [ $1 -eq 0 ]; then
	/sbin/chkconfig --del random
	/sbin/chkconfig --del network
	/sbin/chkconfig --del netfs
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config /etc/inittab
%config /etc/rc.d/rc.sysinit
%config /etc/rc.d/rc
/etc/rc.d/init.d/functions
%config /etc/rc.d/init.d/halt
%config /etc/rc.d/init.d/single
%config /etc/rc.d/init.d/clock
%dir /etc/rc.d
%dir /etc/rc.d/rc*.d
%dir /etc/rc.d/init.d
%config(missingok) /etc/rc.d/rc*.d/*
%config(missingok) /etc/rc.d/init.d/random
%config(missingok) /etc/rc.d/init.d/network
%config(missingok) /etc/rc.d/init.d/netfs
%config(noreplace) /etc/rc.d/rc.local
%config /etc/profile.d/lang.*
%dir /etc/sysconfig/network-scripts
%config /etc/sysconfig/network-scripts/ifcfg-lo
%config /etc/sysconfig/network-scripts/ifdown
%config /etc/sysconfig/network-scripts/ifdown-post
%config /etc/sysconfig/network-scripts/ifup
%config /etc/sysconfig/network-scripts/ifup-aliases
%config /etc/sysconfig/network-scripts/ifup-post
%config /etc/sysconfig/network-scripts/ifup-routes
%config /etc/sysconfig/network-scripts/network-functions
%config /sbin/ifdown
%config /sbin/ifup
%dir /var/run/netreport
/bin/usleep
/bin/ipcalc
/usr/man/man1/usleep.1*
/usr/man/man1/ipcalc.1*
%ghost %attr(0664,root,utmp) /var/log/wtmp
%ghost %attr(0664,root,utmp) /var/run/utmp
%doc redhat

%changelog
* Thu Nov 22 2001 Solar Designer <solar@owl.openwall.com>
- /etc/init.d/halt will now call halt(8) as poweroff (which will fall back
to plain halt if the kernel doesn't have power management support compiled
in); thanks to Piotr Synowiec for reporting the problem and to Miquel van
Smoorenburg for explaining how this approach is in fact in accordance with
the documentation.
- Support /fastboot and /forcefsck which shutdown(8) may create.

* Mon Nov 05 2001 Solar Designer <solar@owl.openwall.com>
- /etc/init.d -> /etc/rc.d/init.d for consistency.

* Fri Jul 27 2001 Solar Designer <solar@owl.openwall.com>
- Setup a RAM disk if we're booting from an Owl CD-ROM; this is done by
running rc.ramdisk which is to be provided by the owl-cdrom package.

* Wed May 30 2001 Solar Designer <solar@owl.openwall.com>
- Set umask to 077 in daemon() for the case when a service is started
manually rather than from rc.sysinit.

* Tue May 08 2001 Michail Litvak <mci@owl.openwall.com>
- added ignoring *.swp, *~, *,

* Wed Apr 11 2001 Michail Litvak <mci@owl.openwall.com>
- removed echo about accounting stopping.

* Wed Mar 28 2001 Solar Designer <solar@owl.openwall.com>
- Disable coredumps with the soft rlimit only.

* Wed Dec 20 2000 Solar Designer <solar@owl.openwall.com>
- Provide wtmp and utmp as ghosts just so that they don't get removed
when upgrading from Red Hat's "initscripts" package.

* Thu Dec 07 2000 Solar Designer <solar@owl.openwall.com>
- Added --pidfile and --expect-user to daemon(), killproc(), and status().
- Added single and symlinked it as rc1.d/S99single.

* Mon Dec 04 2000 Solar Designer <solar@owl.openwall.com>
- Obsoletes: initscripts
- Don't require console-tools for now.
- Create wtmp, utmp and lastlog in %post.
- Enable swapping into files.
- Save dmesg on boot.

* Sun Dec 03 2000 Solar Designer <solar@owl.openwall.com>
- No longer require glib for builds.

* Fri Dec 01 2000 Solar Designer <solar@owl.openwall.com>
- Correctly report non-default signals in killproc().
- %preun: only when last instance is uninstalled.

* Wed Nov 29 2000 Solar Designer <solar@owl.openwall.com>
- Initial version, still uses a lot from RH initscripts.

# $Id: Owl/packages/owl-startup/owl-startup.spec,v 1.2 2000/12/01 18:19:55 solar Exp $

Summary: Startup scripts.
Name: owl-startup
Version: 0.2
Release: 1owl
Copyright: GPL
Group: System Environment/Base
Source0: initscripts-5.00.tar.gz
Source1: inittab
Source2: rc.sysinit
Source3: rc
Source4: functions
Source5: halt
Source6: clock
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Provides: initscripts-5.00
Requires: SysVinit, /sbin/start-stop-daemon
Requires: bash >= 2.0, sh-utils
Requires: mingetty, e2fsprogs >= 1.15, util-linux, net-tools
Requires: gawk, sed, mktemp, console-tools
Prereq: /sbin/chkconfig

%description
The scripts used to boot your system, change runlevels, and shut the
system down cleanly.

%prep
%setup -q -n initscripts-5.00

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/{rc.d/rc{0,1,2,3,4,5,6}.d,init.d}
make ROOT=$RPM_BUILD_ROOT install || :

mkdir redhat
mv sysconfig.txt sysvinitfiles redhat

cd $RPM_BUILD_ROOT

install -m 600 $RPM_SOURCE_DIR/inittab etc/
install -m 700 $RPM_SOURCE_DIR/rc.sysinit etc/rc.d/
install -m 700 $RPM_SOURCE_DIR/rc etc/rc.d/
install -m 644 $RPM_SOURCE_DIR/functions etc/init.d/
install -m 700 $RPM_SOURCE_DIR/halt etc/init.d/
install -m 700 $RPM_SOURCE_DIR/clock etc/init.d/
install -m 700 /dev/null etc/rc.d/rc.local

ln -s ../init.d/halt etc/rc.d/rc0.d/S01halt
ln -s ../init.d/halt etc/rc.d/rc6.d/S01reboot

ln -s ../rc.local etc/rc.d/rc2.d/S99local
ln -s ../rc.local etc/rc.d/rc3.d/S99local
ln -s ../rc.local etc/rc.d/rc5.d/S99local

mkdir -p var/run/netreport

%post
/sbin/chkconfig --add random
/sbin/chkconfig --add network
/sbin/chkconfig --add netfs

%preun
/sbin/chkconfig --del random
/sbin/chkconfig --del network
/sbin/chkconfig --del netfs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config /etc/inittab
%config /etc/rc.d/rc.sysinit
%config /etc/rc.d/rc
/etc/init.d/functions
%config /etc/init.d/halt
%config /etc/init.d/clock
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
%doc redhat

%changelog
* Fri Dec 01 2000 Solar Designer <solar@owl.openwall.com>
- Correctly report non-default signals in killproc().

* Wed Nov 29 2000 Solar Designer <solar@owl.openwall.com>
- Initial version, still uses a lot from RH initscripts.

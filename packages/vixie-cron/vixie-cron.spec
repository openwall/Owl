# $Id: Owl/packages/vixie-cron/vixie-cron.spec,v 1.2 2000/08/20 02:59:33 solar Exp $

Summary: Daemon to execute scheduled commands (Vixie Cron)
Name: vixie-cron
Version: 3.0.2.7
Release: 2owl
Copyright: distributable
Group: System Environment/Base
Source0: vixie-cron-%{version}.tar.gz
Source1: vixie-cron.init
Source2: crontab.control
Patch0: vixie-cron-%{version}-owl-linux.diff
Patch1: vixie-cron-%{version}-owl-sgid-crontab.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: owl-control < 2.0
Prereq: /sbin/chkconfig, /dev/null, grep, shadow-utils

%description
Cron is a standard UNIX daemon that runs specified programs at scheduled
times.  This package contains Paul Vixie's implementation of cron, with
significant modifications by the NetBSD, OpenBSD, Red Hat, and Owl teams.

%prep
%setup
%patch0 -p1
%patch1 -p1

%build
make -C usr.sbin/cron CFLAGS="-c -I. -I../../include $RPM_OPT_FLAGS"
make -C usr.sbin/cron CFLAGS="-c -I. -I../../include $RPM_OPT_FLAGS" \
	-f ../../usr.bin/crontab/Makefile

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,man/man{1,5,8},sbin}
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/{init.d,rc{0,1,2,3,4,5,6}.d}
mkdir -p -m 700 $RPM_BUILD_ROOT/var/spool/cron

install -m 700 usr.sbin/cron/crontab $RPM_BUILD_ROOT/usr/bin
install -m 700 usr.sbin/cron/crond $RPM_BUILD_ROOT/usr/sbin

install -m 644 usr.sbin/cron/crontab.1 $RPM_BUILD_ROOT/usr/man/man1
install -m 644 usr.sbin/cron/crontab.5 $RPM_BUILD_ROOT/usr/man/man5
install -m 644 usr.sbin/cron/cron.8 $RPM_BUILD_ROOT/usr/man/man8
gzip -9nf $RPM_BUILD_ROOT/usr/man/man*/*
ln -s cron.8.gz $RPM_BUILD_ROOT/usr/man/man8/crond.8.gz

install -m 700 $RPM_SOURCE_DIR/vixie-cron.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/crond
cd $RPM_BUILD_ROOT/etc/rc.d
ln -sf ../init.d/crond rc0.d/K60crond
ln -sf ../init.d/crond rc1.d/K60crond
ln -sf ../init.d/crond rc2.d/S40crond
ln -sf ../init.d/crond rc3.d/S40crond
ln -sf ../init.d/crond rc5.d/S40crond
ln -sf ../init.d/crond rc6.d/K60crond

mkdir -p $RPM_BUILD_ROOT/etc/control.d/facilities
install -m 700 $RPM_SOURCE_DIR/crontab.control \
	$RPM_BUILD_ROOT/etc/control.d/facilities/crontab

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep ^crontab: /etc/group &> /dev/null || groupadd -g 160 crontab
grep ^crontab: /etc/passwd &> /dev/null ||
	useradd -g crontab -u 160 -d / -s /bin/false -M crontab

%post
grep ^crontab: /etc/group &> /dev/null || chmod 700 /usr/bin/crontab
/sbin/chkconfig --add crond
test -r /var/run/crond.pid && /etc/rc.d/init.d/crond restart >&2

%preun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del crond
fi

%files
%defattr(-,root,root)
/usr/sbin/crond
%attr(2711,root,crontab) /usr/bin/crontab
/usr/man/man8/crond.*
/usr/man/man8/cron.*
/usr/man/man5/crontab.*
/usr/man/man1/crontab.*
%dir %attr(1730,root,crontab) /var/spool/cron
%config(missingok) /etc/rc.d/rc0.d/K60crond
%config(missingok) /etc/rc.d/rc1.d/K60crond
%config(missingok) /etc/rc.d/rc2.d/S40crond
%config(missingok) /etc/rc.d/rc3.d/S40crond
%config(missingok) /etc/rc.d/rc5.d/S40crond
%config(missingok) /etc/rc.d/rc6.d/K60crond
%config /etc/rc.d/init.d/crond
/etc/control.d/facilities/crontab

%changelog
* Sun Aug 20 2000 Solar Designer <solar@owl.openwall.com>
- crontab is now SGID crontab, not SUID root; the required changes
have been made to crontab, and the file ownership check has been added
into crond for this to make sense.

* Sat Aug 19 2000 Solar Designer <solar@owl.openwall.com>
- Based this package on Vixie cron with modifications from NetBSD and
OpenBSD teams, as found in OpenBSD 2.7.
- Did a number of changes needed for Linux.
- Reviewed all of the Red Hat patches (as of 6.2), changed the code in
a similar way where appropriate. (The /etc/cron.d support isn't
included, yet.)
- Fixed a number of bugs, added a lot of (hopefully healthy) paranoia
(all in the same patch file with the Linux-specific changes for now,
as maintaining separate patches would be non-practical at this stage).
- Took vixie-cron.init from RH.
- Wrote crontab.control.
- Based this spec file on Red Hat's, but changed it heavily.

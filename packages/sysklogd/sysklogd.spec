# $Id: Owl/packages/sysklogd/sysklogd.spec,v 1.2 2000/09/20 01:58:55 solar Exp $

Summary: System logging and kernel message trapping daemons.
Name: sysklogd
Version: 1.3.31
Release: 2owl
Copyright: BSD for syslogd and GPL for klogd
Group: System Environment/Daemons
Source0: ftp://sunsite.unc.edu/pub/Linux/system/daemons/sysklogd-1.3-31.tar.gz
Source1: syslog.conf
Source2: syslog.init
Source3: syslog.logrotate
Patch0: sysklogd-1.3-31-okir-dgram.diff
Patch1: sysklogd-1.3-31-rh-owl-Makefile.diff
Patch2: sysklogd-1.3-31-rh-ksyslog-nul.diff
Patch3: sysklogd-1.3-31-rh-utmp.diff
Patch4: sysklogd-1.3-31-rh-ksymless.diff
Patch5: sysklogd-1.3-31-debian-bug-32580.diff
Patch6: sysklogd-1.3-31-owl-klogd.diff
Patch7: sysklogd-1.3-31-owl-syslogd.diff
Patch8: sysklogd-1.3-31-owl-klogd-drop-root.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: logrotate
Prereq: fileutils, /sbin/chkconfig

%description
The sysklogd package contains two system utilities (syslogd and klogd)
which provide support for system logging.  syslogd and klogd run as
daemons (background processes) and log system messages to different
places according to a configuration file.

%prep
%setup -q -n sysklogd-1.3-31
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
make CFLAGS="$RPM_OPT_FLAGS -Wall -DSYSV"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{etc,usr/{bin,man/man{5,8},sbin}}
mkdir -p $RPM_BUILD_ROOT/sbin

make install TOPDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT

strip sbin/*
chmod 700 sbin/*logd

install -m 644 $RPM_SOURCE_DIR/syslog.conf etc/syslog.conf
mkdir -p etc/{rc.d/init.d,logrotate.d}
install -m 755 $RPM_SOURCE_DIR/syslog.init etc/rc.d/init.d/syslog
mkdir -p etc/rc.d/rc{0,1,2,3,4,5,6}.d
ln -sf ../init.d/syslog etc/rc.d/rc0.d/K99syslog
ln -sf ../init.d/syslog etc/rc.d/rc1.d/K99syslog
ln -sf ../init.d/syslog etc/rc.d/rc2.d/S30syslog
ln -sf ../init.d/syslog etc/rc.d/rc3.d/S30syslog
ln -sf ../init.d/syslog etc/rc.d/rc5.d/S30syslog
ln -sf ../init.d/syslog etc/rc.d/rc6.d/K99syslog
install -m 644 $RPM_SOURCE_DIR/syslog.logrotate etc/logrotate.d/syslog

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep ^klogd: /etc/group &> /dev/null || groupadd -g 180 klogd
grep ^klogd: /etc/passwd &> /dev/null ||
	useradd -g klogd -u 180 -d / -s /bin/false -M klogd

%post
for n in /var/log/{kernel,messages,maillog,cron}
do
	test -f $n && continue
	touch $n
	chmod 600 $n
done
/sbin/chkconfig --add syslog

%preun
if [ $1 = 0 ]; then
	/sbin/chkconfig --del syslog
fi

%files
%defattr(-,root,root)
%doc ANNOUNCE README* NEWS INSTALL Sysklogd-1.3.lsm
%config /etc/syslog.conf
%config /etc/logrotate.d/syslog
%config /etc/rc.d/init.d/syslog
%config(missingok) /etc/rc.d/rc0.d/K99syslog
%config(missingok) /etc/rc.d/rc3.d/S30syslog
%config(missingok) /etc/rc.d/rc1.d/K99syslog
%config(missingok) /etc/rc.d/rc5.d/S30syslog
%config(missingok) /etc/rc.d/rc2.d/S30syslog
%config(missingok) /etc/rc.d/rc6.d/K99syslog
/sbin/*
/usr/man/*/*

%changelog
* Wed Sep 20 2000 Solar Designer <solar@owl.openwall.com>
- Run klogd as a non-root user.

* Tue Sep 12 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file from RH, did the usual cleanups.
- Based many of the patches on those found in RH.
- Added a reliability/security fix by Daniel Jacobowitz of Debian
(http://bugs.debian.org/32580).
- Added a klogd "format bug" fix (found by Jouko Pynnönen).
- Added a syslogd single-byte buffer overflow and control character fix
for printline().
- <thoughts>
We may switch to using an alternative syslogd in the near future.  This
package, in its current form, is kind of temporary.  (It may be changed
to provide klogd only.)
</thoughts>

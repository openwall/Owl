# $Id: Owl/packages/sysklogd/sysklogd.spec,v 1.5 2001/10/08 06:20:28 solar Exp $

Summary: System logging and kernel message trapping daemons.
Name: sysklogd
Version: 1.4.1
Release: 1owl
License: BSD for syslogd and GPL for klogd
Group: System Environment/Daemons
Source0: http://www.infodrom.ffis.de/projects/sysklogd/download/sysklogd-%{version}.tar.gz
Source1: syslog.conf
Source2: syslog.init
Source3: syslog.logrotate
Patch0: sysklogd-1.3-31-rh-owl-Makefile.diff
Patch1: sysklogd-1.3-31-rh-ksyslog-nul.diff
Patch2: sysklogd-1.3-31-rh-utmp.diff
Patch3: sysklogd-1.3-31-rh-ksymless.diff
Patch4: sysklogd-1.4.1-owl-longjmp.diff
Patch5: sysklogd-1.4.1-owl-syslogd-create-mode.diff
Patch6: sysklogd-1.4.1-alt-owl-syslogd-killing.diff
Patch7: sysklogd-1.4.1-caen-owl-klogd-drop-root.diff
Patch8: sysklogd-1.4.1-caen-owl-syslogd-bind.diff
Patch9: sysklogd-1.4.1-caen-owl-syslogd-drop-root.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: logrotate, /var/empty
PreReq: shadow-utils, grep, fileutils, /sbin/chkconfig

%description
The sysklogd package contains two system utilities (syslogd and klogd)
which provide support for system logging.  syslogd and klogd run as
daemons (background processes) and log system messages to different
places according to a configuration file.

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

%build
make CFLAGS="$RPM_OPT_FLAGS -Wall -DSYSV"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%_mandir/man{5,8},/sbin}

%makeinstall TOPDIR=$RPM_BUILD_ROOT MANDIR=$RPM_BUILD_ROOT%_mandir

cd $RPM_BUILD_ROOT

strip sbin/*
chmod 700 sbin/*logd

mkdir -p etc/{rc.d/init.d,logrotate.d}
install -m 644 $RPM_SOURCE_DIR/syslog.conf etc/syslog.conf
install -m 755 $RPM_SOURCE_DIR/syslog.init etc/rc.d/init.d/syslog
install -m 644 $RPM_SOURCE_DIR/syslog.logrotate etc/logrotate.d/syslog

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep ^klogd: /etc/group &> /dev/null || groupadd -g 180 klogd
grep ^klogd: /etc/passwd &> /dev/null ||
	useradd -g klogd -u 180 -d / -s /bin/false -M klogd
grep ^syslogd: /etc/group &> /dev/null || groupadd -g 181 syslogd
grep ^syslogd: /etc/passwd &> /dev/null ||
	useradd -g syslogd -u 181 -d / -s /bin/false -M syslogd
rm -f /var/run/syslog.restart
if [ $1 -ge 2 ]; then
	/etc/rc.d/init.d/syslog status && touch /var/run/syslog.restart || :
	/etc/rc.d/init.d/syslog stop || :
fi

%post
/sbin/chkconfig --add syslog
if [ -f /var/run/syslog.restart ]; then
	/etc/rc.d/init.d/syslog start
elif [ -f /var/run/syslogd.pid -o -f /var/run/klogd.pid ]; then
	/etc/rc.d/init.d/syslog restart
fi
rm -f /var/run/syslog.restart

%preun
if [ $1 -eq 0 ]; then
	/etc/rc.d/init.d/syslog stop
	/sbin/chkconfig --del syslog
fi

%files
%defattr(-,root,root)
%doc COPYING ANNOUNCE README* NEWS CHANGES
%config(noreplace) /etc/syslog.conf
%config(noreplace) /etc/logrotate.d/syslog
%config(noreplace) /etc/rc.d/init.d/syslog
/sbin/*
%_mandir/*/*

%changelog
* Mon Oct 08 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 1.4.1.
- Based the new klogd drop root patch on one from CAEN Linux.
- Added syslogd patches derived from CAEN Linux to allow specifying a
bind address for the UDP socket and to let syslogd run as non-root.
- klogd is now running chrooted to /var/empty.
- syslogd is now running as its dedicated pseudo-user, too.

* Wed May 23 2001 Solar Designer <solar@owl.openwall.com>
- Back-ported a klogd DoS fix from 1.4.1, thanks to the reports from
Jarno Huuskonen and Thomas Roessler who initially reported the problem
to Debian (see http://bugs.debian.org/85478).

* Fri Dec 01 2000 Solar Designer <solar@owl.openwall.com>
- Adjusted syslog.init for owl-startup.
- Restart after package upgrades in an owl-startup compatible way.

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

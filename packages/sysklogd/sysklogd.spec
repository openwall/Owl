# $Owl: Owl/packages/sysklogd/sysklogd.spec,v 1.28 2014/07/12 14:18:29 galaxy Exp $

Summary: System logging and kernel message trapping daemons.
Name: sysklogd
Version: 1.4.1
Release: owl15
License: BSD for syslogd and GPL for klogd
Group: System Environment/Daemons
URL: http://www.infodrom.org/projects/sysklogd/
Source0: http://www.infodrom.org/projects/sysklogd/download/%name-%version.tar.gz
Source1: syslog.conf
Source2: syslog.init
Source3: syslog.logrotate
Source4: syslog.sysconfig
Patch0: sysklogd-1.4.1-cvs-20060928.diff
Patch1: sysklogd-1.4.2-rh-alt-warnings.diff
Patch2: sysklogd-1.4.2-rh-ksymless.diff
Patch3: sysklogd-1.4.2-owl-Makefile.diff
Patch4: sysklogd-1.4.2-alt-format.diff
Patch5: sysklogd-1.4.2-alt-redirect-std.diff
Patch6: sysklogd-1.4.2-alt-syslogd-nonblock.diff
Patch7: sysklogd-1.4.2-owl-syslogd-create-mode.diff
Patch8: sysklogd-1.4.2-owl-syslogd-doexit.diff
Patch9: sysklogd-1.4.2-caen-owl-klogd-drop-root.diff
Patch10: sysklogd-1.4.2-owl-klogd-kmsg.diff
Patch11: sysklogd-1.4.2-caen-owl-syslogd-bind.diff
Patch12: sysklogd-1.4.2-caen-owl-syslogd-drop-root.diff
Patch13: sysklogd-1.4.2-alt-syslogd-chroot.diff
Patch14: sysklogd-1.4.2-alt-syslogd-funix_dir.diff
Patch15: sysklogd-1.4.2-owl-syslogd-unixcred.diff
Patch16: sysklogd-1.4.2-up-SO_BSDCOMPAT.diff
Patch17: sysklogd-1.4.2-owl-ksym_mod-linux.diff
Patch18: sysklogd-1.4.2-owl-syslogd-no-printsys.diff
Requires(pre): shadow-utils, grep, fileutils
Requires(post,preun): chkconfig
Requires: logrotate, /var/empty
BuildRoot: /override/%name-%version

%description
The sysklogd package contains two system utilities (syslogd and klogd)
which provide support for system logging.  syslogd and klogd run as
daemons (background processes) and log system messages to different
places according to a configuration file.

%prep
%setup -q
%patch0 -p0
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
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1

%build
%__make CFLAGS='%optflags -Wall -DSYSV $(shell getconf LFS_CFLAGS)'

%install
rm -rf %buildroot
mkdir -p %buildroot{%_mandir/man{5,8},/sbin,/dev}

%makeinstall prefix=%buildroot MANDIR=%buildroot%_mandir

cd %buildroot

chmod 700 sbin/*logd

mkdir -p etc/{rc.d/init.d,logrotate.d,syslog.d,sysconfig}
install -m 644 %_sourcedir/syslog.conf etc/syslog.conf
install -m 755 %_sourcedir/syslog.init etc/rc.d/init.d/syslog
install -m 644 %_sourcedir/syslog.logrotate etc/logrotate.d/syslog
install -m 600 %_sourcedir/syslog.sysconfig etc/sysconfig/syslog

# XXX: (GM): we need to use mksock(1) from coreutils here, but our
#            coreutils package has no mksock tool.
touch dev/log

%pre
grep -q ^klogd: /etc/group || groupadd -g 180 klogd
grep -q ^klogd: /etc/passwd ||
	useradd -g klogd -u 180 -d / -s /bin/false -M klogd
grep -q ^syslogd: /etc/group || groupadd -g 181 syslogd
grep -q ^syslogd: /etc/passwd ||
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

%triggerpostun -- sysklogd < 1.4.1-1owl
/sbin/chkconfig --add syslog

%files
%defattr(-,root,root)
%doc COPYING ANNOUNCE README* NEWS CHANGES
%config(noreplace) /etc/syslog.conf
%config(noreplace) /etc/logrotate.d/syslog
%config(noreplace) /etc/rc.d/init.d/syslog
%config(noreplace) /etc/sysconfig/syslog
%attr(700,root,root) %dir /etc/syslog.d
%attr(666,root,root) %ghost /dev/log
/sbin/*
%_mandir/*/*

%changelog
* Mon Jun 30 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.4.1-owl15
- Replaced the deprecated PreReq tag with Requires().

* Tue Nov 09 2010 Solar Designer <solar-at-owl.openwall.com> 1.4.1-owl14
- In the unixcred patch, stop the search for a PID at the colon.
- In the unixcred patch, don't log the UID on klogd's messages as long as they
don't claim to be other than from the kernel.
- Dropped printsys() from syslogd.c (it was dead code).

* Sun Sep 20 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.1-owl13
- Updated to post-1.4.1 cvs snapshot 20060928.
- Fixed build with linux kernel 2.6.x headers.
- Fixed CFLAGS to include "getconf LFS_CFLAGS" output.
- Prefixed each syslog.conf entry with the minus sign to avoid syncing
after every logging.

* Wed Oct 24 2007 ArkanoiD <ark-at-owl.openwall.com> 1.4.1-owl12
- Unix socket credentials verification

* Thu Mar 30 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.4.1-owl11
- Replaced make with %%__make.
- Added ghost file /dev/log.

* Wed Aug 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.1-owl10
- Changed klogd to terminate when read from previously opened /proc/kmsg
returns EPERM.
- Added missing linefeed in usage messages.

* Thu Aug 18 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.1-owl9
- Updated to post-1.4.1 cvs snapshot 20050525.
- Reviewed Owl patches, removed obsolete ones, rediffed all the rest.
- Imported a bunch of patches from ALT's sysklogd-1.4.1-alt21 package,
including redirection of standard descriptors to /dev/null in klogd and
syslogd, nonblocking I/O on tty descriptors, new syslogd option "-A"
can be used to specify directory with symlinks to additional sockets
from that syslogd has to listen to, syslogd now can run chrooted.

* Sun Apr 18 2004 Solar Designer <solar-at-owl.openwall.com> 1.4.1-owl8
- Cleaned up the crunch_list() function in syslogd fixing the buffer overflow
discovered by Steve Grubb and a number of other issues.

* Tue Feb 10 2004 Solar Designer <solar-at-owl.openwall.com> 1.4.1-owl7
- Use "sharedscripts" directive in /etc/logrotate.d/syslog such that syslogd
is told to restart only once for all logs rotated.

* Sun Jan 04 2004 Michail Litvak <mci-at-owl.openwall.com> 1.4.1-owl6
- Pass options to syslogd and klogd from /etc/sysconfig/syslog file.

* Sun Aug 10 2003 Solar Designer <solar-at-owl.openwall.com> 1.4.1-owl5
- Build with LFS (thanks to Dmitry V. Levin).

* Fri Aug 01 2003 Solar Designer <solar-at-owl.openwall.com> 1.4.1-owl4
- Added URL.

* Sun Jul 07 2002 Solar Designer <solar-at-owl.openwall.com> 1.4.1-owl3
- Use grep -q in %pre.

* Tue Feb 05 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Mon Nov 05 2001 Solar Designer <solar-at-owl.openwall.com>
- Use a trigger to re-create the rc*.d symlinks when upgrading from
old versions of the package.

* Mon Oct 08 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 1.4.1.
- Based the new klogd drop root patch on one from CAEN Linux.
- Added syslogd patches derived from CAEN Linux to allow specifying a
bind address for the UDP socket and to let syslogd run as non-root.
- klogd is now running chrooted to /var/empty.
- syslogd is now running as its dedicated pseudo-user, too.

* Wed May 23 2001 Solar Designer <solar-at-owl.openwall.com>
- Back-ported a klogd DoS fix from 1.4.1, thanks to the reports from
Jarno Huuskonen and Thomas Roessler who initially reported the problem
to Debian (see http://bugs.debian.org/85478).

* Fri Dec 01 2000 Solar Designer <solar-at-owl.openwall.com>
- Adjusted syslog.init for owl-startup.
- Restart after package upgrades in an owl-startup compatible way.

* Wed Sep 20 2000 Solar Designer <solar-at-owl.openwall.com>
- Run klogd as a non-root user.

* Tue Sep 12 2000 Solar Designer <solar-at-owl.openwall.com>
- Imported this spec file from RH, did the usual cleanups.
- Based many of the patches on those found in RH.
- Added a reliability/security fix by Daniel Jacobowitz of Debian
(http://bugs.debian.org/32580).
- Added a klogd "format bug" fix (found by Jouko Pynn�nen).
- Added a syslogd single-byte buffer overflow and control character fix
for printline().
- <thoughts>
We may switch to using an alternative syslogd in the near future.  This
package, in its current form, is kind of temporary.  (It may be changed
to provide klogd only.)
</thoughts>

# $Id: Owl/packages/vixie-cron/vixie-cron.spec,v 1.23 2003/10/30 21:15:49 solar Exp $

Summary: Daemon to execute scheduled commands (Vixie Cron).
Name: vixie-cron
Version: 3.0.2.7
Release: owl17
License: distributable
Group: System Environment/Base
Source0: vixie-cron-%version.tar.gz
Source1: vixie-cron.init
Source2: crontab.control
Patch0: vixie-cron-%version-owl-linux.diff
Patch1: vixie-cron-%version-owl-sgid-crontab.diff
Patch2: vixie-cron-%version-owl-crond.diff
Patch3: vixie-cron-%version-owl-vitmp.diff
Patch4: vixie-cron-%version-openbsd-sigchld.diff
PreReq: owl-control >= 0.4, owl-control < 2.0
PreReq: /sbin/chkconfig, grep, shadow-utils
BuildRoot: /override/%name-%version

%description
cron is a daemon that runs specified programs at scheduled times.  This
package contains Paul Vixie's implementation of cron, with significant
modifications by the NetBSD, OpenBSD, Red Hat, and Owl teams.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
make -C usr.sbin/cron CFLAGS="-c -I. -I../../include $RPM_OPT_FLAGS"
make -C usr.sbin/cron CFLAGS="-c -I. -I../../include $RPM_OPT_FLAGS" \
	-f ../../usr.bin/crontab/Makefile

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,sbin}
mkdir -p $RPM_BUILD_ROOT%_mandir/man{1,5,8}
mkdir -p -m 700 $RPM_BUILD_ROOT/var/spool/cron
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/cron.d

install -m 700 usr.sbin/cron/crontab $RPM_BUILD_ROOT/usr/bin/
install -m 700 usr.sbin/cron/crond $RPM_BUILD_ROOT/usr/sbin/

install -m 644 usr.sbin/cron/crontab.1 $RPM_BUILD_ROOT%_mandir/man1/
install -m 644 usr.sbin/cron/crontab.5 $RPM_BUILD_ROOT%_mandir/man5/
install -m 644 usr.sbin/cron/cron.8 $RPM_BUILD_ROOT%_mandir/man8/
ln -s cron.8 $RPM_BUILD_ROOT%_mandir/man8/crond.8

install -m 700 -D $RPM_SOURCE_DIR/vixie-cron.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/crond

mkdir -p $RPM_BUILD_ROOT/etc/control.d/facilities
install -m 700 $RPM_SOURCE_DIR/crontab.control \
	$RPM_BUILD_ROOT/etc/control.d/facilities/crontab

%pre
grep -q ^crontab: /etc/group || groupadd -g 160 crontab
grep -q ^crontab: /etc/passwd ||
	useradd -g crontab -u 160 -d / -s /bin/false -M crontab
rm -f /var/run/crond.restart
if [ $1 -ge 2 ]; then
	/etc/rc.d/init.d/crond status && touch /var/run/crond.restart || :
	/etc/rc.d/init.d/crond stop || :
	/usr/sbin/control-dump crontab
fi

%post
if [ $1 -ge 2 ]; then
	/usr/sbin/control-restore crontab
else
	grep -q ^crontab: /etc/group && /usr/sbin/control crontab public
fi
/sbin/chkconfig --add crond
if [ -f /var/run/crond.restart ]; then
	/etc/rc.d/init.d/crond start
elif [ -f /var/run/crond.pid ]; then
	/etc/rc.d/init.d/crond restart
fi
rm -f /var/run/crond.restart

%preun
if [ $1 -eq 0 ]; then
	/etc/rc.d/init.d/crond stop || :
	/sbin/chkconfig --del crond
fi

%files
%defattr(-,root,root)
/usr/sbin/crond
%attr(700,root,root) /usr/bin/crontab
%_mandir/man*/*
%dir %attr(1730,root,crontab) /var/spool/cron
%dir /etc/cron.d
%config /etc/rc.d/init.d/crond
/etc/control.d/facilities/crontab

%changelog
* Wed Jan 29 2003 Michail Litvak <mci@owl.openwall.com> 3.0.2.7-owl17
- Added patch from OpenBSD for setting SIG_DFL action instead of SIG_IGN
for SIGCHLD signal; this fixes the problem with Perl's scripts which run
from cron.

* Sun Nov 03 2002 Solar Designer <solar@owl.openwall.com>
- Dump/restore the owl-control setting for crontab on package upgrades.
- Keep crontab at mode 700 ("restricted") in the package, but default
it to "public" in %post when the package is first installed.  This avoids
a race and fail-open behavior.
- Dropped the trigger which was needed for upgrades from versions of the
package from over a year ago, -- it would wrongly go off on each upgrade
or uninstall of the new package because of our new version numbering.

* Sun Jul 07 2002 Solar Designer <solar@owl.openwall.com>
- Use grep -q in %pre.

* Thu May 09 2002 Solar Designer <solar@owl.openwall.com>
- Ensure all files are closed in crontab(1) when the editor is run; this
fixes the problem pointed out by Paul Starzetz on Bugtraq where crontab
could leak read-only access to /etc/cron.{allow,deny} even if those files
are made readable to just group crontab.

* Thu Apr 25 2002 Solar Designer <solar@owl.openwall.com>
- vitmp has been moved to /bin.

* Sun Apr 21 2002 Solar Designer <solar@owl.openwall.com>
- Use /usr/libexec/vitmp in crontab(1).

* Sat Feb 02 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.
- Use the _mandir macro.

* Mon Nov 05 2001 Solar Designer <solar@owl.openwall.com>
- Use a trigger to re-create the rc*.d symlinks when upgrading from
old versions of the package.

* Wed Jul 18 2001 Michail Litvak <mci@owl.openwall.com>
- rework spooldirs handling to exclude files with
  filenames containing a dot '.' or ending with '~'
- spec changes: remove packaging /etc/rc.d/rc*.d/*
  (this is a chkconfig work)

* Mon Jul 16 2001 Michail Litvak <mci@owl.openwall.com>
- Patch to support /etc/cron.d dir

* Fri Dec 01 2000 Solar Designer <solar@owl.openwall.com>
- Adjusted vixie-cron.init for owl-startup.
- Restart crond after package upgrades in an owl-startup compatible way.

* Sat Oct 28 2000 Solar Designer <solar@owl.openwall.com>
- Added "|| :" to the test in %post, as it should return success to RPM.

* Mon Aug 21 2000 Solar Designer <solar@owl.openwall.com>
- Check nlink and permissions as well as the owner of crontabs.

* Sun Aug 20 2000 Solar Designer <solar@owl.openwall.com>
- crontab is now SGID crontab, not SUID root; the required changes
have been made to crontab, and the file ownership check has been added
into crond for this to make sense.
- Close fd's at crond startup, so they no longer get inherited by cron
jobs if a custom SHELL= is specified.

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

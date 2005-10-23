# $Id: Owl/packages/vixie-cron/vixie-cron.spec,v 1.40 2005/10/23 20:20:13 solar Exp $

Summary: Daemon to execute scheduled commands (Vixie Cron).
Name: vixie-cron
Version: 4.1.20040916
Release: owl4
License: distributable
Group: System Environment/Base
Source0: vixie-cron-%version.tar.bz2
Source1: vixie-cron.init
Source2: crontab.control
Source3: at.control
Source4: crond.pam
Patch0: vixie-cron-4.1.20040916-alt-warnings.diff
Patch1: vixie-cron-4.1.20040916-owl-alt-linux.diff
Patch2: vixie-cron-4.1.20040916-owl-vitmp.diff
Patch3: vixie-cron-4.1.20040916-owl-crond.diff
Patch4: vixie-cron-4.1.20040916-alt-owl-Makefile.diff
Patch5: vixie-cron-4.1.20040916-alt-progname.diff
Patch6: vixie-cron-4.1.20040916-alt-sigpipe.diff
Patch7: vixie-cron-4.1.20040916-alt-pam.diff
Patch8: vixie-cron-4.1.20040916-alt-setlocale.diff
Patch9: vixie-cron-4.1.20040916-alt-children.diff
PreReq: owl-control >= 0.4, owl-control < 2.0
PreReq: /sbin/chkconfig, grep, shadow-utils
Provides: at, crond
Obsoletes: at
BuildRequires: pam-devel
BuildRoot: /override/%name-%version

%description
cron is a daemon that runs specified programs at scheduled times.  This
package contains Paul Vixie's implementation of cron, with significant
modifications by the NetBSD, OpenBSD, Red Hat, ALT, and Owl teams.

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

%{expand:%%define optflags %optflags -Wall}

%build
for dir in usr.sbin/cron usr.bin/crontab usr.bin/at; do
	CFLAGS="$RPM_OPT_FLAGS" %__make -C $dir .CURDIR=. CC="%__cc" LD="%__cc"
done

%install
rm -rf %buildroot

mkdir -p -m 700 %buildroot/var/spool/{cron,at}
mkdir -p -m 755 %buildroot/etc/cron.d

for dir in usr.sbin/cron usr.bin/crontab usr.bin/at; do
	%makeinstall -C $dir .CURDIR=. DESTDIR=%buildroot
done

pushd %buildroot%_bindir
ln -s at atq
ln -s at atrm
ln -s at batch
popd

ln -s cron.8 %buildroot%_mandir/man8/crond.8
ln -s at.1 %buildroot%_mandir/man1/batch.1

install -pD -m700 %_sourcedir/vixie-cron.init \
	%buildroot/etc/rc.d/init.d/crond
install -pD -m700 %_sourcedir/crontab.control \
	%buildroot/etc/control.d/facilities/crontab
install -pD -m700 %_sourcedir/at.control \
	%buildroot/etc/control.d/facilities/at
install -pD -m600 %_sourcedir/crond.pam %buildroot/etc/pam.d/crond

touch %buildroot/etc/{at,cron}.{allow,deny}

%pre
grep -q ^crontab: /etc/group || groupadd -g 160 crontab
grep -q ^crontab: /etc/passwd ||
	useradd -g crontab -u 160 -d / -s /bin/false -M crontab
rm -f /var/run/crond.restart
if [ $1 -ge 2 ]; then
	/etc/rc.d/init.d/crond status && touch /var/run/crond.restart || :
	/etc/rc.d/init.d/crond stop || :
	%_sbindir/control-dump crontab
	if %_sbindir/control at status &> /dev/null; then
		%_sbindir/control-dump at
		touch /var/run/crond.restore-at
	fi
fi

%post
if [ $1 -ge 2 ]; then
	%_sbindir/control-restore crontab
	if [ -f /var/run/crond.restore-at ]; then
		%_sbindir/control-restore at
		rm -f /var/run/crond.restore-at
	fi
else
	grep -q ^crontab: /etc/group && %_sbindir/control crontab public || :
	grep -q ^crontab: /etc/group && %_sbindir/control at public || :
fi
/sbin/chkconfig --add crond
if [ -f /var/run/crond.restart ]; then
	/etc/rc.d/init.d/crond start
elif [ -f /var/run/crond.pid ]; then
	/etc/rc.d/init.d/crond restart
fi
rm -f /var/run/crond.restart

%triggerun -- vixie-cron <= 3.0.2.7
grep -q ^crontab: /etc/group && %_sbindir/control at public || :

%preun
if [ $1 -eq 0 ]; then
	/etc/rc.d/init.d/crond stop || :
	/sbin/chkconfig --del crond
fi

%files
%defattr(-,root,root)
%_sbindir/crond
%attr(700,root,root) %verify(not mode group) %_bindir/crontab
%attr(700,root,root) %verify(not mode group) %_bindir/at
%_bindir/atq
%_bindir/atrm
%_bindir/batch
%_mandir/man?/*
%dir %attr(3730,root,crontab) /var/spool/cron
%dir %attr(1770,root,crontab) /var/spool/at
%dir /etc/cron.d
%config(noreplace) /etc/pam.d/crond
%config /etc/rc.d/init.d/crond
/etc/control.d/facilities/crontab
/etc/control.d/facilities/at
%attr(640,root,crontab) %ghost /etc/*.allow
%attr(640,root,crontab) %config(noreplace) /etc/*.deny

%changelog
* Sat Sep 24 2005 Dmitry V. Levin <ldv@owl.openwall.com> 4.1.20040916-owl4
- Added crond to the package provides list.

* Sat Jun 25 2005 Dmitry V. Levin <ldv@owl.openwall.com> 4.1.20040916-owl3
- Fixed typo in two error messages introduced by PAM support patch.

* Wed Jun 22 2005 Dmitry V. Levin <ldv@owl.openwall.com> 4.1.20040916-owl2
- Imported patch from ALT that implements PAM accounting and session
management support.
- Enabled use of getloadavg(3).

* Mon Mar 14 2005 Solar Designer <solar@owl.openwall.com> 4.1.20040916-owl1
- Applied many assorted corrections and cleanups.

* Sun Feb 20 2005 Juan M. Bello Rivas <jmbr@owl.openwall.com> 4.1.20040916-owl0.1
- Updated to 4.1 as found in OpenBSD CVS snapshot dated 2004/09/16, with
modifications by Jarno Huuskonen and Dmitry V. Levin.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 3.0.2.7-owl19
- Removed verify checks for crontab binary since we are controlling it
through owl-control facility.
- Added a patch to deal with issues after gcc upgrade.
- Cleaned up the spec.

* Sun Feb 29 2004 Michail Litvak <mci@owl.openwall.com> 3.0.2.7-owl18
- Fixed -owl-linux.diff to build on glibc 2.3.2.

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

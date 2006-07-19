# $Owl: Owl/packages/xinetd/xinetd.spec,v 1.38 2006/07/19 22:59:47 solar Exp $

Summary: The extended Internet services daemon.
Name: xinetd
Version: 2.3.13
Release: owl4
License: BSD with minor restrictions
Group: System Environment/Daemons
URL: http://www.xinetd.org
Source0: http://www.xinetd.org/xinetd-%version.tar.gz
Source1: xinetd.init
Source2: xinetd.conf
Source3: xinetd-ttime
Source4: xinetd-utime
Source5: xinetd-tdtime
Source6: xinetd-udtime
Source7: xinetd-echo
Source8: xinetd-uecho
Source9: xinetd-chargen
Source10: xinetd-uchargen
Patch0: xinetd-2.3.13-cvs-20050330-fixes.diff
Patch1: xinetd-2.3.13-owl-fixes.diff
Patch2: xinetd-2.3.13-alt-pidfile.diff
Patch3: xinetd-2.3.13-alt-parse_inet_addresses.diff
PreReq: /sbin/chkconfig
Requires: tcp_wrappers >= 7.6-owl3.2
Provides: inetd
Obsoletes: inetd
BuildRequires: tcp_wrappers >= 7.6-owl3.2
BuildRoot: /override/%name-%version

%description
xinetd performs the same function as inetd: it starts programs that
provide Internet services.  Instead of having such servers started at
system initialization time, and be dormant until a connection request
arrives, xinetd is the only daemon process started and it listens on
all service ports for the services listed in its configuration file.
When a request comes in, xinetd starts the appropriate server.  Because
of the way it operates, xinetd (as well as inetd) is also referred to
as a super-server.

xinetd has access control machanisms, extensive logging capabilities,
the ability to make services available based on time, and can place
limits on the number of servers that can be started, among other things.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
bzip2 -9k CHANGELOG

%{expand:%%define optflags %optflags -Wall -W -Wno-unused -Wno-switch}

%build
export ac_cv_header_DNSServiceDiscovery_DNSServiceDiscovery_h=no \
%configure --with-loadavg --with-libwrap
%__make

%install
rm -rf %buildroot
mkdir -p %buildroot/etc/{rc.d/init.d,xinetd.d}
%makeinstall \
	DAEMONDIR=%buildroot%_sbindir MANDIR=%buildroot%_mandir

cd %buildroot

install -m 755 %_sourcedir/xinetd.init etc/rc.d/init.d/xinetd

install %_sourcedir/xinetd.conf etc/
install %_sourcedir/xinetd-ttime etc/xinetd.d/time
install %_sourcedir/xinetd-utime etc/xinetd.d/time-udp
install %_sourcedir/xinetd-tdtime etc/xinetd.d/daytime
install %_sourcedir/xinetd-udtime etc/xinetd.d/daytime-udp
install %_sourcedir/xinetd-echo etc/xinetd.d/echo
install %_sourcedir/xinetd-uecho etc/xinetd.d/echo-udp
install %_sourcedir/xinetd-chargen etc/xinetd.d/chargen
install %_sourcedir/xinetd-uchargen etc/xinetd.d/chargen-udp

rm .%_sbindir/{itox,xconv.pl} .%_mandir/man8/{itox,xconv.pl}.8*

%pre
rm -f /var/run/xinetd.restart
if [ $1 -ge 2 ]; then
	/etc/rc.d/init.d/xinetd status && touch /var/run/xinetd.restart || :
	/etc/rc.d/init.d/xinetd stop || :
fi

%post
if [ $1 -eq 1 ]; then
	/sbin/chkconfig --add xinetd
fi
if [ -f /var/run/xinetd.restart ]; then
	/etc/rc.d/init.d/xinetd start
fi
rm -f /var/run/xinetd.restart

%preun
if [ $1 -eq 0 ]; then
	/etc/rc.d/init.d/xinetd stop || :
	/sbin/chkconfig --del xinetd
fi

%files
%defattr(-,root,root)
%doc AUDIT CHANGELOG.bz2 COPYRIGHT README xinetd/sample.conf
%attr(640,root,wheel) %config(noreplace) /etc/xinetd.conf
%attr(750,root,wheel) %dir /etc/xinetd.d
%attr(640,root,wheel) %config(noreplace) /etc/xinetd.d/*
%config /etc/rc.d/init.d/xinetd
%_sbindir/*
%_mandir/*/*

%changelog
* Thu Jul 20 2006 Solar Designer <solar-at-owl.openwall.com> 2.3.13-owl4
- Changed the permissions on /etc/xinetd.d to 750 root:wheel, and on
/etc/xinetd.conf and /etc/xinetd.d/* to 640 root:wheel.

* Thu Mar 30 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.3.13-owl3
- Replaced make with %%__make.
- Added /etc/xinetd.d to the filelist.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.3.13-owl2
- Compressed CHANGELOG file.

* Tue Jun 28 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.3.13-owl1
- Updated to 2.3.13.
- Backported bug fixes from cvs snapshot 20050330.
- Applied two patches from ALT's xinetd-2.3.13-alt3 package.
- Fixed compilation warnings.

* Mon May 03 2004 Solar Designer <solar-at-owl.openwall.com> 2.3.12-owl4
- Bumped release to correctly reflect the rebuild against shared libwrap.

* Fri Sep 12 2003 Solar Designer <solar-at-owl.openwall.com> 2.3.12-owl3
- Another fix from the CVS (originally submitted by Red Hat):
Occasionally, Smorefds didn't allocate more fds as expected.

* Fri Sep 05 2003 Solar Designer <solar-at-owl.openwall.com> 2.3.12-owl2
- Back-ported a fix from the CVS, thanks to Steve Grubb:
Add NULL entry to success_log_options to properly end the nvlist.
- With IPv6, correctly extract IPv4 mapped addresses from sa_data:
http://marc.theaimsgroup.com/?l=xinetd&m=106027800730549

* Mon Aug 25 2003 Solar Designer <solar-at-owl.openwall.com> 2.3.12-owl1
- Updated to 2.3.12.

* Wed Apr 16 2003 Solar Designer <solar-at-owl.openwall.com> 2.3.11-owl1
- Updated to 2.3.11.

* Mon Feb 24 2003 Michail Litvak <mci-at-owl.openwall.com>
- TCPMUX parser updates. -Steve Grubb
- TCPMUX was causing core dumps due to changes made in 2.3.10's
  child_process(), reverted changes. -Philip Armstrong
- Fix from ALT Linux Team (fixed a bounds check in Sdone())

* Sat Jan 18 2003 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.3.10, with its meaningless change to Sdone() reverted.

* Thu Dec 19 2002 Solar Designer <solar-at-owl.openwall.com>
- New release number for linking against tcp_wrappers with Steve Grubb's
error handling fix.

* Mon Oct 28 2002 Solar Designer <solar-at-owl.openwall.com>
- Build with load averages support.

* Sat Sep 28 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.3.9, dropping the patch (included).

* Thu Sep 19 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.3.8 with a new set of minor fixes.

* Sun Aug 11 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.3.6 adding fixes or workarounds for issues introduced after
2.3.3 including the signal pipe leak into child processes (a security hole
with 2.3.4+).
- Made xinetd also unlink its PID file when exiting on reload.

* Sat Feb 02 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.
- Dropped the unused xinetd-inetdconvert.

* Mon Nov 05 2001 Solar Designer <solar-at-owl.openwall.com>
- /etc/init.d -> /etc/rc.d/init.d for consistency.

* Thu Aug 30 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.3.3.
- Dropped the big -audit patch all of which went into xinetd 2.3.1+.
- Added the unlinking of PID file when exiting due to no services.

* Sat Jul 28 2001 Solar Designer <solar-at-owl.openwall.com>
- Handle the case of nonexistent /etc/sysconfig/network correctly.
- Don't -stayalive, we may invent a reload-or-start option instead.

* Sun Jul 22 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated the -audit patch based on results of testing by Michail Litvak
<mci at owl.openwall.com>, by ALT Linux Team, and at DataForce ISP.

* Thu Jul 05 2001 Solar Designer <solar-at-owl.openwall.com>
- Applied _many_ security and reliability fixes (in fact so many that
there have to be new bugs as well and testing is needed), see AUDIT.
The patch is 100 KB large.

* Fri Jun 29 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.3.0, which fixes the problem with xinetd's string handling
routines discovered by Sebastian Krahmer of SuSE Security Team.
- Dropped the 2.1.8.9pre15 patches (incorporated into 2.1.8.9pre16+).

* Tue Jun 12 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.1.8.9pre15.
- With includedir, skip all files with names containing a dot ('.') or
ending with a tilde ('~'); this replaces the Red Hat Linux derived patch.
- Minor man page fixes.

* Wed May 30 2001 Solar Designer <solar-at-owl.openwall.com>
- Ensure the umask is no less restrictive than 022.

* Sat Jan 06 2001 Solar Designer <solar-at-owl.openwall.com>
- Corrected the use of "--" in the startup script.

* Fri Dec 15 2000 Solar Designer <solar-at-owl.openwall.com>
- Changed the default xinetd.conf.
- Startup script cleanups.
- Restart after package upgrades in an owl-startup compatible way.

* Mon Dec 11 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import
- xinetd.init -> owl-startup
- 2.1.8.9pre13

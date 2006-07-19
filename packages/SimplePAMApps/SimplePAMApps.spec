# $Owl: Owl/packages/SimplePAMApps/SimplePAMApps.spec,v 1.47 2006/07/19 22:48:16 solar Exp $

Summary: Simple PAM-based Applications.
Name: SimplePAMApps
Version: 0.60
Release: owl30
License: BSD or GPL
Group: System Environment/Base
URL: http://www.kernel.org/pub/linux/libs/pam/
Source0: SimplePAMApps-0.60.tar.gz
Source1: login.pam
Source2: su.pam
Source3: passwd.pam
Source4: su.control
Source5: passwd.control
Patch0: SimplePAMApps-0.60-owl-alt-login.diff
Patch1: SimplePAMApps-0.60-owl-passwd.diff
Patch2: SimplePAMApps-0.60-owl-alt-su.diff
Patch3: SimplePAMApps-0.60-owl-alt-login-su-ut_id.diff
Patch4: SimplePAMApps-0.60-alt-owl-login-su-env.diff
Patch5: SimplePAMApps-0.60-alt-login-su-strip-argv0.diff
Patch6: SimplePAMApps-0.60-alt-owl-warnings.diff
Patch7: SimplePAMApps-0.60-owl-log.diff
Patch8: SimplePAMApps-0.60-owl-su-pam_acct_mgmt.diff
PreReq: owl-control >= 0.4, owl-control < 2.0
Requires: pam >= 0:0.80-owl2, pam_passwdqc >= 0.2, pam_mktemp, tcb
Provides: passwd
Obsoletes: passwd
BuildRequires: pam-devel
BuildRoot: /override/%name-%version

%description
These are applications for use with the Linux-PAM library.  This package
includes "login", "su", and "passwd".

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

%{expand:%%define optflags %optflags -Wall}

%build
touch conf/.ignore_age
CFLAGS="%optflags" ./configure --without-pniam --without-pwdb
%__make

%install
mkdir -p %buildroot/bin
install -m 700 pamapps/{login/login,su/su} %buildroot/bin/

mkdir -p %buildroot%_bindir
install -m 700 pamapps/passwd/passwd %buildroot%_bindir/

mkdir -p %buildroot%_mandir/man1
install -m 644 pamapps/{login/login.1,su/su.1,passwd/passwd.1} \
	%buildroot%_mandir/man1/

mkdir -p %buildroot/etc/pam.d
install -m 600 %_sourcedir/login.pam %buildroot/etc/pam.d/login
install -m 600 %_sourcedir/su.pam %buildroot/etc/pam.d/su
install -m 600 %_sourcedir/passwd.pam %buildroot/etc/pam.d/passwd

mkdir -p %buildroot/etc/control.d/facilities
install -m 700 %_sourcedir/su.control \
	%buildroot/etc/control.d/facilities/su
install -m 700 %_sourcedir/passwd.control \
	%buildroot/etc/control.d/facilities/passwd

%pre
if [ $1 -ge 2 ]; then
	%_sbindir/control-dump passwd su
fi

%post
if [ $1 -ge 2 ]; then
	%_sbindir/control-restore passwd su
	if [ -d /etc/tcb -a -f /etc/shadow-pre-tcb -a ! -e /etc/shadow -a \
	    "`%_sbindir/control passwd`" = traditional ]; then
		echo "Setting passwd(1) file modes for tcb"
		%_sbindir/control passwd tcb
		ls -l %_bindir/passwd
	fi
else
	%_sbindir/control passwd tcb
fi

%files
%defattr(-,root,root)
%doc Copyright Discussions
%attr(0700,root,root) /bin/login
%attr(0700,root,root) %verify(not mode group) /bin/su
%attr(0700,root,root) %verify(not mode group) %_bindir/passwd
%_mandir/man1/*
%config(noreplace) /etc/pam.d/login
%config(noreplace) %verify(not mode group) /etc/pam.d/passwd
%config(noreplace) %verify(not size md5 mtime) /etc/pam.d/su
/etc/control.d/facilities/*

%changelog
* Thu Jul 20 2006 Solar Designer <solar-at-owl.openwall.com> 0.60-owl30
- Changed the default control(8) setting for su from "wheelonly" to
"restricted" (this change affects new installs only).

* Fri May 05 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.60-owl29
- In su, do not ignore pam_acct_mgmt() return values except PAM_ACCT_EXPIRED
and PAM_NEW_AUTHTOK_REQD even if executed by root.

* Tue Dec 27 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.60-owl28
- Fixed build with Linux-PAM >= 0.81.
- Added passwd to provides list for compatibility.

* Sat Oct 29 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.60-owl27
- Changed PAM config files to include system-auth for PAM auth, account,
password and session management.

* Fri Sep 02 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.60-owl26
- Allow users with empty passwords to change their passwords.
- Stripped /lib/security/ prefix from module pathnames in PAM config files.

* Tue Aug 23 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.60-owl25
- Added system logger initialization, removed closelog() calls.

* Tue Jun 28 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.60-owl24
- Fixed compilation warnings.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.60-owl23
- Removed verification of permissions and group owner from su and passwd,
since we are controlling them through control.
- Cleaned up the spec.

* Sun Feb 08 2004 Solar Designer <solar-at-owl.openwall.com> 0.60-owl22
- In login and su, generate ut_id's consistently with libutempter and
openssh (patch from Dmitry Levin of ALT Linux).

* Thu Oct 16 2003 Solar Designer <solar-at-owl.openwall.com> 0.60-owl21
- Invoke "control passwd tcb" when updating old installs; the invocation
from owl-etc could have failed if the previous version of SimplePAMApps
was too old to even know of tcb as a possible setting for passwd.

* Thu May 29 2003 Solar Designer <solar-at-owl.openwall.com> 0.60-owl20
- write_to=tcb
- passwd(1) file modes now default to tcb.

* Thu Apr 17 2003 Solar Designer <solar-at-owl.openwall.com> 0.60-owl19
- Pass prefix= and count= to pam_tcb also for authentication such that it
can use this information to reduce timing leaks.

* Tue Apr 15 2003 Solar Designer <solar-at-owl.openwall.com> 0.60-owl18
- Imported ALT Linux patches, most importantly replacing command line parsing
in su, -- should now better match the behavior of other implementations.

* Sun Nov 03 2002 Solar Designer <solar-at-owl.openwall.com>
- Dump/restore the owl-control settings for passwd and su on package upgrades.
- Support "traditional" and "tcb" settings for permissions on /usr/bin/passwd
and /etc/pam.d/passwd.
- Keep passwd and su at mode 700 ("restricted") in the package, but default
them to "traditional" and "wheelonly", respectively, in %post when the package
is first installed.  This avoids a race and fail-open behavior.

* Thu Aug 22 2002 Solar Designer <solar-at-owl.openwall.com>
- Use pam_motd with login.

* Sun Mar 24 2002 Solar Designer <solar-at-owl.openwall.com>
- Group: System Environment/Base

* Fri Mar 01 2002 Solar Designer <solar-at-owl.openwall.com>
- Pick the best match utmp entry to replace when ut_id's don't match; if
that was the case, leave ut_id at what it was in utmp such that the entry
may be manipulated with pututline(3).

* Mon Feb 04 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.
- Use the _mandir macro.

* Mon Nov 19 2001 Solar Designer <solar-at-owl.openwall.com>
- Use (the recently patched version of) pam_lastlog with login.
- login: treat all PAM errors except PAM_NEW_AUTHTOK_REQD in the same way to
reduce information leaks.
- login: only chdir to the user's home directory after becoming the user.
- su: don't set a fail delay (it made very little sense and may be enabled
from within a PAM module anyway).
- Re-arranged the patches such that we now have one patch file per program.

* Fri Nov 16 2001 Solar Designer <solar-at-owl.openwall.com>
- Use pam_tcb.
- Dropped outdated documentation.

* Sun Apr 01 2001 Solar Designer <solar-at-owl.openwall.com>
- Use pam_limits with login and su.
- passwd: line-buffer stdout.
- passwd: don't require an utmp entry even when run on a tty.

* Mon Mar 19 2001 Solar Designer <solar-at-owl.openwall.com>
- passwd: don't require a tty.
- passwd.pam and su.pam: "nodelay" for pam_pwdb.

* Wed Dec 20 2000 Solar Designer <solar-at-owl.openwall.com>
- Use pam_mktemp.

* Sun Oct 29 2000 Solar Designer <solar-at-owl.openwall.com>
- su: don't require that the tty can be determined when started by root.
- su: don't require that getlogin() works to set PAM_RUSER.
- #include <stdarg.h> in su.c (was needed, but missing).

* Fri Sep 22 2000 Solar Designer <solar-at-owl.openwall.com>
- Make use of the new pam_passwdqc option: min=99,... -> min=disabled,...

* Sat Sep 16 2000 Solar Designer <solar-at-owl.openwall.com>
- Use RPM_OPT_FLAGS correctly.

* Wed Aug 23 2000 Solar Designer <solar-at-owl.openwall.com>
- %%config(noreplace) for /etc/pam.d files.

* Fri Aug 11 2000 Solar Designer <solar-at-owl.openwall.com>
- Added owl-control support for su and passwd.

* Sun Jul 09 2000 Solar Designer <solar-at-owl.openwall.com>
- Imported this spec file from SimplePAMApps-0.56-2.src.rpm and changed it
so heavily that there isn't much left.
- Added a bugfix patch for passwd and a bugfix and security patch for
login.  (In fact, login needs to be re-coded.)
- login can now obtain the username from LOGNAME when started as root (not
SUID), to be used by getty's.

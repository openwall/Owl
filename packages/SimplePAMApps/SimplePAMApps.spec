# $Id: Owl/packages/SimplePAMApps/SimplePAMApps.spec,v 1.15 2001/11/16 03:09:22 solar Exp $

Summary: Simple PAM-based Applications.
Name: SimplePAMApps
Version: 0.60
Release: 12owl
License: BSD or GPL
Group: Utilities/System
URL: http://www.kernel.org/pub/linux/libs/pam/
Source0: SimplePAMApps-0.60.tar.gz
Source1: login.pam
Source2: su.pam
Source3: passwd.pam
Source4: su.control
Source5: passwd.control
Patch0: SimplePAMApps-0.60-owl-passwd-strerror.diff
Patch1: SimplePAMApps-0.60-owl-login.diff
Patch2: SimplePAMApps-0.60-owl-su-no-tty.diff
Patch3: SimplePAMApps-0.60-owl-stdarg.diff
Patch4: SimplePAMApps-0.60-owl-passwd-no-tty.diff
Requires: pam, tcb, pam_passwdqc >= 0.2, pam_mktemp, owl-control < 2.0
Obsoletes: passwd
BuildRoot: /override/%{name}-%{version}

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

%build
touch conf/.ignore_age
CFLAGS="$RPM_OPT_FLAGS -Wall" ./configure
make

%install
mkdir -p $RPM_BUILD_ROOT/bin
install -m 700 pamapps/{login/login,su/su} $RPM_BUILD_ROOT/bin/

mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m 700 pamapps/passwd/passwd $RPM_BUILD_ROOT/usr/bin/

mkdir -p $RPM_BUILD_ROOT/usr/man/man1
install -m 0644 pamapps/{login/login.1,su/su.1,passwd/passwd.1} \
	$RPM_BUILD_ROOT/usr/man/man1/

mkdir -p $RPM_BUILD_ROOT/etc/pam.d
install -m 600 %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/login
install -m 600 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/su
install -m 600 %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/passwd

mkdir -p $RPM_BUILD_ROOT/etc/control.d/facilities
install -m 700 %{SOURCE4} $RPM_BUILD_ROOT/etc/control.d/facilities/su
install -m 700 %{SOURCE5} $RPM_BUILD_ROOT/etc/control.d/facilities/passwd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc Copyright Discussions
%attr(0700,root,root) /bin/login
/usr/man/man1/login.1*
%config(noreplace) /etc/pam.d/login
%attr(4710,root,wheel) /bin/su
/usr/man/man1/su.1*
%config(noreplace) /etc/pam.d/su
%attr(4711,root,root) /usr/bin/passwd
/usr/man/man1/passwd.1*
%config(noreplace) /etc/pam.d/passwd
/etc/control.d/facilities/su
/etc/control.d/facilities/passwd

%changelog
* Fri Nov 16 2001 Solar Designer <solar@owl.openwall.com>
- Use pam_tcb.
- Dropped outdated documentation.

* Sun Apr 01 2001 Solar Designer <solar@owl.openwall.com>
- Use pam_limits with login and su.
- passwd: line-buffer stdout.
- passwd: don't require an utmp entry even when run on a tty.

* Mon Mar 19 2001 Solar Designer <solar@owl.openwall.com>
- passwd: don't require a tty.
- passwd.pam and su.pam: "nodelay" for pam_pwdb.

* Wed Dec 20 2000 Solar Designer <solar@owl.openwall.com>
- Use pam_mktemp.

* Sun Oct 29 2000 Solar Designer <solar@owl.openwall.com>
- su: don't require that the tty can be determined when started by root.
- su: don't require that getlogin() works to set PAM_RUSER.
- #include <stdarg.h> in su.c (was needed, but missing).

* Fri Sep 22 2000 Solar Designer <solar@owl.openwall.com>
- Make use of the new pam_passwdqc option: min=99,... -> min=disabled,...

* Sat Sep 16 2000 Solar Designer <solar@owl.openwall.com>
- Use RPM_OPT_FLAGS correctly.

* Wed Aug 23 2000 Solar Designer <solar@owl.openwall.com>
- %config(noreplace) for /etc/pam.d files.

* Fri Aug 11 2000 Solar Designer <solar@owl.openwall.com>
- Added owl-control support for su and passwd.

* Sun Jul 09 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file from SimplePAMApps-0.56-2.src.rpm and changed it
so heavily that there isn't much left.
- Added a bugfix patch for passwd and a bugfix and security patch for
login.  (In fact, login needs to be re-coded.)
- login can now obtain the username from LOGNAME when started as root (not
SUID), to be used by getty's.

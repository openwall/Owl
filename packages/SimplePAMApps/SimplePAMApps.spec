# $Id: Owl/packages/SimplePAMApps/SimplePAMApps.spec,v 1.6 2000/09/22 03:24:12 solar Exp $

Summary: Simple PAM-based Applications
Name: SimplePAMApps
Version: 0.60
Release: 5owl
Copyright: BSD or GNU GPL
Group: Utilities/System
Source0: SimplePAMApps-0.60.tar.gz
Source1: login.pam
Source2: su.pam
Source3: passwd.pam
Source4: su.control
Source5: passwd.control
Patch0: SimplePAMApps-0.60-owl-passwd-strerror.diff
Patch1: SimplePAMApps-0.60-owl-login.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: pam >= 0.58, pam_passwdqc >= 0.2, owl-control < 2.0
URL: http://parc.power.net/morgan/Linux-PAM/index.html

%description
These are applications for use with the Linux-PAM library.  This package
includes "login", "su", and "passwd".

%prep
%setup -q
%patch0 -p1
%patch1 -p1

echo Checking distribution
make check

%build
touch conf/.ignore_age
CFLAGS="$RPM_OPT_FLAGS -Wall" ./configure
make

%install
mkdir -p $RPM_BUILD_ROOT/bin
install -m 755 pamapps/login/login $RPM_BUILD_ROOT/bin
install -m 755 pamapps/su/su $RPM_BUILD_ROOT/bin

mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m 755 pamapps/passwd/passwd $RPM_BUILD_ROOT/usr/bin

strip $RPM_BUILD_ROOT/bin/* $RPM_BUILD_ROOT/usr/bin/*

mkdir -p $RPM_BUILD_ROOT/usr/man/man1
install -m 0444 pamapps/login/login.1 $RPM_BUILD_ROOT/usr/man/man1
install -m 0444 pamapps/su/su.1 $RPM_BUILD_ROOT/usr/man/man1
install -m 0444 pamapps/passwd/passwd.1 $RPM_BUILD_ROOT/usr/man/man1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/*

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
%doc pgp.keys.asc Copyright conf/pam.conf conf/pam.d/
%doc README CHANGELOG* NOTES.su Discussions

%changelog
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

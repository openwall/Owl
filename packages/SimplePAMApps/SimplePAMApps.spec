# $Id: Owl/packages/SimplePAMApps/SimplePAMApps.spec,v 1.2 2000/07/16 14:10:02 solar Exp $

Summary: Simple PAM-based Applications
Name: SimplePAMApps
Version: 0.60
Release: 2owl
Copyright: BSD or GNU GPL
Group: Utilities/System
Source0: SimplePAMApps-0.60.tar.gz
Source1: login.pam
Source2: su.pam
Source3: passwd.pam
Patch0: SimplePAMApps-0.60-owl-passwd-strerror.diff
Patch1: SimplePAMApps-0.60-owl-login.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: pam >= 0.58 pam_passwdqc
URL: http://parc.power.net/morgan/Linux-PAM/index.html

%description
These are applications for use with the Linux-PAM library.  This package
includes "login", "su", and "passwd".

%prep
rm -rf $RPM_BUILD_ROOT/*

%setup -q
%patch0 -p1
%patch1 -p1

echo Checking distribution
make check

%build
touch conf/.ignore_age
./configure
make COPTFLAGS="$RPM_OPT_FLAGS" WANT_PWDB=no

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

%files
%defattr(-,root,root)
%attr(0700,root,root) /bin/login
/usr/man/man1/login.1*
/etc/pam.d/login
%attr(4711,root,root) /bin/su
/usr/man/man1/su.1*
/etc/pam.d/su
%attr(4711,root,root) /usr/bin/passwd
/usr/man/man1/passwd.1*
/etc/pam.d/passwd
%doc pgp.keys.asc Copyright conf/pam.conf conf/pam.d/
%doc README CHANGELOG* NOTES.su Discussions

%changelog
* Sun Jul  9 2000 Solar Designer <solar@false.com>
- Imported this spec file from SimplePAMApps-0.56-2.src.rpm and changed it
so heavily that there isn't much left.
- Added a bugfix patch for passwd and a bugfix and security patch for
login.  (In fact, login needs to be re-coded.)
- login can now obtain the username from LOGNAME when started as root (not
SUID), to be used by getty's.

# $Id: Owl/packages/pam/pam.spec,v 1.4 2000/08/07 23:30:20 solar Exp $

Summary: A security tool which provides authentication for applications.
Name: pam
Version: 0.72
Release: 10owl
Copyright: GPL or BSD
Group: System Environment/Base
Source0: pam-redhat-%{version}.tar.gz
Source1: other.pamd
Patch0: pam-0.72-owl-pam_pwdb-hack.diff
Patch1: pam-0.72-owl-pam_pwdb-expiration.diff
Patch2: pam-0.72-owl-no-cracklib.diff
Patch3: pam-0.72-owl-install-no-root.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: pwdb >= 0.54-2, initscripts >= 3.94
Obsoletes: pamconfig
Url: http://www.us.kernel.org/pub/linux/libs/pam/index.html

%description
PAM (Pluggable Authentication Modules) is a system security tool
which allows system administrators to set authentication policy
without having to recompile programs which do authentication.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
ln -sf defs/redhat.defs default.defs

%build
touch .freezemake
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/include/security
mkdir -p $RPM_BUILD_ROOT/lib/security
make install FAKEROOT=$RPM_BUILD_ROOT LDCONFIG=:
rm -f $RPM_BUILD_ROOT/lib/security/pam_console.so
install -m 644 libpamc/include/security/pam_client.h $RPM_BUILD_ROOT/usr/include/security
install -d -m 755 $RPM_BUILD_ROOT/etc/pam.d
install -m 644 other.pamd $RPM_BUILD_ROOT/etc/pam.d/other
# make sure the modules built...
[ -f $RPM_BUILD_ROOT/lib/security/pam_deny.so ] || {
  echo "You have LITTLE or NOTHING in your /lib/security directory:"
  echo $RPM_BUILD_ROOT/lib/security/*
  echo ""
  echo "Fix it before you install this package, while you still can!"
  exit 1
}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir /etc/pam.d
%config /etc/pam.d/other
%doc Copyright
%doc doc/html doc/ps doc/txts
%doc doc/specs/rfc86.0.txt
/lib/libpam.so.0.*
/lib/libpam.so
/lib/libpam_misc.so.0.*
/lib/libpam_misc.so
/lib/libpam_misc.a
/usr/include/security/*.h
/sbin/*
/lib/security
%config /etc/security/access.conf
%config /etc/security/time.conf
%config /etc/security/group.conf
%config /etc/security/limits.conf
%config /etc/security/pam_env.conf
/usr/man/man5/*
/usr/man/man8/*

%changelog
* Tue Aug 08 2000 Solar Designer <solar@owl.openwall.com>
- Removed pam_console and its related files.

* Sun Jul 16 2000 Solar Designer <solar@owl.openwall.com>
- Added a password expiration bugfix for pam_pwdb.

* Sun Jul 09 2000 Solar Designer <solar@owl.openwall.com>
- Added installation of pam_client.h

* Sat Jul 08 2000 Solar Designer <solar@owl.openwall.com>
- Imported from RH.
- Ported the Owl pam_pwdb patch from original Linux-PAM-0.72.
- Disabled pam_cracklib as it's to be replaced with pam_passwdqc (not
a part of this package).

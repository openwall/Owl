# $Id: Owl/packages/pam/pam.spec,v 1.12 2001/05/04 23:44:04 solar Exp $

Summary: A security tool which provides authentication for applications.
Name: pam
Version: 0.72
Release: 13owl
Copyright: GPL or BSD
Group: System Environment/Base
Source0: pam-redhat-%{version}.tar.gz
Source1: other.pamd
Patch0: pam-0.72-owl-pam_pwdb-hack.diff
Patch1: pam-0.72-owl-pam_pwdb-expiration.diff
Patch2: pam-0.72-owl-pwdb_chkpwd.diff
Patch3: pam-0.72-owl-no-cracklib.diff
Patch4: pam-0.72-owl-install-no-root.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
BuildRequires: glibc-devel >= 2.1.3-13owl
Requires: glibc >= 2.1.3-13owl
Requires: pwdb >= 0.61-1owl
Obsoletes: pamconfig
Url: http://www.us.kernel.org/pub/linux/libs/pam/index.html

%description
PAM (Pluggable Authentication Modules) is a system security tool
which allows system administrators to set authentication policy
without having to recompile programs which do authentication.

# Use %optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%prep
%setup -q
rm -rf modules/pam_console
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
ln -sf defs/redhat.defs default.defs

%build
touch .freezemake
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/lib/security
mkdir -p $RPM_BUILD_ROOT/usr/{include/security,man/man3,man/man8}
make install FAKEROOT=$RPM_BUILD_ROOT LDCONFIG=:
test -f $RPM_BUILD_ROOT/lib/security/pam_deny.so || exit 1
install -m 644 libpamc/include/security/pam_client.h $RPM_BUILD_ROOT/usr/include/security

mkdir $RPM_BUILD_ROOT/sbin/chkpwd.d
mv $RPM_BUILD_ROOT/sbin/*_chkpwd $RPM_BUILD_ROOT/sbin/chkpwd.d
ln -s /sbin/chkpwd.d/pwdb_chkpwd $RPM_BUILD_ROOT/sbin/pwdb_chkpwd

install -d -m 755 $RPM_BUILD_ROOT/etc/pam.d
install -m 644 other.pamd $RPM_BUILD_ROOT/etc/pam.d/other

install -m 644 doc/man/*.3 $RPM_BUILD_ROOT/usr/man/man3
install -m 644 doc/man/*.8 $RPM_BUILD_ROOT/usr/man/man8
gzip -9nf $RPM_BUILD_ROOT/usr/man/man[38]/*

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- shadow-utils
grep -q '^shadow:[^:]*:42:' /etc/group && \
	chgrp shadow /sbin/chkpwd.d/pwdb_chkpwd && \
	chmod 2711 /sbin/chkpwd.d/pwdb_chkpwd

%pre
grep ^chkpwd: /etc/group &>/dev/null || groupadd -g 163 chkpwd

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
%attr(710,root,chkpwd) %dir /sbin/chkpwd.d/
%attr(700,root,root) /sbin/chkpwd.d/pwdb_chkpwd
/sbin/pwdb_chkpwd
/lib/security
%config /etc/security/access.conf
%config /etc/security/time.conf
%config /etc/security/group.conf
%config /etc/security/limits.conf
%config /etc/security/pam_env.conf
/usr/man/man3/*
/usr/man/man8/*

%changelog
* Sat May 05 2001 Solar Designer <solar@owl.openwall.com>
- Minor updates to use crypt_blowfish interfaces in the now officially
documented ways.

* Thu Mar 08 2001 Solar Designer <solar@owl.openwall.com>
- Patched some of the pam_pwdb/pwdb_chkpwd interaction problems.
- Install pwdb_chkpwd SGID shadow, but restricted to group chkpwd.

* Sat Sep 16 2000 Solar Designer <solar@owl.openwall.com>
- %optflags_lib support.

* Sat Aug 26 2000 Solar Designer <solar@owl.openwall.com>
- Disabled building of pam_console entirely to avoid the dependency on glib.
- Removed the (bogus?) dependency on initscripts from this spec file.
- Added packaging of man pages.

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

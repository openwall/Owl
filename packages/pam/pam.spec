# $Id: Owl/packages/pam/pam.spec,v 1.15 2001/10/07 07:46:29 solar Exp $

Summary: A security tool which provides authentication for applications.
Name: pam
Version: 0.75
Release: 10owl
License: GPL or BSD
Group: System Environment/Base
Source0: pam-redhat-%{version}-10.tar.bz2
Source1: pam_listfile.c
Patch0: pam-0.75-owl-pam_pwdb.diff
Patch1: pam-0.75-owl-pam_chroot.diff
Patch2: pam-0.75-owl-no-cracklib.diff
Patch3: pam-0.75-alt-read_string.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
BuildRequires: glibc-devel >= 2.1.3-13owl
Requires: glibc >= 2.1.3-13owl
Requires: pwdb >= 0.61-1owl
URL: http://www.kernel.org/pub/linux/libs/pam/
 
%description
PAM (Pluggable Authentication Modules) is a system security tool
which allows system administrators to set authentication policy
without having to recompile programs which do authentication.

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%prep
%setup -q
rm -rf modules/pam_{console,cracklib}
rm -f modules/pam_pwdb/{md5*,bigcrypt.*}
cp $RPM_SOURCE_DIR/pam_listfile.c modules/pam_listfile/
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
for f in modules/pam_*/README; do
	d="${f%/*}"
	install -p -m 644 "$f" "doc/txts/README.${d##*/}"
done
autoconf

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC" \
./configure \
	--prefix=/ \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--enable-static-libpam \
	--enable-fakeroot=$RPM_BUILD_ROOT
make

%install
rm -rf $RPM_BUILD_ROOT
make install

install -m 644 modules/pam_chroot/chroot.conf $RPM_BUILD_ROOT/etc/security/

mkdir $RPM_BUILD_ROOT/sbin/chkpwd.d
mv $RPM_BUILD_ROOT/sbin/*_chkpwd $RPM_BUILD_ROOT/sbin/chkpwd.d/
ln -s /sbin/chkpwd.d/pwdb_chkpwd $RPM_BUILD_ROOT/sbin/pwdb_chkpwd

mkdir -m 755 $RPM_BUILD_ROOT/etc/pam.d
install -m 644 other.pamd $RPM_BUILD_ROOT/etc/pam.d/other

install -m 644 doc/man/*.3 $RPM_BUILD_ROOT%{_mandir}/man3/
install -m 644 doc/man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8/

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
%config(noreplace) /etc/pam.d/other
#%config(noreplace) /etc/pam.d/system-auth
%doc Copyright
%doc doc/{html,ps,txts}
%doc doc/specs/rfc86.0.txt
/lib/libpam.so.*
/lib/libpam_misc.so.*

%attr(710,root,chkpwd) %dir /sbin/chkpwd.d/
%attr(700,root,root) /sbin/chkpwd.d/pwdb_chkpwd
/sbin/pwdb_chkpwd

/sbin/pam_tally

%dir /lib/security
/lib/security/pam_access.so
/lib/security/pam_chroot.so
/lib/security/pam_deny.so
/lib/security/pam_env.so
/lib/security/pam_filter.so
/lib/security/pam_ftp.so
/lib/security/pam_group.so
/lib/security/pam_issue.so
/lib/security/pam_lastlog.so
/lib/security/pam_limits.so
/lib/security/pam_listfile.so
/lib/security/pam_localuser.so
/lib/security/pam_mail.so
/lib/security/pam_mkhomedir.so
/lib/security/pam_motd.so
/lib/security/pam_nologin.so
/lib/security/pam_permit.so
/lib/security/pam_pwdb.so
/lib/security/pam_rhosts_auth.so
/lib/security/pam_rootok.so
/lib/security/pam_securetty.so
/lib/security/pam_shells.so
/lib/security/pam_stack.so
/lib/security/pam_stress.so
/lib/security/pam_tally.so
/lib/security/pam_time.so
/lib/security/pam_unix.so
/lib/security/pam_unix_acct.so
/lib/security/pam_unix_auth.so
/lib/security/pam_unix_passwd.so
/lib/security/pam_unix_session.so
/lib/security/pam_userdb.so
/lib/security/pam_warn.so
/lib/security/pam_wheel.so
/lib/security/pam_xauth.so
/lib/security/pam_filter

%dir /etc/security
%attr(640,root,wheel) %config(noreplace) /etc/security/access.conf
%attr(640,root,wheel) %config(noreplace) /etc/security/chroot.conf
%attr(640,root,wheel) %config(noreplace) /etc/security/group.conf
%attr(640,root,wheel) %config(noreplace) /etc/security/limits.conf
%attr(644,root,root) %config(noreplace) /etc/security/pam_env.conf
%attr(640,root,wheel) %config(noreplace) /etc/security/time.conf
%{_mandir}/man8/*

/lib/libpam.so
/lib/libpam_misc.so
/lib/libpam_misc.a
/usr/include/security/
%{_mandir}/man3/*

%changelog
* Sun Oct 07 2001 Solar Designer <solar@owl.openwall.com>
- Updated to Red Hat's 0.75-10 plus our usual patches.
- Replaced pam_listfile with Michael Tokarev's implementation (see
http://archives.neohapsis.com/archives/pam-list/2000-12/0084.html).
- Patched the new pam_chroot to catch the most common misuses which would
result in a security problem, updated its README and example configuration
file to discourage such misuses.

* Mon Jul 30 2001 Solar Designer <solar@owl.openwall.com>
- Fixed a double-free bug in pam_pwdb which caused it to segfault after
successful password changes in some cases.  The bug was specific to Owl.

* Sat May 05 2001 Solar Designer <solar@owl.openwall.com>
- Minor updates to use crypt_blowfish interfaces in the now officially
documented ways.

* Thu Mar 08 2001 Solar Designer <solar@owl.openwall.com>
- Patched some of the pam_pwdb/pwdb_chkpwd interaction problems.
- Install pwdb_chkpwd SGID shadow, but restricted to group chkpwd.

* Sat Sep 16 2000 Solar Designer <solar@owl.openwall.com>
- optflags_lib support.

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

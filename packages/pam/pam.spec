# $Id: Owl/packages/pam/pam.spec,v 1.31 2003/10/29 16:28:17 solar Exp $

Summary: Pluggable Authentication Modules.
Name: pam
Version: 0.75
Release: owl21
%define rh_version %version-10
License: GPL or BSD
Group: System Environment/Base
URL: http://www.kernel.org/pub/linux/libs/pam/
Source0: pam-redhat-%rh_version.tar.bz2
Source1: pam_listfile.c
Patch0: pam-0.75-owl-tmp.diff
Patch1: pam-0.75-owl-pam_get_user-cache-failures.diff
Patch2: pam-0.75-owl-pam_dispatch-debugging.diff
Patch3: pam-0.75-owl-man.diff
Patch9: pam-0.75-alt-read_string.diff
Patch10: pam-0.75-owl-pam_pwdb.diff
Patch11: pam-0.75-owl-pam_chroot.diff
Patch12: pam-0.75-owl-pam_lastlog.diff
Patch13: pam-0.75-owl-pam_securetty.diff
Patch14: pam-0.75-owl-pam_limits.diff
Patch15: pam-0.75-owl-pam_motd.diff
Patch16: pam-0.75-owl-pam_wheel.diff
Patch20: pam-0.75-owl-no-cracklib.diff
PreReq: /sbin/ldconfig
Requires: glibc-crypt_blowfish, pwdb >= 0.61-1owl
# Just to make sure noone misses pam_unix, which is now provided by tcb
Requires: tcb >= 0.9.5
BuildRequires: glibc-crypt_blowfish-devel
BuildRoot: /override/%name-%version

%description
Linux-PAM (Pluggable Authentication Modules for Linux) is a suite of
libraries that enable the local system administrator to choose how
PAM-aware applications authenticate users, without having to recompile
those applications.

%package devel
Summary: Libraries and header files for developing applications with PAM.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
This package contains static Linux-PAM libraries and header files used
for building both PAM-aware applications and PAM modules.

%package doc
Summary: The Linux-PAM documentation.
Group: Documentation

%description doc
This package contains the main Linux-PAM documentation in text, HTML, and
PostScript formats.

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%prep
%setup -q
rm -r modules/pam_{console,cracklib,unix}
rm modules/pam_pwdb/{md5*,bigcrypt.*}
cp $RPM_SOURCE_DIR/pam_listfile.c modules/pam_listfile/
ln -s ../../../libpam_misc/pam_misc.h libpam/include/security/pam_misc.h
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch20 -p1
mkdir modules/READMEs
for f in modules/pam_*/README; do
	d="${f%/*}"
	install -p -m 644 "$f" "modules/READMEs/README.${d##*/}"
done
autoconf

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC" \
./configure \
	--prefix=/ \
	--sysconfdir=%_sysconfdir \
	--infodir=%_infodir \
	--mandir=%_mandir \
	--enable-static-libpam \
	--enable-fakeroot=$RPM_BUILD_ROOT
# List things to make explicitly to not make doc (corrupting the
# pre-compiled docs if we don't have the tools).
make modules libpam libpamc libpam_misc

%install
rm -rf $RPM_BUILD_ROOT
make install THINGSTOMAKE='modules libpam libpamc libpam_misc'

install -m 644 modules/pam_chroot/chroot.conf $RPM_BUILD_ROOT/etc/security/

mkdir -p $RPM_BUILD_ROOT/%_libdir
mv $RPM_BUILD_ROOT/lib/*.a $RPM_BUILD_ROOT/%_libdir/

mkdir -m 755 $RPM_BUILD_ROOT/etc/pam.d
install -m 644 other.pamd $RPM_BUILD_ROOT/etc/pam.d/other

mkdir -p $RPM_BUILD_ROOT%_mandir/man{3,5,8}
install -m 644 doc/man/*.3 $RPM_BUILD_ROOT%_mandir/man3/
install -m 644 doc/man/*.5 $RPM_BUILD_ROOT%_mandir/man5/
install -m 644 doc/man/*.8 $RPM_BUILD_ROOT%_mandir/man8/

rm -f doc/ps/missfont.log
gzip -9nf doc/ps/*.ps
gzip -9nf doc/txts/*.txt

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- shadow-utils
grep -q '^shadow:[^:]*:42:' /etc/group && \
	chgrp shadow %_libexecdir/chkpwd/pwdb_chkpwd && \
	chmod 2711 %_libexecdir/chkpwd/pwdb_chkpwd
grep -q ^chkpwd: /etc/group || groupadd -g 163 chkpwd
chgrp chkpwd %_libexecdir/chkpwd && chmod 710 %_libexecdir/chkpwd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc Copyright
%doc modules/READMEs/*

%dir /etc/pam.d
%config(noreplace) /etc/pam.d/other
#%config(noreplace) /etc/pam.d/system-auth

/lib/libpam.so.*
/lib/libpamc.so.*
/lib/libpam_misc.so.*

%attr(700,root,root) %dir %_libexecdir/chkpwd
%attr(700,root,root) %_libexecdir/chkpwd/pwdb_chkpwd

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

%_mandir/man5/*
%_mandir/man8/*

%files devel
%defattr(-,root,root)
/lib/libpam.so
/lib/libpamc.so
/lib/libpam_misc.so
%_libdir/libpam.a
%_libdir/libpamc.a
%_libdir/libpam_misc.a
/usr/include/security/
%_mandir/man3/*

%files doc
%defattr(-,root,root)
%doc doc/{html,ps,txts}
%doc doc/specs/rfc86.0.txt

%changelog
* Wed Oct 29 2003 Solar Designer <solar@owl.openwall.com> 0.75-owl21
- Require glibc-crypt_blowfish-devel for builds.
- Dropped the obsolete "Provides: pam <= 0.75-14owl" tag which was needed
during our transition to the new Release numbering scheme.

* Sun Aug 10 2003 Solar Designer <solar@owl.openwall.com> 0.75-owl20
- pam_limits: don't invoke setrlimit(2) on limits which are not set
explicitly as simply resetting RLIMIT_FSIZE to what appears to be its
current value may decrease the actual limit with LFS.

* Tue Jul 22 2003 Solar Designer <solar@owl.openwall.com> 0.75-owl19
- Patched pam_wheel to never rely on getlogin(3).

* Thu Aug 22 2002 Solar Designer <solar@owl.openwall.com> 0.75-owl18
- Patched pam_motd to behave on errors.

* Sun Jul 28 2002 Solar Designer <solar@owl.openwall.com>
- Moved pam.d and pam.conf man pages to section 5 where they belong.

* Sat Jul 06 2002 Solar Designer <solar@owl.openwall.com>
- pam_limits: support stacking for account management (as well as for
session setup), be fail-close on configuration file reads, report the
"too many logins" via PAM conversation rather than direct printf(3).

* Sun May 19 2002 Solar Designer <solar@owl.openwall.com>
- Moved the chkpwd directory to /usr/libexec.

* Mon Feb 04 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Mon Nov 19 2001 Solar Designer <solar@owl.openwall.com>
- Cache pam_get_user() failures such that the conversation function isn't
called multiple times with the same prompt if pam_get_user() fails and is
used by more than one module in the stack.
- pam_lastlog: bug and reliability fixes (but the module is still dirty),
"nowtmp" option to disable logging to wtmp when the program does that.
- pam_securetty: be fail-close on user lookups, always log failures (not
just with "debug").

* Fri Nov 16 2001 Solar Designer <solar@owl.openwall.com>
- Use the trigger on shadow-utils for possibly creating and making use of
group chkpwd, not just for group shadow.  This makes no difference on Owl
as either the groups are provided by owl-etc (on new installs) or groupadd
is already available when this package is installed, but may be useful on
hybrid systems.

* Thu Nov 15 2001 Solar Designer <solar@owl.openwall.com>
- No longer build pam_unix, the tcb package will provide compatibility
symlinks instead.
- /tmp fixes in the documentation (don't suggest bad practices).

* Sun Oct 07 2001 Solar Designer <solar@owl.openwall.com>
- Updated to Red Hat's 0.75-10 plus our usual patches.
- Replaced pam_listfile with Michael Tokarev's implementation (see
http://archives.neohapsis.com/archives/pam-list/2000-12/0084.html).
- Patched the new pam_chroot to catch the most common misuses which would
result in a security problem, updated its README and example configuration
file to discourage such misuses.
- Moved development libraries and header files into a subpackage.
- Moved the main Linux-PAM documentation into a documentation subpackage.

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

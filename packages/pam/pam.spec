# $Id: Owl/packages/pam/pam.spec,v 1.40 2005/08/23 22:48:10 solar Exp $

Summary: Pluggable Authentication Modules.
Name: pam
Version: 0.80
Release: owl1
%define rh_version %version-1
License: GPL or BSD
Group: System Environment/Base
URL: http://www.kernel.org/pub/linux/libs/pam/
Source0: ftp://ftp.kernel.org/pub/linux/libs/pam/pre/library/Linux-PAM-%version.tar.bz2
Source1: ftp://ftp.kernel.org/pub/linux/libs/pam/pre/library/Linux-PAM-%version-docs.tar.bz2
Source2: pam-redhat-%rh_version.tar.bz2
Source3: pam_listfile.c
Source4: modules.map
Source5: other.pam
Patch0: Linux-PAM-0.80-cvs-20050728.diff
Patch1: Linux-PAM-0.80-owl-tmp.diff
Patch2: Linux-PAM-0.80-owl-pam_get_user-cache-failures.diff
Patch3: Linux-PAM-0.80-owl-man.diff
Patch4: Linux-PAM-0.80-owl-pam_lastlog.diff
Patch5: Linux-PAM-0.80-owl-pam_securetty.diff
Patch6: Linux-PAM-0.80-owl-pam_limits.diff
Patch7: Linux-PAM-0.80-owl-pam_motd.diff
Patch8: Linux-PAM-0.80-owl-pam_wheel.diff
Patch9: Linux-PAM-0.80-owl-configure.diff
Patch10: Linux-PAM-0.80-owl-pam_filter.diff
Patch11: Linux-PAM-0.80-owl-no-cracklib.diff
Patch12: Linux-PAM-0.80-owl-no-pwdb.diff
Patch13: Linux-PAM-0.80-owl-pammodutil-attribute.diff
Patch14: Linux-PAM-0.80-owl-log.diff
Patch15: Linux-PAM-0.80-owl-pam_mkhomedir.diff
Patch16: Linux-PAM-0.80-owl-converse.diff
Patch17: Linux-PAM-0.79-ibm-man.diff
PreReq: /sbin/ldconfig
Requires: glibc-crypt_blowfish
# Just to make sure noone misses pam_unix and pam_pwdb, which are now
# provided by tcb.
Requires: tcb >= 0.9.9
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

%prep
%setup -q -n Linux-PAM-%version -a2
%setup -qDT -n Linux-PAM-%version/doc -a1
%setup -qDT -n Linux-PAM-%version

%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1

# Remove unwanted modules.
rm -r modules/pam_{console,cracklib,debug,loginuid,postgresok,pwdb,radius,rps,selinux,timestamp,umask,unix}

install -pm644 %_sourcedir/pam_listfile.c modules/pam_listfile/

# Replace _pam_aconf.h with config.h
grep -FZl _pam_aconf.h modules/*/*.c |
	xargs -r0 sed -ie 's/_pam_aconf\.h/config.h/' --

# Use version script during build of pam modules.
install -pm644 %_sourcedir/modules.map modules/
find modules -type f -print0 |
	xargs -r0 grep -FlZ ' -o $@ $(LIBOBJD) ' |
	xargs -r0 sed -ie 's| -o \$@ \$(LIBOBJD) | -Wl,--version-script=../modules.map&|' --

mkdir modules/READMEs
for f in modules/pam_*/README; do
	d="${f%/*}"
	install -p -m 644 "$f" "modules/READMEs/README.${d##*/}"
done
autoconf

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%build
autoreconf -fisv
export ac_cv_lib_ndbm_dbm_store=no \
	ac_cv_lib_db_dbm_store=no \
	ac_cv_lib_selinux_getfilecon=no
%configure \
	--prefix=/ \
	--exec-prefix=/ \
	--libdir=/%_lib \
	--sbindir=/sbin \
	--enable-static-libpam \
	--disable-read-both-confs \
	--enable-fakeroot=%buildroot
%__make

%install
rm -rf %buildroot
%__make install

mkdir -p %buildroot/etc/security
install -m 644 modules/pam_chroot/chroot.conf %buildroot/etc/security/

# Relocate development libraries from /%_lib/ to %_libdir/.
mkdir -p %buildroot%_libdir
mv %buildroot/%_lib/*.*a %buildroot%_libdir/
/sbin/ldconfig -nv %buildroot/%_lib
for f in %buildroot/%_lib/*.so; do
	t=`objdump -p "$f" |awk '/SONAME/ {print $2}'`
	[ -n "$t" ]
	ln -s ../../%_lib/"$t" "%buildroot%_libdir/${f##*/}"
	rm -f "$f"
done

# Make sure that all modules are built.
>check.log
for d in modules/pam_*; do
	[ -d "$d" ] || continue
	m="${d##*/}"
	! ls -1 "%buildroot/%_lib/security/$m"*.so 2>/dev/null || continue
	echo "ERROR: $m module did not build." >&2
	echo "$m" >>check.log
done
! [ -s check.log ] || exit 1

# Make sure that no module exports symbols beyond standard set.
>check.log
for d in modules/pam_*; do
	[ -d "$d" ] || continue
	m="${d##*/}"
	readelf -Ws "%buildroot/%_lib/security/$m"*.so |
		grep -w GLOBAL |
		grep -Ewv 'UND|pam_sm_(acct_mgmt|authenticate|chauthtok|close_session|open_session|setcred)'  ||
			continue
	echo "ERROR: $m module exports symbol(s) beyond standard set." >&2
	echo "$m" >>check.log
done
! [ -s check.log ] || exit 1

# Make sure that no shared object has undefined symbols.
>check.log
for f in %buildroot/%_lib/lib*.so.0 %buildroot/%_lib/security/pam*.so; do
	LD_LIBRARY_PATH="%buildroot/%_lib" ldd -r "$f" 2>&1 >/dev/null |
		tee -a check.log
done
! [ -s check.log ] || exit 1

install -pD -m644 %_sourcedir/other.pam %buildroot/etc/pam.d/other

rm -f doc/ps/missfont.log
gzip -9nf doc/ps/*.ps
gzip -9nf doc/txts/*.txt

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
/lib/security/pam_rhosts_auth.so
/lib/security/pam_rootok.so
/lib/security/pam_securetty.so
/lib/security/pam_shells.so
/lib/security/pam_stack.so
/lib/security/pam_stress.so
/lib/security/pam_succeed_if.so
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
%_libdir/libpam.so
%_libdir/libpamc.so
%_libdir/libpam_misc.so
%_libdir/libpam.a
%_libdir/libpamc.a
%_libdir/libpam_misc.a
%_includedir/security/
%_mandir/man3/*

%files doc
%defattr(-,root,root)
%doc doc/{html,ps,txts}
%doc doc/specs/rfc86.0.txt

%changelog
* Tue Aug 23 2005 Dmitry V. Levin <ldv@owl.openwall.com> 0.80-owl1
- Updated Linux-PAM to 0.80.
- Updated pam-redhat to 0.80-1.
- Reviewed patches, removed obsolete ones, updated all the rest.
- No longer build pam_pwdb, the tcb package will provide compatibility
symlinks instead.
- Restricted list of global symbols exported by PAM modules to
standard set of six pam_sm_* functions.
- Changed modules logging to eliminate disunion in behaviour and
avoid openlog/closelog calls for each logging function invocation.
- Cleaned up conversation wrappers.
- Added pam_sm_acct_mgmt for pam_mkhomedir module.
- Implemented additional build sanity checks to ensure that all shared
objects meet certain requirements.

* Tue Jun 28 2005 Dmitry V. Levin <ldv@owl.openwall.com> 0.75-owl25
- Build this package without optimizations based on strict aliasing rules.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 0.75-owl24
- Removed permissions and group owner verify check for %_libexecdir/chkpwd
due to %%triggerin.
- Cleaned up the spec.

* Tue Feb 24 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 0.75-owl23
- Moved /lib/*.so to %_libdir where corresponding static archives live

* Thu Feb 19 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 0.75-owl22
- Created missing /etc/security directory

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

# $Owl: Owl/packages/pam/pam.spec,v 1.53 2009/08/28 08:02:21 ldv Exp $

Summary: Pluggable Authentication Modules.
Name: pam
Version: 1.1.0
Release: owl1
%define rh_version 0.99.10-1
License: GPLv2+ or BSD-style
Group: System Environment/Base
URL: http://www.kernel.org/pub/linux/libs/pam/
Source0: ftp://ftp.kernel.org/pub/linux/libs/pam/pre/library/Linux-PAM-%version.tar.bz2
Source1: ftp://ftp.kernel.org/pub/linux/libs/pam/pre/library/Linux-PAM-%version-docs.tar.bz2
Source2: pam-redhat-%rh_version.tar.bz2
Source3: pam_listfile.c
Source4: other.pam
Source5: system-auth.pam
Patch0: Linux-PAM-1.1.0-up-20090626-bug2809661.diff
Patch1: Linux-PAM-1.1.0-alt-const.diff
Patch2: Linux-PAM-1.1.0-owl-pam_limits-acct.diff
Patch3: Linux-PAM-1.1.0-alt-pam_mkhomedir-fixes.diff
Patch4: Linux-PAM-1.1.0-owl-pam_mkhomedir-acct.diff
Patch5: Linux-PAM-1.1.0-owl-pam_wheel-use_uid.diff
Patch6: Linux-PAM-1.1.0-alt-pam_xauth-check_acl.diff
Patch7: Linux-PAM-1.1.0-owl-pam_get_authtok.patch
Patch8: Linux-PAM-1.1.0-alt-pam_chroot.diff
Patch9: Linux-PAM-1.1.0-owl-pam_stack.diff
PreReq: /sbin/ldconfig
Requires: glibc-crypt_blowfish
# Just to make sure noone misses pam_unix and pam_pwdb, which are now
# provided by tcb.
Requires: tcb >= 0.9.9
BuildRequires: glibc-crypt_blowfish-devel
BuildRequires: automake, autoconf, bison, flex
BuildRequires: sed >= 4.1, db4-devel >= 4.2
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
This package contains the main Linux-PAM documentation in text, HTML,
and PostScript formats.

%package compat
Summary: PAM modules for backwards compatibility.
Group: System Environment/Base
Requires: %name = %version-%release

%description compat
This package contains PAM modules for backwards compatibility.

%prep
%setup -q -n Linux-PAM-%version -b1 -a2
mv pam-redhat-%rh_version/pam_chroot modules/

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

# Replace pam_listfile.
install -pm644 %_sourcedir/pam_listfile.c modules/pam_listfile/

# Include pam-redhat modules.
for d in stack chroot; do
	sed -i "s,modules/pam_xauth/Makefile ,&modules/pam_$d/Makefile ," configure*
	sed -i "s/ pam_xauth/& pam_$d/" modules/Makefile*
done

# Remove unwanted modules.
for d in cracklib debug loginuid keyinit namespace radius rps \
	 selinux sepermit timestamp tty_audit unix; do
	sed -i "s,modules/pam_$d/Makefile,," configure*
	sed -i "s/pam_$d //" modules/Makefile*
	sed -i "s/tst-pam_$d[0-9]* //" xtests/Makefile*
done

# Workaround old autotools.
touch aclocal.m4 Makefile.in config.h.in
sed -i 's,\(sys_lib_dlsearch_path_spec="/\)[^"]*"$,\1%_lib %_libdir",' configure

%define docdir %_docdir/pam-%version
# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%build
export ac_cv_lib_ndbm_dbm_store=no ac_cv_lib_db_dbm_store=no
%configure \
	--disable-audit \
	--disable-cracklib \
	--disable-nls \
	--disable-read-both-confs \
	--disable-prelude \
	--disable-rpath \
	--disable-selinux \
	--docdir=%docdir \
	--htmldir=%docdir/html \
	--includedir=%_includedir/security \
	--libdir=/%_lib \
	--sbindir=/sbin
%__make
%__make check

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot

mkdir -p %buildroot/etc/security
install -pm644 modules/pam_chroot/chroot.conf %buildroot/etc/security/

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
rm %buildroot{%_libdir,/%_lib/security}/*.la

# Make sure that all modules are built.
>check.log
for d in modules/pam_*; do
	[ -s "$d/Makefile" ] || continue
	m="${d##*/}"
	! ls -1 "%buildroot/%_lib/security/$m"*.so 2>/dev/null || continue
	echo "ERROR: $m module did not build." >&2
	echo "$m" >>check.log
done
! [ -s check.log ] || exit 1

# Make sure that no module exports symbols beyond standard set.
for f in %buildroot/%_lib/security/pam*.so; do
	readelf -Ws "$f" |
		grep -w GLOBAL |
		grep -Ewv 'UND|pam_sm_(acct_mgmt|authenticate|chauthtok|close_session|open_session|setcred)'  ||
			continue
	echo "ERROR: ${f##*/} exports symbol(s) beyond standard set." >&2
	echo "${f##*/}" >>check.log
done
! [ -s check.log ] || exit 1

# Make sure that no shared object has undefined symbols.
for f in %buildroot/%_lib/lib*.so.0 %buildroot/%_lib/security/pam*.so; do
	LD_LIBRARY_PATH="%buildroot/%_lib" ldd -r "$f" 2>&1 >/dev/null |
		tee -a check.log
done
! [ -s check.log ] || exit 1

# Make sure that none of the modules pull in threading libraries.
for f in %buildroot/%_lib/security/pam*.so; do
	# except pam_userdb
	[ "${f##*/}" != pam_userdb.so ] ||
		continue
	LD_LIBRARY_PATH="%buildroot/%_lib" ldd -r "$f" 2>&1 |
		fgrep -q libpthread ||
			continue
	echo "ERROR: ${f##*/} pulls in libpthread." >&2
	echo "${f##*/}" >>check.log
done
! [ -s check.log ] || exit 1

install -pD -m644 %_sourcedir/other.pam %buildroot/etc/pam.d/other
install -pD -m644 %_sourcedir/system-auth.pam %buildroot/etc/pam.d/system-auth

# Documentation
mkdir -p %buildroot%docdir/modules
for f in modules/pam_*/README; do
	d="${f%%/*}"
	[ -s "$d/Makefile" ] || continue
	install -pm644 "$f" "%buildroot%docdir/modules/${d##*/}"
done
install -pm644 AUTHORS NEWS ChangeLog CHANGELOG Copyright %buildroot%docdir/
find %buildroot%docdir/ -type f -size +4k \( -iname changelog -or -name \*.txt \) -print0 |
	xargs -r0 gzip -9nf --
rm %buildroot%docdir/*.pdf

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %docdir
%docdir/[ACNm]*

%dir /etc/pam.d
%config(noreplace) /etc/pam.d/other
%config(noreplace) /etc/pam.d/system-auth

/%_lib/libpam.so.*
/%_lib/libpamc.so.*
/%_lib/libpam_misc.so.*

/sbin/mkhomedir_helper
/sbin/pam_tally
/sbin/pam_tally2

%dir /%_lib/security
/%_lib/security/pam_access.so
/%_lib/security/pam_chroot.so
/%_lib/security/pam_deny.so
/%_lib/security/pam_echo.so
/%_lib/security/pam_env.so
/%_lib/security/pam_exec.so
/%_lib/security/pam_faildelay.so
/%_lib/security/pam_filter.so
/%_lib/security/pam_ftp.so
/%_lib/security/pam_group.so
/%_lib/security/pam_issue.so
/%_lib/security/pam_lastlog.so
/%_lib/security/pam_limits.so
/%_lib/security/pam_listfile.so
/%_lib/security/pam_localuser.so
/%_lib/security/pam_mail.so
/%_lib/security/pam_mkhomedir.so
/%_lib/security/pam_motd.so
/%_lib/security/pam_nologin.so
/%_lib/security/pam_permit.so
/%_lib/security/pam_pwhistory.so
/%_lib/security/pam_rhosts.so
/%_lib/security/pam_rootok.so
/%_lib/security/pam_securetty.so
/%_lib/security/pam_shells.so
/%_lib/security/pam_stress.so
/%_lib/security/pam_succeed_if.so
/%_lib/security/pam_tally.so
/%_lib/security/pam_tally2.so
/%_lib/security/pam_time.so
/%_lib/security/pam_umask.so
/%_lib/security/pam_userdb.so
/%_lib/security/pam_warn.so
/%_lib/security/pam_wheel.so
/%_lib/security/pam_xauth.so
/%_lib/security/pam_filter

%dir /etc/security
%attr(640,root,wheel) %config(noreplace) /etc/security/access.conf
%attr(640,root,wheel) %config(noreplace) /etc/security/chroot.conf
%attr(640,root,wheel) %config(noreplace) /etc/security/group.conf
%attr(640,root,wheel) %config(noreplace) /etc/security/limits.conf
%attr(640,root,wheel) %config(noreplace) /etc/security/time.conf
%attr(644,root,root) %config(noreplace) /etc/security/pam_env.conf
%attr(644,root,root) %config(noreplace) /etc/environment

%_mandir/man5/*
%_mandir/man8/*

%files compat
/%_lib/security/pam_stack.so

%files devel
%defattr(-,root,root)
%_libdir/libpam.so
%_libdir/libpamc.so
%_libdir/libpam_misc.so
%_includedir/security/
%_mandir/man3/*

%files doc
%defattr(-,root,root)
%dir %docdir
%docdir/[^ACNm]*

%changelog
* Fri Aug 28 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.1.0-owl10
- Updated Linux-PAM to 1.1.0, which replaces pam_rhosts_auth.so with
pam_rhosts.so and introduces new modules: pam_faildelay.so, pam_pwhistory.so,
pam_tally2.so and pam_umask.so.
- Updated pam-redhat to 0.99.10-1.
- Reworked layout of documentation files.

* Tue Feb 12 2008 Solar Designer <solar-at-owl.openwall.com> 0.99.4.0-owl3
- In system-auth, reduced the default value for the N2 parameter to
pam_passwdqc's min=... option (the minimum length for passphrases) from
12 to 11.

* Sun Sep 03 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.99.4.0-owl2
- Relaxed the build dependency on db4-devel.

* Tue Jun 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.99.4.0-owl1
- Updated Linux-PAM to post-0.99.4.0 snapshot 20060523.

* Fri Apr 07 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.99.3.0-owl2
- Backported a few fixes from Linux-PAM cvs.
- Rebuilt with libdb-4.3.so.

* Wed Jan 18 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.99.3.0-owl1
- Updated Linux-PAM to 0.99.3.0.

* Mon Dec 26 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.99.2.1-owl1
- Updated Linux-PAM to 0.99.2.1.
- Relocated documentation to %docdir.
- Disabled build of static libraries.
- Moved pam_stack into a new pam-compat subpackage.

* Sat Dec 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.80-owl3
- Rebuilt with libdb-4.2.so.

* Sat Oct 29 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.80-owl2
- Packaged /etc/pam.d/system-auth.

* Tue Aug 23 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.80-owl1
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

* Tue Jun 28 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.75-owl25
- Build this package without optimizations based on strict aliasing rules.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.75-owl24
- Removed permissions and group owner verify check for %_libexecdir/chkpwd
due to %%triggerin.
- Cleaned up the spec.

* Tue Feb 24 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.75-owl23
- Moved /lib/*.so to %_libdir where corresponding static archives live

* Thu Feb 19 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.75-owl22
- Created missing /etc/security directory

* Wed Oct 29 2003 Solar Designer <solar-at-owl.openwall.com> 0.75-owl21
- Require glibc-crypt_blowfish-devel for builds.
- Dropped the obsolete "Provides: pam <= 0.75-14owl" tag which was needed
during our transition to the new Release numbering scheme.

* Sun Aug 10 2003 Solar Designer <solar-at-owl.openwall.com> 0.75-owl20
- pam_limits: don't invoke setrlimit(2) on limits which are not set
explicitly as simply resetting RLIMIT_FSIZE to what appears to be its
current value may decrease the actual limit with LFS.

* Tue Jul 22 2003 Solar Designer <solar-at-owl.openwall.com> 0.75-owl19
- Patched pam_wheel to never rely on getlogin(3).

* Thu Aug 22 2002 Solar Designer <solar-at-owl.openwall.com> 0.75-owl18
- Patched pam_motd to behave on errors.

* Sun Jul 28 2002 Solar Designer <solar-at-owl.openwall.com>
- Moved pam.d and pam.conf man pages to section 5 where they belong.

* Sat Jul 06 2002 Solar Designer <solar-at-owl.openwall.com>
- pam_limits: support stacking for account management (as well as for
session setup), be fail-close on configuration file reads, report the
"too many logins" via PAM conversation rather than direct printf(3).

* Sun May 19 2002 Solar Designer <solar-at-owl.openwall.com>
- Moved the chkpwd directory to /usr/libexec.

* Mon Feb 04 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Mon Nov 19 2001 Solar Designer <solar-at-owl.openwall.com>
- Cache pam_get_user() failures such that the conversation function isn't
called multiple times with the same prompt if pam_get_user() fails and is
used by more than one module in the stack.
- pam_lastlog: bug and reliability fixes (but the module is still dirty),
"nowtmp" option to disable logging to wtmp when the program does that.
- pam_securetty: be fail-close on user lookups, always log failures (not
just with "debug").

* Fri Nov 16 2001 Solar Designer <solar-at-owl.openwall.com>
- Use the trigger on shadow-utils for possibly creating and making use of
group chkpwd, not just for group shadow.  This makes no difference on Owl
as either the groups are provided by owl-etc (on new installs) or groupadd
is already available when this package is installed, but may be useful on
hybrid systems.

* Thu Nov 15 2001 Solar Designer <solar-at-owl.openwall.com>
- No longer build pam_unix, the tcb package will provide compatibility
symlinks instead.
- /tmp fixes in the documentation (don't suggest bad practices).

* Sun Oct 07 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to Red Hat's 0.75-10 plus our usual patches.
- Replaced pam_listfile with Michael Tokarev's implementation (see
http://archives.neohapsis.com/archives/pam-list/2000-12/0084.html).
- Patched the new pam_chroot to catch the most common misuses which would
result in a security problem, updated its README and example configuration
file to discourage such misuses.
- Moved development libraries and header files into a subpackage.
- Moved the main Linux-PAM documentation into a documentation subpackage.

* Mon Jul 30 2001 Solar Designer <solar-at-owl.openwall.com>
- Fixed a double-free bug in pam_pwdb which caused it to segfault after
successful password changes in some cases.  The bug was specific to Owl.

* Sat May 05 2001 Solar Designer <solar-at-owl.openwall.com>
- Minor updates to use crypt_blowfish interfaces in the now officially
documented ways.

* Thu Mar 08 2001 Solar Designer <solar-at-owl.openwall.com>
- Patched some of the pam_pwdb/pwdb_chkpwd interaction problems.
- Install pwdb_chkpwd SGID shadow, but restricted to group chkpwd.

* Sat Sep 16 2000 Solar Designer <solar-at-owl.openwall.com>
- optflags_lib support.

* Sat Aug 26 2000 Solar Designer <solar-at-owl.openwall.com>
- Disabled building of pam_console entirely to avoid the dependency on glib.
- Removed the (bogus?) dependency on initscripts from this spec file.
- Added packaging of man pages.

* Tue Aug 08 2000 Solar Designer <solar-at-owl.openwall.com>
- Removed pam_console and its related files.

* Sun Jul 16 2000 Solar Designer <solar-at-owl.openwall.com>
- Added a password expiration bugfix for pam_pwdb.

* Sun Jul 09 2000 Solar Designer <solar-at-owl.openwall.com>
- Added installation of pam_client.h

* Sat Jul 08 2000 Solar Designer <solar-at-owl.openwall.com>
- Imported from RH.
- Ported the Owl pam_pwdb patch from original Linux-PAM-0.72.
- Disabled pam_cracklib as it's to be replaced with pam_passwdqc (not
a part of this package).

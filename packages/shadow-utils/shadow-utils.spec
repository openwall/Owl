# $Id: Owl/packages/shadow-utils/shadow-utils.spec,v 1.41 2004/11/11 19:04:26 solar Exp $

Summary: Utilities for managing shadow password files and user/group accounts.
Name: shadow-utils
Version: 4.0.4.1
Release: owl4
Epoch: 2
License: BSD
Group: System Environment/Base
Source0: ftp://ftp.pld.org.pl/software/shadow/shadow-%version.tar.bz2
Source1: login.defs
Source2: useradd.default
Source3: user-group-mod.pam
Source4: chage-chfn-chsh.pam
Source5: chpasswd-newusers.pam
Source6: chage.control
Source7: chfn.control
Source8: chsh.control
Source9: gpasswd.control
Source10: newgrp.control
Patch0: shadow-4.0.4.1-owl-check-reads.diff
Patch1: shadow-4.0.4.1-owl-usermod-unlock.diff
Patch2: shadow-4.0.4.1-owl-tmp.diff
Patch3: shadow-4.0.4.1-owl-pam-auth.diff
Patch4: shadow-4.0.4.1-owl-chage-drop-priv.diff
Patch5: shadow-4.0.4.1-owl-chage-ro-no-lock.diff
Patch6: shadow-4.0.4.1-owl-userdel-path_prefix.diff
Patch7: shadow-4.0.4.1-owl-pam_chauthtok.diff
Patch8: shadow-4.0.4.1-owl-usermod-update-lstchg.diff
Patch9: shadow-4.0.4.1-owl-usergroupname_max.diff
Patch19: shadow-4.0.4.1-rh-owl-redhat.diff
Patch20: shadow-4.0.4.1-owl-man.diff
Patch21: shadow-4.0.4.1-owl-create-mailbox.diff
Patch22: shadow-4.0.4.1-owl-restrict-locale.diff
Patch23: shadow-4.0.4.1-owl-crypt_gensalt.diff
Patch24: shadow-4.0.4.1-owl-newgrp.diff
Patch30: shadow-4.0.4.1-owl-tcb.diff
Requires: owl-control >= 0.4, owl-control < 2.0
Requires: pam, tcb >= 0.9.8, pam_userpass >= 0.5
BuildRequires: libtool, gettext = 0.14.1, automake, autoconf
BuildRequires: glibc-crypt_blowfish-devel
BuildRequires: pam-devel, pam_userpass-devel, tcb-devel
BuildRequires: cvs
BuildRoot: /override/%name-%version

%description
The shadow-utils package includes the tools necessary for manipulating
local user and group databases.  It supports both traditional and tcb
shadow password files.

%prep
%setup -q -n shadow-%version
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
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch30 -p1

find . -name '*.orig' -delete

%{expand:%%define optflags %optflags -Wall}

%build
unset LINGUAS || :
find lib libmisc src -name '*.c' -print > po/POTFILES.in
libtoolize --copy --force
autopoint -f
aclocal -I m4
automake -a
autoheader
autoconf
CFLAGS="$RPM_OPT_FLAGS -DEXTRA_CHECK_HOME_DIR -DSHADOWTCB -D_GNU_SOURCE" \
%configure \
	--disable-desrpc --disable-shared \
	--with-libcrypt --with-libpam --without-libcrack
%__make

%install
rm -rf %buildroot
%makeinstall
chmod -R -s %buildroot

# copy shadow.3 as it is in EXTRA_DIST and not installed by default
install -p -m 644 $RPM_BUILD_DIR/shadow-%version/man/shadow.3 \
	%buildroot%_mandir/man3/

# move symlinks to correct locations
mv %buildroot%_bindir/vigr %buildroot%_sbindir/

ln -s useradd %buildroot%_sbindir/adduser

# Fix man pages (XXX: should be moved to owl-man patch)
echo '.so newgrp.1' > %buildroot%_mandir/man1/sg.1
echo '.so pwconv.8' > %buildroot%_mandir/man8/grpconv.8
echo '.so pwconv.8' > %buildroot%_mandir/man8/grpunconv.8
echo '.so vipw.8' > %buildroot%_mandir/man8/vigr.8

mkdir -p -m 700 %buildroot%_sysconfdir/default
install -m 600 $RPM_SOURCE_DIR/login.defs %buildroot%_sysconfdir/
install -m 600 $RPM_SOURCE_DIR/useradd.default \
	%buildroot%_sysconfdir/default/useradd

mkdir -p %buildroot%_sysconfdir/pam.d
pushd %buildroot%_sysconfdir/pam.d
install -m 600 $RPM_SOURCE_DIR/user-group-mod.pam user-group-mod
ln -s user-group-mod groupadd
ln -s user-group-mod groupdel
ln -s user-group-mod groupmod
ln -s user-group-mod useradd
ln -s user-group-mod userdel
ln -s user-group-mod usermod
install -m 644 $RPM_SOURCE_DIR/chage-chfn-chsh.pam chage-chfn-chsh
ln -s chage-chfn-chsh chage
ln -s chage-chfn-chsh chfn
ln -s chage-chfn-chsh chsh
install -m 600 $RPM_SOURCE_DIR/chpasswd-newusers.pam chpasswd-newusers
ln -s chpasswd-newusers chpasswd
ln -s chpasswd-newusers newusers
popd

mkdir -p %buildroot%_sysconfdir/control.d/facilities
cd %buildroot%_sysconfdir/control.d/facilities

install -m 700 $RPM_SOURCE_DIR/chage.control chage
install -m 700 $RPM_SOURCE_DIR/chfn.control chfn
install -m 700 $RPM_SOURCE_DIR/chsh.control chsh
install -m 700 $RPM_SOURCE_DIR/gpasswd.control gpasswd
install -m 700 $RPM_SOURCE_DIR/newgrp.control newgrp

%pre
if [ $1 -ge 2 ]; then
	/usr/sbin/control-dump chage chfn chsh gpasswd newgrp
fi

%post
grep -q ^shadow: %_sysconfdir/group || groupadd -g 42 shadow
if grep -q '^shadow:[^:]*:42:' %_sysconfdir/group; then
	chgrp -f shadow %_sysconfdir/shadow && chmod 440 %_sysconfdir/shadow || :
	chgrp shadow %_sysconfdir/login.defs && chmod 640 %_sysconfdir/login.defs
	chgrp shadow %_sysconfdir/pam.d/chage-chfn-chsh && \
		chmod 640 %_sysconfdir/pam.d/chage-chfn-chsh
fi
grep -q ^auth: %_sysconfdir/group || groupadd -g 164 auth
if [ $1 -ge 2 ]; then
	/usr/sbin/control-restore chage chfn chsh gpasswd newgrp
fi

%files
%defattr(-,root,root)
%doc README NEWS ChangeLog doc/HOWTO
%dir %_sysconfdir/default
%attr(0644,root,root) %config(noreplace) %_sysconfdir/login.defs
%attr(0600,root,root) %config(noreplace) %_sysconfdir/default/useradd
%_sbindir/adduser
%attr(0700,root,root) %_sbindir/user*
%attr(0700,root,root) %_sbindir/group*
%attr(0700,root,root) %_sbindir/pwck
%attr(0700,root,root) %_sbindir/grpck
%attr(0700,root,root) %_sbindir/*conv
%attr(0700,root,root) %_sbindir/chpasswd
%attr(0700,root,root) %_sbindir/newusers
%attr(0700,root,root) %_sbindir/vi*
%attr(0700,root,root) %_bindir/chage
%attr(0700,root,root) %_bindir/chfn
%attr(0700,root,root) %_bindir/chsh
%attr(0700,root,root) %_bindir/gpasswd
%attr(0700,root,root) %_bindir/newgrp
%_bindir/sg
%_bindir/lastlog
%_mandir/man1/chage.1*
%_mandir/man1/chfn.1*
%_mandir/man1/chsh.1*
%_mandir/man1/gpasswd.1*
%_mandir/man1/newgrp.1*
%_mandir/man1/sg.1*
%_mandir/man3/getspnam.3*
%_mandir/man3/shadow.3*
%_mandir/man5/login.defs.5*
%_mandir/man5/shadow.5*
%_mandir/man8/adduser.8*
%_mandir/man8/group*.8*
%_mandir/man8/user*.8*
%_mandir/man8/pwck.8*
%_mandir/man8/grpck.8*
%_mandir/man8/chpasswd.8*
%_mandir/man8/newusers.8*
%_mandir/man8/*conv.8*
%_mandir/man8/lastlog.8*
%_mandir/man8/vi*.8*
%_datadir/locale/*/*/shadow.mo
%config(noreplace) %_sysconfdir/pam.d/*
%_sysconfdir/control.d/facilities/*
# excludes
%exclude %_bindir/expiry
%exclude %_bindir/faillog
%exclude %_bindir/groups
%exclude %_bindir/login
%exclude %_bindir/passwd
%exclude %_bindir/su
%exclude %_libdir
%exclude %_sbindir/logoutd
%exclude %_sbindir/mkpasswd
%exclude %_mandir/man1/expiry*
%exclude %_mandir/man1/groups*
%exclude %_mandir/man1/id*
%exclude %_mandir/man1/login*
%exclude %_mandir/man1/passwd*
%exclude %_mandir/man1/su*
%exclude %_mandir/man5/faillog*
%exclude %_mandir/man5/limits*
%exclude %_mandir/man5/login.access*
%exclude %_mandir/man5/passwd*
%exclude %_mandir/man5/porttime*
%exclude %_mandir/man5/suauth*
%exclude %_mandir/man8/faillog*
%exclude %_mandir/man8/logoutd*
%exclude %_mandir/man8/mkpasswd*

%changelog
* Thu Nov 11 2004 Juan M. Bello Rivas <jmbr@owl.openwall.com> 2:4.0.4.1-owl4
- Added the USERNAME_MAX and GROUPNAME_MAX options.
- Placed the "usermod -p" patch higher in the patch list.

* Thu Nov 11 2004 Dmitry V. Levin <ldv@owl.openwall.com> 2:4.0.4.1-owl3
- Restore chpasswd(8) behaviour, which was broken since 4.0.4.1-owl0.1.

* Tue Sep 28 2004 Juan M. Bello Rivas <jmbr@owl.openwall.com> 2:4.0.4.1-owl2
- Modified usermod to update the last password change field when invoked
with the -p option.

* Fri Jun 11 2004 Michail Litvak <mci@owl.openwall.com> 2:4.0.4.1-owl1
- Originally by solar@ in Owl-current:
Properly check the return value from pam_chauthtok() in
libmisc/pwdcheck.c: passwd_check() that is used by chfn and chsh commands.
Thanks to Steve Grubb and Martin Schulze.

* Thu Mar 19 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2:4.0.4.1-owl0.3
- Removed gettext patch, we are using autopoint now
- Changed patch number for userdel-path_prefix

* Thu Mar 18 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2:4.0.4.1-owl0.2
- Fixed a bug in path_prefix() in userdel
- Fixed a typo in tcb patch

* Fri Feb 27 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2:4.0.4.1-owl0.1
- Updated to the new version
- All patches were regenerated
- Spec file was adopted for RPM4

* Thu Feb 12 2004 Michail Litvak <mci@owl.openwall.com> 2:4.0.0-owl15
- Use RPM macros instead of explicit paths.

* Sat Nov 22 2003 Solar Designer <solar@owl.openwall.com> 2:4.0.0-owl14
- In tcb_move(), use mode 700 and not mode 0 for the directory being
modified as the latter is incompatible with the mode 0 hack in vserver
kernel patches; thanks to Dmitry V. Levin for the report and patch.

* Wed Oct 29 2003 Solar Designer <solar@owl.openwall.com> 2:4.0.0-owl13
- Require glibc-crypt_blowfish-devel for builds.

* Mon Jul 28 2003 Michail Litvak <mci@owl.openwall.com> 2:4.0.0-owl12
- Added patch from ALT to fix user_groups initialization.

* Thu May 29 2003 Solar Designer <solar@owl.openwall.com> 2:4.0.0-owl11
- write_to=tcb
- USE_TCB yes

* Thu Apr 17 2003 Solar Designer <solar@owl.openwall.com> 2:4.0.0-owl10
- Pass prefix= and count= to pam_tcb also for authentication such that it
can use this information to reduce timing leaks.

* Sat Apr 12 2003 Solar Designer <solar@owl.openwall.com> 2:4.0.0-owl9
- Don't let %post fail if group shadow exists, but /etc/shadow doesn't
(tcb is in use).

* Mon Apr 07 2003 Dmitry V. Levin <ldv@owl.openwall.com> 2:4.0.0-owl8
- Updated pam_userpass support: build with libpam_userpass.

* Sun Nov 03 2002 Solar Designer <solar@owl.openwall.com>
- Dump/restore the owl-control settings for chage, chfn, chsh, gpasswd,
and newgrp on package upgrades.

* Thu Oct 24 2002 Solar Designer <solar@owl.openwall.com>
- Cleaned up the recent changes.
- Corrected a newly introduced memory leak on an error path.
- Changed the TCB_SYMLINKS pseudo-code in login.defs(5) manual page to
be C/English rather than shell for consistency with the pam_tcb(8) page.

* Mon Aug 19 2002 Rafal Wojtczuk <nergal@owl.openwall.com>
- Merged the enhancements which remove 32K users limit.

* Sun Jul 21 2002 Solar Designer <solar@owl.openwall.com>
- Made "chage -l" drop its saved GID too.
- Removed the extra space in "[-e expire ]" in the usage instructions for
useradd and usermod.

* Wed Feb 06 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Nov 25 2001 Solar Designer <solar@owl.openwall.com>
- auth group.

* Fri Nov 16 2001 Solar Designer <solar@owl.openwall.com>
- Enable forking for pam_tcb with chage, chfn, and chsh.

* Mon Nov 12 2001 Solar Designer <solar@owl.openwall.com>
- Use /etc/tcb/root as scratch space for "vipw -s user".

* Sun Nov 11 2001 Solar Designer <solar@owl.openwall.com>
- gpasswd will now use crypt_gensalt(3) when setting group passwords; two
new configuration items have been added to login.defs and the man page
updated accordingly.
- newgrp is now packaged here, not from util-linux, for gshadow support.
Patches to both the newgrp/sg program and its man page have been added.
- Moved the PAM authentication in user management commands (which is new
with shadow-4.0.0) to after command-line parsing, made it use separate
service names for each command (with symlinks to common PAM configuration
files provided).
- Use constant strings rather than argv[0] for syslog ident in the user
management commands.
- Check for read errors in commonio and vipw/vigr (not doing so could
result in data loss when the records are written back).
- usermod -U (unlock) is now a no-op when used on an account which never
had a password set; previously, this would open up a passwordless account.
- pwconv and pwunconv will now refuse to work with tcb, pwck will work
but skip shadow file checks.
- Build with -Wall (surprisingly only a few fixes were needed).

* Thu Nov 08 2001 Solar Designer <solar@owl.openwall.com>
- chpasswd(8) and newusers(8) will now talk to pam_userpass for password
changes.
- More bugfixes and code cleanups for the tcb patch.

* Sun Nov 04 2001 Solar Designer <solar@owl.openwall.com>
- Cleaned up all of the patches fixing several bugs and re-coding a few
pieces; the tcb patch is still far from clean, though.

* Wed Aug 21 2001 Rafal Wojtczuk <nergal@owl.openwall.com>
- fixed mailbox creation, which was wrong in rh patch
- added USE_TCB to login.defs.5

* Fri Aug 03 2001 Rafal Wojtczuk <nergal@owl.openwall.com>
- upgrade to 20000902 version
- added tcb support
- merged patches from rawhide, updated owl ones

* Fri Jun 15 2001 Solar Designer <solar@owl.openwall.com>
- Rewrote most of the login.defs(5) man page and enabled its packaging.
- Added more defaults to /etc/login.defs, added a reference to login.defs(5).
- Fixed a bug in the lastlog(8) man page reported by Jarno Huuskonen.

* Sun May 27 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- enable EXTRA_CHECK_HOME_DIR for userdel

* Sat Mar 10 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- restrictions to username/groupname

* Sat Feb 10 2001 Solar Designer <solar@owl.openwall.com>
- shadow group.
- Don't lock password files with "chage -l" (this is read-only access).
- Drop SGID privileges after opening shadow file with "chage -l".

* Sat Aug 26 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file from RH, cleaned it up, and changed heavily.
- Imported many of the Red Hat modifications to useradd, including some
questionable ones.
- Restricted locale support in commands that may be installed SUID/SGID.
- chsh, chfn, vipw, and vigr are now built from this package rather than
from util-linux.  The util-linux versions used incompatible locking, and
vi* lacked the support for shadow files.
- owl-control support for chsh, chfn, chage, and gpasswd.

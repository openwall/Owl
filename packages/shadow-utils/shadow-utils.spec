# $Id: Owl/packages/shadow-utils/shadow-utils.spec,v 1.31 2003/10/29 16:11:44 solar Exp $

Summary: Utilities for managing shadow password files and user/group accounts.
Name: shadow-utils
Version: 4.0.0
Release: owl13
Epoch: 2
License: BSD
Group: System Environment/Base
Source0: ftp://ftp.pld.org.pl/software/shadow/shadow-%{version}.tar.bz2
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
Patch0: shadow-4.0.0-owl-warnings.diff
Patch1: shadow-4.0.0-owl-check-reads.diff
Patch2: shadow-4.0.0-owl-usermod-unlock.diff
Patch3: shadow-4.0.0-owl-tmp.diff
Patch4: shadow-4.0.0-owl-pam-auth.diff
Patch5: shadow-4.0.0-owl-chage-drop-priv.diff
Patch6: shadow-4.0.0-owl-chage-ro-no-lock.diff
Patch7: shadow-4.0.0-owl-useradd-usermod-usage.diff
Patch10: shadow-4.0.0-rh-owl-redhat.diff
Patch20: shadow-4.0.0-owl-man.diff
Patch21: shadow-4.0.0-owl-check_names.diff
Patch22: shadow-4.0.0-owl-create-mailbox.diff
Patch23: shadow-4.0.0-owl-restrict-locale.diff
Patch24: shadow-4.0.0-owl-crypt_gensalt.diff
Patch25: shadow-4.0.0-owl-newgrp.diff
Patch26: shadow-4.0.0-owl-automake.diff
Patch30: shadow-4.0.0-owl-tcb.diff
Patch31: shadow-4.0.0-alt-user_groups.diff
Requires: owl-control >= 0.4, owl-control < 2.0
Requires: pam, tcb >= 0.9.8, pam_userpass >= 0.5
BuildRequires: libtool, gettext, automake, autoconf
BuildRequires: glibc-crypt_blowfish-devel
BuildRequires: pam-devel, pam_userpass-devel, tcb-devel
BuildRoot: /override/%{name}-%{version}

%description
The shadow-utils package includes the tools necessary for manipulating
local user and group databases.  It supports both traditional and tcb
shadow password files.

%prep
%setup -q -n shadow-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch10 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch30 -p1
%patch31 -p1

%{expand:%%define optflags %optflags -Wall}

%build
unset LINGUAS || :
find lib libmisc src -name '*.c' -print > po/POTFILES.in
libtoolize --copy --force
aclocal
gettextize -f
automake -a
autoheader
autoconf
CFLAGS="$RPM_OPT_FLAGS -DEXTRA_CHECK_HOME_DIR" ./configure \
	--prefix=/usr \
	--disable-desrpc --disable-shared \
	--with-libcrypt --with-libpam --without-libcrack
make

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/usr exec_prefix=$RPM_BUILD_ROOT
chmod -R -s $RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT
ln -s useradd usr/sbin/adduser
ln -s vipw usr/sbin/vigr
ln -s vipw.8 usr/man/man8/vigr.8

mkdir -p -m 700 etc/default
install -m 600 $RPM_SOURCE_DIR/login.defs etc/login.defs
install -m 600 $RPM_SOURCE_DIR/useradd.default etc/default/useradd

mkdir -p etc/pam.d
pushd etc/pam.d
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

mkdir -p etc/control.d/facilities
cd etc/control.d/facilities

install -m 700 $RPM_SOURCE_DIR/chage.control chage
install -m 700 $RPM_SOURCE_DIR/chfn.control chfn
install -m 700 $RPM_SOURCE_DIR/chsh.control chsh
install -m 700 $RPM_SOURCE_DIR/gpasswd.control gpasswd
install -m 700 $RPM_SOURCE_DIR/newgrp.control newgrp

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ $1 -ge 2 ]; then
	/usr/sbin/control-dump chage chfn chsh gpasswd newgrp
fi

%post
grep -q ^shadow: /etc/group || groupadd -g 42 shadow
if grep -q '^shadow:[^:]*:42:' /etc/group; then
	chgrp -f shadow /etc/shadow && chmod 440 /etc/shadow || :
	chgrp shadow /etc/login.defs && chmod 640 /etc/login.defs
	chgrp shadow /etc/pam.d/chage-chfn-chsh && \
		chmod 640 /etc/pam.d/chage-chfn-chsh
fi
grep -q ^auth: /etc/group || groupadd -g 164 auth
if [ $1 -ge 2 ]; then
	/usr/sbin/control-restore chage chfn chsh gpasswd newgrp
fi

%files
%defattr(-,root,root)
%doc README NEWS ChangeLog doc/ANNOUNCE doc/LICENSE
%dir /etc/default
%attr(0644,root,root) %config(noreplace) /etc/login.defs
%attr(0600,root,root) %config(noreplace) /etc/default/useradd
/usr/sbin/adduser
%attr(0700,root,root) /usr/sbin/user*
%attr(0700,root,root) /usr/sbin/group*
%attr(0700,root,root) /usr/sbin/pwck
%attr(0700,root,root) /usr/sbin/grpck
%attr(0700,root,root) /usr/sbin/*conv
%attr(0700,root,root) /usr/sbin/chpasswd
%attr(0700,root,root) /usr/sbin/newusers
%attr(0700,root,root) /usr/sbin/vi*
%attr(0700,root,root) /usr/bin/chage
%attr(0700,root,root) /usr/bin/chfn
%attr(0700,root,root) /usr/bin/chsh
%attr(0700,root,root) /usr/bin/gpasswd
%attr(0700,root,root) /usr/bin/newgrp
/usr/bin/sg
/usr/bin/lastlog
/usr/man/man1/chage.1*
/usr/man/man1/chfn.1*
/usr/man/man1/chsh.1*
/usr/man/man1/gpasswd.1*
/usr/man/man1/newgrp.1*
/usr/man/man1/sg.1*
/usr/man/man3/getspnam.3*
/usr/man/man3/shadow.3*
/usr/man/man5/login.defs.5*
/usr/man/man5/shadow.5*
/usr/man/man8/adduser.8*
/usr/man/man8/group*.8*
/usr/man/man8/user*.8*
/usr/man/man8/pwck.8*
/usr/man/man8/grpck.8*
/usr/man/man8/chpasswd.8*
/usr/man/man8/newusers.8*
/usr/man/man8/*conv.8*
/usr/man/man8/lastlog.8*
/usr/man/man8/vi*.8*
/usr/share/locale/*/*/shadow.mo
%config(noreplace) /etc/pam.d/*
/etc/control.d/facilities/*

%changelog
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

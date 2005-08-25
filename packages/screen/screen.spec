# $Id: Owl/packages/screen/screen.spec,v 1.35 2005/08/25 23:08:04 ldv Exp $

Summary: A screen manager that supports multiple sessions on one terminal.
Name: screen
Version: 4.0.2
Release: owl4
License: GPL
Group: Applications/System
Source0: ftp://ftp.uni-erlangen.de/pub/utilities/screen/screen-%version.tar.gz
Source1: screen.pam
Patch0: screen-4.0.2-owl-os.diff
Patch1: screen-4.0.2-owl-config.diff
Patch2: screen-4.0.2-owl-pam.diff
Patch3: screen-4.0.2-deb-owl-home-screen-exchange.diff
Patch4: screen-4.0.2-deb-owl-doc.diff
Patch5: screen-4.0.2-rh-delete-hack.diff
Patch6: screen-4.0.2-rh-doc.diff
Patch7: screen-4.0.2-owl-tmp.diff
Patch8: screen-4.0.2-owl-no-fault-handler.diff
Patch9: screen-4.0.2-alt-utempter.diff
Patch10: screen-4.0.2-owl-warnings.diff
Patch11: screen-4.0.2-owl-logging.diff
Patch12: screen-4.0.2-owl-info.diff
PreReq: /sbin/install-info
Requires: tcb, pam_userpass, libutempter
# Just in case this is built with an older version of RPM package.
Requires: libutempter.so.0(UTEMPTER_1.1)
Prefix: %_prefix
BuildRequires: pam-devel, pam_userpass-devel, libutempter-devel
BuildRoot: /override/%name-%version

%description
The screen utility allows you to have multiple interactive sessions on
just one terminal and keep the sessions over disconnects.  screen is
useful for remote users or users who are connected via a serial line
but want to use more than one session.

%prep
%setup -q
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
%patch10 -p1
%patch11 -p1
%patch12 -p1

%{expand:%%define optflags %optflags -Wall}

%build
autoconf
%configure --disable-socket-dir --enable-pam

rm doc/screen.info*

make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %buildroot
mkdir -p %buildroot/etc/pam.d

make install DESTDIR=%buildroot

mv %buildroot%_bindir/screen-%version %buildroot%_bindir/screen

install -m 644 etc/etcscreenrc %buildroot/etc/screenrc
install -m 644 %_sourcedir/screen.pam %buildroot/etc/pam.d/screen

mkdir -p %buildroot%_libexecdir/screen

# we will make two links in the %triggerin sections, so we want to track them
touch %buildroot%_libexecdir/screen/{tcb_chkpwd,utempter}

# Remove unpackaged files
rm %buildroot%_infodir/dir

%pre
grep -q ^screen: /etc/group || groupadd -g 165 screen

%post
/sbin/install-info %_infodir/screen.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/screen.info %_infodir/dir
	rm -f %_libexecdir/screen/{tcb_chkpwd,utempter}
fi

%triggerin -- tcb >= 0.9.7.1
ln -f %_libexecdir/chkpwd/tcb_chkpwd %_libexecdir/screen/

%triggerin -- libutempter >= 1.1.0-owl1
ln -f %_libexecdir/utempter/utempter %_libexecdir/screen/

%triggerpostun -- tcb
if [ ! -e %_libexecdir/chkpwd/tcb_chkpwd ]; then
	rm -f %_libexecdir/screen/tcb_chkpwd
fi

%triggerpostun -- libutempter
if [ ! -e %_libexecdir/utempter/utempter ]; then
	rm -f %_libexecdir/screen/utempter
fi

%files
%defattr(-,root,root)
%doc NEWS README doc/FAQ doc/README.DOTSCREEN etc/screenrc
%attr(2711,root,screen) %_bindir/screen
%_mandir/man1/screen.1.*
%_infodir/screen.info*
%_datadir/screen/utf8encodings/*
%config(noreplace) /etc/screenrc
%config(noreplace) /etc/pam.d/screen
%attr(710,root,screen) %dir %_libexecdir/screen
%ghost %_libexecdir/screen/tcb_chkpwd
%ghost %_libexecdir/screen/utempter

%changelog
* Fri Aug 26 2005 Dmitry V. Levin <ldv@owl.openwall.com> 4.0.2-owl4
- Added system logger initialization to builtin locker.
- Allowed users with empty passwords to use builtin locker.
- Corrected info files installation.

* Sat Jun 25 2005 Dmitry V. Levin <ldv@owl.openwall.com> 4.0.2-owl3
- Do not link with -lelf even if the library is available during build.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 4.0.2-owl2
- Fixed orphaned files in %_libexecdir/screen created by %triggerin.
- Removed unneeded rm -f of %_bindir/screen{,.old}

* Fri Jan 09 2004 Michail Litvak <mci@owl.openwall.com> 4.0.2-owl1
- 4.0.2
- Dropped obsoleted patches.

* Sun Dec 14 2003 Michail Litvak <mci@owl.openwall.com> 3.9.10-owl8
- Patch from 4.0.2 upstream version - buffer overflow fix in
ANSI characters handling (reported by Timo Sirainen).

* Thu Apr 17 2003 Solar Designer <solar@owl.openwall.com> 3.9.10-owl7
- Pass prefix= and count= to pam_tcb also for authentication such that it
can use this information to reduce timing leaks.

* Mon Apr 07 2003 Dmitry V. Levin <ldv@owl.openwall.com> 3.9.10-owl6
- Updated pam_userpass support: build with libpam_userpass.

* Wed Dec 25 2002 Dmitry V. Levin <ldv@owl.openwall.com> 3.9.10-owl5
- Migrated to libutempter.

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Sun May 19 2002 Solar Designer <solar@owl.openwall.com>
- Grant screen access to both chkpwd and utempter helpers via a group
screen restricted directory and hard links.
- Switch egid for the PAM authentication making use of POSIX saved ID's.
- Don't compile in the SIGSEGV/SIGBUS fault handler (previously it was
only used for SUID installation, not SGID, and would claim to dump core
which it indeed can't do).
- Additional convention enforcement on patch file names.

* Tue Feb 05 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Nov 16 2001 Solar Designer <solar@owl.openwall.com>
- Use pam_tcb.
- Build with -Wall.

* Tue Nov 13 2001 Solar Designer <solar@owl.openwall.com>
- Corrected the package description.

* Tue Nov 13 2001 Michail Litvak <mci@owl.openwall.com>
- 3.9.10
- more tmp fixes in configure

* Sun Oct 07 2001 Solar Designer <solar@owl.openwall.com>
- Updates to appl_userpass.c to support building against Linux-PAM 0.74+.

* Fri Aug 03 2001 Michail Litvak <mci@owl.openwall.com>
- install doc/FAQ as FAQ instead link to doc/FAQ

* Wed Jun 13 2001 Michail Litvak <mci@owl.openwall.com>
- updated to 3.9.9
- patch configure to avoid non secure file creation in /tmp

* Mon Mar 19 2001 Solar Designer <solar@owl.openwall.com>
- screen.pam: explicit pam_deny for everything but authentication.

* Sat Mar 10 2001 Solar Designer <solar@owl.openwall.com>
- Don't require and link against libpam_misc.

* Sat Mar 10 2001 Michail Litvak <mci@owl.openwall.com>
- example user's .screenrc moved to doc
- added patch to builtin telnet (bcopy->memmove)
- spec, patches cleanups

* Thu Mar 08 2001 Michail Litvak <mci@owl.openwall.com>
- Many patches removed and other reworked

* Sat Mar 03 2001 Michail Litvak <mci@owl.openwall.com>
- Added patches imported from Debian, RedHat
- PAM support for screen locking via pam_userpass

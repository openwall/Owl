# $Id: Owl/packages/tcb/tcb/tcb.spec,v 1.12 2002/06/21 14:34:46 solar Exp $

Summary: Libraries and tools implementing the tcb password shadowing scheme.
Name: tcb
Version: 0.9.7.2
Release: owl1
License: BSD or GPL
Group: System Environment/Base
Source: %{name}-%{version}.tar.gz
PreReq: /sbin/ldconfig, %_libexecdir/chkpwd
BuildRequires: glibc-crypt_blowfish, pam-devel
BuildRoot: /override/%{name}-%{version}

%description
The tcb package consists of three components: pam_tcb, libnss_tcb, and
libtcb.  pam_tcb is a PAM module which supersedes pam_unix.  It also
implements the tcb password shadowing scheme (see tcb(5) for details).
The tcb scheme allows many core system utilities (passwd(1) being the
primary example) to operate with little privilege.  libnss_tcb is the
accompanying NSS module.  libtcb contains code shared by the PAM and
NSS modules and is also used by programs from the shadow-utils package.

%package devel
Summary: Libraries and header files for building tcb-aware applications.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains static libraries and header files needed for
building tcb-aware applications.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" make

%install
rm -rf $RPM_BUILD_ROOT
make install-non-root install-pam_unix FAKEROOT=$RPM_BUILD_ROOT MANDIR=%_mandir

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%triggerin -- shadow-utils
grep -q '^shadow:[^:]*:42:' /etc/group && \
	chgrp shadow %_libexecdir/chkpwd/tcb_chkpwd && \
	chmod 2711 %_libexecdir/chkpwd/tcb_chkpwd

# This is needed for upgrades from older versions of the package.
%triggerpostun -- tcb < 0.9.7.1
rmdir /sbin/chkpwd.d

%files
%defattr(-,root,root)
%doc LICENSE
/lib/libnss_tcb.so.2
/lib/libtcb.so.*
/lib/security/pam_tcb.so
/lib/security/pam_unix.so
/lib/security/pam_unix_acct.so
/lib/security/pam_unix_auth.so
/lib/security/pam_unix_passwd.so
/lib/security/pam_unix_session.so
/sbin/tcb_convert
/sbin/tcb_unconvert
%attr(0700,root,root) %_libexecdir/chkpwd/tcb_chkpwd
%_mandir/man5/tcb.5.*
%_mandir/man5/pam_tcb.5.*
%_mandir/man5/pam_unix.5.*
%_mandir/man8/tcb_convert.8.*
%_mandir/man8/tcb_unconvert.8.*

%files devel
%defattr(-,root,root)
/usr/include/tcb.h
/usr/lib/libtcb.a
/lib/libtcb.so

%changelog
* Sun May 19 2002 Solar Designer <solar@owl.openwall.com>
- Moved the chkpwd directory to /usr/libexec.

* Mon Feb 04 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Dec 09 2001 Solar Designer <solar@owl.openwall.com>
- Various minor fixes from Dmitry V. Levin of ALT Linux.
- A GNU-style ChangeLog will now be maintained.

* Sun Nov 18 2001 Solar Designer <solar@owl.openwall.com>
- Patches from Nergal to make delays on failure work with the "fork"
option and to not produce a warning when su'ing to pseudo-users from
root.

* Fri Nov 16 2001 Solar Designer <solar@owl.openwall.com>
- Don't include the /sbin/chkpwd.d directory in this package as it's
provided by our pam package.
- Use a trigger on shadow-utils for possibly creating and making use of
group shadow.  This makes no difference on Owl as either the group is
provided by owl-etc (on new installs) or groupadd is already available
when this package is installed, but may be useful on hybrid systems.

* Thu Nov 15 2001 Solar Designer <solar@owl.openwall.com>
- Provide compatibility symlinks and a man page for pam_unix.
- tcb_convert(8) man page fixes from Nergal.
- Moved all of pam_tcb's prompts and messages to support.h and made them
more consistent with those used by pam_passwdqc.
- Improved logging.

* Thu Nov 01 2001 Solar Designer <solar@owl.openwall.com>
- Changed everything all over the place during October. ;-)

* Tue Sep 11 2001 Rafal Wojtczuk <nergal@owl.openwall.com>
- Makefiles and code layout rewrite.
- Added reentrant tcb_*_privs_r() functions, needed for nss.

* Sun Aug 19 2001 Rafal Wojtczuk <nergal@owl.openwall.com>
- version 0.5
- man pages
- nis fixes
- removed ugly _unix_getpwnam(), clean replacement

* Sat Aug 04 2001 Rafal Wojtczuk <nergal@owl.openwall.com>
- 0.4 packaged for Owl.

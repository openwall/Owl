# $Id: Owl/packages/pam/pam.spec,v 1.3 2000/07/16 14:11:43 solar Exp $

Summary: A security tool which provides authentication for applications.
Name: pam
Version: 0.72
Release: 9owl
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
%config /etc/security/console.perms
%dir /etc/security/console.apps
%dir /var/lock/console
/usr/man/man5/*
/usr/man/man8/*

%changelog
* Sun Jul 16 2000 Solar Designer <solar@false.com>
- Added a password expiration bugfix for pam_pwdb.

* Sun Jul  9 2000 Solar Designer <solar@false.com>
- Added installation of pam_client.h

* Sat Jul  8 2000 Solar Designer <solar@false.com>
- Import from RH, port the Owl pam_pwdb patch from original Linux-PAM-0.72,
disable pam_cracklib as it's to be replaced with pam_passwdqc (not a part
of this package).

* Sat Feb 05 2000 Nalin Dahyabhai <nalin@redhat.com>
- Fix pam_xauth bug #6191.

* Thu Feb 03 2000 Elliot Lee <sopwith@redhat.com>
- Add a patch to accept 'pts/N' in /etc/securetty as a match for tty '5'
  (which is what other pieces of the system think it is). Fixes bug #7641.

* Mon Jan 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- argh, turn off gratuitous debugging

* Wed Jan 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 0.72
- fix pam_unix password-changing bug
- fix pam_unix's cracklib support
- change package URL

* Mon Jan 03 2000 Cristian Gafton <gafton@redhat.com>
- don't allow '/' on service_name

* Thu Oct 21 1999 Cristian Gafton <gafton@redhat.com>
- enhance the pam_userdb module some more

* Fri Sep 24 1999 Cristian Gafton <gafton@redhat.com>
- add documenatation

* Tue Sep 21 1999 Michael K. Johnson <johnsonm@redhat.com>
- a tiny change to pam_console to make it not loose track of console users

* Mon Sep 20 1999 Michael K. Johnson <johnsonm@redhat.com>
- a few fixes to pam_xauth to make it more robust

* Wed Jul 14 1999 Michael K. Johnson <johnsonm@redhat.com>
- pam_console: added <xconsole> to manage /dev/console

* Thu Jul 01 1999 Michael K. Johnson <johnsonm@redhat.com>
- pam_xauth: New refcounting implementation based on idea from Stephen Tweedie

* Sat Apr 17 1999 Michael K. Johnson <johnsonm@redhat.com>
- added video4linux devices to /etc/security/console.perms

* Fri Apr 16 1999 Michael K. Johnson <johnsonm@redhat.com>
- added joystick lines to /etc/security/console.perms

* Thu Apr 15 1999 Michael K. Johnson <johnsonm@redhat.com>
- fixed a couple segfaults in pam_xauth uncovered by yesterday's fix...

* Wed Apr 14 1999 Cristian Gafton <gafton@redhat.com>
- use gcc -shared to link the shared libs

* Wed Apr 14 1999 Michael K. Johnson <johnsonm@redhat.com>
- many bug fixes in pam_xauth
- pam_console can now handle broken applications that do not set
  the PAM_TTY item.

* Tue Apr 13 1999 Michael K. Johnson <johnsonm@redhat.com>
- fixed glob/regexp confusion in pam_console, added kbd and fixed fb devices
- added pam_xauth module

* Sat Apr 10 1999 Cristian Gafton <gafton@redhat.com>
- pam_lastlog does wtmp handling now

* Thu Apr 08 1999 Michael K. Johnson <johnsonm@redhat.com>
- added option parsing to pam_console
- added framebuffer devices to default console.perms settings

* Wed Apr 07 1999 Cristian Gafton <gafton@redhat.com>
- fixed empty passwd handling in pam_pwdb

* Mon Mar 29 1999 Michael K. Johnson <johnsonm@redhat.com>
- changed /dev/cdrom default user permissions back to 0600 in console.perms
  because some cdrom players open O_RDWR.

* Fri Mar 26 1999 Michael K. Johnson <johnsonm@redhat.com>
- added /dev/jaz and /dev/zip to console.perms

* Thu Mar 25 1999 Michael K. Johnson <johnsonm@redhat.com>
- changed the default user permissions for /dev/cdrom to 0400 in console.perms

* Fri Mar 19 1999 Michael K. Johnson <johnsonm@redhat.com>
- fixed a few bugs in pam_console

* Thu Mar 18 1999 Michael K. Johnson <johnsonm@redhat.com>
- pam_console authentication working
- added /etc/security/console.apps directory

* Mon Mar 15 1999 Michael K. Johnson <johnsonm@redhat.com>
- added pam_console files to filelist

* Fri Feb 12 1999 Cristian Gafton <gafton@redhat.com>
- upgraded to 0.66, some source cleanups

* Mon Dec 28 1998 Cristian Gafton <gafton@redhat.com>
- add patch from Savochkin Andrey Vladimirovich <saw@msu.ru> for umask
  security risk

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- upgrade to ver 0.65
- build the package out of internal CVS server


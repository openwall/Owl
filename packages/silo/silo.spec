# $Id: Owl/packages/silo/silo.spec,v 1.8 2003/10/30 21:15:48 solar Exp $

Summary: Sparc Improved boot LOader.
Name: silo
Version: 1.2.5
Release: owl1
License: GPL
Group: System Environment/Base
Source: http://prdownloads.sourceforge.net/silo/silo-%version.tar.bz2
Patch0: silo-1.2.5-owl-Makefile.diff
Patch1: silo-1.2.5-owl-man.diff
ExclusiveArch: sparc sparcv9 sparc64
BuildRoot: /override/%name-%version

%description
The silo package installs the Sparc Improved boot LOader (SILO), which
you'll need to boot Linux on a SPARC.  SILO installs onto your system's
boot block and can be configured to boot Linux, Solaris and SunOS.

%prep
%setup -q -n silo-%version
%patch0 -p1
%patch1 -p1

%build
make CFLAGS="$RPM_OPT_FLAGS -Wall -I. -I../include"

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT MANDIR=%_mandir

%post
test -f /etc/silo.conf -a "$SILO_INSTALL" = "yes" && /sbin/silo $SILO_FLAGS || :

%files
%defattr(-,root,root)
%doc docs COPYING ChangeLog
/sbin/silo
/usr/bin/tilo
/usr/bin/maketilo
/boot/first.b
/boot/ultra.b
/boot/cd.b
/boot/fd.b
/boot/ieee32.b
/boot/silotftp.b
/boot/second.b
/usr/sbin/silocheck
%_mandir/man1/*tilo.1*
%_mandir/man5/silo.conf.5*
%_mandir/man8/silo.8*

%changelog
* Mon Jun 03 2002 Solar Designer <solar@owl.openwall.com> 1.2.5-owl1
- Updated to 1.2.5.
- Don't disable cat anymore; anyone who wants boot loader security
should use the proper measures to achieve it.

* Tue Feb 05 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Jan 18 2001 Solar Designer <solar@owl.openwall.com>
- Run silo in %post if enabled via $SILO_INSTALL.

* Fri Jan 05 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- disable cat command

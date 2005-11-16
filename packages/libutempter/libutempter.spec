# $Owl: Owl/packages/libutempter/libutempter.spec,v 1.10 2005/11/16 13:11:15 solar Exp $

Summary: A privileged helper for utmp/wtmp updates.
Name: libutempter
Version: 1.1.3
Release: owl1
License: LGPL
Group: System Environment/Base
Source: ftp://ftp.altlinux.org/pub/people/ldv/utempter/%name-%version.tar.bz2
PreReq: /sbin/ldconfig, grep, /usr/sbin/groupadd
Provides: utempter = %version-%release
Obsoletes: utempter
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
This package provides library interface for terminal emulators such as
screen and xterm to record user sessions to utmp and wtmp files.

%package devel
Summary: Development environment for libutempter.
Group: Development/Libraries
Requires: %name = %version-%release
Provides: utempter-devel = %version-%release
Obsoletes: utempter-devel

%description devel
This package contains development files required to build utempter-aware
software.

%prep
%setup -q

%{expand:%%define optflags %optflags -Wall}

%build
make CC=gcc libdir="%_libdir" libexecdir="%_libexecdir"

%install
rm -rf %buildroot
make install DESTDIR="%buildroot" libdir="%_libdir" libexecdir="%_libexecdir"
strip %buildroot%_libexecdir/utempter/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%pre
grep -q ^utempter: /etc/group || groupadd -g 162 utempter

%files
%defattr(-,root,root)
%doc COPYING README
%attr(710,root,utempter) %dir %_libexecdir/utempter
%attr(2711,root,utmp) %_libexecdir/utempter/utempter
%_libdir/libutempter.so.*

%files devel
%defattr(-,root,root)
%_libdir/libutempter.so
%_libdir/libutempter.a
%_includedir/utempter.h

%changelog
* Thu Aug 18 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.1.3-owl1
- Updated to 1.1.3: Added multilib support, restricted list of global
symbols exported by the library.

* Mon Feb 24 2003 Michail Litvak <mci-at-owl.openwall.com> 1.1.1-owl1
- Updated to 1.1.1
  * Fri Feb 14 2003 Dmitry V. Levin <ldv at owl.openwall.com> 1.1.1-alt1
  - iface.c: don't block SIGCHLD; redefine signal handler instead.

* Tue Jan 14 2003 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.1.0-owl1
- Migrated to libutempter-1.1.0

* Sun May 19 2002 Solar Designer <solar-at-owl.openwall.com>
- Moved the utempter directory to /usr/libexec.
- Try an alternate utempter helper binary location for screen.

* Mon Feb 04 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Feb 25 2001 Solar Designer <solar-at-owl.openwall.com>
- Various spec file cleanups.
- Corrected the package description.

* Wed Feb 21 2001 Michail Litvak <mci-at-owl.openwall.com>
- imported from RH
- added utempter group
- utempter binary moved to /usr/sbin/utempter.d/
  owned by group utempter with 710 permissions

# $Id: Owl/packages/procps/Attic/procps.spec,v 1.18 2005/01/14 03:27:53 galaxy Exp $

Summary: Utilities for monitoring your system and processes on your system.
Name: procps
Version: 2.0.7
Release: owl7
License: GPL and LGPL
Group: System Environment/Base
URL: http://procps.sf.net
Source: ftp://sunsite.unc.edu/pub/Linux/system/status/ps/procps-%version.tar.gz
Patch0: procps-2.0.6-owl-alt-stale.diff
Patch1: procps-2.0.7-owl-locale.diff
Patch2: procps-2.0.7-owl-meminfo-fixes.diff
Patch3: procps-2.0.7-owl-no-catman-cleanup.diff
Patch4: procps-2.0.7-owl-top-ticks.diff
Patch5: procps-2.0.7-owl-top-include.diff
Patch6: procps-2.0.7-owl-fixes.diff
PreReq: /sbin/ldconfig
BuildRoot: /override/%name-%version

%description
The procps package contains a set of system utilities which provide
system information.  procps includes ps, free, skill, snice, tload,
top, pgrep, pkill, uptime, vmstat, w, and watch.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%__make CC="%__cc" OPT="$RPM_OPT_FLAGS"

%install
rm -rf %buildroot
mkdir -p %buildroot{/bin,/%_lib,/sbin,%_bindir,/usr/X11R6/bin,%_mandir/{man1,man5,man8}}
%__make install \
    DESTDIR="%buildroot" \
    MANDIR="%_mandir" \
    USRBINDIR="%buildroot%_bindir" \
    PROCDIR="%buildroot%_bindir" \
    SHLIBDIR="%buildroot/%_lib" \
    INSTALLBIN="install -m 0755" \
    INSTALLSCT="install -m 0755" \
    INSTALLMAN="install -m 0644" \
    OWNERGROUP=""
chmod 755 %buildroot/{%_lib,bin,sbin,%_bindir}/*

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot/usr/X11R6/bin/XConsole
rm %buildroot%_bindir/kill
rm %buildroot%_mandir/man1/kill.1*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc NEWS BUGS TODO
/%_lib/libproc.so.%version
/bin/ps
/sbin/sysctl
%_bindir/oldps
%_bindir/uptime
%_bindir/tload
%_bindir/free
%_bindir/w
%_bindir/top
%_bindir/vmstat
%_bindir/watch
%_bindir/skill
%_bindir/snice
%_bindir/pgrep
%_bindir/pkill
%_mandir/man1/free.1*
%_mandir/man1/ps.1*
%_mandir/man1/oldps.1*
%_mandir/man1/skill.1*
%_mandir/man1/snice.1*
%_mandir/man1/pgrep.1*
%_mandir/man1/pkill.1*
%_mandir/man1/tload.1*
%_mandir/man1/top.1*
%_mandir/man1/uptime.1*
%_mandir/man1/w.1*
%_mandir/man1/watch.1*
%_mandir/man5/sysctl.conf.5*
%_mandir/man8/vmstat.8*
%_mandir/man8/sysctl.8*

%changelog
* Fri Jan 07 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 2.0.7-owl7
- Added gcc343-fixes patch to solve issues after gcc upgrade.
- Cleaned up the spec.

* Fri May 14 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.0.7-owl6
- Changed order of included headers in top to flawlessly build against
ncurses 5.4

* Thu Feb 12 2004 Michail Litvak <mci@owl.openwall.com> 2.0.7-owl5
- Use RPM macros instead of explicit paths.

* Sat Jan 17 2004 Solar Designer <solar@owl.openwall.com> 2.0.7-owl4
- Handle ticks going backwards gracefully.

* Thu Oct 16 2003 Solar Designer <solar@owl.openwall.com> 2.0.7-owl3
- Patched top to use unsigned long long's for tick counts; previously,
its SMP-specific code used just int which resulted in the overflow
happening twice earlier than it does in the kernel on x86/SMP (that is,
after 248 days of idle time of a CPU instead of after 497 days) or
really early on Alpha/SMP (after just 24 days whereas the kernel uses
64-bit jiffies and essentially never overflows).

* Fri Jan 17 2003 Solar Designer <solar@owl.openwall.com> 2.0.7-owl2
- Don't try to remove catman (preformatted) manual pages during package
builds: this fails with an error if the files do exist because we build
as non-root.

* Wed Feb 06 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Sat Dec 02 2000 Solar Designer <solar@owl.openwall.com>
- Updated to 2.0.7, removed 3 patches which are now obsolete.
- Added a C-locale-for-sscanf patch similar to one found in RH 7.0.
- Fixed a new long long / meminfo bug.

* Mon Nov 13 2000 Solar Designer <solar@owl.openwall.com>
- Added a patch from Red Hat to prevent divide by zero on big-endian.

* Wed Jul 05 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec from iNs/Linux, cleaned it up a bit, and added the
patch for alternative stale utmp entry checking.

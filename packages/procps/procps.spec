# $Id: Owl/packages/procps/Attic/procps.spec,v 1.12 2004/02/12 01:28:49 mci Exp $

Summary: Utilities for monitoring your system and processes on your system.
Name: procps
Version: 2.0.7
Release: owl5
License: GPL and LGPL
Group: System Environment/Base
URL: http://procps.sf.net
Source: ftp://sunsite.unc.edu/pub/Linux/system/status/ps/procps-%version.tar.gz
Patch0: procps-2.0.6-owl-alt-stale.diff
Patch1: procps-2.0.7-owl-locale.diff
Patch2: procps-2.0.7-owl-meminfo-fixes.diff
Patch3: procps-2.0.7-owl-no-catman-cleanup.diff
Patch4: procps-2.0.7-owl-top-ticks.diff
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

%build
make CC="gcc $RPM_OPT_FLAGS" LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{/bin,/lib,/sbin,/usr/{bin,X11R6/bin},%_mandir/{man1,man5,man8}}
make DESTDIR=$RPM_BUILD_ROOT MANDIR=%_mandir OWNERGROUP= install
chmod 755 $RPM_BUILD_ROOT/{lib,bin,sbin,usr/bin}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc NEWS BUGS TODO
/lib/libproc.so.%version
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

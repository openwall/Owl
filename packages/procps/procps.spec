# $Id: Owl/packages/procps/Attic/procps.spec,v 1.10.2.1 2004/01/17 17:55:42 solar Exp $

Summary: Utilities for monitoring your system and processes on your system.
Name: procps
Version: 2.0.7
Release: owl4
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
mkdir -p $RPM_BUILD_ROOT/{bin,lib,sbin,usr/{bin,X11R6/bin,man/{man1,man5,man8}}}
make DESTDIR=$RPM_BUILD_ROOT OWNERGROUP= install
chmod 755 $RPM_BUILD_ROOT/{lib,bin,sbin,usr/bin}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc NEWS BUGS TODO
/lib/libproc.so.%version
/bin/ps
/sbin/sysctl
/usr/bin/oldps
/usr/bin/uptime
/usr/bin/tload
/usr/bin/free
/usr/bin/w
/usr/bin/top
/usr/bin/vmstat
/usr/bin/watch
/usr/bin/skill
/usr/bin/snice
/usr/bin/pgrep
/usr/bin/pkill
/usr/man/man1/free.1*
/usr/man/man1/ps.1*
/usr/man/man1/oldps.1*
/usr/man/man1/skill.1*
/usr/man/man1/snice.1*
/usr/man/man1/pgrep.1*
/usr/man/man1/pkill.1*
/usr/man/man1/tload.1*
/usr/man/man1/top.1*
/usr/man/man1/uptime.1*
/usr/man/man1/w.1*
/usr/man/man1/watch.1*
/usr/man/man5/sysctl.conf.5*
/usr/man/man8/vmstat.8*
/usr/man/man8/sysctl.8*

%changelog
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

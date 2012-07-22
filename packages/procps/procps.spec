# $Owl: Owl/packages/procps/Attic/procps.spec,v 1.34 2012/07/22 18:34:02 segoon Exp $

Summary: Utilities for monitoring your system and processes on your system.
Name: procps
Version: 3.2.5
Release: owl10
License: GPL and LGPL
Group: System Environment/Base
URL: http://procps.sf.net
Source: ftp://sunsite.unc.edu/pub/Linux/system/status/ps/procps-%version.tar.gz
Patch0: procps-3.2.5-rh-top-pseudo.diff
Patch1: procps-3.2.5-rh-owl-top-rc.diff
Patch2: procps-3.2.5-rh-top-sigwinch.diff
Patch3: procps-3.2.5-rh-vmstat-bound.diff
Patch10: procps-3.2.5-suse-top-cpus.diff
Patch11: procps-3.2.5-suse-top-eof.diff
Patch12: procps-3.2.5-suse-w-notruncate.diff
Patch13: procps-3.2.5-suse-w-maxcmd.diff
Patch14: procps-3.2.5-suse-pwdx-bound.diff
Patch15: procps-3.2.5-suse-buffersize.diff
Patch20: procps-3.2.5-alt-Makefile.diff
Patch21: procps-3.2.5-alt-sysctl-messages.diff
Patch22: procps-3.2.5-alt-sysctl-verbose.diff
Patch23: procps-3.2.5-alt-watch-stdin.diff
Patch24: procps-3.2.5-alt-proc-sbuf.diff
Patch25: procps-3.2.5-alt-man.diff
Patch26: procps-3.2.5-owl-format.diff
Patch27: procps-3.2.5-owl-proc.diff
Patch28: procps-3.2.5-owl-pmap.diff
Patch29: procps-3.2.5-owl-stat2proc.diff
Patch30: procps-3.2.5-owl-top.diff
Patch31: procps-3.2.5-owl-warnings.diff
Patch32: procps-3.2.5-owl-PAGE_SIZE.diff
Patch33: procps-3.2.5-owl-man.diff
PreReq: /sbin/ldconfig
BuildRequires: ncurses-devel
BuildRoot: /override/%name-%version

%description
The procps package contains a set of system utilities which provide
system information.  procps includes: free, pgrep, pkill, pmap, ps, pwdx,
skill, slabtop, snice, sysctl, tload, top, uptime, vmstat, w, and watch.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1

%build
%__make CC="%__cc" CFLAGS="%optflags" LDFLAGS=-ltinfo

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot lib64=%_lib

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc NEWS BUGS TODO
/%_lib/*
/bin/*
/sbin/*
%_bindir/*
%_mandir/man?/*

%changelog
* Sun Jul 22 2012 Vasiliy Kulikov <segoon-at-owl.openwall.com> 3.2.5-owl10
- Added -ltinfo into LDFLAGS to fix build error under binutils >= 2.21.
- Fixed build failure with headers of Linux 2.6.32.

* Wed Dec 01 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 3.2.5-owl9
- Fixed parsing warnings of ps(1) and top(1) man pages.

* Mon Nov 23 2009 Solar Designer <solar-at-owl.openwall.com> 3.2.5-owl8
- Temporarily #define __KERNEL__ when including <asm/page.h> to get PAGE_SIZE.
This is addressed differently (in a cleaner way) in 3.2.7, but the resulting
change to OUTBUF_SIZE is not obviously correct.

* Mon Dec 05 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.2.5-owl7
- Changed top's default view to summary when only one CPU is installed.

* Mon Oct 31 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.2.5-owl6
- Fixed array subscript type warnings.

* Mon Oct 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.2.5-owl4
- Corrected spelling in the top utility, changed its default view to SMP
unless more than 4 CPUs are installed.

* Sat Sep 17 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.2.5-owl3
- Restored old behavior of all utilities except w(1) wrt unreadable
/proc/#/stat files.

* Wed Sep 14 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.2.5-owl2
- Fixed handling of processes with unreadable /proc/#/stat files.
- Suppressed bogus error message in pmap utility.

* Tue Aug 30 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.2.5-owl1
- Updated to 3.2.5, removed obsolete patches.
- Packaged new procps utilities: pmap, pwdx, slabtop.
- Imported a bunch of patches from RH's procps-3.2.5-6.3,
SuSE's procps-3.2.5-5, and ALT's procps-3.2.5-alt2 packages.
- Corrected error diagnostics when /proc filesystem is not mounted.

* Fri Jan 07 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.0.7-owl7
- Added a patch to solve issues after gcc upgrade.
- Cleaned up the spec.

* Fri May 14 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.0.7-owl6
- Changed order of included headers in top to flawlessly build against
ncurses 5.4

* Thu Feb 12 2004 Michail Litvak <mci-at-owl.openwall.com> 2.0.7-owl5
- Use RPM macros instead of explicit paths.

* Sat Jan 17 2004 Solar Designer <solar-at-owl.openwall.com> 2.0.7-owl4
- Handle ticks going backwards gracefully.

* Thu Oct 16 2003 Solar Designer <solar-at-owl.openwall.com> 2.0.7-owl3
- Patched top to use unsigned long long's for tick counts; previously,
its SMP-specific code used just int which resulted in the overflow
happening twice earlier than it does in the kernel on x86/SMP (that is,
after 248 days of idle time of a CPU instead of after 497 days) or
really early on Alpha/SMP (after just 24 days whereas the kernel uses
64-bit jiffies and essentially never overflows).

* Fri Jan 17 2003 Solar Designer <solar-at-owl.openwall.com> 2.0.7-owl2
- Don't try to remove catman (preformatted) manual pages during package
builds: this fails with an error if the files do exist because we build
as non-root.

* Wed Feb 06 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sat Dec 02 2000 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.0.7, removed 3 patches which are now obsolete.
- Added a C-locale-for-sscanf patch similar to one found in RH 7.0.
- Fixed a new long long / meminfo bug.

* Mon Nov 13 2000 Solar Designer <solar-at-owl.openwall.com>
- Added a patch from Red Hat to prevent divide by zero on big-endian.

* Wed Jul 05 2000 Solar Designer <solar-at-owl.openwall.com>
- Imported this spec from iNs/Linux, cleaned it up a bit, and added the
patch for alternative stale utmp entry checking.

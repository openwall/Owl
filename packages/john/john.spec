# $Id: Owl/packages/john/john.spec,v 1.40 2005/02/15 08:50:42 solar Exp $

Summary: John the Ripper password cracker.
Name: john
Version: 1.6.37.4
Release: owl1
License: GPL
Group: Applications/System
URL: http://www.openwall.com/john/
Source0: ftp://ftp.openwall.com/pub/projects/john/john-%version.tar.gz
Source1: ftp://ftp.openwall.com/pub/projects/john/john-1.6.tar.gz
BuildRoot: /override/%name-%version

%description
John the Ripper is a fast password cracker (password security auditing
tool).  Its primary purpose is to detect weak Unix passwords, but a number
of other hash types are supported as well.

%prep
%setup -q -a 1

%define cflags -c %optflags -Wall -DJOHN_SYSTEMWIDE=1
%define with_cpu_fallback 0

%build
cd src
%ifarch athlon i786 i886 i986
make linux-x86-mmx-elf CFLAGS='%cflags'
%else
%ifarch %ix86
%define with_cpu_fallback 1
make linux-x86-any-elf CFLAGS='%cflags'
mv ../run/john ../run/john-non-mmx
make clean
make linux-x86-mmx-elf CFLAGS='%cflags -DCPU_FALLBACK=1'
%endif
%endif
%ifarch alpha alphaev5 alphaev56 alphapca56 alphaev6 alphaev67
make linux-alpha CFLAGS='%cflags'
%endif
%ifarch sparc sparcv9
make linux-sparc CFLAGS='%cflags'
%endif
%ifarch ppc
make linux-ppc CFLAGS='%cflags'
%endif

%install
mkdir -p %buildroot{%_bindir,%_datadir/john}
install -m 700 run/john %buildroot%_bindir/
cp -a run/un* %buildroot%_bindir/
%if %with_cpu_fallback
mkdir -p %buildroot%_libexecdir/john
install -m 700 run/john-* %buildroot%_libexecdir/john/
%endif
install -m 644 run/{john.conf,password.lst} john-1.6/run/*.chr \
	%buildroot%_datadir/john/
install -m 644 -p run/mailer doc/
mkdir doc/john-1.6
cp -a john-1.6/doc/* doc/john-1.6/

%files
%defattr(-,root,root)
%doc doc/*
%attr(750,root,wheel) %_bindir/john
%_bindir/un*
%if %with_cpu_fallback
%dir %_libexecdir/john
%attr(750,root,wheel) %_libexecdir/john/*
%endif
%dir %_datadir/john
%attr(640,root,wheel) %config(noreplace) %_datadir/john/john.conf
%attr(644,root,root) %_datadir/john/password.lst
%attr(644,root,root) %_datadir/john/*.chr

%changelog
* Tue Feb 15 2005 Solar Designer <solar@owl.openwall.com> 1.6.37.4-owl1
- New make target for 64-bit PowerPC (G5+) running Mac OS X (32-bit
inter-function interfaces).

* Tue Nov 09 2004 Solar Designer <solar@owl.openwall.com> 1.6.37.3-owl1
- Properly report effective c/s rates in excess of 2**32 (now up to
2**32 * 10**6), report large c/s rates in thousands or millions.

* Sat Jun 19 2004 Solar Designer <solar@owl.openwall.com> 1.6.37.2-owl1
- "N passwords cracked" -> "N password hashes cracked" because there can be
multiple hashes per password with LM or double-length DES-based crypt(3).
- Updated some documentation files from John 1.6 and included them in doc/

* Sun Jun 13 2004 Solar Designer <solar@owl.openwall.com> 1.6.37.1-owl1
- Freeze the timestamps that are being logged for the duration of loading
of password files; clock is reset to 0 or to the restore point when the
actual cracking starts to ensure the reported c/s rate is not affected by
load time, but we don't want this clock reset to be seen in event logs.

* Mon Feb 23 2004 Solar Designer <solar@owl.openwall.com> 1.6.37-owl1
- Bumped the release to 1.6.37 to make it available separately from Owl.

* Sat Jan 10 2004 Solar Designer <solar@owl.openwall.com> 1.6.36.9-owl1
- Corrected a segfault with --stdin introduced with 1.6.34.2.

* Wed Dec 03 2003 Solar Designer <solar@owl.openwall.com> 1.6.36.8-owl1
- Avoid triggering a Mac OS X cpp bug(?) where it would detect and refuse to
handle "recursive" cpp macros.

* Sun Nov 30 2003 Solar Designer <solar@owl.openwall.com> 1.6.36.7-owl1
- When calculating the c/s rate in benchmarks (bench.c, best.c), use 64-bit
integer operations to avoid a possible integer overflow on 32-bit systems
with large CLK_TCK (e.g. Win32).

* Sun Nov 16 2003 Solar Designer <solar@owl.openwall.com> 1.6.36.6-owl1
- When generating a new charset file, first do a self-test of the specified
CHARSET_* parameters to ensure they don't cause a 64-bit integer overflow.

* Sat Oct 25 2003 Solar Designer <solar@owl.openwall.com> 1.6.36.5-owl1
- In x86 assembly code, detect and choose optimal existing code version for
Centaur Technology processors (IDT Winchip to VIA C3 and beyond).

* Fri Oct 10 2003 Solar Designer <solar@owl.openwall.com> 1.6.36.4-owl1
- Also support Matthew Kwan's older DES S-box expressions with standard
gates only, use them for x86-64 and autodetect between them and the
non-standard gates version with "make generic".

* Sun Oct 05 2003 Solar Designer <solar@owl.openwall.com> 1.6.36.3-owl1
- Added two make targets for Linux on x86-64, thanks to John Edward Scott.

* Wed Oct 01 2003 Solar Designer <solar@owl.openwall.com> 1.6.36.2-owl1
- Replaced mem_free() with a macro to keep gcc 3.3.1's strict aliasing
happy (thanks to Anatoly Pugachev for reporting the gcc warnings).

* Mon Sep 22 2003 Solar Designer <solar@owl.openwall.com> 1.6.36.1-owl1
- Support OpenBSD/x86 w/ ELF binaries (Makefile patch by demon).

* Thu Sep 18 2003 Solar Designer <solar@owl.openwall.com> 1.6.36-owl1
- Corrected the generic and SPARC make targets broken with 1.6.34.2.

* Mon Sep 15 2003 Solar Designer <solar@owl.openwall.com> 1.6.35-owl1
- Log two more events.
- With the AIX make target, use -qunroll=2 instead of plain -qunroll.

* Sun Sep 07 2003 Solar Designer <solar@owl.openwall.com> 1.6.34.2-owl1
- Verbose logging; John now logs how it proceeds through stages of each
of its cracking modes, regardless of whether there're guesses or not.

* Mon Aug 25 2003 Solar Designer <solar@owl.openwall.com> 1.6.34.1-owl1
- Added an event logging framework; only session start/stop, cracking
modes, and cracked login names are logged currently, but the plan is to
log many more events in the future.

* Sun Jun 29 2003 Solar Designer <solar@owl.openwall.com> 1.6.34-owl1
- solaris-sparc64-cc, contributed by Thomas Nau.
- Check for and report invalid MinLen / MaxLen settings.

* Mon Jun 02 2003 Solar Designer <solar@owl.openwall.com> 1.6.33-owl2
- Added URL.

* Fri Jan 24 2003 Solar Designer <solar@owl.openwall.com> 1.6.33-owl1
- Added a 64-bit Solaris SPARC make target (recent gcc only for now).

* Wed Jan 15 2003 Solar Designer <solar@owl.openwall.com>
- Split the 64-bit MIPS target into two such that it is possible to have
64-bit builds which do or don't require at least an R10K CPU.

* Tue Nov 05 2002 Solar Designer <solar@owl.openwall.com>
- Workaround a Solaris stdio bug triggered by code in "unique".

* Fri Nov 01 2002 Solar Designer <solar@owl.openwall.com>
- Fixed a bug in "unique" which caused it to fail on big-endian boxes
on files bigger than a single buffer, thanks to Corey Becker.

* Sat Oct 19 2002 Solar Designer <solar@owl.openwall.com>
- Simplified DES_bs_get_binary_raw().

* Thu Oct 03 2002 Solar Designer <solar@owl.openwall.com>
- Never point cfg_name to path_expand()'s result buffer, make a copy.

* Thu Sep 05 2002 Solar Designer <solar@owl.openwall.com>
- Never put dupes in crk_guesses, that could overflow it and would be
inefficient anyway.

* Fri Apr 26 2002 Solar Designer <solar@owl.openwall.com>
- Check for with_cpu_fallback correctly (unbreak builds on non-x86).

* Thu Apr 11 2002 Solar Designer <solar@owl.openwall.com>
- On x86, always build the MMX binary, with a run-time fallback to the
non-MMX one if necessary.

* Wed Apr 10 2002 Solar Designer <solar@owl.openwall.com>
- Packaged 1.6.31-dev for Owl, with minor modifications.

# $Owl: Owl/packages/john/john.spec,v 1.107 2009/09/09 16:44:55 ldv Exp $

Summary: John the Ripper password cracker.
Name: john
Version: 1.7.3.3
%define charsets_version 20051216
Release: owl1
License: GPL
Group: Applications/System
URL: http://www.openwall.com/john/
Source0: john-%version.tar.gz
Source1: john-charsets-%charsets_version.tar.bz2
BuildRoot: /override/%name-%version

%description
John the Ripper is a fast password cracker (password security auditing
tool).  Its primary purpose is to detect weak Unix passwords, but a number
of other hash types are supported as well.

%prep
%setup -q -a 1

%ifarch x86_64
%define cflags -c %optflags -Wall -DJOHN_SYSTEMWIDE=1
%else
%define cflags -c %optflags -finline-limit=2000 --param inline-unit-growth=2000 -Wall -DJOHN_SYSTEMWIDE=1
%endif
%define with_cpu_fallback 0

%build
cd src
%ifarch %ix86
%define with_cpu_fallback 1
%ifarch athlon i786 i886 i986
%__make linux-x86-mmx CFLAGS='%cflags'
%else
%__make linux-x86-any CFLAGS='%cflags'
%{!?_without_check:%{!?_without_test:%__make check}}
mv ../run/john ../run/john-non-mmx
%__make clean
%__make linux-x86-mmx CFLAGS='%cflags -DCPU_FALLBACK=1'
%endif
%{!?_without_check:%{!?_without_test:%__make check}}
mv ../run/john ../run/john-non-sse
%__make clean
%__make linux-x86-sse2 CFLAGS='%cflags -DCPU_FALLBACK=1'
%endif
%ifarch x86_64
%__make linux-x86-64 CFLAGS='%cflags'
%endif
%ifarch alpha alphaev5 alphaev56 alphapca56 alphaev6 alphaev67
%__make linux-alpha CFLAGS='%cflags'
%endif
%ifarch sparc sparcv9
%__make linux-sparc CFLAGS='%cflags'
%endif
%ifarch ppc
%__make linux-ppc32 CFLAGS='%cflags'
%endif
%{!?_without_check:%{!?_without_test:%__make check}}

%install
rm -rf %buildroot
mkdir -p %buildroot{%_bindir,%_datadir/john}
install -m 700 run/john %buildroot%_bindir/
cp -a run/un* %buildroot%_bindir/
%if %with_cpu_fallback
mkdir -p %buildroot%_libexecdir/john
install -m 700 run/john-* %buildroot%_libexecdir/john/
%endif
install -m 644 -p run/{john.conf,password.lst} \
	john-charsets-%charsets_version/*.chr \
	%buildroot%_datadir/john/
install -m 644 -p run/mailer doc/

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
* Wed Sep 09 2009 Solar Designer <solar-at-owl.openwall.com> 1.7.3.3-owl1
- "make check" has been implemented.
- The --test option will now take an optional argument - the duration of each
benchmark in seconds.
- Section .note.GNU-stack has been added to all assembly files to avoid the
stack area unnecessarily being made executable on Linux systems that use this
mechanism.
- In DumbForce, explicitly NUL-terminate word[] when switching to a new length.

* Thu Jul 23 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.7.3.2-owl1
- Fixed off-by-one header->version overflow.  The overflow itself is
harmless, but fresh gcc in fortified mode complains, so the overflow is
removed to satisfy the modern requirements, as well as to be safe in
case of major re-arrangements to the charset_header structure.

* Fri Jul 18 2008 Solar Designer <solar-at-owl.openwall.com> 1.7.3.1-owl1
- Corrected the x86 assembly files for building on Mac OS X.
- Merged in some generic changes from JtR Pro.

* Thu Jul 10 2008 Solar Designer <solar-at-owl.openwall.com> 1.7.3-owl1
- Disabled BF_X2 on RISC architectures for now.
- Documentation updates to refer to LM hashes in a non-confusing way.

* Tue Jul 08 2008 Solar Designer <solar-at-owl.openwall.com> 1.7.2.4-owl1
- Many updates to x86*.S and Makefile associated with addition of
solaris-x86-* targets (beyond plain x86, which was already supported).

* Sun Jun 22 2008 Solar Designer <solar-at-owl.openwall.com> 1.7.2.3-owl1
- Two Blowfish-based crypt(3) hashes may now be computed in parallel for much
better performance on modern multi-issue CPUs with a sufficient number of
registers (e.g., x86-64, RISC).

* Sat Jun 21 2008 Solar Designer <solar-at-owl.openwall.com> 1.7.2.2-owl1
- Converted the code in x86-64.S to use %rip-relative addressing because
"32-bit absolute addressing is not supported for x86-64" on Mac OS X,
as well as to reduce code size (by 1348 bytes).
- Added DumbForce and KnownForce external mode samples to the default
john.conf.

* Wed Sep 13 2006 Solar Designer <solar-at-owl.openwall.com> 1.7.2.1-owl1
- Corrected the error message reported when "Extra = ..." contains characters
that are outside of the compile-time specified range (thanks to Radim Horak
for the bug report).

* Mon May 15 2006 Solar Designer <solar-at-owl.openwall.com> 1.7.2-owl1
- Added bitslice DES assembly code for x86-64 making use of the 64-bit mode
extended SSE2 with 16 XMM registers.

* Wed May 10 2006 Solar Designer <solar-at-owl.openwall.com> 1.7.1-owl1
- Added SSE2 support with runtime fallback to the MMX build.
- Treat AMD's 64-bit processors the same as AMD Athlon for the purpose of
selection of optimal 32-bit Blowfish and non-bitslice DES code.
- Don't pass function inlining tweaks to gcc on x86-64 as this actually hurts
performance with gcc 3.4.5 (that is currently in Owl) on current processors.
With no special options (only -finline-functions), gcc 3.4.5 inlines only
s4(), which turns out to actually be optimal for current processors.
- Use only a 32-bit data type within the MD5 implementation, not ARCH_WORD.
While the latter sometimes worked a little bit better on Alpha, it turned
out to kill performance on x86-64.
- Enhanced the self-test loop to proceed until we hit the maximum key index
even if the number of different test vectors is smaller.

* Mon Mar 20 2006 Solar Designer <solar-at-owl.openwall.com> 1.7.0.2-owl1
- Fixed a long-standing bug in the rule preprocessor which caused some
duplicate characters to not be omitted on platforms where ARCH_WORD is bigger
than int (that's all supported 64-bit platforms).

* Tue Mar 07 2006 Solar Designer <solar-at-owl.openwall.com> 1.7.0.1-owl1
- Fixed a bug introduced with 1.6.40 which caused spurious "charset file
changed" errors in batch mode if interrupted and restored before pass 3.
- Handle 8-bit characters in external mode program sources correctly.
Thanks to Frank Dittrich for reporting these two problems.
- Implemented extra ticks overflow safety - timer-based rather than just
crypts count based.
- Save/update the recovery file after the end of each pass in batch mode
to make sure that the file is up to date in case the next pass refuses to
start for whatever reason.
- Remove the recovery file when all hashes get cracked also in batch mode.
- Detect and report MinLen / MaxLen settings and charset files inconsistent
with the hash type.
- Perform additional sanity checking of charset files, distinguish incorrect
vs. incompatible ones.
- Use sysconf(_SC_CLK_TCK) instead of CLK_TCK when _SC_CLK_TCK is known to
be available or CLK_TCK is not (needed for glibc 2.3.90+).
- Worked around a gcc 4.1.0 strict aliasing bug affecting BF_std.c, BF_body:
http://gcc.gnu.org/bugzilla/show_bug.cgi?id=26587
- Added a separate DO_ALIGN(5) (cache line alignment) into x86.S after a
possible switch to .bss from .data or .text.
- Added "notes to packagers" to params.h.
- Added a sample but fully-functional "keyboard-based" external mode to the
default john.conf.

* Thu Feb 02 2006 Solar Designer <solar-at-owl.openwall.com> 1.7-owl2
- Pass -finline-limit=2000 --param inline-unit-growth=2000 to gcc such that
it inlines the S-boxes on non-x86 just like gcc 2.x used to do.

* Mon Jan 09 2006 Solar Designer <solar-at-owl.openwall.com> 1.7-owl1
- Documentation updates: separated CONTACT from CREDITS, added some FAQ
entries, etc.
- When displaying programs' usage information, use either an equivalent of
basename(argv[0]) (with the main John program) or fixed strings (with the
auxiliary tools).
- In rec_done(), do a log_flush() even if the session completes normally;
this is needed to hopefully update the pot file prior to our removal of the
crash recovery file.
- Applied some Cygwin-specific updates to signals.c and DOS/Win32-specific
updates to the Makefile.

* Fri Dec 16 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.40-owl1
- Detect changed charset files when restoring sessions.
- Updated the supplied password.lst.
- Added a new pre-defined "incremental" mode "Alnum", along with its
corresponding filter.
- Package new charset files (a separate tarball) instead of those from 1.6.

* Sat Nov 12 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.39.4-owl1
- Corrected the way nouns ending in "z" and "h" (other than those ending in
"ch" and "sh") are pluralized with the "p" wordlist rules command.

* Tue Nov 08 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.39.3-owl1
- When eliminating any duplicate and already-cracked hashes, compare the
internal representations first.
- When displaying cracked passwords, let split() unify the encoding of hashes.
(This only works when the only difference is upper vs. lower vs. mixed case
since we're using a hash table and would not do a comparison against hashes
which look very different.)
- Force the encoding of LM hashes that get into john.pot to all-lowercase.
- Corrected the handling of break statements with nested loops in the external
mode compiler.

* Fri Oct 28 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.39.2-owl1
- Re-worked the Makefile: dropped "-elf" suffixes from make target names,
re-ordered the targets for best to most generic (for individual platforms),
marked some targets as "best" or "obsolete", added openbsd-x86-64 (thanks to
Sebastian Rother), added many openbsd-* targets based on the OpenBSD port.
- Minor corrections to EXAMPLES.

* Sun Oct 09 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.39.1-owl1
- With linux-sparc make target, let's not use sparc.S because it uses
registers reserved by the SPARC ABI (%%g5-%%g7) and this no longer works with
glibc 2.3.x.
- Fixed a bug in best.sh which could result in MD5_IMM being enabled wrongly
when MD5_X2 is determined to improve performance (this only affected builds
with "make generic").
- Added a workaround for "some kaserver.DB0 files created by OpenAFS"; this
issue was brought up on john-users by Heiko Schulz and the patch produced by
Lionel Cons (thanks!)

* Thu Sep 08 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.39-owl1
- Fixed a bug in the loader introduced with 1.6.37.10 where "john --show"
would report split hashes with the last piece not yet cracked as if they
were fully cracked (thanks to Stephen Cartwright for the problem report).

* Mon Sep 05 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.38.2-owl1
- All of the remaining bits of John 1.6 documentation have been updated to
apply to the current version.
- Dropped John 1.6 documentation from the package.
- Added the macosx-x86-mmx-cc make target (thanks to Brian Bechtel).

* Sun May 15 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.38.1-owl1
- Added a sample case toggler for cracking MD4-based NTLM hashes (with the
contributed patch), given already cracked DES-based LM hashes.

* Wed May 04 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.38-owl1
- Further updates of the PPC make targets for Mac OS X 10.4+ and Linux/ppc64.

* Wed Apr 27 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.37.11-owl1
- Fixed a long-standing bug in "unshadow" which showed up on recent OpenBSD.
- Added the openbsd-x86-mmx-elf make target.

* Wed Apr 20 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.37.10-owl1
- Fixed a long-standing bug in the loader where "john --show" would segfault
when an invalid or unsupported hash is present in both john.pot and the
password file.

* Wed Apr 20 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.37.9-owl1
- Corrected handling of BSDI-style DES-based hashes and of 8-bit characters
with traditional DES-based hashes; this was broken with the previous change.

* Tue Apr 17 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.37.8-owl1
- Even more bitslice DES set_key*() optimizations: use a separate loop for
undoing the old password beyond the new password's length (this simplifies
the exit check of both loops), store byte offsets into K[] rather than bit
positions in s1[] (this simplifies effective address calculation), quickly
skip over the first 4 characters if they're unchanged (on archs supporting
unaligned accesses only).

* Tue Apr 05 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.37.7-owl1
- Further bitslice DES set_key*() optimizations.

* Mon Feb 28 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.37.6-owl1
- Generic bitslice DES set_key*() optimizations.
- Further AltiVec optimizations for LM hashes.

* Tue Feb 15 2005 Solar Designer <solar-at-owl.openwall.com> 1.6.37.4-owl1
- New make target for 64-bit PowerPC (G5+) running Mac OS X (32-bit
inter-function interfaces).
- New make targets for PowerPC w/ AltiVec (effective 128-bitness for
bitslice DES).

* Tue Nov 09 2004 Solar Designer <solar-at-owl.openwall.com> 1.6.37.3-owl1
- Properly report effective c/s rates in excess of 2**32 (now up to
2**32 * 10**6), report large c/s rates in thousands or millions.

* Sat Jun 19 2004 Solar Designer <solar-at-owl.openwall.com> 1.6.37.2-owl1
- "N passwords cracked" -> "N password hashes cracked" because there can be
multiple hashes per password with LM or double-length DES-based crypt(3).
- Updated some documentation files from John 1.6 and included them in doc/

* Sun Jun 13 2004 Solar Designer <solar-at-owl.openwall.com> 1.6.37.1-owl1
- Freeze the timestamps that are being logged for the duration of loading
of password files; clock is reset to 0 or to the restore point when the
actual cracking starts to ensure the reported c/s rate is not affected by
load time, but we don't want this clock reset to be seen in event logs.

* Mon Feb 23 2004 Solar Designer <solar-at-owl.openwall.com> 1.6.37-owl1
- Bumped the release to 1.6.37 to make it available separately from Owl.

* Sat Jan 10 2004 Solar Designer <solar-at-owl.openwall.com> 1.6.36.9-owl1
- Corrected a segfault with --stdin introduced with 1.6.34.2.

* Wed Dec 03 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.36.8-owl1
- Avoid triggering a Mac OS X cpp bug(?) where it would detect and refuse to
handle "recursive" cpp macros.

* Sun Nov 30 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.36.7-owl1
- When calculating the c/s rate in benchmarks (bench.c, best.c), use 64-bit
integer operations to avoid a possible integer overflow on 32-bit systems
with large CLK_TCK (e.g. Win32).

* Sun Nov 16 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.36.6-owl1
- When generating a new charset file, first do a self-test of the specified
CHARSET_* parameters to ensure they don't cause a 64-bit integer overflow.

* Sat Oct 25 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.36.5-owl1
- In x86 assembly code, detect and choose optimal existing code version for
Centaur Technology processors (IDT Winchip to VIA C3 and beyond).

* Fri Oct 10 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.36.4-owl1
- Also support Matthew Kwan's older DES S-box expressions with standard
gates only, use them for x86-64 and autodetect between them and the
non-standard gates version with "make generic".

* Sun Oct 05 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.36.3-owl1
- Added two make targets for Linux on x86-64, thanks to John Edward Scott.

* Wed Oct 01 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.36.2-owl1
- Replaced mem_free() with a macro to keep gcc 3.3.1's strict aliasing
happy (thanks to Anatoly Pugachev for reporting the gcc warnings).

* Mon Sep 22 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.36.1-owl1
- Support OpenBSD/x86 w/ ELF binaries (Makefile patch by demon).

* Thu Sep 18 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.36-owl1
- Corrected the generic and SPARC make targets broken with 1.6.34.2.

* Mon Sep 15 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.35-owl1
- Log two more events.
- With the AIX make target, use -qunroll=2 instead of plain -qunroll.

* Sun Sep 07 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.34.2-owl1
- Verbose logging; John now logs how it proceeds through stages of each
of its cracking modes, regardless of whether there're guesses or not.

* Mon Aug 25 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.34.1-owl1
- Added an event logging framework; only session start/stop, cracking
modes, and cracked login names are logged currently, but the plan is to
log many more events in the future.

* Sun Jun 29 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.34-owl1
- solaris-sparc64-cc, contributed by Thomas Nau.
- Check for and report invalid MinLen / MaxLen settings.

* Mon Jun 02 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.33-owl2
- Added URL.

* Fri Jan 24 2003 Solar Designer <solar-at-owl.openwall.com> 1.6.33-owl1
- Added a 64-bit Solaris SPARC make target (recent gcc only for now).

* Wed Jan 15 2003 Solar Designer <solar-at-owl.openwall.com>
- Split the 64-bit MIPS target into two such that it is possible to have
64-bit builds which do or don't require at least an R10K CPU.

* Tue Nov 05 2002 Solar Designer <solar-at-owl.openwall.com>
- Workaround a Solaris stdio bug triggered by code in "unique".

* Fri Nov 01 2002 Solar Designer <solar-at-owl.openwall.com>
- Fixed a bug in "unique" which caused it to fail on big-endian boxes
on files bigger than a single buffer, thanks to Corey Becker.

* Sat Oct 19 2002 Solar Designer <solar-at-owl.openwall.com>
- Simplified DES_bs_get_binary_raw().

* Thu Oct 03 2002 Solar Designer <solar-at-owl.openwall.com>
- Never point cfg_name to path_expand()'s result buffer, make a copy.

* Thu Sep 05 2002 Solar Designer <solar-at-owl.openwall.com>
- Never put dupes in crk_guesses, that could overflow it and would be
inefficient anyway.

* Fri Apr 26 2002 Solar Designer <solar-at-owl.openwall.com>
- Check for with_cpu_fallback correctly (unbreak builds on non-x86).

* Thu Apr 11 2002 Solar Designer <solar-at-owl.openwall.com>
- On x86, always build the MMX binary, with a run-time fallback to the
non-MMX one if necessary.

* Wed Apr 10 2002 Solar Designer <solar-at-owl.openwall.com>
- Packaged 1.6.31-dev for Owl, with minor modifications.

# $Id: Owl/packages/glibc/glibc.spec,v 1.67 2004/12/25 20:33:16 galaxy Exp $

%define BUILD_PROFILE 0

Summary: The GNU libc libraries.
Name: glibc
Version: 2.3.2
%define crypt_bf_version 0.4.6
Release: owl3
License: LGPL
Group: System Environment/Libraries
Source0: glibc-%version.tar.bz2
Source1: glibc-linuxthreads-%version.tar.bz2
Source2: crypt_blowfish-%crypt_bf_version.tar.gz
Source3: crypt_freesec.c
Source4: crypt_freesec.h
Patch0: glibc-2.3.2-rh-27.9.7-wo-nptl.diff.bz2
Patch10: glibc-2.3.2-owl-crypt_freesec.diff
# XXX: (GM): ToDo: update sanitize-env patch to reflect all environment
# variable uses found in the current version of glibc.
Patch11: glibc-2.3.2-owl-sanitize-env.diff
Patch12: glibc-2.3.2-owl-res_randomid.diff
Patch13: glibc-2.3.2-owl-iscntrl.diff
Patch14: glibc-2.3.2-owl-quota.diff
Patch15: glibc-2.3.2-owl-ldd.diff
Patch16: glibc-2.3.2-owl-tmp.diff
Patch17: glibc-2.3.2-owl-vitmp.diff
Patch18: glibc-2.3.2-owl-glibcbug-COMMAND.diff
Patch19: glibc-2.3.2-owl-info.diff
Patch20: glibc-2.3.2-owl-syslog-ident.diff
Patch21: glibc-2.3.2-mjt-owl-syslog-timestamp.diff
Patch22: glibc-2.3.2-owl-alt-asprintf-error-handling.diff
Patch23: glibc-2.3.2-owl-alt-fts.diff
Patch24: glibc-2.3.2-owl-resolv-QFIXEDSZ-underfills.diff
Patch25: glibc-2.3.2-owl-realpath-comments.diff
Patch26: glibc-2.3.2-owl-malloc-unlink-sanity-check.diff
Patch30: glibc-2.3.2-suse-resolv-response-length.diff
Requires: /etc/nsswitch.conf
Provides: glibc-crypt_blowfish = %crypt_bf_version, ldconfig
Obsoletes: ldconfig
BuildRoot: /override/%name-%version

%description
The glibc package contains standard libraries which are used by
multiple programs on the system.  In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs.  This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library.  Without these two libraries, a
Linux system will not function.  The glibc package also contains
national language (locale) support and timezone databases.

%package utils
Summary: The GNU libc miscellaneous utilities.
Group: System Environment/Base
Requires: %name >= %version

%description utils
The glibc-utils package contains miscellaneous glibc utilities.

%package devel
Summary: Header and object files for development using standard C libraries.
Group: Development/Libraries
PreReq: /sbin/install-info
Requires: kernel-headers >= 2.2.1
Provides: glibc-crypt_blowfish-devel = %crypt_bf_version
Conflicts: texinfo < 3.11

%description devel
The glibc-devel package contains the header and object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard header and object files available in order to create the
executables.

%if %BUILD_PROFILE
%package profile
Summary: The GNU libc libraries, including support for gprof profiling.
Group: Development/Libraries
Requires: %name = %version-%release

%description profile
The glibc-profile package includes the GNU libc libraries and support
for profiling using the gprof program.  Profiling is analyzing a
program's functions to see how much CPU time they use and determining
which functions are calling other functions during execution.  To use
gprof to profile a program, your program needs to use the GNU libc
libraries included in glibc-profile (instead of the standard GNU libc
libraries included in the glibc package).
%endif

%package compat-fake
Summary: Fake package to help upgrade glibc from 2.1.3 to 2.3+.
Group: System Environment/Libraries
Provides: libdb.so.2
Provides: libdb.so.2(GLIBC_2.0)
Provides: libdb.so.3
Provides: libdb.so.3(GLIBC_2.0)
Provides: libdb.so.3(GLIBC_2.1)

%description compat-fake
This package solves the problem with upgrading glibc 2.1.3 -based Owl to
glibc 2.3+ version by reporting necessary Provides to RPM.  All packages
in glibc 2.3+ -based Owl don't rely on libdb.so.2 and libdb.so.3.  If
you have a package which uses these older libraries, you have to recompile
that package against the db4 package supplied with Owl or create a
compatibility package with necessary binaries of old libdb libraries.

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%prep
%setup -q -a 1 -a 2
patch -p1 < crypt_blowfish-%crypt_bf_version/glibc-%version-crypt.diff
mv crypt/{crypt.h,gnu-crypt.h}
mv crypt_blowfish-%crypt_bf_version/*.[chS] crypt/
cp %_sourcedir/crypt_freesec.[ch] crypt/

# RH9 Update - begin
%patch0 -p1
find . -name configure -exec touch {} \;
# RH9 Update - finish
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch30 -p1
# XXX: check sparcv9 builds and probably fix this for main Owl.
#%ifarch sparcv9
#echo 'ASFLAGS-.os += -Wa,-Av8plusa' >> sysdeps/sparc/sparc32/elf/Makefile
#%endif

cat > find_provides.sh << EOF
#!/bin/sh
/usr/lib/rpm/find-provides | fgrep -v GLIBC_PRIVATE
exit 0
EOF
chmod +x find_provides.sh
cat > find_requires.sh << EOF
#!/bin/sh
/usr/lib/rpm/find-requires | fgrep -v GLIBC_PRIVATE
exit 0
EOF
chmod +x find_requires.sh

%define __find_provides %_builddir/%name-%version/find_provides.sh
%define __find_requires %_builddir/%name-%version/find_requires.sh

%build
# Remove precompiled info manuals to get fresh ones.
# XXX: There're no precompiled info manuals included with current glibc.
#rm manual/libc.info*
# remove stamps
rm manual/stamp-*

rm -rf build-%_target_cpu-linux
mkdir build-%_target_cpu-linux
pushd build-%_target_cpu-linux
CFLAGS="-g %optflags -DNDEBUG=1 -finline-limit=2000" \
../configure \
	--build=%_target_platform --target=%_target_platform \
	--prefix=%_prefix \
	--exec-prefix=%_exec_prefix \
	--bindir=%_bindir \
	--sbindir=%_sbindir \
	--sysconfdir=%_sysconfdir \
	--datadir=%_datadir \
	--includedir=%_includedir \
	--libdir=%_libdir \
	--libexecdir=%_libexecdir \
	--localstatedir=%_localstatedir \
	--sharedstatedir=%_sharedstatedir \
	--mandir=%_mandir \
	--infodir=%_infodir \
%if !%BUILD_PROFILE
	--disable-profile \
%endif
	--enable-add-ons \
	--without-cvs \
	--without-__thread
%__make MAKE="%__make -s"
popd

%__make -C linuxthreads/man

%install
rm -rf %buildroot
mkdir -p %buildroot
%__make install_root=%buildroot install -C build-$RPM_ARCH-linux
pushd build-$RPM_ARCH-linux
%__make install_root=%buildroot install-locales -C ../localedata objdir=`pwd`
popd

# The man pages for linuxthreads and crypt_blowfish require special attention
mkdir -p %buildroot%_mandir/man3
make -C linuxthreads/man
install -m 644 linuxthreads/man/*.3thr %buildroot%_mandir/man3/
make -C crypt_blowfish-%crypt_bf_version man
install -m 644 crypt_blowfish-%crypt_bf_version/*.3 %buildroot%_mandir/man3/

ln -s libbsd-compat.a %buildroot%_libdir/libbsd.a

# /etc/localtime - we're proud of our timezone
rm %buildroot%_sysconfdir/localtime
cp %buildroot%_datadir/zoneinfo/Europe/Moscow %buildroot%_sysconfdir/localtime

# Create empty ldconfig configuration file
> %buildroot%_sysconfdir/ld.so.conf

# The database support
# XXX: why is this disabled?
#mkdir -p %buildroot/var/db
#install -m 644 nss/db-Makefile %buildroot/var/db/Makefile

# BUILD THE FILE LIST
find %buildroot -type f -or -type l |
	sed -e 's|.*%_sysconfdir|%config &|' > rpm.filelist.in
for n in %_includedir %_libdir %_datadir; do
    find %buildroot$n -type d |
	sed 's/^/%dir /' >> rpm.filelist.in
done

# primary filelist
sed "s|^%buildroot||" < rpm.filelist.in |
	sed "s| %buildroot| |" | \
	grep -v '^%dir %_includedir$' | \
	grep -v '^%dir %_libdir$' | \
	grep -v '^%dir %_datadir$' | \
	grep -v '^%dir %_mandir$' | \
	grep -v '^%dir %_infodir$' | \
	grep -v '^%config %_sysconfdir/' | \
	sort > rpm.filelist

%if %BUILD_PROFILE
grep '%_libdir/lib.*_p\.a' < rpm.filelist > profile.filelist
%endif

egrep "(%_includedir)|(%_infodir)" < rpm.filelist |
	grep -v "%_infodir/dir" |
	grep -v "\.info-" |
	sed -e 's|\.info.*$|&\*|' > devel.filelist

mv rpm.filelist rpm.filelist.full
grep -v '%_libdir/lib.*_p.a' rpm.filelist.full |
	egrep -v "(%_includedir)|(%_infodir)" > rpm.filelist

grep '%_libdir/lib.*\.a' < rpm.filelist >> devel.filelist
grep '%_libdir/.*\.o' < rpm.filelist >> devel.filelist
grep '%_libdir/lib.*\.so' < rpm.filelist >> devel.filelist
grep '%_mandir/man' < rpm.filelist | sed -e 's|$|\*|' >> devel.filelist

mv rpm.filelist rpm.filelist.full
grep -v '%_libdir/lib.*\.a' < rpm.filelist.full |
	grep -v '%_bindir/' |
	grep -v '%_sbindir/' |
	grep -v '%_libdir/.*\.o' |
	grep -v '%_libdir/lib.*\.so'|
	grep -v '%_mandir/man' |
	grep -v 'nscd' |
	grep -v 'sln' > rpm.filelist

# The last bit: more documentation
rm -rf documentation
mkdir documentation
cp linuxthreads/ChangeLog documentation/ChangeLog.threads
cp linuxthreads/Changes documentation/Changes.threads
cp linuxthreads/README documentation/README.threads
cp linuxthreads/FAQ.html documentation/FAQ-threads.html
cp -r linuxthreads/Examples documentation/examples.threads
cp timezone/README documentation/README.timezone
cp ChangeLog* documentation
gzip -9nf documentation/ChangeLog*
mkdir documentation/crypt_blowfish-%crypt_bf_version
cp crypt_blowfish-%crypt_bf_version/{README,LINKS,PERFORMANCE} \
	documentation/crypt_blowfish-%crypt_bf_version

# Final step: remove unpackaged files.
rm %buildroot%_infodir/dir
rm %buildroot%_sbindir/nscd
rm %buildroot%_sbindir/nscd_nischeck

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %_infodir/libc.info.gz %_infodir/dir

%preun devel
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/libc.info.gz %_infodir/dir
fi

%files -f rpm.filelist
%defattr(-,root,root)
%doc README NEWS INSTALL FAQ BUGS NOTES PROJECTS
%doc documentation/* README.libm
%doc hesiod/README.hesiod
%doc crypt/README.ufc-crypt
%config(noreplace) %_sysconfdir/localtime
%ghost %config(noreplace) %_sysconfdir/ld.so.cache
%config %_sysconfdir/ld.so.conf
%config(noreplace) %_sysconfdir/rpc
# XXX
#%dir /var/db
%if %BUILD_PROFILE
%exclude %_libdir/*_p.a
%endif

%files utils
%defattr(-,root,root)
/sbin/sln
%_bindir/*
%_sbindir/*

%files devel -f devel.filelist
%defattr(-,root,root)

%if %BUILD_PROFILE
%files profile -f profile.filelist
%defattr(-,root,root)
%endif

%files compat-fake

%changelog
* Wed Dec 08 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.3.2-owl3
- Fixed compat-fake's provides to deal with Owl 1.1 release upgrades

* Wed Dec 08 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.3.2-owl2
- Fixed <sys/quota.h> types (we were using types from linux/types.h instead
of sys/types). Thanks goes to Sergio <sergio@openwall.com>.

* Tue Nov 02 2004 Solar Designer <solar@owl.openwall.com> 2.3.2-owl1
- Corrected the -compat-fake sub-package description.
- Set Release to -owl1 such that we can make it public, then proceed with
further corrections for whatever we've broken with the big update.

* Thu Sep 30 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.3.2-owl0.8
- Added compat-fake sub-package to help upgrade procedure

* Sat Mar 20 2004 Solar Designer <solar@owl.openwall.com> 2.3.2-owl0.7
- Corrections to BUILD_PROFILE support.

* Wed Mar 10 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.3.2-owl0.6
- Moved big rh9 patch to the sources
- Split glibc utility programs into glibc-utils subpackage

* Tue Mar 09 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.3.2-owl0.5
- Updated patch set for 2.3.2 version

* Thu Mar 04 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.3.2-owl0.4
- Spec clean up, added documentation

* Mon Mar 01 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.3.2-owl0.3
- Prepared spec for FHS 2.2

* Thu Feb 24 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.3.2-owl0.2
- Cleaned up spec for building under "stage4" environment.

* Thu Feb 19 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.3.2-owl0.1
- Regenerated crypt_blowfish patch against this version of glibc

* Mon Feb 16 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.3.2-owl0
- Updated to the new version - 2.3.2 (official release); This cannot be used
as primary glibc on system yet due to missing crypt_blowfish.

* Mon Dec 08 2003 Solar Designer <solar@owl.openwall.com> 2.1.3-owl38
- Sanity check the forward and backward chunk pointers in dlmalloc's
unlink() macro, thanks to Stefan Esser for the idea.

* Sun Dec 07 2003 Solar Designer <solar@owl.openwall.com> 2.1.3-owl37
- Allow tmpfile(3) to use $TMPDIR, thanks to the report and patch by
(GalaxyMaster).  Certain other implementations are known to do the same.

* Wed Oct 29 2003 Solar Designer <solar@owl.openwall.com> 2.1.3-owl36
- Added "Provides: glibc-crypt_blowfish-devel" tag to -devel subpackage.
- Dropped the obsolete "Provides: glibc <= 2.1.3-19owl" tag which was
needed during our transition to the new Release numbering scheme.

* Sat Aug 02 2003 Solar Designer <solar@owl.openwall.com> 2.1.3-owl35
- Back-ported a fix from glibc CVS to pass the high and low 32 bits of
file offsets into ftruncate64, truncate64, pread64, and pwrite64
syscalls under the correct endianness.  Of the architectures we support
currently, this only makes a difference for SPARC.  The MIPS-specific
bits of this fix are intentionally not included (we'll probably update
glibc earlier than we might possibly support it).

* Sat Jun 28 2003 Solar Designer <solar@owl.openwall.com> 2.1.3-owl34
- Corrected the comments in stdlib.h for canonicalize_file_name() and
realpath() to not describe behavior that is not actually implemented.

* Sun Jun 22 2003 Solar Designer <solar@owl.openwall.com> 2.1.3-owl33
- Back-ported a fix from glibc CVS to relax the mutex ownership checks
in pthread_cond_wait(3) and related functions.

* Sat Jun 21 2003 Solar Designer <solar@owl.openwall.com> 2.1.3-owl32
- Applied a fix by Dmitry V. Levin to call openlog_internal() with a
NULL ident instead of with LogTag to not cause possible deallocation
of LogTagDynamic.

* Fri May 23 2003 Solar Designer <solar@owl.openwall.com> 2.1.3-owl31
- Moved /etc/nsswitch.conf from glibc to owl-etc package.

* Sun Mar 23 2003 Solar Designer <solar@owl.openwall.com> 2.1.3-owl30
- Included Red Hat's back-port of the Sun RPC XDR integer overflow fixes
from glibc CVS; the fixes are by Paul Eggert and Roland McGrath, and the
xdrmem_getbytes() integer overflow has been discovered by Riley Hassell
of eEye Digital Security.

* Fri Nov 08 2002 Solar Designer <solar@owl.openwall.com>
- Made the x86 assembly code in crypt_blowfish reentrant (this time for
real), added a test for proper operation with multiple threads, made
crypt_blowfish more careful about overwriting sensitive data.
- Cleaned up the default /etc/nsswitch.conf file.  Now it refers to
nsswitch.conf(5) for more information, uses the proper terms instead of
calling everything an "entry" (now we use "databases", name "services",
and "entries" being looked up via NSS), and lists "tcb" among possible
name services and provides an example of its use.

* Tue Oct 01 2002 Solar Designer <solar@owl.openwall.com>
- Avoid read buffer overruns in glibc itself and applications that
naively assume the length returned by res_* is always less than or equal
to the answer buffer size (CERT VU#738331, CVE CAN-2002-1146), by
truncating the answer in res_send(3); the patch is by Olaf Kirch of SuSE.
- Avoid some potential reads beyond end of undersized DNS responses by
making sure they're at least HFIXEDSZ+QFIXEDSZ in size; pointed out by
Dmitry V. Levin of ALT Linux.

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Tue Aug 06 2002 Solar Designer <solar@owl.openwall.com>
- Updated the recent calloc(3) patch to conform to POSIX-2001 wrt the
behavior on elsize == 0.  Pointed out by Sebastian Krahmer of SuSE.

* Sun Aug 04 2002 Solar Designer <solar@owl.openwall.com>
- Made the FreeSec code reentrant, adjusted crypt*(3) wrappers and the
manual page accordingly.

* Thu Aug 01 2002 Solar Designer <solar@owl.openwall.com>
- Patched two potential integer overflows (and thus buffer overflows) in
calloc(3) and xdr_array (the latter discovered by ISS X-Force).

* Fri Jul 05 2002 Solar Designer <solar@owl.openwall.com>
- Added the patch by NISHIMURA Daisuke and Tomohiro 'Tomo-p' KATO of
Vine Linux to fix the DNS resolver buffer overflows affecting both host
and net lookups in the glibc-compat code that is used by binaries built
against glibc 2.0:
http://sources.redhat.com/ml/bug-glibc/2002-07/msg00119.html

* Thu Jul 04 2002 Solar Designer <solar@owl.openwall.com>
- Back-ported the fix to buffer overflow in resolv/nss_dns/dns-network.c
affecting getnetby{addr,name}{,_r}(3) when "dns" is listed on "networks"
line in /etc/nsswitch.conf (which is not the default).
- Improved the code used to produce unpredictable DNS query IDs to make
it generate different sequences of IDs in forked processes (problem
noted by Jarno Huuskonen), conserve the kernel's randomness pool (based
on feedback from Michael Tokarev), and properly reseed when chrooted.

* Thu Jul 04 2002 Michail Litvak <mci@owl.openwall.com>
- patch to build with new texinfo

* Wed Jun 12 2002 Solar Designer <solar@owl.openwall.com>
- ldd(1) will no longer try to invoke programs directly, even when it
seems like that would work.  The dynamic linker will be invoked as a
program instead.  This makes a difference when the program is SGID and
is being ldd'ed by root.  If the program was executed directly, glibc
would detect its SGID status and drop LD_* variables, resulting in the
program being actually started rather than ldd'ed.  Thanks to Dmitry
V. Levin of ALT Linux for suggesting this solution.
- Use ctime_r() instead of strftime_r() in syslog(3) so that month names
will not depend on current locale settings.  The patch is originally by
Michael Tokarev, with modifications to apply to our glibc.
- glibcbug: use mktemp(1) in a fail-close way, let it use $TMPDIR, default
to vitmp(1) for the editor.
- crypt_blowfish-0.4.3 (documentation updates, a check to produce better
code for PA-RISC).

* Mon Feb 04 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Dec 14 2001 Solar Designer <solar@owl.openwall.com>
- Back-ported a glob(3) buffer overflow fix from the CVS; the bug has been
discovered and an initial patch produced by Flavio Veloso of Magnux.
- Applied fixes to vasprintf(3) (thus affecting asprintf(3) as well) to
make it behave on errors, changed the semantics to match Todd Miller's
implementation on *BSD, fixed uses of [v]asprintf(3) in glibc itself to
handle possible errors.  Thanks to Dmitry V. Levin of ALT Linux for
discovering and looking into these issues.
- Updated to crypt_blowfish-0.4.2 (more man page fixes).

* Thu Nov 08 2001 Solar Designer <solar@owl.openwall.com>
- If syslog(3) is called by a SUID/SGID program without a preceding call to
openlog(3), don't blindly trust __progname for the syslog ident.

* Fri Jul 06 2001 Solar Designer <solar@owl.openwall.com>
- Corrected the declaration of struct dqstats in <sys/quota.h>.

* Wed Jun 13 2001 Solar Designer <solar@owl.openwall.com>
- Back-ported a patch from the CVS to handle unaligned relocations on Alpha.
References:
http://bugs.debian.org/43401
http://www.alphalinux.org/archives/debian-alpha/February2000/0183.html
http://www.alphalinux.org/archives/debian-alpha/February2000/0197.html
http://gcc.gnu.org/ml/gcc/1999-07n/msg00968.html
http://gcc.gnu.org/ml/gcc/1999-07n/msg01041.html

* Sun Jun 03 2001 Solar Designer <solar@owl.openwall.com>
- Sync the fts(3) routines with current OpenBSD and FreeBSD; this is
triggered by Nick Cleaton's report of yet another FTS vulnerability
to FreeBSD, and a discussion with Kris Kennaway and Todd Miller.  It
should no longer be possible to trick FTS into leaving the intended
directory hierarchy, but DoS attacks on FTS itself remain possible.
- Updated to crypt_blowfish-0.4.1 (man page fixes).

* Thu May 10 2001 Solar Designer <solar@owl.openwall.com>
- Updated to crypt_blowfish-0.4 (release).

* Fri May 04 2001 Solar Designer <solar@owl.openwall.com>
- Updated to crypt_blowfish-0.3.9, which adds crypt_ra, crypt_gensalt_ra
and an up-to-date crypt(3) man page.

* Sat Apr 07 2001 Solar Designer <solar@owl.openwall.com>
- Force known control characters for iscntrl(3) (in localedef and C locale).

* Thu Jan 11 2001 Solar Designer <solar@owl.openwall.com>
- Sanitize the environment in a paranoid way (this was meant to be delayed
until we add a configuration file, but well...).

* Wed Jan 10 2001 Solar Designer <solar@owl.openwall.com>
- Included several critical dynamic linker security fixes from the CVS.

* Tue Jan 02 2001 Solar Designer <solar@owl.openwall.com>
- Back-ported the mktemp, tempnam, tmpnam, and tmpnam_r link_warning's.

* Fri Nov 17 2000 Solar Designer <solar@owl.openwall.com>
- 'ASFLAGS-.os += -Wa,-Av8plusa' for sparcv9.

* Thu Sep 07 2000 Solar Designer <solar@owl.openwall.com>
- Added optflags_lib support and _target_platform to configure.

* Fri Sep 01 2000 Solar Designer <solar@owl.openwall.com>
- One more security fix (locale once again) from the CVS version.
- Fixed a bug in crypt_gensalt*() reported by Michael Tokarev.

* Fri Aug 25 2000 Solar Designer <solar@owl.openwall.com>
- Back-ported 3 security-related fixes from the CVS version.

* Sun Aug 06 2000 Solar Designer <solar@owl.openwall.com>
- Added FreeSec (as a patch) to support extended/new-style/BSDI password
hashes in crypt(3) (but not in the reentrant versions; this is a hack).
- The building of profiling libraries is now optional and disabled by
default.

* Fri Jul 14 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import syslog fix from RH
- import time fix from RH
- import timezone fixes from RH
- import ldd patch to handle non-executable shared objects. (mdk)
- import ucontext.h patch from mdk

* Wed Jul 12 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- paths patch from RH
- import libNoVersion from RH
- import xdr_ypall patch (RH bug id #249)
- import linuxthreads patches from RH
- import nis malloc fixes from RH
- import some little fixes from RH
- import cp1251 locales from BCL

* Sun Jun 18 2000 Solar Designer <solar@owl.openwall.com>
- import this spec from RH, and make it use the original glibc 2.1.3
code with Owl patches only; libNoVersion and other RH hacks may be added
at a later stage.

# $Id: Owl/packages/glibc/glibc.spec,v 1.30 2002/06/12 00:55:34 solar Exp $

%define BUILD_PROFILE 0

Summary: The GNU libc libraries.
Name: glibc
Version: 2.1.3
%define crypt_bf_version 0.4.3
Release: owl21
License: LGPL
Group: System Environment/Libraries
Source0: glibc-%{version}.tar.gz
Source1: glibc-linuxthreads-%{version}.tar.gz
Source2: glibc-crypt-2.1.tar.gz
Source3: nsswitch.conf
Source4: glibc-compat-%{version}.tar.gz
Source5: crypt_blowfish-%{crypt_bf_version}.tar.gz
Source6: crypt_freesec.c
Patch0: glibc-2.1.3-owl-freesec-hack.diff
Patch1: glibc-2.1.3-owl-dl-open.diff
Patch2: glibc-2.1.3-owl-sanitize-env.diff
Patch3: glibc-2.1.3-owl-res_randomid.diff
Patch4: glibc-2.1.3-owl-iscntrl.diff
Patch5: glibc-2.1.3-openbsd-freebsd-owl-fts.diff
Patch6: glibc-2.1.3-owl-quota.diff
Patch7: glibc-2.1.3-owl-syslog-ident.diff
Patch8: glibc-2.1.3-owl-alt-asprintf-error-handling.diff
Patch10: glibc-2.1.3-rh-libnoversion.diff
Patch11: glibc-2.1.3-rh-paths.diff
Patch12: glibc-2.1.3-rh-linuxthreads.diff
Patch13: glibc-2.1.3-rh-nis-malloc.diff
Patch14: glibc-2.1.3-rh-c-type.diff
Patch15: glibc-2.1.3-rh-cppfix.diff
Patch16: glibc-2.1.3-rh-db2-closedir.diff
Patch17: glibc-2.1.3-rh-glob.diff
Patch18: glibc-2.1.3-rh-localedata.diff
Patch19: glibc-2.1.3-rh-yp_xdr.diff
Patch20: glibc-2.1.3-rh-makeconfig.diff
Patch21: glibc-2.1.3-rh-time.diff
Patch22: glibc-2.1.3-rh-timezone.diff
Patch23: glibc-2.1.3-rh-syslog.diff
Patch30: glibc-2.1.3-bcl-cyr-locale.diff
Patch31: glibc-2.1.3-mdk-fix-ucontext.diff
Patch32: glibc-2.1.3-mdk-ldd.diff
Patch40: glibc-2.1.3-cvs-20000827-locale.diff
Patch41: glibc-2.1.3-cvs-20000824-unsetenv.diff
Patch42: glibc-2.1.3-cvs-20000824-md5-align-clean.diff
Patch43: glibc-2.1.3-cvs-20000926-tmp-warnings.diff
Patch44: glibc-2.1.3-cvs-20010109-dl.diff
Patch45: glibc-2.1.3-cvs-20000929-alpha-reloc.diff
Patch46: glibc-2.1.3-cvs-20011129-glob.diff
PreReq: /sbin/ldconfig
%ifarch alpha
Provides: ld.so.2
%endif
Provides: glibc-crypt_blowfish = %{crypt_bf_version}, glibc <= 2.1.3-19owl
AutoReq: false
BuildRoot: /override/%{name}-%{version}

%description
The glibc package contains standard libraries which are used by
multiple programs on the system.  In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs.  This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library.  Without these two libraries, a
Linux system will not function.  The glibc package also contains
national language (locale) support and timezone databases.

%package devel
Summary: Header and object files for development using standard C libraries.
Group: Development/Libraries
Conflicts: texinfo < 3.11
PreReq: /sbin/install-info
Requires: kernel-headers >= 2.2.1
AutoReq: true

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

%description profile
The glibc-profile package includes the GNU libc libraries and support
for profiling using the gprof program.  Profiling is analyzing a
program's functions to see how much CPU time they use and determining
which functions are calling other functions during execution.  To use
gprof to profile a program, your program needs to use the GNU libc
libraries included in glibc-profile (instead of the standard GNU libc
libraries included in the glibc package).
%endif

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%prep
%setup -q -a 1 -a 2 -a 4 -a 5
patch -p1 < crypt_blowfish-%{crypt_bf_version}/glibc-%{version}-crypt.diff
mv crypt/sysdeps/unix/{crypt.h,gnu-crypt.h}
mv crypt_blowfish-%{crypt_bf_version}/*.[chS] crypt/sysdeps/unix/
cp $RPM_SOURCE_DIR/crypt_freesec.c crypt/sysdeps/unix/
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
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
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch40 -p1
%patch41 -p1
cd md5-crypt
%patch42 -p2
cd ..
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%ifarch sparcv9
echo 'ASFLAGS-.os += -Wa,-Av8plusa' >> sysdeps/sparc/sparc32/elf/Makefile
%endif

%build
rm -rf build-$RPM_ARCH-linux
mkdir build-$RPM_ARCH-linux
cd build-$RPM_ARCH-linux
%if %BUILD_PROFILE
CFLAGS="-g $RPM_OPT_FLAGS" ../configure --prefix=/usr \
	--enable-add-ons=yes --without-cvs \
	%_target_platform
%else
CFLAGS="-g $RPM_OPT_FLAGS" ../configure --prefix=/usr \
	--enable-add-ons=yes --without-cvs --disable-profile \
	%_target_platform
%endif
make MAKE='make -s'

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install_root=$RPM_BUILD_ROOT install -C build-$RPM_ARCH-linux
pushd build-$RPM_ARCH-linux
make install_root=$RPM_BUILD_ROOT install-locales -C ../localedata objdir=`pwd`
popd

# the man pages for linuxthreads and crypt_blowfish require special attention
mkdir -p $RPM_BUILD_ROOT/usr/man/man3
make -C linuxthreads/man
install -m 0644 linuxthreads/man/*.3thr $RPM_BUILD_ROOT/usr/man/man3
make -C crypt_blowfish-%{crypt_bf_version} man
install -m 0644 crypt_blowfish-%{crypt_bf_version}/*.3 \
	$RPM_BUILD_ROOT/usr/man/man3

# Have to compress them explicitly for the filelists we build
gzip -9nf $RPM_BUILD_ROOT/usr/{man/man3/*,info/libc*}

ln -sf libbsd-compat.a $RPM_BUILD_ROOT/usr/lib/libbsd.a

install -m 644 $RPM_SOURCE_DIR/nsswitch.conf \
	$RPM_BUILD_ROOT/etc/nsswitch.conf

# Take care of setuids
chmod 755 $RPM_BUILD_ROOT/usr/libexec/pt_chown

# The database support
mkdir -p $RPM_BUILD_ROOT/var/db
install -m 644 nss/db-Makefile $RPM_BUILD_ROOT/var/db/Makefile

# Backwards compatibility only and unaudited
rm -f $RPM_BUILD_ROOT/usr/sbin/utmpd

# Strip binaries
strip $RPM_BUILD_ROOT/sbin/* || :
strip $RPM_BUILD_ROOT/usr/bin/* || :
strip $RPM_BUILD_ROOT/usr/sbin/* || :

# BUILD THE FILE LIST
find $RPM_BUILD_ROOT -type f -or -type l |
	sed -e 's|.*/etc|%config &|' > rpm.filelist.in
for n in /usr/share /usr/include; do
    find ${RPM_BUILD_ROOT}${n} -type d | \
	sed "s/^/%dir /" >> rpm.filelist.in
done

# primary filelist
sed "s|^$RPM_BUILD_ROOT||" < rpm.filelist.in |
	sed "s| $RPM_BUILD_ROOT| |" | \
	grep -v '^%dir /usr/share$' | \
	grep -v '^%config /etc/localtime' | \
	grep -v '^%config /etc/nsswitch.conf' | \
	sort > rpm.filelist

%if %BUILD_PROFILE
grep '/usr/lib/lib.*_p\.a' < rpm.filelist > profile.filelist
%endif

egrep "(/usr/include)|(/usr/info)" < rpm.filelist |
	grep -v /usr/info/dir > devel.filelist

mv rpm.filelist rpm.filelist.full
grep -v '/usr/lib/lib.*_p.a' rpm.filelist.full |
	egrep -v "(/usr/include)|(/usr/info)" > rpm.filelist

grep '/usr/lib/lib.*\.a' < rpm.filelist >> devel.filelist
grep '/usr/lib/.*\.o' < rpm.filelist >> devel.filelist
grep '/usr/lib/lib.*\.so' < rpm.filelist >> devel.filelist
grep '/usr/man/man' < rpm.filelist >> devel.filelist

mv rpm.filelist rpm.filelist.full
grep -v '/usr/lib/lib.*\.a' < rpm.filelist.full |
	grep -v '/usr/lib/.*\.o' |
	grep -v '/usr/lib/lib.*\.so'|
	grep -v '/usr/man/man' |
	grep -v 'nscd' > rpm.filelist

# /etc/localtime - we're proud of our timezone
rm -f $RPM_BUILD_ROOT/etc/localtime
cp -f $RPM_BUILD_ROOT/usr/share/zoneinfo/Europe/Moscow $RPM_BUILD_ROOT/etc/localtime

# the last bit: more documentation
rm -rf documentation
mkdir documentation
cp linuxthreads/ChangeLog  documentation/ChangeLog.threads
cp linuxthreads/Changes documentation/Changes.threads
cp linuxthreads/README documentation/README.threads
cp linuxthreads/FAQ.html documentation/FAQ-threads.html
cp -r linuxthreads/Examples documentation/examples.threads
cp crypt/README documentation/README.crypt
cp db2/README documentation/README.db2
cp db2/mutex/README documentation/README.db2.mutex
cp timezone/README documentation/README.timezone
cp ChangeLog* documentation
gzip -9nf documentation/ChangeLog*
mkdir documentation/crypt_blowfish-%{crypt_bf_version}
cp crypt_blowfish-%{crypt_bf_version}/{README,LINKS,PERFORMANCE} \
	documentation/crypt_blowfish-%{crypt_bf_version}

%clean
rm -rf $RPM_BUILD_ROOT
rm -f *.filelist*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info /usr/info/libc.info.gz /usr/info/dir

%preun devel
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete /usr/info/libc.info.gz /usr/info/dir
fi

%files -f rpm.filelist
%defattr(-,root,root)
%config(noreplace) /etc/localtime
%config(noreplace) /etc/nsswitch.conf
%doc README NEWS INSTALL FAQ BUGS NOTES PROJECTS
%doc documentation/* README.libm
%doc hesiod/README.hesiod
%dir /var/db

%files -f devel.filelist devel
%defattr(-,root,root)

%if %BUILD_PROFILE
%files -f profile.filelist profile
%defattr(-,root,root)
%endif

%changelog
* Wed Jun 12 2002 Solar Designer <solar@owl.openwall.com>
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

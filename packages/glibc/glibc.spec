# $Id: Owl/packages/glibc/glibc.spec,v 1.10 2000/09/08 18:27:25 solar Exp $

%define BUILD_PROFILE	'no'

Summary: The GNU libc libraries.
Name: glibc
Version: 2.1.3
Release: 7owl
Copyright: LGPL
Group: System Environment/Libraries
Source0: glibc-2.1.3.tar.gz
Source1: glibc-linuxthreads-2.1.3.tar.gz
Source2: glibc-crypt-2.1.tar.gz
Source3: nsswitch.conf
Source4: glibc-compat-2.1.3.tar.gz
Patch0: glibc-2.1.3-owl-dl-open.diff
Patch1: glibc-2.1.3-owl-malloc-check.diff
Patch2: glibc-2.1.3-owl-res_randomid.diff
Patch3: glibc-2.1.3-owl-blowfish.diff
Patch4: glibc-2.1.3-owl-freesec-hack.diff
Patch5: glibc-2.1.3-rh-libnoversion.diff
Patch6: glibc-2.1.3-rh-paths.diff
Patch7: glibc-2.1.3-rh-linuxthreads.diff
Patch8: glibc-2.1.3-rh-nis-malloc.diff
Patch9: glibc-2.1.3-rh-c-type.diff
Patch10: glibc-2.1.3-rh-cppfix.diff
Patch11: glibc-2.1.3-rh-db2-closedir.diff
Patch12: glibc-2.1.3-rh-glob.diff
Patch13: glibc-2.1.3-rh-localedata.diff
Patch14: glibc-2.1.3-rh-yp_xdr.diff
Patch15: glibc-2.1.3-rh-makeconfig.diff
Patch16: glibc-2.1.3-bcl-cyr-locale.diff
Patch17: glibc-2.1.3-mdk-fix-ucontext.diff
Patch18: glibc-2.1.3-mdk-ldd.diff
Patch19: glibc-2.1.3-rh-time.diff
Patch20: glibc-2.1.3-rh-timezone.diff
Patch21: glibc-2.1.3-rh-syslog.diff
Patch22: glibc-2.1.3-cvs-20000827-locale.diff
Patch23: glibc-2.1.3-cvs-20000824-unsetenv.diff
Patch24: glibc-2.1.3-cvs-20000824-md5-align-clean.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Autoreq: false
%ifarch alpha
Provides: ld.so.2
%endif

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
Prereq: /sbin/install-info
Prereq: kernel-headers
Requires: kernel-headers >= 2.2.1
Autoreq: true

%description devel
The glibc-devel package contains the header and object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard header and object files available in order to create the
executables.

Install glibc-devel if you are going to develop programs which will
use the standard C libraries.

%if "%{BUILD_PROFILE}"=="'yes'"
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

If you are going to use the gprof program to profile a program, you'll
need to install the glibc-profile program.
%endif

# Use %optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%prep
%setup -q -a 1 -a 2 -a 4
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
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
cd md5-crypt
%patch24 -p2

%build
rm -rf build-$RPM_ARCH-linux
mkdir build-$RPM_ARCH-linux
cd build-$RPM_ARCH-linux
%if "%{BUILD_PROFILE}"=="'yes'"
CFLAGS="-g $RPM_OPT_FLAGS" ../configure --prefix=/usr \
	--enable-add-ons=yes \
	%_target_platform
%else
CFLAGS="-g $RPM_OPT_FLAGS" ../configure --prefix=/usr \
	--enable-add-ons=yes --disable-profile \
	%_target_platform
%endif
make MAKE='make -s'

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install_root=$RPM_BUILD_ROOT install -C build-$RPM_ARCH-linux
cd build-$RPM_ARCH-linux && \
    make install_root=$RPM_BUILD_ROOT install-locales -C ../localedata objdir=`pwd` && \
    cd ..

# the man pages for the linuxthreads require special attention
make -C linuxthreads/man
mkdir -p $RPM_BUILD_ROOT/usr/man/man3
install -m 0644 linuxthreads/man/*.3thr $RPM_BUILD_ROOT/usr/man/man3
gzip -9nvf $RPM_BUILD_ROOT/usr/man/man3/*

gzip -9nvf $RPM_BUILD_ROOT/usr/info/libc*

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

%if "%{BUILD_PROFILE}"=="'yes'"
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
gzip -9 documentation/ChangeLog*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info /usr/info/libc.info.gz /usr/info/dir

%preun devel
if [ "$1" = 0 ]; then
    /sbin/install-info --delete /usr/info/libc.info.gz /usr/info/dir
fi

%clean
rm -rf "$RPM_BUILD_ROOT"
rm -f *.filelist*

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

%if "%{BUILD_PROFILE}"=="'yes'"
%files -f profile.filelist profile
%defattr(-,root,root)
%endif

%changelog
* Thu Sep 07 2000 Solar Designer <solar@owl.openwall.com>
- Added %optflags_lib support and %_target_platform to configure.

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

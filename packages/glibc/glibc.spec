Summary: The GNU libc libraries.
Name: glibc
Version: 2.1.3
Release: 1owl
Copyright: LGPL
Group: System Environment/Libraries
Source0: glibc-2.1.3.tar.gz
Source1: glibc-linuxthreads-2.1.3.tar.gz
Source2: glibc-crypt-2.1.tar.gz
Source3: nsswitch.conf
Patch0: glibc-2.1.3-owl-dl-open.diff
Patch1: glibc-2.1.3-owl-malloc-check.diff
Patch2: glibc-2.1.3-owl-res_randomid.diff
Patch3: glibc-2.1.3-owl-blowfish.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Autoreq: false
%ifarch alpha
Provides: ld.so.2
%endif

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
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

%prep
%setup -q -a 1 -a 2
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
 
%build
rm -rf build-$RPM_ARCH-linux
mkdir build-$RPM_ARCH-linux ; cd build-$RPM_ARCH-linux
CFLAGS="-g $RPM_OPT_FLAGS" ../configure --prefix=/usr \
	--enable-add-ons %{_target_cpu}-redhat-linux
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

grep '/usr/lib/lib.*_p\.a' < rpm.filelist > profile.filelist
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

%files -f profile.filelist profile
%defattr(-,root,root)

%changelog
* Sun Jun 18 2000 Solar Designer <solar@false.com>
- import this spec from RH, and make it use the original glibc 2.1.3
  code with Owl patches only; libNoVersion and other RH hacks may be
  added at a later stage.

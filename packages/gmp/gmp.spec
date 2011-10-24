# $Owl: Owl/packages/gmp/gmp.spec,v 1.5 2011/10/24 18:19:31 solar Exp $

Summary: The GNU multiple precision arithmetic library.
Name: gmp
Version: 5.0.2
Release: owl1
Epoch: 1
License: LGPLv3+
Group: System Environment/Libraries
URL: http://gmplib.org
Source0: gmp-%version.tar.xz
# ftp://ftp.gnu.org/pub/gnu/gmp/gmp-%version.tar.bz2
# Signature: ftp://ftp.gmplib.org/pub/gmp-%version/gmp-%version.tar.bz2.sig
Source1: gmp.h
Source2: gmp-mparam.h
BuildRequires: autoconf automake libtool
BuildRoot: /override/%name-%version
Provides: libgmp.so.3%(test %_lib = lib64 && echo -n '()(64bit)')

%description
GMP is a free library for arbitrary precision arithmetic, operating on signed
integers, rational numbers, and floating point numbers.  There is no practical
limit to the precision except the ones implied by the available memory in the
machine GMP runs on.  GMP has a rich set of functions, and the functions have a
regular interface.

The main target applications for GMP are cryptography applications and
research, Internet security applications, algebra systems, computational
algebra research, etc.

GMP is carefully designed to be as fast as possible, both for small operands
and for huge operands.  The speed is achieved by using full machine words as
the basic arithmetic type, by using fast algorithms, with highly optimized
assembly code for the most common inner loops for a lot of CPUs, and by a
general emphasis on speed.

%package devel
Summary: Development files for the GMP library.
Group: Development/Libraries
Requires: %name = %epoch:%version-%release
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description devel
Header files, static libraries, and documentation for using the GNU multiple
precision arithmetic library in applications.

%prep
%setup -q

%build
autoreconf -if

# GMP does not require an executable stack despite of its use of hand-written
# assembly sources.
export CCAS='%__cc -c -Wa,--noexecstack'

mkdir base
cd base
ln -s ../configure .

export CFLAGS='%optflags'
export CXXFLAGS='%optflags'
./configure --build=%_build --host=%_host \
	--program-prefix=%?_program_prefix \
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
	--enable-mpbsd \
	--enable-cxx

perl -pi -e 's|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=\"-L\\\$libdir\"|g;' libtool
export LD_LIBRARY_PATH=`pwd`/.libs
%__make

%if 0
#%ifarch %ix86
cd ..
mkdir build-sse2
cd build-sse2
ln -s ../configure .
CFLAGS="%optflags -march=pentium4"
./configure --build=%_build --host=%_host \
	--program-prefix=%?_program_prefix \
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
	--enable-mpbsd \
	--enable-cxx

perl -pi -e 's|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=\"-L\\\$libdir\"|g;' libtool
export LD_LIBRARY_PATH=`pwd`/.libs
%__make
%endif

%install
rm -rf %buildroot

cd base
export LD_LIBRARY_PATH=`pwd`/.libs
%__make install DESTDIR=%buildroot
install -m 644 gmp-mparam.h %buildroot%_includedir
rm -f %buildroot%_libdir/lib{gmp,mp,gmpxx}.la
rm -f %buildroot%_infodir/dir
/sbin/ldconfig -n %buildroot%_libdir
ln -sf libgmpxx.so.4 %buildroot%_libdir/libgmpxx.so
ln -s libgmp.so %buildroot%_libdir/libgmp.so.3

%if 0
#%ifarch %ix86
cd ../build-sse2
export LD_LIBRARY_PATH=`pwd`/.libs
mkdir %buildroot%_libdir/sse2
install -m 755 .libs/libgmp.so.*.* %buildroot%_libdir/sse2
cp -a .libs/libgmp.so.[^.]* %buildroot%_libdir/sse2
chmod 755 %buildroot%_libdir/sse2/libgmp.so.[^.]*
install -m 755 .libs/libgmpxx.so.*.* %buildroot%_libdir/sse2
cp -a .libs/libgmpxx.so.? %buildroot%_libdir/sse2
chmod 755 %buildroot%_libdir/sse2/libgmpxx.so.?
install -m 755 .libs/libmp.so.*.* %buildroot%_libdir/sse2
cp -a .libs/libmp.so.? %buildroot%_libdir/sse2
chmod 755 %buildroot%_libdir/sse2/libmp.so.?
%endif

cd ..

# Rename gmp.h to gmp-<arch>.h and gmp-mparam.h to gmp-mparam-<arch>.h to
# avoid file conflicts on multilib systems, and install wrapper include files
# gmp.h and gmp-mparam.h.
basearch=%_arch
# always use i386 for iX86
%ifarch %ix86
basearch=i386
%endif
# always use arm for arm*
%ifarch %arm
basearch=arm
%endif
# superH architecture support
%ifarch sh3 sh4
basearch=sh
%endif
# Rename files and install wrappers
mv %buildroot/%_includedir/gmp.h %buildroot/%_includedir/gmp-${basearch}.h
install -pm644 %_sourcedir/gmp.h %buildroot/%_includedir/
mv %buildroot/%_includedir/gmp-mparam.h \
    %buildroot/%_includedir/gmp-mparam-${basearch}.h
install -pm644 %_sourcedir/gmp-mparam.h %buildroot/%_includedir/

%check
cd base
export LD_LIBRARY_PATH=`pwd`/.libs
%__make check
%if 0
#%ifarch %ix86
# Test SSE2 libraries only if either the build host's CPU supports SSE2 or we
# can't determine whether it does.
if ! [ -r /proc/cpuinfo ] || grep -q '^flags.* sse2' /proc/cpuinfo; then
	cd ../build-sse2
	export LD_LIBRARY_PATH=`pwd`/.libs
	%__make check
fi
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %_infodir/gmp.info.gz %_infodir/dir || :

%preun devel
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gmp.info.gz %_infodir/dir || :
fi

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LIB NEWS README
%_libdir/libgmp.so.*
%_libdir/libmp.so.*
%_libdir/libgmpxx.so.*
%if 0
#%ifarch %ix86
%_libdir/sse2/*
%endif

%files devel
%defattr(-,root,root,-)
%_libdir/libmp.so
%_libdir/libgmp.so
%_libdir/libgmpxx.so
%_includedir/*.h
%_infodir/gmp.info*
%_libdir/libmp.a
%_libdir/libgmp.a
%_libdir/libgmpxx.a

%changelog
* Mon Oct 24 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 5.0.2-owl1
- Updated to 5.0.2.
- Multilib support for gmp-devel.

* Fri Oct 21 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 4.3.2-owl1
- Initial import from Fedora.

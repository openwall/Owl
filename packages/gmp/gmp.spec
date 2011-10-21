# $Owl: Owl/packages/gmp/gmp.spec,v 1.1 2011/10/21 17:02:44 segoon Exp $

#
# Important for %ix86:
# This rpm should be built on a CPU with sse2 support like Pentium 4.
# Otherwise, sse2 tests will be skipped.

Summary: A GNU arbitrary precision library.
Name: gmp
Version: 4.3.2
Release: owl1
Epoch: 1
License: LGPLv3+
Group: System Environment/Libraries
URL: http://gmplib.org/
Source0: ftp://ftp.gnu.org/pub/gnu/gmp/gmp-%version.tar.bz2
# Signature: ftp://ftp.gmplib.org/pub/gmp-%version/gmp-%version.tar.bz2.sig
BuildRequires: autoconf automake libtool
BuildRoot: /override/%name-%version

%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

Install the gmp package if you need a fast arbitrary precision
library.

%package devel
Summary: Development tools for the GNU MP arbitrary precision librar.
Group: Development/Libraries
Requires: %name = %epoch:%version-%release
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description devel
The libraries, header files and documentation for using the GNU MP 
arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

%prep
%setup -q

%build
autoreconf -if

# the object files do not require an executable stack
export CCAS="%__cc -c -Wa,--noexecstack"

mkdir base
cd base
ln -s ../configure .

export CFLAGS="%optflags"
export CXXFLAGS="%optflags"
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
cd ..
%ifarch %ix86
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
cd ..
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
cd ..
%ifarch %ix86
cd build-sse2
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
cd ..
%endif

# Rename gmp.h to gmp-<arch>.h and gmp-mparam.h to gmp-mparam-<arch>.h to 
# avoid file conflicts on multilib systems and install wrapper include files
# gmp.h and gmp-mparam-<arch>.h
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

# Looks like it's redundant for x86 - segoon
#mv %buildroot/%_includedir/gmp.h %buildroot/%_includedir/gmp-${basearch}.h
#install -m644 %SOURCE2 %buildroot/%_includedir/gmp.h
#mv %buildroot/%_includedir/gmp-mparam.h %buildroot/%_includedir/gmp-mparam-${basearch}.h
#install -m644 %SOURCE3 %buildroot/%_includedir/gmp-mparam.h


%check
%ifnarch ppc
cd base
export LD_LIBRARY_PATH=`pwd`/.libs
%__make check
cd ..
%endif
%ifarch %ix86
# Test SSE2 libraries only if we either have SSE2 CPU support
# or we don't know whether we have it.
if ! [ -e /proc/cpuinfo ] || grep -q sse2 /proc/cpuinfo; then
    cd build-sse2
    export LD_LIBRARY_PATH=`pwd`/.libs
    %__make check
    cd ..
fi
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %_infodir/gmp.info.gz %_infodir/dir || :
exit 0

%preun devel
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gmp.info.gz %_infodir/dir || :
fi
exit 0

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LIB NEWS README
%_libdir/libgmp.so.*
%_libdir/libmp.so.*
%_libdir/libgmpxx.so.*
%ifarch %ix86
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
* Fri Oct 21 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 4.3.2-owl1
- Initial import from Fedora.

# $Id: Owl/packages/gcc/gcc.spec,v 1.33 2004/11/02 02:58:32 solar Exp $

# The only supported frontend for now is GXX.
# G77, JAVA, and OBJC frontends build, but were not tested.
# Ada95 is not supported yet (and does not build).
# Testsuite is not supported because of its requirement for additional
# packages to run (dejagnu, tcl, expect).
%define BUILD_GXX 1
%define BUILD_G77 0
%define BUILD_JAVA 0
%define BUILD_OBJC 0
%define BUILD_ADA 0
%define BUILD_TESTSUITE 0

# Do we need libstdc++-compat libraries?
%define BUILD_CXX_COMPAT 1

# If this variable is set to non-zero, then all support libraries
# will be placed into %_libdir/gcc-lib/%_target_platform/%_version
# sub-directory (allowing to have several binary incompatible
# versions of compilers).
%define USE_VERSION_SPECIFIC_LIBS 0

# Use or not Boehm's Garbage Collector in ObjC compiler frontend.
# Note: Boehm's GC is included in Java frontend source tarball, we
# may find a nice solution in the future to enable builds of ObjC
# frontend with this GC without requiring Java frontend build.
%define USE_BOEHM_GC 0

Summary: C compiler from the GNU Compiler Collection.
Name: gcc
Version: 3.2.2
Release: owl2
Epoch: 1
License: GPL
Group: Development/Languages
URL: http://gcc.gnu.org
Source0: ftp://ftp.gnu.org/gnu/gcc/gcc-core-%version.tar.bz2
%if %BUILD_ADA
Source1: ftp://ftp.gnu.org/gnu/gcc/gcc-ada-%version.tar.bz2
%endif
%if %BUILD_GXX
Source2: ftp://ftp.gnu.org/gnu/gcc/gcc-g++-%version.tar.bz2
%endif
%if %BUILD_G77
Source3: ftp://ftp.gnu.org/gnu/gcc/gcc-g77-%version.tar.bz2
%endif
%if %BUILD_JAVA
Source4: ftp://ftp.gnu.org/gnu/gcc/gcc-java-%version.tar.bz2
%endif
%if %BUILD_OBJC
Source5: ftp://ftp.gnu.org/gnu/gcc/gcc-objc-%version.tar.bz2
%endif
%if %BUILD_TESTSUITE
Source6: ftp://ftp.gnu.org/gnu/gcc/gcc-testsuite-%version.tar.bz2
%endif
%if %BUILD_CXX_COMPAT
# 2.7.2.8, 2.8.0, 2.9.0 (Red Hat Linux 6.2 and below)
Source7: libstdc++-compat.tar.bz2
# 2.95.3 (Owl 1.0, 1.1)
Source8: libstdc++-compat-2.95.3-i386.tar.bz2
%endif
PreReq: /sbin/ldconfig, /sbin/install-info
# This is the version of binutils we have tested this package with; older
# ones might work, but were not tested.
Requires: binutils >= 2.10.1.0.4
Requires: cpp = %version-%release
Obsoletes: egcs
BuildRoot: /override/%name-%version

%description
The gcc package contains C compiler from the GNU Compiler Collection,
as well as documentation which is not limited to just the C compiler.

%package -n cpp
Summary: GNU C preprocessor.
Group: Development/Languages
PreReq: /sbin/install-info

%description -n cpp
cpp (or cccp) is the GNU C Compatible Compiler Preprocessor.  cpp is a
macro processor which is used automatically by the C compiler to
transform program source before actual compilation.  cpp may also be
used independently from the C compiler and the C language.

%if %BUILD_GXX
%package c++
Summary: C++ support for gcc.
Group: Development/Languages
Requires: gcc = %version-%release, cpp = %version-%release
Obsoletes: egcs-c++

%description c++
This package contains the C++ compiler from the GNU Compiler Collection.
It includes support for most of the current C++ specification, including
templates and exception handling.  It does include the static standard
C++ library and C++ header files.  The library for dynamically linking
programs is available as a separate binary package.

%package -n libstdc++
Summary: GNU C++ library.
Group: System Environment/Libraries
PreReq: /sbin/ldconfig
Obsoletes: gcc-libstdc++

%description -n libstdc++
The libstdc++ package contains a snapshot of the GCC Standard C++
Library v3, an ongoing project to implement the ISO 14882 Standard C++
library.

%if %BUILD_CXX_COMPAT
%ifarch %ix86
%package -n libstdc++-compat
Summary: Old GNU C++ libraries for binary compatibility.
Group: System Environment/Libraries
PreReq: /sbin/ldconfig

%description -n libstdc++-compat
This package includes the old shared libraries necessary to run C++
applications built against the libraries.
%endif
%endif

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development.
Group: Development/Libraries
Obsoletes: gcc-libstdc++-devel

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++ development.
%endif

%if %BUILD_OBJC
%package objc
Summary: Objective C support for gcc.
Group: Development/Languages
PreReq: /sbin/ldconfig
Requires: gcc = %version-%release, cpp = %version-%release
Obsoletes: egcs-objc

%description objc
This package contains the Objective C compiler from the GNU Compiler
Collection.  Objective C is an object oriented derivative of the C
language, mainly used on systems running NeXTSTEP.  This package does
not include the standard Objective C object library.
%endif

%if %BUILD_G77
%package g77
Summary: Fortran 77 support for gcc.
Group: Development/Languages
PreReq: /sbin/ldconfig, /sbin/install-info
Requires: gcc = %version-%release
Obsoletes: egcs-g77

%description g77
This package contains the Fortran 77 compiler from the GNU Compiler
Collection.
%endif

%if %BUILD_JAVA
%package java
Summary: Java support for gcc.
Group: Development/Languages
PreReq: /sbin/ldconfig, /sbin/install-info
Requires: gcc = %version-%release

%description java
This package adds support for compiling Java programs with the GNU
compiler.
%endif

%if %BUILD_ADA
%package ada
Summary: ADA support for gcc.
Group: Development/Languages
PreReq: /sbin/ldconfig
Requires: gcc = %version-%release

%description ada
This package adds support for compiling ADA programs with the GNU
compiler.
%endif

%if %USE_VERSION_SPECIFIC_LIBS
%define version_libdir %_libdir/gcc-lib/%_target_platform/%version
%else
%define version_libdir %_libdir
%endif

%prep
%if %BUILD_ADA
	echo "Sorry, but building Ada95 GCC frontend is not supported by"
	echo "Openwall team."
	exit 1
%endif

%setup -q

%if %BUILD_ADA
%setup -q -T -D -b 1
%endif

%if %BUILD_GXX
%setup -q -T -D -b 2
%if %BUILD_CXX_COMPAT
%setup -q -n %name-%version -T -D -a 7
# These will be overridden by the next tarball.
rm compat/i386/libstdc++-libc6.1-1.so.2
rm compat/i386/libstdc++.so.2.9
rm compat/i386/libstdc++.so.2.9.dummy
%setup -q -n %name-%version -T -D -a 8
%endif
%endif

%if %BUILD_G77
%setup -q -T -D -b 3
%endif

%if %BUILD_JAVA
%setup -q -T -D -b 4
%endif

%if %BUILD_OBJC
%setup -q -T -D -b 5
%endif

%if %BUILD_TESTSUITE
%setup -q -T -D -b 6
%endif

%build
# XXX: This does not work with new autotools and is presently not needed.
%if 0
# Rebuild configure(s) and Makefile(s) if templates are newer...
for f in */acinclude.m4; do
	pushd "${f%/*}"
# Run aclocal & autoconf only if files aclocal.m4 and configure.in exist
# and acinclude.m4 is newer than aclocal.m4.
	if [ -f aclocal.m4 -a -f configure.in -a acinclude.m4 -nt aclocal.m4 ]
	then
		aclocal
		autoconf
	fi
	popd
done
for f in */configure.in; do
	pushd "${f%/*}"
	[ configure.in -nt configure ] && autoconf && autoheader
	popd
done
for f in */Makefile.am; do
	pushd "${f%/*}"
	[ Makefile.am -nt Makefile.in ] && automake
	popd
done
%endif

%ifarch sparcv9
%define _target_platform sparc-%_vendor-%_target_os
%endif
%ifarch sparc sparcv9
# pthreads are currently not supported on SPARC.
%define threads	single
%else
%define threads posix
%endif

# We will build this software outside source tree as recommended by INSTALL/*
rm -rf obj-%_target_platform
mkdir obj-%_target_platform
cd obj-%_target_platform

CFLAGS="$RPM_OPT_FLAGS" \
CXXFLAGS="`echo "$RPM_OPT_FLAGS" | sed -e 's/-fno-rtti//g'`" \
GCJFLAGS="$CFLAGS" \
XCFLAGS="$CFLAGS" \
TCFLAGS="$CFLAGS" \
../configure \
	--prefix=%_prefix \
	--exec-prefix=%_exec_prefix \
	--bindir=%_bindir \
	--libdir=%_libdir \
	--with-slib=/lib \
	--infodir=%_infodir \
	--mandir=%_mandir \
	--with-gxx-include-dir=%_includedir/g++-v3 \
	--enable-shared \
	--enable-threads=%threads \
%if %USE_VERSION_SPECIFIC_LIBS
	--enable-version-specific-runtime-libs \
%endif
	--disable-checking \
	--enable-nls \
	--enable-c-mbchar \
	--enable-long-long \
	--enable-__cxa_atexit \
%if %USE_BOEHM_GC
	--enable-objc-gc \
%endif
	--host=%_target_platform \
	--build=%_target_platform \
	--target=%_target_platform

%__make bootstrap-lean STAGE1_CFLAGS="-O -fomit-frame-pointer" \
	BOOT_CFLAGS="$RPM_OPT_FLAGS"

# Copy various doc files here and there.
cd ..
mkdir -p rpm-doc/gcc
install -p gcc/*ChangeLog* gcc/NEWS rpm-doc/gcc/
install -p BUGS COPYING* FAQ GNATS MAINTAINERS README gcc/SERVICE rpm-doc/gcc/

%if %BUILD_GXX
mkdir -p rpm-doc/g++
install -p gcc/cp/{ChangeLog*,NEWS} rpm-doc/g++/

mkdir -p rpm-doc/libstdc++
install -p libstdc++-v3/{ChangeLog*,README} rpm-doc/libstdc++/
%endif

%if %BUILD_G77
mkdir -p rpm-doc/g77
install -p gcc/f/{ChangeLog*,NEWS,README,BUGS} rpm-doc/g77/
pushd libf2c
for i in ChangeLog* README *.netlib; do
	install -p $i ../rpm-doc/g77/$i.libf2c
done
popd
%endif

%if %BUILD_JAVA
mkdir -p rpm-doc/java
install -p gcc/java/ChangeLog* libjava/doc/cni* rpm-doc/java/
pushd libffi
for i in ChangeLog* README LICENSE; do
	install -p $i ../rpm-doc/java/$i.libffi
done
popd
pushd libjava
for i in ChangeLog* README NEWS THANKS HACKING LIBGCJ_LICENSE; do
	install -p $i ../rpm-doc/java/$i.libjava
done
popd
%endif

%if %BUILD_OBJC
mkdir -p rpm-doc/objc
install -p gcc/objc/README* rpm-doc/objc/
pushd libobjc
for i in ChangeLog* README* THREADS*; do
	install -p $i ../rpm-doc/java/$i.libobjc
done
popd
%endif

%if %BUILD_ADA
mkdir -p rpm-doc/ada
%endif

%install
rm -rf $RPM_BUILD_ROOT

cd obj-%_target_platform
%__make	DESTDIR=$RPM_BUILD_ROOT install

FULLVER=`$RPM_BUILD_ROOT%_bindir/%_target_platform-gcc -dumpversion`
FULLPATH=$(dirname $RPM_BUILD_ROOT%_libdir/gcc-lib/%_target_platform/$FULLVER/cc1)

# Fix some things.
ln -s gcc $RPM_BUILD_ROOT%_bindir/cc
echo ".so gcc.1" > $RPM_BUILD_ROOT%_mandir/man1/cc.1

%if %BUILD_GXX
echo ".so g++.1" > $RPM_BUILD_ROOT%_mandir/man1/c++.1
%endif

%if %BUILD_G77
ln -s g77 $RPM_BUILD_ROOT%_bindir/f77
echo ".so g77.1" > $RPM_BUILD_ROOT%_mandir/man1/f77.1
%endif

mkdir -p $RPM_BUILD_ROOT/lib
ln -s ../${FULLPATH##$RPM_BUILD_ROOT/}/cpp0 $RPM_BUILD_ROOT/lib/cpp

%if %BUILD_CXX_COMPAT
%ifarch %ix86
cp -d --preserve=timestamps ../compat/i386/* $RPM_BUILD_ROOT%_libdir/
%endif
%endif

cd ..
echo '%defattr(-,root,root)' > gcc-fixinc-filelist
# First, we make a directory list and prepend each directory with properly
# attributes...
find $RPM_BUILD_ROOT%_libdir/gcc-lib/%_target_platform/%version/include \
	-type d -print | \
	sed "s#^$RPM_BUILD_ROOT#%dir %attr(0755,root,root) #g" | \
	egrep -v '^((objc)|(exception)|(typeinfo)|(new(\.h)?))$' >> \
		gcc-fixinc-filelist
# Second, we just create a filelist (assuming default attributes)
find $RPM_BUILD_ROOT%_libdir/gcc-lib/%_target_platform/%version/include \
	-type f -print | \
	sed "s#^$RPM_BUILD_ROOT##g" | \
	egrep -v '^((objc)|(exception)|(typeinfo)|(new(\.h)?))$' >> \
		gcc-fixinc-filelist

# Remove unpackaged files
rm $RPM_BUILD_ROOT%_bindir/c++filt
rm $RPM_BUILD_ROOT%_libdir/libiberty.a

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot%_datadir/locale/de/LC_MESSAGES/libstdc++.mo
rm %buildroot%_datadir/locale/fr/LC_MESSAGES/libstdc++.mo

%post
/sbin/install-info --info-dir=%_infodir %_infodir/gcc.info.gz
/sbin/install-info --info-dir=%_infodir %_infodir/gccint.info.gz
/sbin/ldconfig

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/gccint.info.gz
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/gcc.info.gz
fi

%postun -p /sbin/ldconfig

%post -n cpp
/sbin/install-info --info-dir=%_infodir %_infodir/cpp.info.gz
/sbin/install-info --info-dir=%_infodir %_infodir/cppinternals.info.gz

%preun -n cpp
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/cppinternals.info.gz
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/cpp.info.gz
fi

%if %BUILD_GXX
%post -n libstdc++ -p /sbin/ldconfig
%postun -n libstdc++ -p /sbin/ldconfig
%if %BUILD_CXX_COMPAT
%ifarch %ix86
%post -n libstdc++-compat -p /sbin/ldconfig
%postun -n libstdc++-compat -p /sbin/ldconfig
%endif
%endif
%endif

%if %BUILD_G77
%post g77
/sbin/install-info --info-dir=%_infodir %_infodir/g77.info.gz
/sbin/ldconfig

%preun g77
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/g77.info.gz
fi

%postun g77 -p /sbin/ldconfig
%endif

%if %BUILD_OBJC
%post objc -p /sbin/ldconfig
%postun objc -p /sbin/ldconfig
%endif

%if %BUILD_JAVA
%post java
/sbin/install-info --info-dir=%_infodir %_infodir/gcj.info.gz
/sbin/ldconfig

%preun java
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/gcj.info.gz
fi

%postun java -p /sbin/ldconfig
%endif

%if %BUILD_ADA
%post ada -p /sbin/ldconfig
%postun ada -p /sbin/ldconfig
%endif

%files -f gcc-fixinc-filelist
%defattr(-,root,root)
%_bindir/cc
%attr(0755,root,root) %_bindir/gcc
%attr(0755,root,root) %_bindir/gccbug
%attr(0755,root,root) %_bindir/gcov
%attr(0755,root,root) %_bindir/%_target_platform-gcc
%_infodir/gcc.info*
%_infodir/gccint.info*
%dir %_libdir/gcc-lib
%dir %_libdir/gcc-lib/%_target_platform
%dir %_libdir/gcc-lib/%_target_platform/%version
%attr(0755,root,root) %_libdir/gcc-lib/%_target_platform/%version/cc1
%attr(0755,root,root) %_libdir/gcc-lib/%_target_platform/%version/collect2
%_libdir/gcc-lib/%_target_platform/%version/crt*.o
%_libdir/gcc-lib/%_target_platform/%version/libgcc*.a
%version_libdir/libgcc*.so*
%_libdir/gcc-lib/%_target_platform/%version/specs
#dir %_libdir/gcc-lib/%_target_platform/%version/include
%_mandir/man1/cc.1*
%_mandir/man1/gcc.1*
%_mandir/man1/gcov.1*
%_mandir/man7/fsf-funding.7*
%_mandir/man7/gfdl.7*
%_mandir/man7/gpl.7*
%_datadir/locale/*/LC_MESSAGES/gcc.mo
%doc rpm-doc/gcc/*

%files -n cpp
%defattr(-,root,root)
%attr(0755,root,root) %_bindir/cpp
%_infodir/cpp.info*
%_infodir/cppinternals.info*
%dir %_libdir/gcc-lib
%dir %_libdir/gcc-lib/%_target_platform
%dir %_libdir/gcc-lib/%_target_platform/%version
%attr(0755,root,root) %_libdir/gcc-lib/%_target_platform/%version/cpp0
%attr(0755,root,root) %_libdir/gcc-lib/%_target_platform/%version/tradcpp0
%_mandir/man1/cpp.1*
/lib/cpp

%if %BUILD_GXX
%files c++
%defattr(-,root,root)
%attr(0755,root,root) %_bindir/?++
%attr(0755,root,root) %_bindir/%_target_platform-?++
%attr(0755,root,root) %_libdir/gcc-lib/%_target_platform/%version/cc1plus
%_mandir/man1/?++.1*
%doc gcc/cp/ChangeLog*
%doc rpm-doc/g++/*

%files -n libstdc++
%defattr(-,root,root)
%version_libdir/libstdc++.so.[^2]*
%doc rpm-doc/libstdc++/*
%doc libstdc++-v3/docs/html

%if %BUILD_CXX_COMPAT
%ifarch %ix86
%files -n libstdc++-compat
%defattr(-,root,root)
%_libdir/libstdc++.so.2.7.2.8
%_libdir/libg++.so.2.7.2.8
%_libdir/libstdc++.so.2.8.0
%_libdir/libstdc++.so.2.9
%_libdir/libstdc++-*libc6*.so*
%endif
%endif

%files -n libstdc++-devel
%defattr(-,root,root)
%_includedir/g++-v3
%version_libdir/libs*++.*a
%attr(0755,root,root) %version_libdir/libstdc++.so
%endif

%if %BUILD_G77
%files g77
%defattr(-,root,root)
%attr(0755,root,root) %_bindir/?77
%_infodir/g77*
%version_libdir/libfrt*.*a
%version_libdir/libg2c*.*a
%attr(0755,root,root) %version_libdir/libg2c*.so*
%attr(0755,root,root) %_libdir/gcc-lib/%_target_platform/%version/f771
%_mandir/man1/?77.1*
%_libdir/gcc-lib/%_target_platform/%version/include/g2c.h
%doc rpm-doc/g77/*
%endif

%if %BUILD_OBJC
%files objc
%defattr(-,root,root)
%_libdir/gcc-lib/%_target_platform/%version/include/objc
%version_libdir/libobjc*.*a
%attr(0755,root,root) %version_libdir/libobjc*.so*
%attr(0755,root,root) %_libdir/gcc-lib/%_target_platform/%version/cc1obj
%doc rpm-doc/objc/*
%endif

%if %BUILD_JAVA
%files java
%defattr(-,root,root)
%attr(0755,root,root) %_bindir/addr2name.awk
%attr(0755,root,root) %_bindir/g?j*
%attr(0755,root,root) %_bindir/grepjar
%attr(0755,root,root) %_bindir/j*
%attr(0755,root,root) %_bindir/rmi*
%_includedir/gcj
%_includedir/gnu
%_includedir/java
%_includedir/javax
%_includedir/org
%_includedir/gc*.h
%_includedir/j*.h
%_infodir/gcj*.info*
%version_libdir/libgcj*.*a
%attr(0755,root,root) %version_libdir/libgcj*.so*
%version_libdir/libgcj.spec
%_libdir/security
%attr(0755,root,root) %_libdir/gcc-lib/%_target_platform/%version/j*
%_libdir/gcc-lib/%_target_platform/%version/include/gcj
%_mandir/man1/g?j*.1*
%_mandir/man1/j*.1*
%_mandir/man1/rmi*.1*
%_datadir/java
%doc rpm-doc/java/*
%endif

%if %BUILD_ADA
%files ada
%defattr(-,root,root)
%doc rpm-doc/ada/*
%endif

%changelog
* Thu Sep 02 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 1:3.2.2-owl2
- Imported into Owl-current
- Removed duplicate entry in filelist for include directory

* Tue May 25 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 1:3.2.2-owl1.6
- Fixed a typo in spec file

* Tue Apr 20 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 1:3.2.2-owl1.5
- Additional optimization fixes for build process (using STAGE1_CFLAGS and
BOOT_CFLAGS)
- Moved extraction of '-fno-rtti' to CXXFLAGS, because this is C++ options

* Fri Apr 16 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 1:3.2.2-owl1.4
- Removed extra_c_flags and "XXX:" comment from spec file
- Passing "-O -fomit-frame-pointers" in CFLAGS variable to improve build times

* Thu Feb 26 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 1:3.2.2-owl1.3
- Removed wchar patch as we are building against glibc 2.3.2

* Thu Feb 26 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 1:3.2.2-owl1.2
- Temporarily disabled regeneration of configure due to conflict with new
autotools.

* Mon Feb 23 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 1:3.2.2-owl1.1
- Fixed permission of %_libdir/gcc-lib/%_target_platform/%version/include/*
directories
- Removed unpackaged files to make RPM4 happy :)

* Thu Feb 05 2004 Solar Designer <solar@owl.openwall.com> 1:3.2.2-owl1
- Added libstdc++ compatibility libraries for gcc 2.95.3 as a separate
source tarball.

* Tue Feb 03 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 1:3.2.2-owl0.3
- Cleaned up the spec file (reordered scripts & files sections).
- Avoid using of subshells in build section to not mask possible errors.

* Mon Feb 02 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 1:3.2.2-owl0.2
- Added a patch to enable limited wchar support.

* Fri Jan 30 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 1:3.2.2-owl0.1
- Updated to 3.2.2 version.

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com> 1:2.95.3-owl5
- Deal with info dir entries such that the menu looks pretty.

* Fri Jun 21 2002 Solar Designer <solar@owl.openwall.com>
- Provide a cc(1) man page.

* Tue May 28 2002 Solar Designer <solar@owl.openwall.com>
- Don't override the linker's default library path for elf32_sparc, place
/lib64 before /usr/lib64 in the path for elf64_sparc; this is needed to
support dynamic linking with libraries from packages which only place the
.so's in /lib (/lib64), not /usr/lib (/usr/lib64).

* Sat May 25 2002 Solar Designer <solar@owl.openwall.com>
- Do use some optimization when building the stage1 compiler to make our gcc
builds faster.

* Tue Jan 29 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions (but more cleanups are still needed).
- Dropped the 2.95.2-specific patches entirely.

* Sun Mar 18 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 2.95.3.
- Dropped the duplicate_decls() patch (included in 2.95.3).
- Various spec file cleanups (use the ix86 macro, avoid subshells).

* Fri Nov 17 2000 Solar Designer <solar@owl.openwall.com>
- No pthreads on sparcv9, not just on plain sparc.
- Pass plain sparc- target to configure when building for sparcv9, to
allow for the use of sparcv9 optflags while not confusing configure.
- Check for __arch64__ rather than __sparc_v9__ in limits.h.
- %defattr(-,root,root) for all architectures, not just x86 and alpha
(no idea why this was restricted).

* Wed Nov 08 2000 Solar Designer <solar@owl.openwall.com>
- Added a patch for copying of DECL_MODE in duplicate_decls(), by
Richard Henderson (http://gcc.gnu.org/ml/gcc-patches/1999-11/msg00087.html).

* Sun Oct 29 2000 Solar Designer <solar@owl.openwall.com>
- libstdc++-compat is for x86 only, corrected the %ifarch's.

* Sat Oct 21 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- texconfig bug hack

* Fri Oct 20 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- disable dvi generation

* Fri Aug 25 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- removed make -j

* Sat Jul 29 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- spec cleanup.
- duplicate file fix.

* Sun Jul 09 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- Imported from RH.

# $Id: Owl/packages/gcc/gcc.spec,v 1.29 2002/08/27 18:25:00 solar Exp $

%define GCC_PREFIX /usr
%define CPP_PREFIX /lib
%define GCC_VERSION 2.95.3
%define STDC_VERSION 2.10.0

%define BUILD_OBJC 0
%define BUILD_F77 0
%define BUILD_CHILL 0

Summary: C compiler from the GNU Compiler Collection.
Name: gcc
Version: %{GCC_VERSION}
Release: owl5
Epoch: 1
License: GPL
Group: Development/Languages
URL: http://gcc.gnu.org
Source0: ftp://ftp.gnu.org/gnu/gcc/gcc-%{GCC_VERSION}.tar.gz
Source1: libstdc++-compat.tar.bz2
Patch0: gcc-2.95.3-rh-warn.diff
Patch1: gcc-2.95.2-owl-disable-dvi.diff
Patch2: gcc-2.95.2-owl-texconfig-bug.diff
Patch3: gcc-2.95.3-owl-sparcv9-LONG_MAX.diff
Patch4: gcc-2.95.3-owl-sparc-library-path.diff
Patch5: gcc-2.95.3-owl-info.diff
PreReq: /sbin/install-info
Requires: binutils >= 2.9.1.0.25
Requires: cpp = %{GCC_VERSION}
Obsoletes: egcs
BuildRoot: /override/%{name}-%{version}

%description
The gcc package contains C compiler from the GNU Compiler Collection,
as well as documentation which is not limited to just the C compiler.

%package -n cpp
Summary: GNU C preprocessor.
Group: Development/Languages
PreReq: /sbin/ldconfig, /sbin/install-info

%description -n cpp
cpp (or cccp) is the GNU C Compatible Compiler Preprocessor.  cpp is a
macro processor which is used automatically by the C compiler to
transform program source before actual compilation.  cpp may also be
used independently from the C compiler and the C language.

%package c++
Summary: C++ support for gcc.
Group: Development/Languages
Requires: gcc = %{GCC_VERSION}, cpp = %{GCC_VERSION}
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
PreReq: /sbin/ldconfig, grep, fileutils
Provides: libstdc++-libc6.1-1.so.2, libstdc++-libc6.1-2.so.3, libstdc++.so.2.9
Obsoletes: gcc-libstdc++

%description -n libstdc++
The libstdc++ package contains a snapshot of the GCC Standard C++
Library v3, an ongoing project to implement the ISO 14882 Standard C++
library.

%ifarch %ix86
%package -n libstdc++-compat
Summary: Old GNU C++ libraries for binary compatibility.
Group: System Environment/Libraries
PreReq: /sbin/ldconfig, grep, fileutils

%description -n libstdc++-compat
This package includes the old shared libraries necessary to run C++
applications built against the libraries.
%endif

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development.
Group: Development/Libraries
Obsoletes: gcc-libstdc++-devel

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++ development.

%if %BUILD_OBJC
%package objc
Summary: Objective C support for gcc.
Group: Development/Languages
Requires: gcc = %{GCC_VERSION}, cpp = %{GCC_VERSION}
Obsoletes: egcs-objc

%description objc
This package contains the Objective C compiler from the GNU Compiler
Collection.  Objective C is an object oriented derivative of the C
language, mainly used on systems running NeXTSTEP.  This package does
not include the standard Objective C object library.
%endif

%if %BUILD_F77
%package g77
Summary: Fortran 77 support for gcc.
Group: Development/Languages
PreReq: /sbin/install-info
Requires: gcc = %{GCC_VERSION}
Obsoletes: egcs-g77

%description g77
This package contains the Fortran 77 compiler from the GNU Compiler
Collection.
%endif

%if %BUILD_CHILL
%package chill
Summary: CHILL support for gcc.
Group: Development/Languages
PreReq: /sbin/install-info
Requires: gcc = %{GCC_VERSION}

%description chill
This package adds support for compiling CHILL programs with the GNU
compiler.

CHILL is the "CCITT High-Level Language", where CCITT is the old
name for what is now ITU, the International Telecommunications Union.
It is a language in the Modula2 family, and targets many of the same
applications as Ada (especially large embedded systems).  Chill was
never used much in the United States, but is still being used in Europe,
Brazil, Korea, and other places.
%endif

%prep
%setup -q -n gcc-%{GCC_VERSION} -a 1
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# Remove bison-generated files - we want bison 1.28+'ish versions...
for i in gcc/cp/parse gcc/c-parse gcc/cexp gcc/java/parse-scan gcc/java/parse gcc/objc/objc-parse; do
	rm -f $i.c
done

# Remove unneeded languages.
rm -f gcc/java/config-lang.in

%if !%BUILD_OBJC
	rm -f gcc/objc/config-lang.in
%endif
%if !%BUILD_F77
	rm -f gcc/f/config-lang.in
%endif
%if !%BUILD_CHILL
	rm -f gcc/ch/config-lang.in
%endif

%build
# There're currently no pre-compiled versions of these texinfo files
# included, should uncomment if that changes.
#rm gcc/{gcc,cpp}.info
%ifarch sparcv9
%define _target_platform sparc-%{_vendor}-%{_target_os}
%endif
%ifarch sparc sparcv9
# pthreads are currently not supported on sparc
ENABLE_THREADS=''
%else
ENABLE_THREADS='--enable-threads=posix'
%endif

rm -rf obj-%{_target_platform}
mkdir obj-%{_target_platform}
cd obj-%{_target_platform}

CFLAGS="`echo "$RPM_OPT_FLAGS" | sed -e 's/-fno-rtti//g'` -fexceptions"
export extra_c_flags="-O -fomit-frame-pointer"
CFLAGS="$CFLAGS" \
CXXFLAGS="$CFLAGS" \
XCFLAGS="$CFLAGS" \
TCFLAGS="$CFLAGS" \
../configure \
	--prefix=%{GCC_PREFIX} \
	--mandir=${RPM_BUILD_ROOT}%{_mandir} \
	--infodir=${RPM_BUILD_ROOT}%{_infodir} \
	--enable-shared --enable-haifa $ENABLE_THREADS \
	--host=%{_target_platform}
touch ../gcc/c-gperf.h

make bootstrap-lean

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/libstdc++ rpm.doc/g77 rpm.doc/chill rpm.doc/objc

pushd libio
for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libstdc++/$i.libio
done
popd

pushd libstdc++
for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libstdc++/$i.libstdc++
done
popd

pushd gcc/f
for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/g77/$i.f
done
popd

pushd libf2c
for i in ChangeLog*; do
	cp -p $i ../rpm.doc/g77/$i.libf2c
done
popd

pushd gcc/ch
for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/chill/$i.ch
done
popd

pushd libchill
for i in ChangeLog*; do
	cp -p $i ../rpm.doc/chill/$i.libchill
done
popd

pushd gcc/objc
for i in README*; do
	cp -p $i ../../rpm.doc/objc/$i.objc
done
popd

pushd libobjc
for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done
popd

%install
rm -rf $RPM_BUILD_ROOT

cd obj-%{_target_platform}
make prefix=$RPM_BUILD_ROOT%{GCC_PREFIX} install

FULLVER=`$RPM_BUILD_ROOT%{GCC_PREFIX}/bin/%{_target_platform}-gcc --version | \
	cut -d' ' -f1`
FULLPATH=$(dirname $RPM_BUILD_ROOT%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/$FULLVER/cc1)

# fix some things
ln -sf gcc $RPM_BUILD_ROOT%{GCC_PREFIX}/bin/cc
ln -sf gcc.1 $RPM_BUILD_ROOT%{GCC_PREFIX}/man/man1/cc.1
rm -f $RPM_BUILD_ROOT%{GCC_PREFIX}/info/dir
%if %BUILD_F77
ln -sf g77 $RPM_BUILD_ROOT%{GCC_PREFIX}/bin/f77
%endif

mkdir -p $RPM_BUILD_ROOT/lib
ln -sf ../${FULLPATH##$RPM_BUILD_ROOT/}/cpp0 $RPM_BUILD_ROOT/lib/cpp
ln -sf cccp.1 $RPM_BUILD_ROOT%{GCC_PREFIX}/man/man1/cpp.1

%ifarch %ix86
# install the compatibility libstdc++ library
test -d ../compat/i386 && install -m 755 ../compat/i386/* $RPM_BUILD_ROOT%{GCC_PREFIX}/lib/
%endif

cd ..
cat >gcc-filelist <<EOF
%defattr(-,root,root)
%{GCC_PREFIX}/bin/gcc
%{GCC_PREFIX}/bin/cc
%{GCC_PREFIX}/bin/protoize
%{GCC_PREFIX}/bin/unprotoize
%{GCC_PREFIX}/bin/gcov
%{GCC_PREFIX}/bin/%{_target_platform}-gcc
%{GCC_PREFIX}/man/man1/gcc.1*
%{GCC_PREFIX}/man/man1/cc.1*
%{GCC_PREFIX}/info/gcc*
%dir %{GCC_PREFIX}/lib/gcc-lib
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/cc1
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/collect2
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/crt*.o
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/libgcc.a
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/SYSCALLS.c.X
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/specs
%doc gcc/README* gcc/*ChangeLog*
EOF

(cd $RPM_BUILD_ROOT%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include &&
	ls | egrep -v '^((objc)|(exception)|(typeinfo)|(new(\.h)?))$'
) | sed 's|^|%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include/|' \
	>>gcc-filelist

# This is required for the old Red Hat Linux 6 based programs ...
cd $RPM_BUILD_ROOT/usr/lib
ln -sf libstdc++-3-libc6.1-2-2.10.0.so libstdc++-libc6.1-1.so.2
ln -sf libstdc++-3-libc6.1-2-2.10.0.so libstdc++-libc6.1-1.1.so.2
ln -sf libstdc++-3-libc6.1-2-2.10.0.so libstdc++.so.2.9

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/gcc.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/gcc.info.gz %{_infodir}/dir
fi

%post -n libstdc++
if ! grep -qs '^%{GCC_PREFIX}/lib$' /etc/ld.so.conf; then
	echo %{GCC_PREFIX}/lib >> /etc/ld.so.conf
fi
/sbin/ldconfig

%postun -n libstdc++
if [ $1 -eq 0 ]; then
	grep -v "%{GCC_PREFIX}/lib" /etc/ld.so.conf > /etc/ld.so.conf.new &&
	mv -f /etc/ld.so.conf.new /etc/ld.so.conf
fi
/sbin/ldconfig

%ifarch %ix86
%post -n libstdc++-compat
if ! grep -qs '^%{GCC_PREFIX}/lib$' /etc/ld.so.conf; then
	echo %{GCC_PREFIX}/lib >>/etc/ld.so.conf
fi
/sbin/ldconfig

%postun -n libstdc++-compat
if [ $1 -eq 0 ]; then
	grep -v "%{GCC_PREFIX}/lib" /etc/ld.so.conf > /etc/ld.so.conf.new &&
	mv -f /etc/ld.so.conf.new /etc/ld.so.conf
fi
/sbin/ldconfig
%endif

%post -n cpp
/sbin/install-info %{_infodir}/cpp.info.gz %{_infodir}/dir

%preun -n cpp
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/cpp.info.gz %{_infodir}/dir
fi
/sbin/ldconfig

%files -f gcc-filelist

%files -n cpp
%defattr(-,root,root)
%{CPP_PREFIX}/cpp
%{GCC_PREFIX}/man/man1/cpp.1*
%{GCC_PREFIX}/man/man1/cccp.1*
%{GCC_PREFIX}/info/cpp.info*.gz
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/cpp0

%files c++
%defattr(-,root,root)
%{GCC_PREFIX}/man/man1/g++.1*
%{GCC_PREFIX}/bin/g++
%{GCC_PREFIX}/bin/c++
%dir %{GCC_PREFIX}/lib/gcc-lib
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/cc1plus
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include/exception
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include/new
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include/new.h
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include/typeinfo
%doc gcc/cp/ChangeLog*

%files -n libstdc++
%defattr(-,root,root)
%{GCC_PREFIX}/lib/libstdc++-3-libc*-%{STDC_VERSION}.so
%{GCC_PREFIX}/lib/libstdc++-libc*.so.3
%{GCC_PREFIX}/lib/libstdc++-libc*.so.2
%{GCC_PREFIX}/lib/libstdc++.so.2.9
%dir %{GCC_PREFIX}/lib/gcc-lib
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/libstdc++.so

%ifarch %ix86
%files -n libstdc++-compat
%defattr(-,root,root)
%{GCC_PREFIX}/lib/libstdc++.so.2.7.2.8
%{GCC_PREFIX}/lib/libstdc++.so.2.8.0
%{GCC_PREFIX}/lib/libstdc++-2-libc6.1-1-2.9.0.so
%{GCC_PREFIX}/lib/libstdc++.so.2.9.dummy
%{GCC_PREFIX}/lib/libstdc++.so.2.9
%endif

%files -n libstdc++-devel
%defattr(-,root,root)
%{GCC_PREFIX}/lib/libstdc++-3-libc*-%{STDC_VERSION}.a
%{GCC_PREFIX}/lib/libstdc++-libc*.a.3
%{GCC_PREFIX}/include/g++-3
%dir %{GCC_PREFIX}/lib/gcc-lib
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/libstdc++.a
%doc rpm.doc/libstdc++/*

%if %BUILD_OBJC
%files objc
%defattr(-,root,root)
%dir %{GCC_PREFIX}/lib/gcc-lib
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/cc1obj
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/libobjc.a
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include/objc
%doc rpm.doc/objc/*
%doc libobjc/THREADS* libobjc/ChangeLog
%endif

%if %BUILD_F77
%post g77
/sbin/install-info %{_infodir}/g77.info.gz %{_infodir}/dir

%preun g77
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/g77.info.gz %{_infodir}/dir
fi

%files g77
%defattr(-,root,root)
%{GCC_PREFIX}/bin/g77
%{GCC_PREFIX}/bin/f77
%{GCC_PREFIX}/info/g77*
%dir %{GCC_PREFIX}/lib/gcc-lib
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/f771
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/libg2c.a
%{GCC_PREFIX}/man/man1/g77.1*
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include/g2c.h
%doc gcc/f/README rpm.doc/g77/*
%endif

%if %BUILD_CHILL
%post chill
/sbin/install-info %{_infodir}/chill.info.gz %{_infodir}/dir

%preun chill
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/chill.info.gz %{_infodir}/dir
fi

%files chill
%defattr(-,root,root)
%{GCC_PREFIX}/bin/chill
%{GCC_PREFIX}/info/chill*
%dir %{GCC_PREFIX}/lib/gcc-lib
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/cc1chill
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/chill*.o
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/libchill.a
%doc gcc/ch/README gcc/ch/chill.brochure rpm.doc/chill/*
%endif

%changelog
* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com>
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

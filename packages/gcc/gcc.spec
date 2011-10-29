# $Owl: Owl/packages/gcc/gcc.spec,v 1.66 2011/10/29 09:15:18 segoon Exp $

# The only supported frontend for now is GXX.
# Testsuite is not supported because of its requirement for additional
# packages to run (dejagnu, tcl, expect).
%define BUILD_GXX 1
%undefine _with_test

%define gcc_branch 4.6

Summary: C compiler from the GNU Compiler Collection.
Name: gcc
Version: 4.6.2
Release: owl1
Epoch: 1
License: GPLv3+
Group: Development/Languages
URL: http://gcc.gnu.org
Source0: gcc-core-%version.tar.xz
# ftp://ftp.gnu.org/gnu/gcc/gcc-%version/gcc-core-%version.tar.bz2
# Signature: ftp://ftp.gnu.org/gnu/gcc/gcc-%version/gcc-core-%version.tar.bz2.sig
%if %BUILD_GXX
Source2: gcc-g++-%version.tar.xz
# ftp://ftp.gnu.org/gnu/gcc/gcc-%version/gcc-g++-%version.tar.bz2
# Signature: ftp://ftp.gnu.org/gnu/gcc/gcc-%version/gcc-g++-%version.tar.bz2.sig
%endif

PreReq: /sbin/install-info
Requires: binutils
Requires: cpp = %epoch:%version-%release
Requires: libgcc >= %epoch:%version-%release
Obsoletes: egcs
BuildRequires: binutils, gettext, bison, flex, texinfo
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

%package -n libgcc
Summary: GCC shared support library.
Group: System Environment/Libraries
PreReq: /sbin/ldconfig

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libgcc%gcc_branch-plugin-devel
Summary: GCC plugin header files.
Group: Development/Libraries
Provides: libgcc-plugin-devel = %version-%release

%description -n libgcc%gcc_branch-plugin-devel
This package contains header files required to build GCC plugins.

%if %BUILD_GXX
%package c++
Summary: C++ support for gcc.
Group: Development/Languages
Requires: gcc = %epoch:%version-%release, cpp = %epoch:%version-%release
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
Requires: libgcc >= %epoch:%version-%release
Obsoletes: gcc-libstdc++

%description -n libstdc++
The libstdc++ package contains the GCC Standard C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development.
Group: Development/Libraries
Requires: libstdc++ = %epoch:%version-%release
Obsoletes: gcc-libstdc++-devel

%description -n libstdc++-devel
Header files and libraries needed for C++ development.
%endif

####################################################################
# OpenMP library

%package -n libgomp%gcc_branch
Summary: GCC OpenMP shared support library.
Group: System/Libraries
Provides: libgomp = %version-%release
Provides: libgomp4.1 = %version-%release
Provides: libgomp4.3 = %version-%release
Provides: libgomp4.4 = %version-%release
Obsoletes: libgomp4.1, libgomp4.3 libgomp4.4
Conflicts: libgomp > %version

%description -n libgomp%gcc_branch
This package contains GCC OpenMP shared support library.

%package -n libgomp%gcc_branch-devel
Summary: GCC OpenMP support files.
Group: Development/Libraries
Provides: libgomp-devel = %version-%release
Requires: libgomp%gcc_branch >= %version-%release
Requires: glibc-devel

%description -n libgomp%gcc_branch-devel
This package contains GCC OpenMP headers and library.

####################################################################
# mudflap library

%package -n libmudflap%gcc_branch
Summary: GCC mudflap shared support libraries.
Group: System/Libraries
Provides: libmudflap = %version-%release
Provides: libmudflap4.1 = %version-%release
Provides: libmudflap4.3 = %version-%release
Provides: libmudflap4.4 = %version-%release
Obsoletes: libmudflap4.1, libmudflap4.3 libmudflap4.4
Conflicts: libmudflap > %version

%description -n libmudflap%gcc_branch
This package contains GCC shared support libraries which are needed for
mudflap support.

%package -n libmudflap%gcc_branch-devel
Summary: GCC mudflap support files.
Group: Development/Libraries
Provides: libmudflap-devel = %version-%release
Requires: libmudflap%gcc_branch >= %version-%release
Requires: glibc-devel

%description -n libmudflap%gcc_branch-devel
This package contains headers and libraries for building mudflap-instrumented
programs.
To instrument a non-threaded program, add -fmudflap option to GCC and
when linking add -lmudflap, for threaded programs also add -fmudflapth
and -lmudflapth.

%prep
%setup -q
%if %BUILD_GXX
%setup -q -T -D -b 2
%endif
%{?_with_test:%setup -q -T -D -b 6}

%build
# Rebuild configure(s) and Makefile(s) if templates are newer...
for f in */acinclude.m4; do
	pushd "${f%%/*}"
# Run aclocal & autoconf only if files aclocal.m4 and configure.in exist
# and acinclude.m4 is newer than aclocal.m4.
	if [ -f aclocal.m4 -a -f configure.in -a acinclude.m4 -nt aclocal.m4 ]
	then
		aclocal
		autoconf
	fi
	popd
done
for f in */Makefile.am; do
	pushd "${f%%/*}"
	[ Makefile.am -nt Makefile.in ] && automake
	popd
done

%ifarch sparcv9
%define _target_platform sparc-%_vendor-%_target_os
%endif

# We will build this software outside source tree as recommended by INSTALL/*
rm -rf obj-%_target_platform
mkdir obj-%_target_platform
cd obj-%_target_platform

../configure \
	--prefix=%_prefix \
	--exec-prefix=%_exec_prefix \
	--bindir=%_bindir \
	--libdir=%_libdir \
	--libexecdir=%_libdir \
	--with-slib=/%_lib \
	--infodir=%_infodir \
	--mandir=%_mandir \
	--enable-shared \
	--enable-threads=posix \
%if %BUILD_GXX
	--with-gxx-include-dir=%_includedir/c++/%version \
%endif # BUILD_GXX
%if %BUILD_GXX
	--disable-libstdcxx-pch \
%endif # BUILD_GXX
	--disable-checking \
	--enable-nls \
	--enable-c-mbchar \
	--enable-long-long \
	--enable-__cxa_atexit \
	--disable-multilib \
	--host=%_target_platform \
	--build=%_target_platform \
	--target=%_target_platform

TARGET_OPT_FLAGS='%optflags'
TARGET_OPT_LIBFLAGS='%{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}'

# Let's compile the thing
# STAGE1_CFLAGS is used for stage1 compiler
# BOOT_FLAGS is used for stage2..n compiler
# ..._FOR_TARGET is used for final compiler

%__make bootstrap-lean \
	STAGE1_CFLAGS="-O -fomit-frame-pointer" \
	BOOT_CFLAGS="-O -fomit-frame-pointer" \
	CFLAGS_FOR_TARGET="$TARGET_OPT_FLAGS" \
	LIBCFLAGS_FOR_TARGET="$TARGET_OPT_LIBFLAGS" \
	CXXFLAGS_FOR_TARGET="${TARGET_OPT_FLAGS//-fno-rtti/} -D_GNU_SOURCE" \
	LIBCXXFLAGS_FOR_TARGET="${TARGET_OPT_LIBFLAGS//-fno-rtti/} -D_GNU_SOURCE"

# Copy various doc files here and there.

cd ..
mkdir -p rpm-doc/gcc
install -pm 644 -p gcc/ChangeLog rpm-doc/gcc/
#install -pm 644 -p BUGS COPYING* FAQ MAINTAINERS README* gcc/SERVICE rpm-doc/gcc/
install -pm 644 -p COPYING* MAINTAINERS README* rpm-doc/gcc/

%if %BUILD_GXX
mkdir -p rpm-doc/g++
install -pm 644 -p gcc/cp/{ChangeLog,NEWS} rpm-doc/g++/

mkdir -p rpm-doc/libstdc++
install -pm 644 -p libstdc++-v3/{ChangeLog,README} rpm-doc/libstdc++/
%endif

find rpm-doc -type f \( -iname '*changelog*' -not -name '*.bz2' \) -print0 |
	xargs -r0 bzip2 -9 --

%install
rm -rf %buildroot

%__make -C obj-%_target_platform DESTDIR=%buildroot install

# Relocate libgcc shared library from %_libdir/ to /%_lib/.
mkdir %buildroot/%_lib
mv %buildroot%_libdir/libgcc_s.so.1 %buildroot/%_lib/
ln -s ../../../../../%_lib/libgcc_s.so.1 \
	%buildroot%_libdir/gcc/%_target_platform/%version/libgcc_s.so
rm %buildroot%_libdir/libgcc_s.so

# Fix some things.
ln -s gcc %buildroot%_bindir/cc
echo ".so gcc.1" > %buildroot%_mandir/man1/cc.1

%if %BUILD_GXX
echo ".so g++.1" > %buildroot%_mandir/man1/c++.1
%endif

# Remove unpackaged files
rm %buildroot%_infodir/dir
rm %buildroot%_infodir/gccinstall.info*
rm %buildroot%_libdir/libiberty.a
rm -f %buildroot%_libdir/*.la

%find_lang cpplib
%find_lang gcc

# autogen is needed for this
#
# %check
# cd obj-%_target_platform
# %__make -k check
# cd -

%post
/sbin/install-info --info-dir=%_infodir %_infodir/gcc.info
/sbin/install-info --info-dir=%_infodir %_infodir/gccint.info
%_libdir/gcc/%_target_platform/%version/install-tools/mkheaders
chmod -R go+rX %_libdir/gcc/%_target_platform/%version/include/*

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/gccint.info
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/gcc.info
	if [ -d %_libdir/gcc/%_target_platform/%version/include ]; then
		rm -rf %_libdir/gcc/%_target_platform/%version/include/*
	fi
fi

%post -n libgcc -p /sbin/ldconfig
%postun -n libgcc -p /sbin/ldconfig

%post -n cpp
/sbin/install-info --info-dir=%_infodir %_infodir/cpp.info
/sbin/install-info --info-dir=%_infodir %_infodir/cppinternals.info

%preun -n cpp
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/cppinternals.info
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/cpp.info
fi

%if %BUILD_GXX
%post -n libstdc++ -p /sbin/ldconfig
%postun -n libstdc++ -p /sbin/ldconfig
%endif

%files -f gcc.lang
%defattr(-,root,root)
%_bindir/cc
%_bindir/gcc
%_bindir/gcov
%_bindir/%_target_platform-gcc
%_bindir/%_target_platform-gcc-%version
%_infodir/gcc.info*
%_infodir/gccint.info*
%dir %_libdir/gcc
%dir %_libdir/gcc/%_target_platform
%dir %_libdir/gcc/%_target_platform/%version
%_libdir/gcc/%_target_platform/%version/cc1
%_libdir/gcc/%_target_platform/%version/collect2
%_libdir/gcc/%_target_platform/%version/crt*.o
%_libdir/gcc/%_target_platform/%version/libgcc*.a
%_libdir/gcc/%_target_platform/%version/libgcc*.so
%_libdir/gcc/%_target_platform/%version/libgcov*.a

%_libdir/gcc/%_target_platform/%version/include

%_libdir/gcc/%_target_platform/%version/include-fixed
%_libdir/gcc/%_target_platform/%version/install-tools

%_mandir/man1/cc.1*
%_mandir/man1/gcc.1*
%_mandir/man1/gcov.1*
%_mandir/man7/fsf-funding.7*
%_mandir/man7/gfdl.7*
%_mandir/man7/gpl.7*
%doc rpm-doc/gcc/*

%_libdir/gcc/%_target_platform/%version/lto1
%_libdir/gcc/%_target_platform/%version/lto-wrapper
%exclude %_libdir/gcc/%_target_platform/%version/*.la
%_libdir/gcc/%_target_platform/%version/liblto_plugin.so.0.0.0

%files -n cpp
%defattr(-,root,root)
%_bindir/cpp
%_infodir/cpp.info*
%_infodir/cppinternals.info*
%dir %_libdir/gcc
%dir %_libdir/gcc/%_target_platform
%_mandir/man1/cpp.1*

%files -n libgcc
%defattr(-,root,root)
/%_lib/libgcc*.so.*
%_libdir/libquadmath.so.*
%_libdir/libssp.so.*

%if %BUILD_GXX
%files c++ -f cpplib.lang
%defattr(-,root,root)
%_bindir/?++
%_bindir/%_target_platform-?++
%dir %_libdir/gcc
%dir %_libdir/gcc/%_target_platform
%_libdir/gcc/%_target_platform/%version/cc1plus
%_mandir/man1/?++.1*
%doc rpm-doc/g++/*

%files -n libstdc++
%defattr(-,root,root)
%_libdir/libstdc++.so.6*
%_datadir/locale/*/LC_MESSAGES/libstdc++.mo
%doc rpm-doc/libstdc++/*
%doc libstdc++-v3/doc/html
%exclude %_datadir/gcc-%version/python
%exclude %_libdir/libstdc++.so.6.0.16-gdb.py

%files -n libstdc++-devel
%defattr(-,root,root)
%_includedir/c++/%version
%_libdir/libs*++.a
%_libdir/libstdc++.so
%endif

%files -n libgcc%gcc_branch-plugin-devel
%_libdir/gcc/%_target_platform/%version/plugin/include
%_infodir/libquadmath.info*
%_libdir/libquadmath.a
%_libdir/libssp.a
%_libdir/libssp_nonshared.a

%files -n libgomp%gcc_branch
%_libdir/libgomp.so.*

%files -n libmudflap%gcc_branch
%_libdir/libmudflap.so.*
%_libdir/libmudflapth.so.*

%files -n libgomp%gcc_branch-devel
%dir %_libdir/gcc/%_target_platform/%version
%dir %_libdir/gcc/%_target_platform/%version/include
%_libdir/gcc/%_target_platform/%version/plugin/include
%_libdir/gcc/%_target_platform/%version/include/omp.h
%dir %_libdir/gcc/%_target_platform/%version
%_infodir/libgomp*.info*
%_libdir/libgomp.a
%_libdir/libgomp.spec

%files -n libmudflap%gcc_branch-devel
%dir %_libdir/gcc/%_target_platform/%version
%dir %_libdir/gcc/%_target_platform/%version/include
%_libdir/gcc/%_target_platform/%version/include/mf-runtime.h
%dir %_libdir/gcc/%_target_platform/%version
%_libdir/libmudflap.a
%_libdir/libmudflapth.a

%changelog
* Sat Oct 29 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1:4.6.2-owl1
- Updated to 4.6.2.

* Fri Oct 21 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1:4.6.1-owl1
- Updated to 4.6.1.

* Wed Dec 01 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1:3.4.5-owl5
- Fixed build bug with binutils 2.20.

* Fri Nov 20 2009 Solar Designer <solar-at-owl.openwall.com> 1:3.4.5-owl4
- Disabled building of V2 and V3 compat subpackages (gcc 2.x'ish libstdc++).

* Wed May 27 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:3.4.5-owl3
- Disabled unused libstdc++ precompiled header files.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:3.4.5-owl2
- Dropped old ChangeLog files, compressed the remaining ChangeLog files.

* Wed Dec 21 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:3.4.5-owl1
- Updated to 3.4.5.
- Packaged libgcc shared library in separate subpackage.

* Tue Dec 13 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:3.4.3-owl5
- Corrected interpackage dependencies.

* Sun Oct 23 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.4.3-owl4
- Added sed to Requires(post), since we are using sed in mkheaders;
commented out this Requires(post), since we will use this spec with RPM3.
- Added BuildRequires as suggested by kad@.
- Added a missing requirement for libstdc++ to libstdc++-devel.

* Fri Sep 23 2005 Michail Litvak <mci-at-owl.openwall.com> 1:3.4.3-owl3
- Don't package .la files.

* Wed Jan 19 2005 Solar Designer <solar-at-owl.openwall.com> 1:3.4.3-owl2
- Provide/obsolete libstdc++-compat in libstdc++-v3-compat.
- Restored the cc(1) and c++(1) man pages.

* Fri Jan 14 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.4.3-owl1
- Reverted the change with removing symbolic links from gcc to cc.
- Fixed missed compile flags for target compiler.

* Thu Jan 06 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.4.3-owl0
- Updated to 3.4.3.
- Enabled autotools magic, it works as expected.
- Added libstdc++ compatible libraries for glibc 3.2.2 based builds.
- Added BUILD_CXX_COMPAT_* macros to control building of compatibility
packages. I hope that after next release of Owl we will drop this crap.
- Spec was revised and cleaned up.

* Fri Jul 16 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.4.1-owl0
- Updated to 3.4.1.

* Thu Jun 04 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.4.0-owl0.2
- Updated to 3.4.0.
- Tested only C and C++ compilers, ObjC has compilation issues when using
Boehm GC, Ada unsupported by this build.

* Tue May 25 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.2.2-owl1.6
- Fixed a typo in spec file.

* Tue Apr 20 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.2.2-owl1.5
- Additional optimization fixes for build process (using STAGE1_CFLAGS and
BOOT_CFLAGS).
- Moved extraction of '-fno-rtti' to CXXFLAGS, because this is C++ options.

* Fri Apr 16 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.2.2-owl1.4
- Removed extra_c_flags and "XXX:" comment from spec file.
- Passing "-O -fomit-frame-pointers" in CFLAGS variable to improve build times.

* Thu Feb 26 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.2.2-owl1.3
- Removed wchar patch as we are building against glibc 2.3.2.

* Thu Feb 26 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.2.2-owl1.2
- Temporarily disabled regeneration of configure due to conflict with new
autotools.

* Mon Feb 23 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.2.2-owl1.1
- Fixed permission of %_libdir/gcc-lib/%_target_platform/%version/include/*
directories.
- Removed unpackaged files to make RPM4 happy. :)

* Thu Feb 05 2004 Solar Designer <solar-at-owl.openwall.com> 1:3.2.2-owl1
- Added libstdc++ compatibility libraries for gcc 2.95.3 as a separate
source tarball.

* Tue Feb 03 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.2.2-owl0.3
- Cleaned up the spec file (reordered scripts & files sections).
- Avoid using of subshells in build section to not mask possible errors.

* Mon Feb 02 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.2.2-owl0.2
- Added a patch to enable limited wchar support.

* Fri Jan 30 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:3.2.2-owl0.1
- Updated to 3.2.2 version.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 1:2.95.3-owl5
- Deal with info dir entries such that the menu looks pretty.

* Fri Jun 21 2002 Solar Designer <solar-at-owl.openwall.com>
- Provide a cc(1) man page.

* Tue May 28 2002 Solar Designer <solar-at-owl.openwall.com>
- Don't override the linker's default library path for elf32_sparc, place
/lib64 before /usr/lib64 in the path for elf64_sparc; this is needed to
support dynamic linking with libraries from packages which only place the
.so's in /lib (/lib64), not /usr/lib (/usr/lib64).

* Sat May 25 2002 Solar Designer <solar-at-owl.openwall.com>
- Do use some optimization when building the stage1 compiler to make our gcc
builds faster.

* Tue Jan 29 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions (but more cleanups are still needed).
- Dropped the 2.95.2-specific patches entirely.

* Sun Mar 18 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.95.3.
- Dropped the duplicate_decls() patch (included in 2.95.3).
- Various spec file cleanups (use the ix86 macro, avoid subshells).

* Fri Nov 17 2000 Solar Designer <solar-at-owl.openwall.com>
- No pthreads on sparcv9, not just on plain sparc.
- Pass plain sparc- target to configure when building for sparcv9, to
allow for the use of sparcv9 optflags while not confusing configure.
- Check for __arch64__ rather than __sparc_v9__ in limits.h.
- %%defattr(-,root,root) for all architectures, not just x86 and alpha
(no idea why this was restricted).

* Wed Nov 08 2000 Solar Designer <solar-at-owl.openwall.com>
- Added a patch for copying of DECL_MODE in duplicate_decls(), by
Richard Henderson (http://gcc.gnu.org/ml/gcc-patches/1999-11/msg00087.html).

* Sun Oct 29 2000 Solar Designer <solar-at-owl.openwall.com>
- libstdc++-compat is for x86 only, corrected the %ifarch's.

* Sat Oct 21 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- texconfig bug hack

* Fri Oct 20 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- disable dvi generation

* Fri Aug 25 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- removed make -j

* Sat Jul 29 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- spec cleanup.
- duplicate file fix.

* Sun Jul 09 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- Imported from RH.

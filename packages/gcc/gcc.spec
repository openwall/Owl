%define GCC_PREFIX /usr
%define CPP_PREFIX /lib
%define GCC_VERSION 2.95.2
%define STDC_VERSION 2.10.0

%define BUILD_OBJC 	'yes'
%define BUILD_F77	'yes'
%define BUILD_CHILL 	'yes'

Summary:	Various compilers (C, C++, Objective-C, f77, ...)
Name:           gcc
Version:        %{GCC_VERSION}
Release:        2owl
Serial:         1
Copyright:	GPL
URL:            http://gcc.gnu.org
Group:		Development/Languages
Source0:	ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%{GCC_VERSION}.tar.gz
Source1:	libstdc++-compat.tar.bz2
Patch:		gcc-2.95.2-rh-warn.patch
Packager:       <kad@openwall.com>
Distribution:   Owl
BuildRoot:      /var/rpm-buildroot/%{name}-root
Obsoletes: 	egcs
Requires: 	binutils >= 2.9.1.0.25
Requires: 	cpp = %{GCC_VERSION}
Prereq: 	/sbin/install-info

%description
The gcc package contains the GNU Compiler Collection: cc and gcc. You'll need
this package in order to compile C/C++ code.

%package c++
Summary: 	C++ support for gcc
Obsoletes: 	egcs-c++
Group: 		Development/Languages
Requires: 	gcc = %{GCC_VERSION}
Requires: 	cpp = %{GCC_VERSION}

%description c++
This package adds C++ support to the GNU C compiler. It includes support
for most of the current C++ specification, including templates and
exception handling. It does include the static standard C++
library and C++ header files; the library for dynamically linking
programs is available separately.

%package -n libstdc++
Summary: 	GNU c++ library
Group: 		System Environment/Libraries
Obsoletes: 	gcc-libstdc++
Provides: libstdc++-libc6.1-1.so.2 libstdc++-libc6.1-2.so.3 libstdc++.so.2.9

%description -n libstdc++
The libstdc++ package contains a snapshot of the GCC Standard C++
Library v3, an ongoing project to implement the ISO 14882 Standard C++
library.

%ifarch i386 i486 i586 k6 i686 sparc alpha

%package -n libstdc++-compat
Summary: GNU old c++ library
Group: System Environment/Libraries

%description -n libstdc++-compat
This is the GNU implementation of the standard C++ libraries. This package
includes the old shared libraries necessary to run C++ applications.

%endif

%package -n libstdc++-devel
Summary: 	Header files and libraries for C++ development
Group: 		Development/Libraries
Obsoletes: 	gcc-libstdc++-devel

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes SGI's implementation of the STL.

%package -n cpp
Summary: 	The C Preprocessor.
Group: 		Development/Languages
Prereq: 	/sbin/install-info

%description -n cpp
Cpp (or cccp) is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%if "%{BUILD_OBJC}"=="'yes'"
%package objc
Summary: 	Objective C support for gcc
Group:          Development/Languages
Obsoletes:      egcs-objc
Requires:       gcc = %{GCC_VERSION}
Requires:       cpp = %{GCC_VERSION}

%description objc
This package adds Objective C support to the GNU C compiler. Objective
C is a object oriented derivative of the C language, mainly used on
systems running NeXTSTEP. This package does not include the standard
objective C object library.
%endif

%if "%{BUILD_F77}"=="'yes'"
%package g77
Summary: 	Fortran 77 support for gcc
Group:          Development/Languages
Obsoletes: 	egcs-g77
Requires:       gcc = %{GCC_VERSION}

%description g77
This package adds support for compiling Fortran 77 programs with the GNU
compiler.

%endif

%if "%{BUILD_CHILL}"=="'yes'"
%package chill
Summary: 	CHILL support for gcc
Group:          Development/Languages
Requires:       gcc = %{GCC_VERSION}
#Obsoletes: 	gcc-CHILL

%description chill
This package adds support for compiling CHILL programs with the GNU
compiler.

Chill is the "CCITT High-Level Language", where CCITT is the old
name for what is now ITU, the International Telecommunications Union.
It is is language in the Modula2 family, and targets many of the
same applications as Ada (especially large embedded systems).
Chill was never used much in the United States, but is still
being used in Europe, Brazil, Korea, and other places.

%endif


%prep
%setup -q -n gcc-%{GCC_VERSION}

%setup -q -D -T -n gcc-%{GCC_VERSION}
%patch -p1

mkdir compat
bzip2 -cd %{SOURCE1} | tar xv -C compat

# Remove bison-generated files - we want bison 1.28'ish versions...
for i in gcc/cp/parse gcc/c-parse gcc/cexp gcc/java/parse-scan gcc/java/parse gcc/objc/objc-parse; do
    rm -f $i.c
done

%build
rm -fr obj-%{_target_platform}
mkdir obj-%{_target_platform}
cd obj-%{_target_platform}

%ifarch sparc
# pthreads are currently not supported on sparc
CFLAGS="`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g'` -fexceptions" \
	CXXFLAGS="`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g'` -fexceptions" \
	XCFLAGS="`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g'` -fexceptions" \
	TCFLAGS="`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g'` -fexceptions" \
	../configure --prefix=%{GCC_PREFIX} \
	--enable-shared --enable-haifa \
	--host=%{_target_platform}
%else
CFLAGS="`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g'` -fexceptions" \
	CXXFLAGS="`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g'` -fexceptions" \
	XCFLAGS="`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g'` -fexceptions" \
	TCFLAGS="`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g'` -fexceptions" \
	../configure --prefix=%{GCC_PREFIX} \
	--enable-shared --enable-threads=posix --enable-haifa \
	--host=%{_target_platform}
%endif
numprocs=`cat /proc/cpuinfo | grep processor | wc | cut -c7`
if [ "x$numprocs" = "x" -o "x$numprocs" = "x0" ]; then
  numprocs=1
fi
touch ../gcc/c-gperf.h

make -j$numprocs bootstrap-lean

# run the tests.
# rpm seems to terminate when make -k check fails.
# make -k check || true

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/libstdc++ rpm.doc/g77 rpm.doc/chill rpm.doc/objc

(cd libio; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libstdc++/$i.libio
done)
(cd libstdc++; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libstdc++/$i.libstdc++
done)

%install
rm -fr $RPM_BUILD_ROOT

cd obj-%{_target_platform}
make prefix=$RPM_BUILD_ROOT%{GCC_PREFIX} install

FULLVER=`$RPM_BUILD_ROOT%{GCC_PREFIX}/bin/%{_target_platform}-gcc --version | \
	cut -d' ' -f1`
FULLPATH=$(dirname $RPM_BUILD_ROOT%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/$FULLVER/cc1)

file $RPM_BUILD_ROOT/%{GCC_PREFIX}/bin/* | grep ELF | cut -d':' -f1 | xargs strip || :
strip $FULLPATH/cc1

# fix some things
ln -sf gcc $RPM_BUILD_ROOT%{GCC_PREFIX}/bin/cc
rm -f $RPM_BUILD_ROOT%{GCC_PREFIX}/info/dir
gzip -9 $RPM_BUILD_ROOT%{GCC_PREFIX}/info/*.info*

mkdir -p $RPM_BUILD_ROOT/lib
ln -sf ../${FULLPATH##$RPM_BUILD_ROOT/}/cpp $RPM_BUILD_ROOT/lib/cpp

ln -sf cccp.1 $RPM_BUILD_ROOT%{GCC_PREFIX}/man/man1/cpp.1

#install the compatibility libstdc++ library
[ -d ../compat/$RPM_ARCH ] && install -m 755 ../compat/$RPM_ARCH/* $RPM_BUILD_ROOT%{GCC_PREFIX}/lib/

cd ..
cat >gcc-filelist <<EOF
%ifarch i386 i486 i586 i686 alpha
%defattr(-,root,root)
%endif
%{GCC_PREFIX}/bin/gcc
%{GCC_PREFIX}/bin/cc
%{GCC_PREFIX}/bin/protoize
%{GCC_PREFIX}/bin/unprotoize
%{GCC_PREFIX}/bin/gcov
%{GCC_PREFIX}/bin/%{_target_platform}-gcc
%{GCC_PREFIX}/man/man1/gcc.1
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

# This is required for the old RedHat 6. based programs ...

(
cd $RPM_BUILD_ROOT/usr/lib
ln -sf libstdc++-3-libc6.1-2-2.10.0.so libstdc++-libc6.1-1.so.2
ln -sf libstdc++-3-libc6.1-2-2.10.0.so libstdc++-libc6.1-1.1.so.2
ln -sf libstdc++-3-libc6.1-2-2.10.0.so libstdc++.so.2.9
)

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info \
        --info-dir=%{GCC_PREFIX}/info %{GCC_PREFIX}/info/gcc.info.gz

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete \
        --info-dir=%{GCC_PREFIX}/info %{GCC_PREFIX}/info/gcc.info.gz
fi

%post -n libstdc++
if ! grep '^%{GCC_PREFIX}/lib$' /etc/ld.so.conf > /dev/null 2>&1; then
	echo %{GCC_PREFIX}/lib >>/etc/ld.so.conf
fi
/sbin/ldconfig

%postun -n libstdc++
if [ "$1" = "0" ]; then
	grep -v "%{GCC_PREFIX}/lib" /etc/ld.so.conf >/etc/ld.so.conf.new
	mv -f /etc/ld.so.conf.new /etc/ld.so.conf
fi
/sbin/ldconfig

%ifarch i386 i486 i586 k6 i686 alpha sparc

%post -n libstdc++-compat
if ! grep '^%{GCC_PREFIX}/lib$' /etc/ld.so.conf > /dev/null 2>&1; then
	echo %{GCC_PREFIX}/lib >>/etc/ld.so.conf
fi
/sbin/ldconfig

%postun -n libstdc++-compat
if [ "$1" = "0" ]; then
	grep -v "%{GCC_PREFIX}/lib" /etc/ld.so.conf >/etc/ld.so.conf.new
	mv -f /etc/ld.so.conf.new /etc/ld.so.conf
fi
/sbin/ldconfig

%endif

%post -n cpp
/sbin/install-info \
	--info-dir=%{GCC_PREFIX}/info %{GCC_PREFIX}/info/cpp.info.gz

%preun -n cpp
if [ $1 = 0 ]; then
   /sbin/install-info --delete \
	--info-dir=%{GCC_PREFIX}/info %{GCC_PREFIX}/info/cpp.info.gz
fi

/sbin/ldconfig

%files -f gcc-filelist

%files -n cpp
%ifarch i386 i486 i586 i686 alpha
%defattr(-,root,root)
%endif
%{CPP_PREFIX}/cpp
%{GCC_PREFIX}/man/man1/cpp.1
%{GCC_PREFIX}/man/man1/cccp.1
%{GCC_PREFIX}/info/cpp.info*.gz
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/cpp

%files c++
%ifarch i386 i486 i586 i686 alpha
%defattr(-,root,root)
%endif
%{GCC_PREFIX}/man/man1/g++.1
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
%ifarch i386 i486 i586 i686 alpha
%defattr(-,root,root)
%endif
%{GCC_PREFIX}/lib/libstdc++-3-libc*-%{STDC_VERSION}.so
%{GCC_PREFIX}/lib/libstdc++-libc*.so.3
%{GCC_PREFIX}/lib/libstdc++-libc*.so.2
%{GCC_PREFIX}/lib/libstdc++.so.2.9
%dir %{GCC_PREFIX}/lib/gcc-lib
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/libstdc++.so

%ifarch i386 i486 i586 k6 i686 alpha
%files -n libstdc++-compat
%defattr(-,root,root)
%{GCC_PREFIX}/lib/libstdc++.so.2.7.2.8
%{GCC_PREFIX}/lib/libstdc++.so.2.8.0
%{GCC_PREFIX}/lib/libstdc++-2-libc6.1-1-2.9.0.so
%{GCC_PREFIX}/lib/libstdc++-libc6.1-1.so.2
%{GCC_PREFIX}/lib/libstdc++.so.2.9.dummy
%{GCC_PREFIX}/lib/libstdc++.so.2.9
%endif

%ifarch sparc
%files -n libstdc++-compat
%{GCC_PREFIX}/lib/libstdc++.so.2.8.0
%{GCC_PREFIX}/lib/libstdc++-2-libc6.1-1-2.9.0.so
%{GCC_PREFIX}/lib/libstdc++-libc6.1-1.so.2
%endif

%files -n libstdc++-devel
%ifarch i386 i486 i586 i686 alpha
%defattr(-,root,root)
%endif
%{GCC_PREFIX}/lib/libstdc++-3-libc*-%{STDC_VERSION}.a
%{GCC_PREFIX}/lib/libstdc++-libc*.a.3
%{GCC_PREFIX}/include/g++-3
%dir %{GCC_PREFIX}/lib/gcc-lib
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}
%dir %{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/include
%{GCC_PREFIX}/lib/gcc-lib/%{_target_platform}/%{GCC_VERSION}/libstdc++.a
%doc rpm.doc/libstdc++/*


%if "%{BUILD_OBJC}"=="'yes'"
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

%if "%{BUILD_F77}"=="'yes'"
%post g77
/sbin/install-info \
        --info-dir=%{GCC_PREFIX}/info %{GCC_PREFIX}/info/g77.info.bz2

%preun g77
if [ $1 = 0 ]; then
   /sbin/install-info --delete \
        --info-dir=%{GCC_PREFIX}/info %{GCC_PREFIX}/info/g77.info.bz2
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

%if "%{BUILD_CHILL}"=="'yes'"
%post chill
/sbin/install-info \
        --info-dir=%{GCC_PREFIX}/info %{GCC_PREFIX}/info/chill.info.bz2

%preun chill
if [ $1 = 0 ]; then
   /sbin/install-info --delete \
        --info-dir=%{GCC_PREFIX}/info %{GCC_PREFIX}/info/chill.info.bz2
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
* Sun Jul  9 2000 Alexandr D. Kanevskiy <kad@blackcatlinux.com>
- Imported from RH.

* Sat Dec 11 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Obsolete egcs*, g77
- Add egcs 1.1.x'ish libstdc++ versions to libstdc++-compat

* Wed Dec  8 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build on sparc

* Tue Dec  7 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Add -warn patch (adapted from egcs-1.1.2 RPM)
- drop release number to 1 for 7.0 tree

* Tue Oct 26 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.95.2 release

* Sun Oct 24 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- initial RPM

# $Id: Owl/packages/bzip2/bzip2.spec,v 1.8 2002/02/01 21:02:24 solar Exp $

Summary: A file compression utility.
Name: bzip2
Version: 1.0.2
Release: owl0
License: BSD
Group: Applications/File
URL: http://sources.redhat.com/bzip2/
Source: ftp://sources.redhat.com/pub/bzip2/v102/bzip2-%{version}.tar.gz
Patch0: bzip2-1.0.2-owl-Makefiles.diff
Patch1: bzip2-1.0.2-owl-tmp.diff
Requires: mktemp >= 1:1.3.1
Provides: libbz2.so.0
BuildRoot: /override/%{name}-%{version}

%description
bzip2 is a freely available, patent-free, high quality data compressor.

bzip2 compresses files using the Burrows-Wheeler block sorting text
compression algorithm and Huffman coding.  Compression is generally
considerably better than that achieved by more conventional LZ77/LZ78-based
compressors (such as gzip), and approaches the performance of the PPM
family of statistical compressors.  bzip2 is by far not the fastest
compression utility, but it does strike a balance between speed and
compression capability.

%package devel
Summary: Header files and libraries for developing apps which will use bzip2.
Group: Development/Libraries
Requires: bzip2 = %{version}

%description devel
Header files and a static library of bzip2 functions, for developing apps
which will use the library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{expand:%%define optflags %optflags -Wall}

%build
make -f Makefile-libbz2_so CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -fPIC"
rm *.o
make CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64"

%install
rm -rf $RPM_BUILD_ROOT

make install PREFIX="${RPM_BUILD_ROOT}/usr"
make -f Makefile-libbz2_so install PREFIX="${RPM_BUILD_ROOT}/usr"

# Hack!
ln -s libbz2.so.%{version} ${RPM_BUILD_ROOT}%{_libdir}/libbz2.so.0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGES LICENSE README Y2K_INFO
%{_bindir}/*
%{_mandir}/*/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
* Fri Feb 01 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 1.0.2.
- Dropped Red Hat's autoconf/libtoolize patch.
- Use the new Makefile-libbz2_so for building the shared library.
- Package the bzip2 binary that is statically-linked against libbz2 for
better performance on register-starved architectures such as the x86.
- Patched bzdiff/bzcmp (new with 1.0.2) to use mktemp(1) instead of
"tempfile" and to remove the temporary file in all cases.
- Build with -Wall.

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Patched a double-fclose() bug which could be triggered on certain
error conditions including running "bzip2 -f" on a directory (which
is the particular scenario reported to and dealt with by Red Hat).
- Enforce our new spec file conventions.
- Based the new package description on the man page.

* Wed Nov 29 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- bzip2 ver 0.x compat hack

* Sun Oct 01 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
- patch goes to repacked

# $Id: Owl/packages/bzip2/bzip2.spec,v 1.7 2002/01/28 19:23:23 solar Exp $

%define bz2libver 1.0.0

Summary: A file compression utility.
Name: bzip2
Version: 1.0.1
Release: owl6
License: BSD
Group: Applications/File
URL: http://sources.redhat.com/bzip2/
Source0: ftp://sources.redhat.com/pub/bzip2/v100/bzip2-%{version}.tar.gz
Source1: bzgrep
Patch0: bzip2-1.0.1-autoconflibtoolize.patch.gz
Patch1: bzip2-1.0.1-owl-double-fclose-fix.diff
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
cp m4/largefile.m4 .
chmod a+x configure
touch ChangeLog

%build
%configure --enable-shared --enable-static

# XXX avoid rerunning automake et al.
touch aclocal.m4

touch configure
chmod +x install-sh

make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

install -m 755 $RPM_SOURCE_DIR/bzgrep ${RPM_BUILD_ROOT}%{_bindir}

# Hack!
ln -s libbz2.so.%{bz2libver} ${RPM_BUILD_ROOT}%{_libdir}/libbz2.so.0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README README.COMPILATION.PROBLEMS Y2K_INFO NEWS ChangeLog
%{_bindir}/*
%{_mandir}/*/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
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

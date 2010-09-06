# $Owl: Owl/packages/xz/xz.spec,v 1.1 2010/09/06 19:40:21 ldv Exp $

Summary: XZ/LZMA data compression library and tools.
Name: xz
Version: 4.999.9
Release: owl1
License: Public Domain
Group: Applications/File
URL: http://tukaani.org/xz/
%define snapshot xz-4.999.9beta-172-ge6ad
# http://tukaani.org/xz/%snapshot.tar.gz
Source: %snapshot.tar.bz2
BuildRoot: /override/%name-%version

%description
This package provides data compression library and a set of gzip-style
tools for working with files compressed with the Lempel-Ziv-Markov chain
algorithm (LZMA).
It supports two formats: .xz and the older .lzma format.

%package devel
Summary: Development files for liblzma.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
This package provides liblzma development library and header files.

%prep
%setup -q -n %snapshot
sed -i '/SUBDIRS/ s/ scripts//' src/Makefile*

%build
%configure --enable-dynamic
make

%install
rm -rf %buildroot
make install DESTDIR=%buildroot docdir=
rm %buildroot%_libdir/*.la
%find_lang %name

%check
LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make check

%clean
rm -rf %buildroot

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root)
%_libdir/lib*.so.*
%_bindir/*
%_mandir/man1/*
%doc AUTHORS README THANKS doc/faq.txt doc/history.txt

%files devel
%defattr(-,root,root)
%_includedir/*
%_libdir/lib*.so
%_libdir/lib*.a
%_libdir/pkgconfig/*.pc

%changelog
* Mon Sep 06 2010 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.999.9-owl1
- Initial build of xz-4.999.9beta-172-ge6ad for Openwall GNU/*/Linux.

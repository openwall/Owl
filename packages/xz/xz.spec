# $Owl: Owl/packages/xz/xz.spec,v 1.2 2010/11/25 12:05:43 segoon Exp $

Summary: XZ/LZMA data compression library and tools.
Name: xz
Version: 5.0.0
Release: owl1
License: Public Domain
Group: Applications/File
URL: http://tukaani.org/xz/
#%define snapshot xz-4.999.9beta-172-ge6ad
# http://tukaani.org/xz/%snapshot.tar.gz
#Source: %snapshot.tar.bz2
Source: http://tukaani.org/%name/%name-%version.tar.bz2
BuildRoot: /override/%name-%version
%define compat_sonames liblzma.so.0.0.0 liblzma.so.0
Provides: %(test %_lib = lib64 && s='()(64bit)' || s=; for n in %compat_sonames; do echo -n "$n$s "; done)

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
%setup -q
sed -i '/SUBDIRS/ s/ scripts//' src/Makefile*

%build
%configure --enable-dynamic
make

%install
rm -rf %buildroot
%makeinstall \
        docdir=

rm %buildroot%_libdir/*.la
%find_lang %name

for n in %compat_sonames; do 
    ln -s liblzma.so.%version %buildroot%_libdir/$n
done

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
* Thu Nov 25 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 5.0.0-owl1
- Updated to 5.0.0.
- Provided compatibility symlinks for liblzma.so.

* Mon Sep 06 2010 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.999.9-owl1
- Initial build of xz-4.999.9beta-172-ge6ad for Openwall GNU/*/Linux.

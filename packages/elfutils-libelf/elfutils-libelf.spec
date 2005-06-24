# $Id: Owl/packages/elfutils-libelf/elfutils-libelf.spec,v 1.3 2005/06/24 23:06:42 ldv Exp $

Summary: Library to read and write ELF files.
Name: elfutils-libelf
Version: 0.108
Release: owl2
License: GPL
Group: System Environment/Libraries
Source: elfutils-%version.tar.gz
Patch0: elfutils-0.108-rh-robustify.diff
Patch1: elfutils-0.108-owl-fixes.diff
Obsoletes: libelf
BuildRequires: bison >= 1.35
BuildRequires: flex >= 2.5.4a
BuildRequires: gcc >= 3.4
BuildRoot: /override/%name-%version

%description
The elfutils-libelf package provides a DSO which allows reading and
writing ELF files on a high level.  Third party programs depend on
this package to read internals of ELF files.  The programs of the
elfutils package use it also to generate new ELF files.

%package devel
Summary: Development support for libelf.
Group: Development/Libraries
Requires: %name = %version-%release
Obsoletes: libelf-devel

%description devel
The elfutils-libelf-devel package contains the libraries to create
applications for handling compiled objects.  libelf allows you to
access the internals of the ELF object file format, so you can see the
different sections of an ELF file.

%prep
%setup -q -n elfutils-%version
%patch0 -p1
%patch1 -p1

%build
%configure --enable-shared
%__make -C libelf

%install
rm -rf %buildroot
%makeinstall -C libelf

# XXX: Remove unpackaged files (check later)
rm %buildroot%_includedir/elfutils/elf-knowledge.h

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%_libdir/libelf-%version.so
%_libdir/libelf*.so.*

%files devel
%defattr(-,root,root)
%_includedir/libelf.h
%_includedir/gelf.h
%_includedir/nlist.h
%_libdir/libelf.a
%_libdir/libelf.so

%changelog
* Fri Jun 24 2005 Dmitry V. Levin <ldv@owl.openwall.com> 0.108-owl2
- Corrected library symlinks packaging.

* Mon Jun 13 2005 Michail Litvak <mci@owl.openwall.com> 0.108-owl1
- Reworked spec from RH - build only elfutils-libelf and elfutils-libelf-devel.
- Patch to fix compilation on Owl.
- Fixes from RH.

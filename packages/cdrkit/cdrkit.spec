# $Owl: Owl/packages/cdrkit/cdrkit.spec,v 1.3 2009/05/06 16:36:07 solar Exp $

Summary: A collection of command-line CD/DVD recording utilities.
Name: cdrkit
Version: 1.1.9
Release: owl0
License: GPLv2
Group: Applications/System
URL: http://cdrkit.org
Source0: http://cdrkit.org/releases/cdrkit-%version.tar.gz
Source1: cdrkit-build
Source2: cdrkit-install
Source3: align.h
Source4: xconfig.h
# README-cmakeless is unused by this package.
# It is specified here such that it gets included into the .src.rpm file.
Source10: README-cmakeless
#Provides: mkisofs
#Obsoletes: mkisofs
BuildRequires: zlib-devel, bzip2-devel, libmagic-devel, libcap-devel
BuildRequires: glibc >= 0:2.3, sed >= 0:4.1
ExclusiveArch: %ix86 x86_64
BuildRoot: /override/%name-%version

%description
cdrkit is a suite of programs for recording CDs and DVDs, blanking CD-RW
media, creating ISO-9660 filesystem images, extracting audio CD data,
and more.  The programs included in the cdrkit package were originally
derived from several sources, most notably mkisofs by Eric Youngdale and
others, cdda2wav by Heiko Eissfeldt, and cdrecord by Jrg Schilling.
However, cdrkit is not affiliated with any of these authors; it is now
an independent project.

%prep
%setup -q
sed -ni '/^require v5\.8\.1;$/!p' 3rd-party/dirsplit/dirsplit

%build
mkdir build
cp -v %_sourcedir/{align,xconfig}.h build/
CC=%__cc AR=%__ar CFLAGS='%optflags -Wall -Wno-unused' sh %_sourcedir/cdrkit-build

%install
rm -rf %buildroot
DESTDIR=%buildroot/usr sh %_sourcedir/cdrkit-install

%files
%defattr(-,root,root)
%_bindir/*
%_sbindir/*
%_mandir/man?/*

%changelog
* Wed May 06 2009 Solar Designer <solar-at-owl.openwall.com> 1.1.9-owl0
- Initial cmake-less packaging of cdrkit for Openwall GNU/*/Linux.

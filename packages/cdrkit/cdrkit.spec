# $Owl: Owl/packages/cdrkit/cdrkit.spec,v 1.8 2009/05/18 01:50:32 solar Exp $

%{?!BUILD_NETSCSID:	%define BUILD_NETSCSID 0}

Summary: A collection of command-line CD/DVD recording utilities.
Name: cdrkit
Version: 1.1.9
Release: owl3
License: GPLv2
Group: Applications/System
URL: http://cdrkit.org
Source0: http://cdrkit.org/releases/cdrkit-%version.tar.gz
Source1: cdrkit-build
Source2: cdrkit-install
Source3: align.h
Source4: xconfig.h
Source10: README.ATAPI.setup
# README-cmakeless is unused by this package.
# It is specified here such that it gets included into the .src.rpm file.
Source99: README-cmakeless
Patch0: cdrkit-1.1.9-owl-fixes.diff
Patch1: cdrkit-1.1.9-owl-tmp.diff
Patch2: cdrkit-1.1.9-owl-doc.diff
Patch3: cdrkit-1.1.9-owl-rcfile.diff
Patch4: cdrkit-1.1.9-owl-privacy.diff
Patch5: cdrkit-1.1.9-rh-bound.diff
Patch6: cdrkit-1.1.9-owl-messages.diff
Provides: cdrecord = 9:2.01-12, dvdrecord = 0:0.1.5.1
Obsoletes: cdrecord, dvdrecord
Provides: mkisofs = 9:2.01-12
Obsoletes: mkisofs
Provides: cdda2wav = 9:2.01-12
Obsoletes: cdda2wav
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
sed -i '/^require v5\.8\.1;$/d' 3rd-party/dirsplit/dirsplit
sed -i '1s,/usr/local,/usr,' doc/icedax/tracknames.pl
chmod -x doc/icedax/tracknames.pl

# Make sure we don't use or package any files with references to /tmp, except
# for those that have been patched by this point.  If a new reference to /tmp
# is introduced into a build-critical file in a new version, we'd rather have
# the build fail such that we're notified and can make a determination.
find . -type f -print0 |
	xargs -r0 grep -FlZ -- /tmp |
	xargs -r0 rm -vf --

cp -v %_sourcedir/cdrkit-{build,install} .
%if !%BUILD_NETSCSID
sed -i '/netscsid/d' cdrkit-{build,install}
find . -type f -name '*netscsid*' -print -delete
%endif

mkdir build
cp -v %_sourcedir/{align,xconfig}.h build/

install -pm 644 %_sourcedir/README.ATAPI.setup doc/READMEs/

%build
CC=%__cc AR=%__ar CFLAGS='%optflags -fno-strict-aliasing -Wall -Wno-unused' \
	sh cdrkit-build

%install
rm -rf %buildroot
DESTDIR=%buildroot BINDIR=%_bindir SBINDIR=%_sbindir MANDIR=%_mandir \
	sh cdrkit-install
cd %buildroot%_bindir
ln -s genisoimage mkisofs
ln -s genisoimage mkhybrid
ln -s icedax cdda2wav
ln -s wodim cdrecord
ln -s wodim dvdrecord
cd %buildroot%_mandir
ln -s genisoimage.1 man1/mkisofs.1
ln -s genisoimage.1 man1/mkhybrid.1
ln -s icedax.1 man1/cdda2wav.1
ln -s wodim.1 man1/cdrecord.1
ln -s wodim.1 man1/dvdrecord.1

%files
%defattr(-,root,root)
%doc ABOUT COPYING FAQ FORK
%doc doc/READMEs doc/genisoimage doc/icedax doc/wodim
%_bindir/*
%if %BUILD_NETSCSID
%_sbindir/netscsid
%endif
%_mandir/man?/*

%changelog
* Mon May 18 2009 Solar Designer <solar-at-owl.openwall.com> 1.1.9-owl3
- Patched some confusing/erroneous messages from wodim(1).
- Replaced README.ATAPI.setup with a version more useful on Owl (loosely
based on the original file found in the included cdrkit documentation).

* Sat May 09 2009 Solar Designer <solar-at-owl.openwall.com> 1.1.9-owl2
- Ported the patches found in our mkisofs package (to be removed) to
genisoimage.
- Added security warnings to the documentation (man pages, README.suidroot).

* Fri May 08 2009 Solar Designer <solar-at-owl.openwall.com> 1.1.9-owl1
- Disabled building/packaging of netscsid by default (this program, if
used, may pose a significant security risk, yet most Owl users won't
need it, so we'd rather exclude it and thus not be responsible for it).
- Patched some issues in C source files as pointed out by gcc warnings
and FIXME comments.
- Patched out some unimportant references to /tmp, made this spec file
remove any remaining files with references to /tmp.
- Added symlinks and Obsoletes/Provides tags to replace our mkisofs
package and for compatibility with the Fedora package.
- Package some documentation files (a further review may be needed).

* Wed May 06 2009 Solar Designer <solar-at-owl.openwall.com> 1.1.9-owl0
- Initial cmake-less packaging of cdrkit for Openwall GNU/*/Linux
(not released).

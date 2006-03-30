# $Owl: Owl/packages/file/file.spec,v 1.16 2006/03/30 02:27:37 galaxy Exp $

Summary: A utility for determining file types.
Name: file
Version: 4.16
Release: owl2
License: distributable
Group: Applications/File
URL: http://www.darwinsys.com/file/
Source0: ftp://ftp.astron.com/pub/file/file-%version.tar.gz
Source1: magic.local
Patch0: file-4.16-rh-alt-compress.diff
Patch1: file-4.16-rh-alt-elf.diff
Patch2: file-4.16-deb-owl-fixes.diff
Patch3: file-4.16-rh-order.diff
Patch4: file-4.16-rh-selinux.diff
Patch5: file-4.16-alt-magic.diff
Patch6: file-4.16-deb-magic.diff
Patch7: file-4.16-deb-owl-man.diff
Prefix: %_prefix
Requires: libmagic = %version-%release
BuildRequires: zlib-devel, automake, autoconf
BuildRoot: /override/%name-%version

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  file can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

%package -n libmagic
Summary: Shared library for handling magic files.
Group: System Environment/Libraries

%description -n libmagic
This package contains shared library for handling magic files.

%package -n libmagic-devel
Summary: Development files to build applications that handle magic files.
Group: Development/Libraries
Requires: libmagic = %version-%release

%description -n libmagic-devel
This package contains development files to build applications that handle
magic files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%{expand:%%define optflags %optflags -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -Wall}

%build
autoreconf -f
%configure --enable-fsect-man5
%__make

%install
rm -rf %buildroot
mkdir -p %buildroot%_bindir
mkdir -p %buildroot%_mandir/man{1,5}
mkdir -p %buildroot%_datadir

%makeinstall
install -p -D -m 644 %_sourcedir/magic.local %buildroot/etc/magic

ln -s file/magic %buildroot%_datadir/magic
ln -s file/magic.mime %buildroot%_datadir/magic.mime

rm -f %buildroot%_libdir/*.la

%files
%defattr(-,root,root)
%config(noreplace) /etc/magic
%_bindir/*
%_datadir/magic*
%dir %_datadir/file
%_datadir/file/*
%_mandir/man1/*
%_mandir/man5/*

%files -n libmagic
%defattr(-,root,root)
%_libdir/*.so.*

%files -n libmagic-devel
%defattr(-,root,root)
%_libdir/*.so
%_libdir/*.a
%_includedir/*
%_mandir/man3/*

%changelog
* Tue Mar 30 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.16-owl2
- Dropped LDFLAGS=-s from the %%build section, let's brp-* scripts do their
work.
- Added the %%_datadir/file directory to the filelist (it was orhaned).

* Sun Oct 23 2005 Michail Litvak <mci-at-owl.openwall.com> 4.16-owl1
- 4.16
- Updated patches.
- New subpackages libmagic, libmagic-devel.

* Thu Feb 26 2004 Michail Litvak <mci-at-owl.openwall.com> 3.41-owl3
- Fixed building with new auto* tools.

* Tue Apr 29 2003 Michail Litvak <mci-at-owl.openwall.com> 3.41-owl2
- Patch to remove annoying message: "Using regular magic file..."

* Fri Mar 07 2003 Michail Litvak <mci-at-owl.openwall.com>
- 3.41
- Patch updates

* Thu Jan 31 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Nov 29 2000 Michail Litvak <mci-at-owl.openwall.com>
- Imported from RH and updated to 3.33
- added some patches from Debian and RH

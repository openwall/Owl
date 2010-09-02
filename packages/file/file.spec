# $Owl: Owl/packages/file/file.spec,v 1.26 2010/09/02 19:31:19 segoon Exp $

Summary: A utility for determining file types.
Name: file
Version: 5.04
Release: owl2
License: distributable
Group: Applications/File
URL: http://www.darwinsys.com/file/
Source0: ftp://ftp.astron.com/pub/file/file-%version.tar.gz
Source1: magic.local
Patch0: file-5.04-rh-alt-compress.diff
Patch1: file-5.04-deb-owl-fixes.diff
Patch2: file-5.04-alt-magic.diff
Patch3: file-5.04-deb-magic.diff
Patch4: file-5.04-deb-owl-man.diff
Patch5: file-5.04-deb-doc-manpages-typo.diff
Patch6: file-5.04-rh-owl-ulaw-segfault.diff
Patch7: file-5.04-rh-core-prpsinfo.diff
Patch8: file-5.04-deb-core-trim.diff
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
%patch8 -p1

%{expand:%%define optflags %optflags -D_GNU_SOURCE -Wall}

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

rm %buildroot%_libdir/*.la

%files
%defattr(-,root,root)
%doc COPYING ChangeLog README TODO
%config(noreplace) /etc/magic
%_bindir/*
%_datadir/misc/magic*
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
* Wed Sep 02 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 5.04-owl2
- Silenced incorrect 'from' field message, patch from fedora
  (https://bugzilla.redhat.com/show_bug.cgi?id=599695).
- Fixed segfault, patch from fedora, additionally silenced compiler warning
  (https://bugzilla.redhat.com/show_bug.cgi?id=533245).
- Do not trim 'from' field of core files, debian patch
  (https://bugzilla.redhat.com/show_bug.cgi?id=566305,
   http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=422524).

* Wed Sep 01 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 5.04-owl1
- Updated to 5.04.
- Updated patches.
- Dropped patches rh-selinux, rh-alt-elf, owl-bound (fixed in upstream).
- Dropped patch rh-order.
- Imported patch from debian (doc-manpages-typo).

* Tue May 22 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.16-owl4
- Fixed integer overflow check in file_printf function, reported by
Colin Percival.

* Sun Mar 25 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.16-owl3
- Fixed potential heap corruption in file_printf function (CVE-2007-1536).
- Removed no longer required addition of "-D_FILE_OFFSET_BITS=64
-D_LARGEFILE_SOURCE" flags to %%optflags.

* Thu Mar 30 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.16-owl2
- Dropped LDFLAGS=-s from the %%build section, let's allow brp-* scripts
to do their work.
- Added the %%_datadir/file directory to the filelist (it was orphaned).

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

# $Id: Owl/packages/e2fsprogs/e2fsprogs.spec,v 1.15 2004/02/11 21:48:02 solar Exp $

Summary: Utilities for managing the second extended (ext2) filesystem.
Name: e2fsprogs
Version: 1.27
Release: owl5
License: GPL
Group: System Environment/Base
Source: http://prdownloads.sourceforge.net/e2fsprogs/e2fsprogs-%version.tar.gz
Patch0: e2fsprogs-1.27-alt-fixes.diff
Patch1: e2fsprogs-1.27-alt-notitle.diff
Patch2: e2fsprogs-1.27-rh-c++.diff
Patch3: e2fsprogs-1.27-rh-owl-mountlabel3.diff
Patch4: e2fsprogs-1.27-owl-lost+found-mode.diff
Patch5: e2fsprogs-1.27-owl-warnings.diff
Patch6: e2fsprogs-1.27-owl-info.diff
PreReq: /sbin/ldconfig
BuildRoot: /override/%name-%version

%description
The e2fsprogs package contains a number of utilities for creating,
checking, modifying and correcting any inconsistencies in second
extended (ext2) filesystems.  e2fsprogs contains e2fsck (used to repair
filesystem inconsistencies after an unclean shutdown), mke2fs (used to
initialize a partition to contain an empty ext2 filesystem), debugfs
(used to examine the internal structure of a filesystem, to manually
repair a corrupted filesystem or to create test cases for e2fsck), tune2fs
(used to modify filesystem parameters) and most of the other core ext2fs
filesystem utilities.

%package devel
Summary: Ext2 filesystem-specific static libraries and headers.
Group: Development/Libraries
PreReq: /sbin/install-info
Requires: e2fsprogs

%description devel
e2fsprogs-devel contains the libraries and header files needed to
develop second extended (ext2) filesystem-specific programs.

%prep
%setup -q
chmod -R u+w .
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%{expand:%%define optflags %optflags -Wall}

%build
# There're currently no pre-compiled versions of these texinfo files
# included, should uncomment if that changes.
#rm doc/libext2fs.info
autoconf
%configure --enable-elf-shlibs
make

%install
rm -rf $RPM_BUILD_ROOT
make install install-libs DESTDIR="$RPM_BUILD_ROOT" \
	root_sbindir=/sbin root_libdir=/lib

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %_infodir/libext2fs.info.gz %_infodir/dir

%postun devel
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/libext2fs.info.gz %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc README RELEASE-NOTES ChangeLog

/sbin/badblocks
/sbin/debugfs
/sbin/dumpe2fs
/sbin/e2fsck
/sbin/e2label
/sbin/fsck
/sbin/fsck.ext2
/sbin/fsck.ext3
/sbin/mke2fs
/sbin/mkfs.ext2
/sbin/mkfs.ext3
/sbin/tune2fs
%_sbindir/mklost+found

/lib/libcom_err.so.*
/lib/libe2p.so.*
/lib/libext2fs.so.*
/lib/libss.so.*
/lib/libuuid.so.*

%_bindir/chattr
%_bindir/lsattr
%_bindir/uuidgen
%_mandir/man1/chattr.1*
%_mandir/man1/lsattr.1*
%_mandir/man1/uuidgen.1*

%_mandir/man3/libuuid.3*
%_mandir/man3/uuid_clear.3*
%_mandir/man3/uuid_compare.3*
%_mandir/man3/uuid_copy.3*
%_mandir/man3/uuid_generate.3*
%_mandir/man3/uuid_is_null.3*
%_mandir/man3/uuid_parse.3*
%_mandir/man3/uuid_time.3*
%_mandir/man3/uuid_unparse.3*

%_mandir/man8/badblocks.8*
%_mandir/man8/debugfs.8*
%_mandir/man8/dumpe2fs.8*
%_mandir/man8/e2fsck.8*
%_mandir/man8/e2label.8*
%_mandir/man8/fsck.8*
%_mandir/man8/fsck.ext2.8*
%_mandir/man8/fsck.ext3.8*
%_mandir/man8/mke2fs.8*
%_mandir/man8/mkfs.ext2.8*
%_mandir/man8/mkfs.ext3.8*
%_mandir/man8/mklost+found.8*
%_mandir/man8/tune2fs.8*

%files devel
%defattr(-,root,root)
%_infodir/libext2fs.info*
%_bindir/compile_et
%_bindir/mk_cmds

%_libdir/libcom_err.a
%_libdir/libcom_err.so
%_libdir/libe2p.a
%_libdir/libe2p.so
%_libdir/libext2fs.a
%_libdir/libext2fs.so
%_libdir/libss.a
%_libdir/libss.so
%_libdir/libuuid.a
%_libdir/libuuid.so

%_datadir/et
%_datadir/ss
%_includedir/et
%_includedir/ext2fs
%_includedir/ss
%_includedir/uuid
%_mandir/man1/compile_et.1*
%_mandir/man3/com_err.3*

%changelog
* Mon Feb 09 2004 Michail Litvak <mci@owl.openwall.com> 1.27-owl5
- Use RPM macros instead of explicit paths.

* Sat Oct 12 2002 Solar Designer <solar@owl.openwall.com> 1.27-owl4
- Dropped the mke2fs lost+found permissions patch (leaving only the hunks
for e2fsck and mklost+found) as it's no longer needed with 1.27.

* Wed Oct 09 2002 Solar Designer <solar@owl.openwall.com>
- Updated the lost+found permissions patch to cover e2fsck as well, thanks
to Jarno Huuskonen for noticing that this was missing.

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Mon Apr 22 2002 Michail Litvak <mci@owl.openwall.com>
- 1.27
- Build with -Wall
- Added some reviewed patches from RH and ALT, removed unnecessary patches

* Wed Jan 30 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.
- New source URL

* Tue Aug 08 2000 Solar Designer <solar@owl.openwall.com>
- Added a patch by Miquel van Smoorenburg to fix the progress indicator
in e2fsck.

* Wed Aug 03 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file from RH.
- Added a patch for the permissions on lost+found.

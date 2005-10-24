# $Id: Owl/packages/e2fsprogs/e2fsprogs.spec,v 1.30 2005/10/24 03:06:23 solar Exp $

# Owl doesn't have pkgconfig yet
%define USE_PKGCONFIG 0
# compression is experimental feature
%define BUILD_COMPRESSION 0
# profiling needs frame pointers
%define BUILD_PROFILE 0
# our gcc doesn't support -checker option
%define BUILD_CHECKER 0
%define BUILD_DEBUG 0

Summary: Utilities for managing the second extended (ext2) filesystem.
Name: e2fsprogs
Version: 1.37
Release: owl2
License: GPL
Group: System Environment/Base
Source: http://prdownloads.sourceforge.net/e2fsprogs/e2fsprogs-%version.tar.gz
Patch0: e2fsprogs-1.37-owl-fixes.diff
Patch1: e2fsprogs-1.37-owl-tests.diff
Patch2: e2fsprogs-1.37-owl-blkid-env.diff
Patch3: e2fsprogs-1.37-owl-messages.diff
PreReq: /sbin/ldconfig
BuildRequires: gettext, texinfo, automake, autoconf
%if !%USE_PKGCONFIG
BuildRequires: rpm-build >= 0:4
%endif
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

%{expand:%%define optflags %optflags -Wall}

%build
# There're currently no pre-compiled versions of these texinfo files
# included, should uncomment if that changes.
#rm doc/libext2fs.info
%configure \
	--with-cc="%__cc" \
	--enable-elf-shlibs \
	--enable-htree \
	--enable-htree-clear \
	--enable-nls \
%if %BUILD_COMPRESSION
	--enable-compression \
%endif
%if %BUILD_PROFILE
	--enable-profile \
%endif
%if %BUILD_CHECKER
	--enable-checker \
%endif
%if %BUILD_DEBUG
	--enable-jbd-debug \
	--enable-blkid-debug \
	--enable-testio-debug \
%endif
	--enable-maintainer-mode # to build NLS files

# NB: this package cannot be built using parallel tasks -- (GM)
%__make all check

%install
rm -rf %buildroot
%__make install install-libs DESTDIR="%buildroot" LDCONFIG= \
	root_sbindir=/sbin root_libdir=/%_lib

/sbin/ldconfig -N -n %buildroot%_libdir

# this binary has no documentation and its use is under question
rm %buildroot%_libdir/e2initrd_helper

# fix permissions
chmod 0644 %buildroot%_libdir/*.a

%find_lang %name

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %_infodir/libext2fs.info.gz %_infodir/dir

%postun devel
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/libext2fs.info.gz %_infodir/dir
fi

%files -f %name.lang
%defattr(-,root,root)
%doc README RELEASE-NOTES ChangeLog

/sbin/badblocks
/sbin/blkid
/sbin/debugfs
/sbin/dumpe2fs
/sbin/e2fsck
/sbin/e2image
/sbin/e2label
/sbin/findfs
/sbin/fsck
/sbin/fsck.ext2
/sbin/fsck.ext3
/sbin/logsave
/sbin/mke2fs
/sbin/mkfs.ext2
/sbin/mkfs.ext3
/sbin/resize2fs
/sbin/tune2fs
%_sbindir/filefrag
%_sbindir/mklost+found

/%_lib/libblkid.so.*
/%_lib/libcom_err.so.*
/%_lib/libe2p.so.*
/%_lib/libext2fs.so.*
/%_lib/libss.so.*
/%_lib/libuuid.so.*

%_bindir/chattr
%_bindir/lsattr
%_bindir/uuidgen
%_mandir/man1/chattr.1*
%_mandir/man1/lsattr.1*
%_mandir/man1/uuidgen.1*

%_mandir/man8/badblocks.8*
%_mandir/man8/blkid.8*
%_mandir/man8/debugfs.8*
%_mandir/man8/dumpe2fs.8*
%_mandir/man8/e2fsck.8*
%_mandir/man8/e2image.8*
%_mandir/man8/e2label.8*
%_mandir/man8/filefrag.8*
%_mandir/man8/findfs.8*
%_mandir/man8/fsck.8*
%_mandir/man8/fsck.ext2.8*
%_mandir/man8/fsck.ext3.8*
%_mandir/man8/logsave.8*
%_mandir/man8/mke2fs.8*
%_mandir/man8/mkfs.ext2.8*
%_mandir/man8/mkfs.ext3.8*
%_mandir/man8/mklost+found.8*
%_mandir/man8/resize2fs.8*
%_mandir/man8/tune2fs.8*

%files devel
%defattr(-,root,root)
%_infodir/libext2fs.info*
%_bindir/compile_et
%_bindir/mk_cmds

%_libdir/libblkid.a
%_libdir/libblkid.so
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

%if %USE_PKGCONFIG
%_libdir/pkgconfig/blkid.pc
%_libdir/pkgconfig/com_err.pc
%_libdir/pkgconfig/e2p.pc
%_libdir/pkgconfig/ext2fs.pc
%_libdir/pkgconfig/ss.pc
%_libdir/pkgconfig/uuid.pc
%else
%exclude %_libdir/pkgconfig
%endif

%_datadir/et
%_datadir/ss
%_includedir/blkid
%_includedir/e2p
%_includedir/et
%_includedir/ext2fs
%_includedir/ss
%_includedir/uuid

%_mandir/man1/compile_et.1*
%_mandir/man1/mk_cmds.1*
%_mandir/man3/com_err.3*
%_mandir/man3/libblkid.3*
%_mandir/man3/uuid.3*
%_mandir/man3/uuid_clear.3*
%_mandir/man3/uuid_compare.3*
%_mandir/man3/uuid_copy.3*
%_mandir/man3/uuid_generate*.3*
%_mandir/man3/uuid_is_null.3*
%_mandir/man3/uuid_parse.3*
%_mandir/man3/uuid_time.3*
%_mandir/man3/uuid_unparse.3*

%changelog
* Sun Sep 04 2005 Solar Designer <solar-at-owl.openwall.com> 1.37-owl2
- Corrected grammar in the error message fsck outputs on conflicting options.

* Fri Mar 25 2005 Solar Designer <solar-at-owl.openwall.com> 1.37-owl1
- Updated to 1.37 (the previous update to 1.36 was never made public).
- Patched blkid_get_cache() to use __secure_getenv() instead of an explicit
UID/EUID check.
- Fixed more compiler warnings, including some for real bugs.

* Mon Mar 01 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.36-owl1
- Updated to 1.36.
- Reviewed all patches, dropped the ones accepted.
- Dropped the "notitle" patch.
- Fixed make check to fail in case of failed tests.

* Sun Jan 09 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.27-owl7
- Using %__cc macro during configure
- Cleaned up the spec.

* Tue Nov 02 2004 Solar Designer <solar-at-owl.openwall.com> 1.27-owl6
- Bumped the release to reflect Galaxy's change to remove unpackaged files.

* Mon Feb 09 2004 Michail Litvak <mci-at-owl.openwall.com> 1.27-owl5
- Use RPM macros instead of explicit paths.

* Sat Oct 12 2002 Solar Designer <solar-at-owl.openwall.com> 1.27-owl4
- Dropped the mke2fs lost+found permissions patch (leaving only the hunks
for e2fsck and mklost+found) as it's no longer needed with 1.27.

* Wed Oct 09 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated the lost+found permissions patch to cover e2fsck as well, thanks
to Jarno Huuskonen for noticing that this was missing.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Mon Apr 22 2002 Michail Litvak <mci-at-owl.openwall.com>
- 1.27
- Build with -Wall
- Added some reviewed patches from RH and ALT, removed unnecessary patches

* Wed Jan 30 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.
- New source URL

* Tue Aug 08 2000 Solar Designer <solar-at-owl.openwall.com>
- Added a patch by Miquel van Smoorenburg to fix the progress indicator
in e2fsck.

* Wed Aug 03 2000 Solar Designer <solar-at-owl.openwall.com>
- Imported this spec file from RH.
- Added a patch for the permissions on lost+found.

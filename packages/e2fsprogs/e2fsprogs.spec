# $Owl: Owl/packages/e2fsprogs/e2fsprogs.spec,v 1.51 2009/10/13 23:03:12 solar Exp $

# Owl doesn't have pkgconfig yet
%define USE_PKGCONFIG 0
# compression is experimental feature
%define BUILD_COMPRESSION 0
# profiling needs frame pointers
%define BUILD_PROFILE 0
# our gcc doesn't support -checker option
%define BUILD_CHECKER 0
%define BUILD_DEBUG 0

Summary: Utilities for managing ext2/ext3/ext4 filesystems.
Name: e2fsprogs
Version: 1.41.9
Release: owl1
License: GPL
Group: System Environment/Base
URL: http://e2fsprogs.sourceforge.net
Source: http://prdownloads.sourceforge.net/e2fsprogs/e2fsprogs-%version.tar.gz
# Signature: http://prdownloads.sourceforge.net/e2fsprogs/e2fsprogs-%version.tar.gz.asc
# http://repo.or.cz/w/e2fsprogs.git?a=shortlog;h=maint
#Patch0: e2fsprogs-1.40.4-git-20071229-maint.diff
Patch1: e2fsprogs-1.41.5-alt-fixes.diff
Patch2: e2fsprogs-1.41.5-owl-blkid-env.diff
Patch3: e2fsprogs-1.41.5-owl-tests.diff
Patch4: e2fsprogs-1.41.9-owl-warnings.diff
PreReq: /sbin/ldconfig
BuildRequires: gettext, texinfo, automake, autoconf
BuildRequires: glibc >= 0:2.2, sed >= 0:4.1
%if !%USE_PKGCONFIG
BuildRequires: rpm-build >= 0:4
%endif
BuildRoot: /override/%name-%version

%description
The e2fsprogs package contains a number of utilities for creating,
checking, modifying, and correcting any inconsistencies in ext2, ext3,
and ext4 filesystems.  E2fsprogs contains e2fsck (used to repair
filesystem inconsistencies after an unclean shutdown), mke2fs (used to
initialize a partition to contain an empty ext2 filesystem), debugfs
(used to examine the internal structure of a filesystem, to manually
repair a corrupted filesystem or to create test cases for e2fsck),
tune2fs (used to modify filesystem parameters), resize2fs to grow and
shrink unmounted ext2 filesystems, and most of the other core ext2fs
filesystem utilities.

%package devel
Summary: Ext2/ext3/ext4 filesystem-specific static libraries and headers.
Group: Development/Libraries
PreReq: /sbin/install-info
Requires: e2fsprogs = %version-%release

%description devel
e2fsprogs-devel contains the libraries and header files needed to build
ext2, ext3, and/or ext4 filesystem-specific programs.

%prep
%setup -q
chmod -R u+w .
#patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
bzip2 -9k RELEASE-NOTES

# remove these unwanted header files just in case
rm -r include

# add noreturn attribute to usage functions
find -type f -print0 |
	xargs -r0 grep -lZ '^static void usage' -- |
	xargs -r0 sed -i 's/^static void usage/__attribute__((noreturn)) &/' --

%{expand:%%define optflags %optflags -Wall}

%build
# There're currently no pre-compiled versions of these texinfo files
# included, should uncomment if that changes.
#rm doc/libext2fs.info
%configure \
	--with-cc="%__cc" \
	--disable-e2initrd-helper \
	--disable-tls \
	--disable-uuidd \
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
%__make all

%check
%__make check

%install
rm -rf %buildroot
%__make install install-libs DESTDIR="%buildroot" LDCONFIG= \
	root_sbindir=/sbin root_libdir=/%_lib

# make symlinks relative
for f in %buildroot%_libdir/*.so; do
	v="$(readlink -v "$f")"
	v="${v##*/}"
	ln -sf ../../%_lib/"$v" "$f"
done

# fix permissions
chmod 644 %buildroot%_libdir/*.a

# ensure that %buildroot did not get into installed files
sed -i 's,^ET_DIR=.*$,ET_DIR=%_datadir/et,' %buildroot%_bindir/compile_et
sed -i 's,^SS_DIR=.*$,SS_DIR=%_datadir/ss,' %buildroot%_bindir/mk_cmds
! fgrep -rl %buildroot %buildroot/

%find_lang %name

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %_infodir/libext2fs.info %_infodir/dir

%postun devel
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/libext2fs.info %_infodir/dir
fi

%files -f %name.lang
%defattr(-,root,root)
%doc README RELEASE-NOTES.bz2

%config(noreplace) %_sysconfdir/*.conf

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
/sbin/fsck.ext4
/sbin/fsck.ext4dev
/sbin/logsave
/sbin/mke2fs
/sbin/mkfs.ext2
/sbin/mkfs.ext3
/sbin/mkfs.ext4
/sbin/mkfs.ext4dev
/sbin/resize2fs
/sbin/tune2fs
/sbin/e2undo
%_sbindir/filefrag
%_sbindir/e2freefrag
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
%_mandir/man5/*
%_mandir/man8/badblocks.8*
%_mandir/man8/blkid.8*
%_mandir/man8/debugfs.8*
%_mandir/man8/dumpe2fs.8*
%_mandir/man8/e2fsck.8*
%_mandir/man8/e2image.8*
%_mandir/man8/e2label.8*
%_mandir/man8/e2undo.8*
%_mandir/man8/filefrag.8*
%_mandir/man8/e2freefrag.8*
%_mandir/man8/findfs.8*
%_mandir/man8/fsck.8*
%_mandir/man8/fsck.ext2.8*
%_mandir/man8/fsck.ext3.8*
%_mandir/man8/fsck.ext4.8*
%_mandir/man8/fsck.ext4dev.8*
%_mandir/man8/logsave.8*
%_mandir/man8/mke2fs.8*
%_mandir/man8/mkfs.ext2.8*
%_mandir/man8/mkfs.ext3.8*
%_mandir/man8/mkfs.ext4.8*
%_mandir/man8/mkfs.ext4dev.8*
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
* Mon Oct 12 2009 Michail Litvak <mci-at-owl.openwall.com> 1.41.9-owl1
- Updated to 1.41.9.
- Updated -owl-warnings patch.

* Thu May 05 2009 Michail Litvak <mci-at-owl.openwall.com> 1.41.5-owl2
- Fixed compiler warnings.

* Thu Apr 30 2009 Michail Litvak <mci-at-owl.openwall.com> 1.41.5-owl1
- Updated to 1.41.5.
- Dropped -owl-alt-maint-fixes patch (fixed in upstream).

* Tue Jan 01 2008 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.40.4-owl1
- Updated to 1.40.4.

* Thu Dec 06 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.40.2-owl2
- Updated to post-1.40.2 snapshot 20071202 of e2fsprogs maint branch.
- Applied upstream patch to fix integer overflows in libext2fs (CVE-2007-5497).

* Thu Nov 15 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.40.2-owl1
- Updated to post-1.40.2 snapshot 20071015 of e2fsprogs maint branch.
- Removed the /proc workaround added in previous build.

* Mon Mar 26 2007 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.39-owl4
- Added a fix for running tests on a system without the /proc filesystem
mounted (e.g. chroot'ed installation).
A side effect of the above patch is that resize2fs honours the -f
option now and the tool doesn't abort if it cannot determine whether a
requested filesystem is mounted or not.  IMHO, this is not an issue
since -f is dangerous anyway and only experiencied users should use this
option.

* Sun Oct 29 2006 Alexandr D. Kanevskiy <kad-at-owl.openwall.com> 1.39-owl3
- Patch from upstream Mercurial repository:
Changeset 1953: Fix SIGBUS through unaligned access to FAT superblocks.

* Fri Jun 16 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.39-owl2
- Fixed temporary file handling issues during the build process.

* Tue Jun 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.39-owl1
- Updated to 1.39.

* Sun Mar 12 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.37-owl4
- Made %_libdir/*.so symlinks relative.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.37-owl3
- Compressed ChangeLog and RELEASE-NOTES files.
- Corrected info files installation.

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

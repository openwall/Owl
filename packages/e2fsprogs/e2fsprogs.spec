# $Id: Owl/packages/e2fsprogs/e2fsprogs.spec,v 1.2 2000/08/03 00:57:10 solar Exp $

Summary: Utilities for managing the second extended (ext2) filesystem.
Name: e2fsprogs
Version: 1.18
Release: 6owl
Copyright: GPL
Group: System Environment/Base
Source: ftp://sunsite.unc.edu/pub/Linux/system/filesystems/ext2/e2fsprogs-%{version}.tar.gz
Patch0: e2fsprogs-1.18-owl-lost+found-mode.diff
Patch1: e2fsprogs-1.18-rh-debugfs-y2k.diff
Patch2: e2fsprogs-1.18-rh-et.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Prereq: /sbin/ldconfig

%description
The e2fsprogs package contains a number of utilities for creating,
checking, modifying and correcting any inconsistencies in second
extended (ext2) filesystems.  E2fsprogs contains e2fsck (used to repair
filesystem inconsistencies after an unclean shutdown), mke2fs (used to
initialize a partition to contain an empty ext2 filesystem), debugfs
(used to examine the internal structure of a filesystem, to manually
repair a corrupted filesystem or to create test cases for e2fsck), tune2fs
(used to modify filesystem parameters) and most of the other core ext2fs
filesystem utilities.

You should install the e2fsprogs package if you need to manage the
performance of an ext2 filesystem.

%package devel
Summary: Ext2 filesystem-specific static libraries and headers.
Group: Development/Libraries
Requires: e2fsprogs
Prereq: /sbin/install-info

%description devel
E2fsprogs-devel contains the libraries and header files needed to
develop second extended (ext2) filesystem-specific programs.

You should install e2fsprogs-devel if you want to develop ext2
filesystem-specific programs.  If you install e2fsprogs-devel, you'll
also want to install e2fsprogs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
autoconf
#CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr --enable-elf-shlibs
%configure --enable-elf-shlibs
make libs progs docs

%install
rm -rf $RPM_BUILD_ROOT
export PATH=/sbin:$PATH
make install install-libs DESTDIR="$RPM_BUILD_ROOT" \
	root_sbindir=/sbin root_libdir=/lib

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info /usr/info/libext2fs.info.gz /usr/info/dir

%postun devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete /usr/info/libext2fs.info.gz /usr/info/dir
fi

%files
%defattr(-,root,root)
%doc README RELEASE-NOTES

/sbin/badblocks
/sbin/debugfs
/sbin/dumpe2fs
/sbin/e2fsck
/sbin/e2label
/sbin/fsck
/sbin/fsck.ext2
/sbin/mke2fs
/sbin/mkfs.ext2
/sbin/tune2fs
/usr/sbin/mklost+found

/lib/libcom_err.so.*
/lib/libe2p.so.*
/lib/libext2fs.so.*
/lib/libss.so.*
/lib/libuuid.so.*

/usr/bin/chattr
/usr/bin/lsattr
/usr/bin/uuidgen
/usr/man/man1/chattr.1*
/usr/man/man1/lsattr.1*
/usr/man/man1/uuidgen.1*

/usr/man/man8/badblocks.8*
/usr/man/man8/debugfs.8*
/usr/man/man8/dumpe2fs.8*
/usr/man/man8/e2fsck.8*
/usr/man/man8/e2label.8*
/usr/man/man8/fsck.8*
/usr/man/man8/mke2fs.8*
/usr/man/man8/mklost+found.8*
/usr/man/man8/tune2fs.8*

%files devel
%defattr(-,root,root)
/usr/info/libext2fs.info*
/usr/bin/compile_et
/usr/bin/mk_cmds

/usr/lib/libcom_err.a
/usr/lib/libcom_err.so
/usr/lib/libe2p.a
/usr/lib/libe2p.so
/usr/lib/libext2fs.a
/usr/lib/libext2fs.so
/usr/lib/libss.a
/usr/lib/libss.so
/usr/lib/libuuid.a
/usr/lib/libuuid.so

/usr/share/et
/usr/share/ss
/usr/include/et
/usr/include/ext2fs
/usr/include/ss
/usr/include/uuid
/usr/man/man1/compile_et.1*
/usr/man/man3/com_err.3*

%changelog
* Wed Aug 03 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file from RH.
- Added a patch for the permissions on lost+found.

# $Id: Owl/packages/e2fsprogs/e2fsprogs.spec,v 1.7 2002/01/31 18:18:31 solar Exp $

Summary: Utilities for managing the second extended (ext2) filesystem.
Name: e2fsprogs
Version: 1.18
Release: owl7
License: GPL
Group: System Environment/Base
Source: http://prdownloads.sourceforge.net/e2fsprogs/e2fsprogs-%{version}.tar.gz
Patch0: ftp://ftp.cistron.nl/pub/people/miquels/misc/e2fsprogs-1.18-spinnerfix.diff
Patch1: e2fsprogs-1.18-owl-lost+found-mode.diff
Patch2: e2fsprogs-1.18-rh-debugfs-y2k.diff
Patch3: e2fsprogs-1.18-rh-et.diff
PreReq: /sbin/ldconfig
BuildRoot: /override/%{name}-%{version}

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
autoconf
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
if [ $1 -eq 0 ]; then
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
* Wed Jan 30 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.
- New source URL

* Tue Aug 08 2000 Solar Designer <solar@owl.openwall.com>
- Added a patch by Miquel van Smoorenburg to fix the progress indicator
in e2fsck.

* Wed Aug 03 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file from RH.
- Added a patch for the permissions on lost+found.

# $Id: Owl/packages/e2fsprogs/e2fsprogs.spec,v 1.9 2002/08/26 15:26:29 mci Exp $

Summary: Utilities for managing the second extended (ext2) filesystem.
Name: e2fsprogs
Version: 1.27
Release: owl2
License: GPL
Group: System Environment/Base
Source: http://prdownloads.sourceforge.net/e2fsprogs/e2fsprogs-%{version}.tar.gz
Patch0: e2fsprogs-1.27-alt-fixes.diff
Patch1: e2fsprogs-1.27-alt-notitle.diff
Patch2: e2fsprogs-1.27-rh-c++.diff
Patch3: e2fsprogs-1.27-rh-owl-mountlabel3.diff
Patch4: e2fsprogs-1.27-owl-lost+found-mode.diff
Patch5: e2fsprogs-1.27-owl-warnings.diff
Patch6: e2fsprogs-1.27-owl-info.diff
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
rm doc/libext2fs.info
autoconf
%configure --enable-elf-shlibs
make

%install
rm -rf $RPM_BUILD_ROOT
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
/usr/sbin/mklost+found

/lib/libcom_err.so.*
/lib/libe2p.so.*
/lib/libext2fs.so.*
/lib/libss.so.*
/lib/libuuid.so.*

/usr/bin/chattr
/usr/bin/lsattr
/usr/bin/uuidgen
%{_mandir}/man1/chattr.1*
%{_mandir}/man1/lsattr.1*
%{_mandir}/man1/uuidgen.1*

%{_mandir}/man3/libuuid.3*
%{_mandir}/man3/uuid_clear.3*
%{_mandir}/man3/uuid_compare.3*
%{_mandir}/man3/uuid_copy.3*
%{_mandir}/man3/uuid_generate.3*
%{_mandir}/man3/uuid_is_null.3*
%{_mandir}/man3/uuid_parse.3*
%{_mandir}/man3/uuid_time.3*
%{_mandir}/man3/uuid_unparse.3*

%{_mandir}/man8/badblocks.8*
%{_mandir}/man8/debugfs.8*
%{_mandir}/man8/dumpe2fs.8*
%{_mandir}/man8/e2fsck.8*
%{_mandir}/man8/e2label.8*
%{_mandir}/man8/fsck.8*
%{_mandir}/man8/fsck.ext2.8*
%{_mandir}/man8/fsck.ext3.8*
%{_mandir}/man8/mke2fs.8*
%{_mandir}/man8/mkfs.ext2.8*
%{_mandir}/man8/mkfs.ext3.8*
%{_mandir}/man8/mklost+found.8*
%{_mandir}/man8/tune2fs.8*

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
%{_mandir}/man1/compile_et.1*
%{_mandir}/man3/com_err.3*

%changelog
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

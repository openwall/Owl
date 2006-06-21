# $Owl: Owl/packages/cpio/cpio.spec,v 1.24 2006/06/21 16:00:30 ldv Exp $

Summary: A GNU archiving program.
Name: cpio
Version: 2.6
Release: owl4
License: GPL
Group: Applications/Archiving
URL: http://www.gnu.org/software/cpio/
Source0: ftp://ftp.gnu.org/gnu/cpio-%version.tar.bz2
Source1: rmt.8
Patch0: cpio-2.6-cvs-20050131-umask.diff
Patch1: cpio-2.6-cvs-20041221-configure-mt.diff
Patch10: cpio-2.6-alt-lstat.diff
Patch11: cpio-2.6-alt-i18n.diff
Patch12: cpio-2.6-alt-sparse.diff
Patch13: cpio-2.6-alt-error-details.diff
Patch14: cpio-2.6-alt-warnings.diff
Patch15: cpio-2.6-alt-safer_name_suffix.diff
Patch16: cpio-2.6-alt-chown-chmod.diff
Patch17: cpio-2.6-alt-open-mkdir-mknod.diff
Patch18: cpio-2.6-rh-alt-lfs.diff
Patch19: cpio-2.6-rh-svr4compat.diff
Patch20: cpio-2.6-owl-info.diff
Patch21: cpio-2.6-pld-alt-configure.diff
Patch22: cpio-2.6-deb-find_inode_file.diff
Patch23: cpio-2.6-owl-mt-argmatch.diff
Patch24: cpio-2.6-deb-owl-mt-scsi.diff
Patch25: cpio-2.6-deb-owl-rmt.diff
Patch26: cpio-2.6-cvs-20051112-copyout.diff
Patch27: cpio-2.6-up-savedir.diff
Patch28: cpio-2.6-rh-header-init.diff
PreReq: /sbin/install-info
Provides: mt-st, rmt
Prefix: %_prefix
BuildRequires: texinfo, automake, autoconf, gettext
BuildRoot: /override/%name-%version

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

%prep
%setup -q
install -m644 %_sourcedir/rmt.8 .
%patch0 -p0
%patch1 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1

%build
# Several patches modify configure.ac
%__autoconf
%configure --enable-mt
%__make LDFLAGS=-s
%__make -k check

%install
rm -rf %buildroot
%makeinstall bindir=%buildroot/bin mandir=%buildroot%_mandir/

mkdir -p %buildroot%_mandir/man8/
install -m 644 rmt.8 %buildroot%_mandir/man8/

mkdir -p %buildroot/{etc,sbin}
# Can't have relative symlinks out of /etc as it's moved under /ram on CDs
ln -s %_libexecdir/rmt %buildroot/etc/
ln -s ..%_libexecdir/rmt %buildroot/sbin/

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/cpio.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/cpio.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README THANKS
/bin/cpio
/bin/mt
%_libexecdir/rmt
/sbin/rmt
/etc/rmt
%_infodir/cpio.*
%_mandir/man1/cpio.1*
%_mandir/man1/mt.1*
%_mandir/man8/rmt.8*
%_datadir/locale/*/LC_MESSAGES/cpio.mo

%changelog
* Wed Jun 21 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.6-owl4
- Imported FC patch to initialize header structure in copyin mode properly.
- Fixed build with gcc-4.x.

* Wed Nov 16 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.6-owl3
- Backported fixes for write_out_header() and read_for_checksum()
  from cpio CVS.
- Backported savedir() fix from gnulib CVS.

* Wed May 11 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.6-owl2
- Imported patch from ALT that fixes three race condition issues
while setting permissions in copy-in and copy-pass modes:
+ corrected open(2) calls to use O_EXCL;
+ corrected mkdir(2) and mknod(2) calls to use safe permissions;
+ corrected directory creation algorithm to chmod existing directory
using safe mode before chown, for each directory which is going to
be reused by cpio.

* Thu May 05 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.6-owl1
- Updated to 2.6.
- Imported a bunch of patches from ALT's cpio-2.6-alt9 package,
including fix for directory traversal issue (CAN-2005-1229) and
fixes for race condition issues (CAN-2005-1111).
- Reviewed Owl patches, removed obsolete ones.
- Updated patches which introduce additional functionality to mt(1)
and rmt(8) utilities.
- Corrected info files installation.
- Packaged cpio translations.
- Added URL.

* Sun Feb 06 2005 Solar Designer <solar-at-owl.openwall.com> 2.4.2-owl28
- With "cpio -oO ...", postpone the setting of umask to 0 (yes, that's
still far from perfect!) to until after the output file is created;
thanks to Mike O'Connor for bringing this up.

* Sun Oct 19 2003 Solar Designer <solar-at-owl.openwall.com> 2.4.2-owl27
- Install the mt(1) man page.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 2.4.2-owl26
- Deal with info dir entries such that the menu looks pretty.

* Sun Mar 24 2002 Solar Designer <solar-at-owl.openwall.com>
- Group: Applications/Archiving (be the same as tar).

* Thu Jan 24 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Dec 24 2000 Solar Designer <solar-at-owl.openwall.com>
- Conflicts -> Provides: mt-st, rmt

* Sat Dec 02 2000 Solar Designer <solar-at-owl.openwall.com>
- Added /etc/rmt and /sbin/rmt symlinks.
- Conflicts: rmt

* Wed Nov 29 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- imported lchown patch from RH7

* Sun Nov 26 2000 Michail Litvak <mci-at-owl.openwall.com>
- Imported from RH
- added some patches from Debian
  (many bug fixes in cpio, mt and rmt improvements)
- man page for rmt

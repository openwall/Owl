# $Id: Owl/packages/patch/patch.spec,v 1.9 2005/11/13 03:46:25 ldv Exp $

Summary: The GNU patch command, for modifying/upgrading files.
Name: patch
Version: 2.5.9
Release: owl1
License: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/patch/
Source: ftp://alpha.gnu.org/gnu/diffutils/patch-%version.tar.gz
Patch0: patch-2.5.9-cvs-20030702-p_strip_trailing_cr.diff
Patch1: patch-2.5.9-suse-remember-backup-files.diff
Patch2: patch-2.5.9-rh-stderr.diff
Patch3: patch-2.5.9-mdk-sigsegv.diff
Patch4: patch-2.5.9-mdk-backup.diff
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
The patch program applies diff files to originals.  The diff command
is used to compare an original to a changed file.  Diff lists the
changes made to the file.  A person who has the original file can then
use the patch command with the diff file to add the changes to their
original file (patching the file).

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
autoreconf -fisv
ADDITIONAL_ARCH_FLAGS=
# (ldv) Could anybody on sparc*/alpha recheck the following statement, please?
# (fg) Large file support can be disabled from ./configure - it is necessary at
# least on sparcs
%ifarch sparc sparc64 alpha
ADDITIONAL_ARCH_FLAGS=--disable-largefile
%endif
%configure $ADDITIONAL_ARCH_FLAGS

%__make "CFLAGS=%optflags -D_GNU_SOURCE -W -Wall" LDFLAGS=-s
bzip2 -9fk ChangeLog

%install
rm -rf %buildroot
%makeinstall

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog.bz2 NEWS README
%_bindir/*
%_mandir/*/*

%changelog
* Sat Nov 12 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.5.9-owl1
- Updated to 2.5.9.
- Applied upstream fix for CR handling bug.
- Applied SuSE patch to prevent previously created backup files from
being overwritten.

* Thu Feb 07 2002 Michail Litvak <mci-at-owl.openwall.com> 2.5.4-owl6
- Enforce our new spec file conventions.

* Wed Dec 20 2000 Michail Litvak <mci-at-owl.openwall.com>
- added patch to fix default backup extension

* Tue Nov 17 2000 Michail Litvak <mci-at-owl.openwall.com>
- import from RH and Mandrake
- sigsegv patch from MDK, stderr from RH

# $Id: Owl/packages/fileutils/Attic/fileutils.spec,v 1.16 2004/11/02 02:54:47 solar Exp $

# The texinfo documentation for fileutils, sh-utils, and textutils is
# currently provided by fileutils.
%define BUILD_INFO 1

Summary: The GNU versions of common file management utilities.
Name: fileutils
Version: 4.1.11
Release: owl4
License: GPL
Group: Applications/File
Source0: ftp://alpha.gnu.org/gnu/fetish/fileutils-%version.tar.bz2
Source1: colorls.sh
Source2: colorls.csh
Source3: DIR_COLORS
Patch0: fileutils-4.1.11-rh-owl-install-C.diff
Patch1: fileutils-4.1.11-rh-owl-default-time-style.diff
Patch2: fileutils-4.1.11-rh-stoneage.diff
Patch3: fileutils-4.1.11-rh-owl-ls-dumbterm.diff
Patch4: fileutils-4.1.11-owl-alt-rh-restore-color.diff
Patch5: fileutils-4.1.11-alt-cp-force.diff
Patch6: fileutils-4.1.11-alt-owl-chown.diff
Patch7: fileutils-4.1.11-owl-fixes.diff
Patch8: fileutils-4.1.11-owl-info.diff
Patch9: fileutils-4.1.11-owl-ls-max-columns.diff
%if %BUILD_INFO
PreReq: /sbin/install-info
%endif
Conflicts: sh-utils < 2.0-owl3, textutils < 2.0.11-owl3
Obsoletes: stat
BuildRoot: /override/%name-%version

%description
The fileutils package includes a number of GNU versions of common and
popular file management utilities.  fileutils includes the following
tools: chgrp (changes a file's group ownership), chown (changes a
file's ownership), chmod (changes a file's permissions), cp (copies
files), dd (copies and converts files), df (shows a filesystem's disk
usage), dir (gives a brief directory listing), dircolors (the setup
program for the color version of the ls command), du (shows disk
usage), install (copies files and sets permissions), ln (creates file
links), ls (lists directory contents), mkdir (creates directories),
mkfifo (creates FIFOs or named pipes), mknod (creates special files),
mv (renames files), rm (removes/deletes files), rmdir (removes empty
directories), sync (synchronizes memory and disk), touch (changes file
timestamps), and vdir (provides long directory listings).

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
%patch9 -p1

%{expand:%%define optflags %optflags -Wall -Dlint}

%build
rm doc/coreutils.info
unset LINGUAS || :
%define _exec_prefix /
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

cd $RPM_BUILD_ROOT

mkdir -p .%_prefix/bin
for i in dir dircolors du install mkfifo shred vdir; do
	mv -f bin/$i .%_prefix/bin/
done

mkdir -p etc/profile.d
install -c -m 644 $RPM_SOURCE_DIR/DIR_COLORS etc/
install -c -m 755 $RPM_SOURCE_DIR/colorls.{c,}sh etc/profile.d/

# Remove unpackaged files
rm %buildroot%_infodir/dir

%if %BUILD_INFO
%pre
/sbin/install-info --quiet --delete \
	%_infodir/fileutils.info.gz %_infodir/dir
/sbin/install-info --quiet --delete \
	%_infodir/sh-utils.info.gz %_infodir/dir
/sbin/install-info --quiet --delete \
	%_infodir/textutils.info.gz %_infodir/dir

%post
/sbin/install-info %_infodir/coreutils.info.gz %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/coreutils.info.gz %_infodir/dir
fi
%else
%pre
/sbin/install-info --quiet --delete \
	%_infodir/fileutils.info.gz %_infodir/dir
/sbin/install-info --quiet --delete \
	%_infodir/coreutils.info.gz %_infodir/dir
%endif

%files
%defattr(-,root,root)
%doc COPYING NEWS README THANKS TODO
%config %_sysconfdir/*
%_exec_prefix/bin/*
%_prefix/bin/*
%_mandir/man*/*
%if %BUILD_INFO
%_infodir/coreutils.info*
%endif
%_datadir/locale/*/*/*

%changelog
* Thu Oct 16 2003 Solar Designer <solar@owl.openwall.com> 4.1.11-owl4
- Place a limit on the number of columns in ls; previously, ls -w (and
other equivalent invocations) could result in excessive memory
consumption and even an integer overflow resulting in incorrect memory
allocation (thanks to Georgi Guninski).

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com> 4.1.11-owl3
- Deal with info dir entries such that the menu looks pretty.

* Mon Aug 12 2002 Solar Designer <solar@owl.openwall.com>
- Handle SIGTSTP in the ls restore colors patch (from ALT Linux).
- Two additional -Wall fixes for SPARC and Alpha (the issues were real).
- Also remove the obsolete textutils info dir entry.
- Obsoletes: stat

* Sun Aug 04 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 4.1.11.
- Reviewed all patches in current Red Hat and ALT Linux packages, imported
some with modifications.
- Improved the colorls* scripts.

* Sun Jul 07 2002 Solar Designer <solar@owl.openwall.com>
- Use grep -q in colorls.sh.

* Fri Feb 01 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.
- Changed SOURCE* to explicit $RPM_SOURCE_DIR/*

* Thu Nov 30 2000 Solar Designer <solar@owl.openwall.com>
- Avoid listing %_sysconfdir/profile.d (the directory itself).

* Wed Nov 29 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- add warning to shred(1) man.

* Thu Oct 19 2000 Solar Designer <solar@owl.openwall.com>
- Fixed a bug in RH patch to mv (don't exit if lstat on a file fails).

* Sun Oct 01 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- v4.0.27

* Sun Sep 24 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH

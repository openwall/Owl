# $Id: Owl/packages/gzip/gzip.spec,v 1.17 2005/05/21 00:18:49 ldv Exp $

Summary: The GNU data compression program.
Name: gzip
Version: 1.3.5
Release: owl1
License: GPL
Group: Applications/File
URL: http://www.gnu.org/software/%name/
Source: ftp://alpha.gnu.org/gnu/gzip/gzip-%version.tar.gz
Patch0: gzip-1.3.5-owl-info.diff
Patch1: gzip-1.3.5-alt-basename.diff
Patch2: gzip-1.3.5-openbsd-owl-alt-tmp.diff
Patch3: gzip-1.3.5-rh-alt-stderr.diff
Patch4: gzip-1.3.5-rh-owl-alt-zgrep.diff
Patch5: gzip-1.3.5-deb-alt-signal.diff
Patch6: gzip-1.3.5-deb-alt-original-filename.diff
Patch7: gzip-1.3.5-alt-copy_stat.diff
Patch8: gzip-1.3.5-alt-bzip2.diff
BuildRoot: /override/%name-%version

%description
The gzip package contains the popular GNU gzip data compression
program and its associated scripts to manage compressed files.

%package utils
Summary: Utilities for handy use of the GNU gzip.
Group: Applications/File
Requires: %name = %version-%release, bzip2, mktemp >= 1:1.3.1
# due to bz*grep, bzcmp, bzdiff, bzmore and bzless
Conflicts: bzip2 < 0:1.0.3-owl4

%description utils
This package contains additional utilities for the popular
GNU gzip and bzip2 data compression programs.

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

%build
%configure --bindir=/bin
make
bzip2 -9fk ChangeLog

%install
rm -rf %buildroot
%makeinstall bindir=%buildroot/bin
mkdir -p %buildroot%_bindir

for i in zcmp zegrep zforce zless znew gzexe zdiff zfgrep zgrep zmore; do
	mv %buildroot/bin/$i %buildroot%_bindir/
done

# replace hardlinks with symlinks
ln -sf gzip %buildroot/bin/gunzip
ln -sf gzip %buildroot/bin/zcat
ln -sf zdiff %buildroot%_bindir/zcmp
ln -sf zgrep %buildroot%_bindir/zegrep
ln -sf zgrep %buildroot%_bindir/zfgrep

# compatibility symlinks
for i in gzip gunzip; do
	ln -s ../../bin/gzip %buildroot%_bindir/$i
done

# additional utilities
ln -s zdiff %buildroot%_bindir/bzcmp
ln -s zdiff %buildroot%_bindir/bzdiff
ln -s zgrep %buildroot%_bindir/bzgrep
ln -s zgrep %buildroot%_bindir/bzegrep
ln -s zgrep %buildroot%_bindir/bzfgrep
ln -s zmore %buildroot%_bindir/bzmore

# additional manpages
echo '.so man1/zgrep.1' >%buildroot%_mandir/man1/zegrep.1
echo '.so man1/zgrep.1' >%buildroot%_mandir/man1/zfgrep.1
echo '.so man1/zgrep.1' >%buildroot%_mandir/man1/bzgrep.1
echo '.so man1/zgrep.1' >%buildroot%_mandir/man1/bzegrep.1
echo '.so man1/zgrep.1' >%buildroot%_mandir/man1/bzfgrep.1
echo '.so man1/zdiff.1' >%buildroot%_mandir/man1/bzcmp.1
echo '.so man1/zdiff.1' >%buildroot%_mandir/man1/bzdiff.1
echo '.so man1/zmore.1' >%buildroot%_mandir/man1/bzmore.1
echo '.so man1/zless.1' >%buildroot%_mandir/man1/bzless.1

cat > %buildroot%_bindir/zless <<EOF
#!/bin/sh
/bin/zcat "\$@" | %_bindir/less
EOF
cat > %buildroot%_bindir/bzless <<EOF
#!/bin/sh
/bin/bzcat "\$@" | %_bindir/less
EOF
chmod 755 %buildroot%_bindir/{,b}zless

# Remove unpackaged files if any
rm -f %buildroot%_infodir/dir

%triggerin -- info
/sbin/install-info %_infodir/gzip.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gzip.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog.bz2 NEWS README THANKS TODO
/bin/*
%_bindir/g*zip
%_mandir/*/g*zip.*
%_mandir/*/zcat.*
%_infodir/gzip.info*

%files utils
%defattr(-,root,root)
%_bindir/*
%_mandir/man1/*
%exclude %_bindir/g*zip
%exclude %_mandir/*/g*zip.*
%exclude %_mandir/*/zcat.*

%changelog
* Fri May 20 2005 Dmitry V. Levin <ldv@owl.openwall.com> 1.3.5-owl1
- Updated to 1.3.5.
- Reviewed Owl patches, removed obsolete ones.
- Imported a bunch of patches from ALT's gzip-1.3.5-alt1 package,
including fix for directory traversal issue in "gunzip -N"
(CAN-2005-1228), fix for race condition in file permission handling code
of gzip and gunzip (CAN-2005-0988), and fix of zgrep utility to properly
sanitize arguments (CAN-2005-0758).
- Changed zgrep, zdiff and zmore utilities to handle also functionality
of bz*grep, bzdiff and bzmore utilities, packaged bz*grep, bzcmp, bzdiff,
bzmore and bzless within separate subpackage, gzip-utils.
- Added zegrep(1) and zfgrep(1) manpage links.
- Corrected info files installation.
- Updated URL.

* Tue Aug 27 2002 Solar Designer <solar@owl.openwall.com> 1.3-owl17
- Use a trigger instead of a dependency on /sbin/install-info to avoid a
dependency loop with the new texinfo.

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Sun Jul 07 2002 Solar Designer <solar@owl.openwall.com>
- Use grep -q in zforce, zgrep.
- Use mktemp -t rather than substitute $TMPDIR manually in gzexe, zdiff.

* Sun Feb 03 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Sat Sep 29 2001 Solar Designer <solar@owl.openwall.com>
- Synced with Todd's latest fixes: re-create the temporary file in gzexe
safely when run on multiple files, support GZIP="--suffix .suf" in znew.

* Fri Sep 28 2001 Solar Designer <solar@owl.openwall.com>
- Patched unsafe temporary file handling in gzexe, zdiff, and znew based
on work by Todd Miller of OpenBSD.
- Dropped Red Hat's patch which attempted to fix some of the same issues
for gzexe but was far from sufficient.

* Sat Jun 16 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- sync mktemp patch from RH
- errors go to stderror
- add handler for SIGPIPE in zgrep

* Sun Aug  6 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

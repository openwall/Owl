# $Owl: Owl/packages/gzip/gzip.spec,v 1.30 2010/03/22 18:44:38 solar Exp $

Summary: The GNU data compression program.
Name: gzip
Version: 1.4
Release: owl2
License: GPLv3+
Group: Applications/File
URL: http://www.gnu.org/software/%name/
Source: ftp://ftp.gnu.org/gnu/gzip/gzip-%version.tar.gz
# Signature: ftp://ftp.gnu.org/gnu/gzip/gzip-%version.tar.gz.sig
Patch0: gzip-1.4-up-znew-K.diff
Patch1: gzip-1.4-up-gzexe-signal.diff
Patch2: gzip-1.4-up-stderr.diff
Patch3: gzip-1.4-up-zgrep-signal.diff
Patch4: gzip-1.4-owl-info.diff
Patch5: gzip-1.4-openbsd-owl-alt-tmp.diff
Patch6: gzip-1.4-alt-bzip2-xz.diff
Patch7: gzip-1.4-owl-tests.diff
BuildRequires: rpm-build >= 0:4
BuildRoot: /override/%name-%version

%description
The gzip package contains the popular GNU gzip data compression
program and its associated scripts to manage compressed files.

%package utils
Summary: Utilities for handy use of the GNU gzip.
Group: Applications/File
Requires: %name = %version-%release, bzip2 >= 0:1.0.3-owl4, mktemp >= 1:1.3.1

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

%{expand:%%define optflags %optflags -Wall -DGNU_STANDARD=0}

%build
# Unset the variable gl_printf_safe to indicate that we do not need
# a safe handling of non-IEEE-754 'long double' values.
# This is required to enforce build with system vfprintf().
sed -i 's/gl_printf_safe=yes/gl_printf_safe=/' configure

%configure --bindir=/bin --disable-silent-rules
%__make
ln -sf zdiff zcmp
cp gzip.1 gzip.doc

%check
%__make check

%install
rm -rf %buildroot
%makeinstall bindir=%buildroot/bin
mkdir -p %buildroot%_bindir

# uncompress is a part of ncompress package
rm %buildroot/bin/uncompress

for i in zcmp zegrep zforce zless znew gzexe zdiff zfgrep zgrep zmore; do
	mv %buildroot/bin/$i %buildroot%_bindir/
done

# replace wrappers with symlinks
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
%_bindir/bzcat "\$@" | %_bindir/less
EOF
chmod 755 %buildroot%_bindir/{,b}zless

# Remove unpackaged files
rm %buildroot%_infodir/dir

%triggerin -- info
/sbin/install-info %_infodir/gzip.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gzip.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README THANKS TODO
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
* Mon Mar 22 2010 Solar Designer <solar-at-owl.openwall.com> 1.4-owl2
- Skip the "zgrep -f" test when /proc/$$/fd is not available (patch by
Dmitry V. Levin).

* Tue Feb 02 2010 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4-owl1
- Updated to 1.4.
- Reviewed patches, removed obsolete ones.
- Enabled test suite.

* Tue Jan 19 2010 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.3.5-owl5
- Applied upstream fix for an integer underflow bug (CVE-2010-0001).

* Tue Sep 19 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.3.5-owl4
- Fixed several bugs (CVE-2006-433[5678]) based on patch from Tavis Ormandy.
- Changed zgrep to exit when pipeline is interrupted by signal.

* Wed Jan 04 2006 Michail Litvak <mci-at-owl.openwall.com> 1.3.5-owl3
- Fixed path to bzcat.

* Mon Jul 18 2005 Solar Designer <solar-at-owl.openwall.com> 1.3.5-owl2
- Fixed a segfault on invalid compressed data (patch from Gentoo).

* Fri May 20 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.3.5-owl1
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

* Tue Aug 27 2002 Solar Designer <solar-at-owl.openwall.com> 1.3-owl17
- Use a trigger instead of a dependency on /sbin/install-info to avoid a
dependency loop with the new texinfo.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Sun Jul 07 2002 Solar Designer <solar-at-owl.openwall.com>
- Use grep -q in zforce, zgrep.
- Use mktemp -t rather than substitute $TMPDIR manually in gzexe, zdiff.

* Sun Feb 03 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Sat Sep 29 2001 Solar Designer <solar-at-owl.openwall.com>
- Synced with Todd's latest fixes: re-create the temporary file in gzexe
safely when run on multiple files, support GZIP="--suffix .suf" in znew.

* Fri Sep 28 2001 Solar Designer <solar-at-owl.openwall.com>
- Patched unsafe temporary file handling in gzexe, zdiff, and znew based
on work by Todd Miller of OpenBSD.
- Dropped Red Hat's patch which attempted to fix some of the same issues
for gzexe but was far from sufficient.

* Sat Jun 16 2001 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- sync mktemp patch from RH
- errors go to stderror
- add handler for SIGPIPE in zgrep

* Sun Aug  6 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH

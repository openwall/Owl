# $Owl: Owl/packages/patchutils/patchutils.spec,v 1.10 2009/05/25 13:19:24 solar Exp $

Summary: Patchutils is a small collection of programs that operate on patch files.
Name: patchutils
Version: 0.3.1
Release: owl1
License: GPL
Group: Applications/Text
URL: http://cyberelk.net/tim/patchutils/
Source: http://cyberelk.net/tim/data/patchutils/stable/patchutils-%version.tar.bz2
# Signature: http://cyberelk.net/tim/data/patchutils/stable/patchutils-%version.tar.bz2.sig
Patch0: patchutils-0.2.30-owl-tmp.diff
PreReq: /sbin/install-info
Requires: mktemp >= 1:1.3.1
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
Patchutils is a small collection of programs that operate on patch files.
This version contains:
+ combinediff: creates a cumulative patch from two incremental patches;
+ dehtmldiff: gets usable diff from an HTML page;
+ editdiff: simple wrapper around rediff;
+ espdiff: applies the appropriate transformation to a set of patches;
+ filterdiff: extracts or excludes diffs from a diff file;
+ fixcvsdiff: fixes problematic cvs diff files;
+ flipdiff: exchanges the order of two incremental patches;
+ grepdiff: shows files modified by a diff containing a regex;
+ interdiff: shows differences between two unified diff files;
+ lsdiff: shows which files are modified by a patch;
+ recountdiff: recomputes patch counts and offsets;
+ rediff: fixes offsets and counts of a hand-edited diff;
+ splitdiff: separates out incremental patches;
+ unwrapdiff: demangles word-wrapped patches.

%prep
%setup -q
%patch0 -p1
bzip2 -9k ChangeLog

%build
%configure
%__make

%install
rm -rf %buildroot
%makeinstall

%files
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING ChangeLog.bz2 NEWS README
%_bindir/*
%_mandir/*/*

%changelog
* Sun May 24 2009 Michail Litvak <mci-at-owl.openwall.com> 0.3.1-owl1
- Updated to 0.3.1.

* Tue Jun 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.2.31-owl1
- Updated to 0.2.31.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.2.30-owl5
- Compressed ChangeLog file.

* Tue Apr 26 2005 Solar Designer <solar-at-owl.openwall.com> 0.2.30-owl4
- Dropped the currently unneeded invocations of autoconf, aclocal, automake
to make the package build with the new automake installed on the system.
- Added an explicit invocation of make in %build, do not rely on make install
to also build the programs.

* Sun Nov 28 2004 Juan M. Bello Rivas <jmbr-at-owl.openwall.com> 0.2.30-owl3
- Corrected two instances of calls to memory allocation functions where there
was no check for their return values.

* Sat Nov 27 2004 Juan M. Bello Rivas <jmbr-at-owl.openwall.com> 0.2.30-owl2
- Implemented temporary file handling and bounds checking fixes.

* Mon Nov 22 2004 Juan M. Bello Rivas <jmbr-at-owl.openwall.com> 0.2.30-owl1
- Adapted from ALT Linux.

# $Id: Owl/packages/patchutils/patchutils.spec,v 1.2 2004/11/27 17:32:49 solar Exp $

Summary: Patchutils is a small collection of programs that operate on patch files.
Name: patchutils
Version: 0.2.30
Release: owl2
License: GPL
Group: Applications/Text
URL: http://cyberelk.net/tim/%name/
Source: http://cyberelk.net/tim/data/%name/stable/%name-%version.tar.bz2
Patch0: patchutils-0.2.30-owl-tmp.diff
Patch1: patchutils-0.2.30-owl-bound.diff
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
%patch1 -p1

%build
autoconf
aclocal
automake -ia
%configure

%install
rm -rf %buildroot
%makeinstall

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README COPYING BUGS NEWS
%_bindir/*
%_mandir/*/*

%changelog
* Mon Nov 27 2004 Juan M. Bello Rivas <jmbr@owl.openwall.com> 0.2.30-owl2
- Implemented temporary file handling and bounds checking fixes.

* Mon Nov 22 2004 Juan M. Bello Rivas <jmbr@owl.openwall.com> 0.2.30-owl1
- Adapted from ALT Linux.

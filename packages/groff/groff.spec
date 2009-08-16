# $Owl: Owl/packages/groff/groff.spec,v 1.26 2009/08/16 02:30:42 solar Exp $

%define BUILD_USE_X 0
%define BUILD_CURRENT 0

Summary: A document formatting system.
Name: groff
Version: 1.20.1
Release: owl3
License: mostly GPLv3+ and FDL
Group: System Environment/Base
URL: http://groff.ffii.org
Source0: ftp://ftp.gnu.org/gnu/groff/groff-%version.tar.gz
# Signature: ftp://ftp.gnu.org/gnu/groff/groff-%version.tar.gz.sig
%if %BUILD_CURRENT
Source1: ftp://ftp.ffii.org/pub/groff/devel/groff-%version-current.diff.gz
%endif
Source2: README.A4
Patch0: groff-1.20.1-rh-nohtml.diff
Patch1: groff-1.20.1-owl-tmp.diff
Patch2: groff-1.20.1-alt-docdir.diff
Patch3: groff-1.20.1-alt-old_drawing_scheme.diff
Patch4: groff-1.20.1-owl-pdfroff-gs-dSAFER.diff
Patch5: groff-1.20.1-owl-groffer-Makefile.diff
Obsoletes: groff-tools
Requires: mktemp >= 1:1.3.1
BuildRequires: mktemp >= 1:1.3.1, zlib-devel, gcc-c++
BuildRoot: /override/%name-%version

%description
groff is a document formatting system.  groff takes standard text and
formatting commands as input and produces formatted output.  The
created documents can be shown on a display or printed on a printer.
groff's formatting commands allow you to specify font type and size,
bold type, italic type, the number and size of columns on a page, and
more.  groff is also used to format man pages.

%if %BUILD_USE_X
If you are going to use groff with the X Window System, you'll also
need to install the groff-gxditview package.
%endif

%package perl
Summary: Parts of the groff formatting system that require Perl.
Group: Applications/Publishing
Requires: %name = %version-%release

%description perl
The groff-perl package contains the parts of the groff text processor
package that require Perl.  These include the afmtodit font processor
for creating PostScript font files, the grog utility that can be used
to automatically determine groff command-line options, the mmroff
reference preprocessor, and some others.

%if %BUILD_USE_X
%package gxditview
Summary: An X previewer for groff text processor output.
Group: Applications/Publishing
Requires: %name = %version-%release

%description gxditview
gxditview displays the groff text processor's output on an X Window
System display.

If you are going to use groff as a text processor, you should install
gxditview so that you preview your processed text files in X.  You'll
also need to install the groff package and the X Window System.
%endif

%package doc
Summary: Reference manuals and examples for groff.
Group: Documentation
Requires: %name = %version-%release

%description doc
This package contains reference manuals and examples for languages and
macros implemented in the groff package.

%prep
%setup -q
%if %BUILD_CURRENT
zcat %SOURCE1 | patch -p1 -l
%endif
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
install -pm 644 %_sourcedir/README.A4 .

# Remove/disable unused files with temporary file handling issues in them to
# make sure that these are in fact unused.
rm -r contrib/groffer/shell
echo -e '#!/bin/sh\nexit 1' > install-sh

%build
%if %BUILD_USE_X
PATH=$PATH:%_prefix/X11R6/bin
%endif

export ac_cv_func_mkstemp=yes \
%configure
make

%if %BUILD_USE_X
cd src/xditview
xmkmf && make
%endif

%install
rm -rf %buildroot

%if %BUILD_USE_X
PATH=$PATH:%_prefix/X11R6/bin
%endif

mkdir -p %buildroot%_prefix

%makeinstall

%if %BUILD_USE_X
cd src/xditview
%makeinstall DESTDIR=%buildroot
cd ../..
%endif

pushd %buildroot%_bindir
ln -s troff gtroff
ln -s tbl gtbl
ln -s pic gpic
ln -s eqn geqn
ln -s neqn gneqn
ln -s refer grefer
ln -s lookbib glookbib
ln -s indxbib gindxbib
ln -s soelim gsoelim
ln -s nroff gnroff
popd

pushd %buildroot%_mandir/man1
ln -s eqn.1 geqn.1
ln -s indxbib.1 gindxbib.1
ln -s lookbib.1 glookbib.1
ln -s nroff.1 gnroff.1
ln -s pic.1 gpic.1
ln -s refer.1 grefer.1
ln -s soelim.1 gsoelim.1
ln -s tbl.1 gtbl.1
ln -s troff.1 gtroff.1
popd

# Prepare documentation.  groff's install creates this directory on its own.
%define docdir %_docdir/%name-%version
install -pm 644 \
	COPYING FDL LICENSES \
	BUG-REPORT MORE.STUFF NEWS PROBLEMS PROJECTS README README.A4 TODO \
	%buildroot%docdir/
find %buildroot%docdir \( -name '*.html' -o -name '*.ps' -o -name '*.eps' \) \
	-type f -print0 | xargs -r0 gzip -9n --
find %buildroot%docdir \( -name '*.m[es]' -o -name '*.xpm' \) \
	-type f -print0 | xargs -r0 bzip2 -9 --
bzip2 -9 %buildroot%docdir/NEWS

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/groff.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/groff.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc %dir %docdir
%doc %docdir/[A-Z]*
%_bindir/*
%_libdir/groff
%_datadir/groff
%_mandir/man?/*
%_infodir/groff.info*
%if %BUILD_USE_X
%exclude %_bindir/gxditview
%endif
# These are part of -perl
%exclude %_bindir/afmtodit
%exclude %_bindir/groffer
%exclude %_bindir/grog
%exclude %_bindir/mmroff
%exclude %_bindir/roff2*
%exclude %_mandir/man1/afmtodit.*
%exclude %_mandir/man1/groffer.*
%exclude %_mandir/man1/grog.*
%exclude %_mandir/man1/mmroff.*
%exclude %_mandir/man1/roff2*
%exclude %_libdir/groff/groffer

%files perl
%defattr(-,root,root)
%_bindir/afmtodit
%_bindir/groffer
%_bindir/grog
%_bindir/mmroff
%_bindir/roff2*
%_mandir/man1/afmtodit.*
%_mandir/man1/groffer.*
%_mandir/man1/grog.*
%_mandir/man1/mmroff.*
%_mandir/man1/roff2*
%_libdir/groff/groffer

%if %BUILD_USE_X
%files gxditview
%defattr(-,root,root)
%_bindir/gxditview
%_datadir/X11/app-defaults/GXditview
%endif

%files doc
%defattr(-,root,root)
%doc %docdir/[a-z]*

%changelog
* Sun Aug 16 2009 Solar Designer <solar-at-owl.openwall.com> 1.20.1-owl3
- Require mktemp in the main package (for the packaged shell scripts).
- Require the main package in all subpackages.
- Install groffer's "library" scripts, which were mistakenly excluded with the
update to 1.20.1.
- Moved all extra Perl scripts introduced with our update to 1.20.1 to the
-perl subpackage where they belong.
- Re-worked the way the documentation is packaged by making use of portions of
documentation installed by groff's normal install procedure, introduced a -doc
subpackage for newly packaged language & macro reference manuals and examples.

* Fri Aug 14 2009 Solar Designer <solar-at-owl.openwall.com> 1.20.1-owl2
- Patched many additional temporary file handling issues, including in pdfroff
(reported by brian m. carlson via Debian), in scripts used during build,
and in the documentation.
- Patched pdfroff to invoke gs with the -dSAFER option (also reported by
brian m. carlson via Debian).  pdfroff is new with our update to 1.20.1.
- Revised the set of documentation files to package.

* Tue Aug 04 2009 Michail Litvak <mci-at-owl.openwall.com> 1.20.1-owl1
- Updated to 1.20.1.
- Added two patches from ALT: to correct the /usr/share/doc subdirectory name,
and to restore the old default not to emit SGR escape sequences.
- Added patch from Red Hat to not build html documentation.
- Dropped the now obsolete patches.

* Sun Feb 03 2002 Michail Litvak <mci-at-owl.openwall.com> 1.17.2-owl2
- Enforce our new spec file conventions

* Fri Dec 21 2001 Solar Designer <solar-at-owl.openwall.com>
- Patched two buffer overflow bugs in grn(1) discovered by zen-parse.
- Made the configure script fail-close on the temporary directory creation,
corrected the dependency on mktemp(1).

* Sun Sep 02 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 1.17.2.
- Added Sebastian Krahmer's patch for the pic(1) plot command's "format
feature" which zen-parse has demonstrated to be a security problem when
groff is used with LPRng on Red Hat Linux.
- Dropped troff-to-ps.fpi which offered groff for use by print servers and
on untrusted input.
- Dropped the now obsolete patches.

* Sun May 06 2001 Solar Designer <solar-at-owl.openwall.com>
- README.A4 updates (mention grops -g and a4.tmac).

* Sat May 05 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 1.17.
- Reviewed post-1.17 changes, included one tiny and obviously correct
fix as a patch.
- Patched the soft hyphen character out of the latin1 device such that
latin1 may be used with non-Latin-1 8-bit character sets.  We might
add an ascii8 device in the future.  Why this is needed is explained
at http://www.ffii.org/archive/mails/groff/2000/Nov/0050.html
- Added a patch for pre-grohtml's insecure temporary file handling as
it's now actually used with -Thtml.

* Sat Jan 06 2001 Solar Designer <solar-at-owl.openwall.com>
- Enable mkstemp explicitly, not rely on configure.

* Thu Nov 23 2000 Solar Designer <solar-at-owl.openwall.com>
- Updated to today's -current.
- Dropped the now obsolete patches from Nov 21.

* Tue Nov 21 2000 Solar Designer <solar-at-owl.openwall.com>
- Updated to -current which now includes fixes for the current directory
problem described in the ISS X-Force advisory.
- Restrict .mso and hpf in a similar way (patch for -current).
- Use safer_macro_path for .eqnrc (patch for -current).
- Dropped the RH safer patch for .so (source) as it is non-obvious whether
this needed fixing, and the patch wasn't a complete fix anyway (it trusted
files under the cwd and had races).

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH
- update to 1.16.1

# $Id: Owl/packages/groff/groff.spec,v 1.15 2003/10/29 19:22:05 solar Exp $

%define BUILD_USE_X 0
%define BUILD_CURRENT 0

Summary: A document formatting system.
Name: groff
Version: 1.17.2
Release: owl2
License: GPL
Group: System Environment/Base
Source0: ftp://ftp.gnu.org/gnu/groff/groff-%version.tar.gz
%if %BUILD_CURRENT
Source1: ftp://ftp.ffii.org/pub/groff/devel/groff-%version-current.diff.gz
%endif
Source2: README.A4
Patch0: groff-1.17-owl-latin1-shc-hack.diff
Patch1: groff-1.17.2-suse-pic-format.diff
Patch2: groff-1.17.2-owl-grn-bound.diff
Patch3: groff-1.17.2-owl-tmp.diff
Obsoletes: groff-tools
BuildRequires: mktemp >= 1:1.3.1
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

%description perl
The groff-perl package contains the parts of the groff text processor
package that require Perl.  These include the afmtodit font processor
for creating PostScript font files, the grog utility that can be used
to automatically determine groff command-line options, and the mmroff
reference preprocessor.

%if %BUILD_USE_X
%package gxditview
Summary: An X previewer for groff text processor output.
Group: Applications/Publishing

%description gxditview
gxditview displays the groff text processor's output on an X Window
System display.

If you are going to use groff as a text processor, you should install
gxditview so that you preview your processed text files in X.  You'll
also need to install the groff package and the X Window System.
%endif

%prep
%setup -q
%if %BUILD_CURRENT
zcat %SOURCE1 | patch -p1 -l
%endif
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
install -m 644 $RPM_SOURCE_DIR/README.A4 .

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
rm -rf $RPM_BUILD_ROOT

%if %BUILD_USE_X
PATH=$PATH:%_prefix/X11R6/bin
%endif

mkdir -p $RPM_BUILD_ROOT%_prefix

%makeinstall

%if %BUILD_USE_X
cd src/xditview
%makeinstall DESTDIR=$RPM_BUILD_ROOT
cd ../..
%endif

pushd $RPM_BUILD_ROOT%_prefix/bin
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

pushd $RPM_BUILD_ROOT%_mandir/man1
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

find $RPM_BUILD_ROOT%_prefix/bin $RPM_BUILD_ROOT%_mandir \
	-type f -o -type l | \
	grep -Ev 'afmtodit|grog|mdoc\.samples|mmroff' | \
	sed -e "s|${RPM_BUILD_ROOT}||g" -e "s|\.[0-9]|\.*|g" > groff-files

%files -f groff-files
%defattr(-,root,root)
%doc BUG-REPORT NEWS PROBLEMS README README.A4 TODO VERSION
%_prefix/share/groff

%files perl
%defattr(-,root,root)
%_prefix/bin/grog
%_prefix/bin/mmroff
%_prefix/bin/afmtodit
%_mandir/man1/afmtodit.*
%_mandir/man1/grog.*
%_mandir/man7/mmroff*

%if %BUILD_USE_X
%files gxditview
%defattr(-,root,root)
%_prefix/X11R6/bin/gxditview
%config /etc/X11/app-defaults/GXditview
%endif

%changelog
* Sun Feb 03 2002 Michail Litvak <mci@owl.openwall.com> 1.17.2-owl2
- Enforce our new spec file conventions

* Fri Dec 21 2001 Solar Designer <solar@owl.openwall.com>
- Patched two buffer overflow bugs in grn(1) discovered by zen-parse.
- Made the configure script fail-close on the temporary directory creation,
corrected the dependency on mktemp(1).

* Sun Sep 02 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 1.17.2.
- Added Sebastian Krahmer's patch for the pic(1) plot command's "format
feature" which zen-parse has demonstrated to be a security problem when
groff is used with LPRng on Red Hat Linux.
- Dropped troff-to-ps.fpi which offered groff for use by print servers and
on untrusted input.
- Dropped the now obsolete patches.

* Sun May 06 2001 Solar Designer <solar@owl.openwall.com>
- README.A4 updates (mention grops -g and a4.tmac).

* Sat May 05 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 1.17.
- Reviewed post-1.17 changes, included one tiny and obviously correct
fix as a patch.
- Patched the soft hyphen character out of the latin1 device such that
latin1 may be used with non-Latin-1 8-bit character sets.  We might
add an ascii8 device in the future.  Why this is needed is explained
at http://www.ffii.org/archive/mails/groff/2000/Nov/0050.html
- Added a patch for pre-grohtml's insecure temporary file handling as
it's now actually used with -Thtml.

* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- Enable mkstemp explicitly, not rely on configure.

* Thu Nov 23 2000 Solar Designer <solar@owl.openwall.com>
- Updated to today's -current.
- Dropped the now obsolete patches from Nov 21.

* Tue Nov 21 2000 Solar Designer <solar@owl.openwall.com>
- Updated to -current which now includes fixes for the current directory
problem described in the ISS X-Force advisory.
- Restrict .mso and hpf in a similar way (patch for -current).
- Use safer_macro_path for .eqnrc (patch for -current).
- Dropped the RH safer patch for .so (source) as it is non-obvious whether
this needed fixing, and the patch wasn't a complete fix anyway (it trusted
files under the cwd and had races).

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- update to 1.16.1

# $Id: Owl/packages/groff/groff.spec,v 1.8 2001/05/05 20:03:42 solar Exp $

%define BUILD_USE_X	'no'
%define BUILD_CURRENT	'no'

Summary: A document formatting system.
Name: 		groff
Version: 	1.17
Release: 	1owl
Copyright: 	GPL
Group: 		System Environment/Base
Source0: 	ftp://ftp.gnu.org/gnu/groff/groff-%{version}.tar.gz
%if "%{BUILD_CURRENT}"=="'yes'"
Source1:	ftp://ftp.ffii.org/pub/groff/devel/groff-%{version}-current.diff.gz
%endif
Source2: 	troff-to-ps.fpi
Source3: 	README.A4
Patch0:		groff-1.17-cvs-20010421-indxbib-nasty-typo.diff
Patch1:		groff-1.16.1-owl-man.diff
Patch2:		groff-1.17-owl-latin1-shc-hack.diff
Patch3:		groff-1.17-owl-pre-grohtml-tmp.diff
Requires: 	mktemp
Buildroot:      /var/rpm-buildroot/%{name}-root
Obsoletes: 	groff-tools

%description
groff is a document formatting system.  groff takes standard text and
formatting commands as input and produces formatted output.  The
created documents can be shown on a display or printed on a printer.
groff's formatting commands allow you to specify font type and size,
bold type, italic type, the number and size of columns on a page, and
more.

You should install groff if you want to use it as a document
formatting system.  groff is also used to format man pages.

%if "%{BUILD_USE_X}"=="'yes'"
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
to automatically determine groff command-line options, and the
troff-to-ps print filter.

%if "%{BUILD_USE_X}"=="'yes'"
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
%if "%{BUILD_CURRENT}"=="'yes'"
zcat %{SOURCE1} | patch -p1 -l
%endif
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
cp %{SOURCE3} .

%build
%if "%{BUILD_USE_X}"=="'yes'"
PATH=$PATH:%{_prefix}/X11R6/bin
%endif

export ac_cv_func_mkstemp=yes \
%configure
make

%if "%{BUILD_USE_X}"=="'yes'"
cd src/xditview
xmkmf && make
%endif

%install
rm -rf ${RPM_BUILD_ROOT}

%if "%{BUILD_USE_X}"=="'yes'"
PATH=$PATH:%{_prefix}/X11R6/bin
%endif

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}

%makeinstall

%if "%{BUILD_USE_X}"=="'yes'"
cd src/xditview
%makeinstall DESTDIR=$RPM_BUILD_ROOT
cd ../..
%endif

pushd ${RPM_BUILD_ROOT}%{_prefix}/bin
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

pushd ${RPM_BUILD_ROOT}%{_mandir}/man1
# Build system is compressing man-pages
ln -s eqn.1.gz geqn.1.gz
ln -s indxbib.1.gz gindxbib.1.gz
ln -s lookbib.1.gz glookbib.1.gz
ln -s nroff.1.gz gnroff.1.gz
ln -s pic.1.gz gpic.1.gz
ln -s refer.1.gz grefer.1.gz
ln -s soelim.1.gz gsoelim.1.gz
ln -s tbl.1.gz gtbl.1.gz
ln -s troff.1.gz gtroff.1.gz
popd

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/rhs/rhs-printfilters
install -m 755 %{SOURCE2} ${RPM_BUILD_ROOT}%{_prefix}/share/rhs/rhs-printfilters

find ${RPM_BUILD_ROOT}%{_prefix}/bin ${RPM_BUILD_ROOT}%{_mandir} \
	-type f -o -type l | \
	grep -Ev 'afmtodit|grog|mdoc\.samples|mmroff' | \
	sed -e "s|${RPM_BUILD_ROOT}||g" -e "s|\.[0-9]|\.*|g" > groff-files

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f groff-files
%defattr(-,root,root)
%doc BUG-REPORT NEWS PROBLEMS README README.A4 TODO VERSION
%{_prefix}/share/groff

%files perl
%defattr(-,root,root)
%{_prefix}/bin/grog
%{_prefix}/bin/mmroff
%{_prefix}/bin/afmtodit
%{_mandir}/man1/afmtodit.*
%{_mandir}/man1/grog.*
%{_mandir}/man7/mmroff*
%{_prefix}/share/rhs/*/*

%if "%{BUILD_USE_X}"=="'yes'"
%files gxditview
%defattr(-,root,root)
%{_prefix}/X11R6/bin/gxditview
%config /etc/X11/app-defaults/GXditview
%endif

%changelog
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

* Mon Jul 17 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to fix miscompilation manifesting in alpha build of tcltk.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun  9 2000 Bill Nottingham <notting@redhat.com>
- move mmroff to -perl

* Wed Jun  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build
- FHS
- 1.16

* Sun May 14 2000 Jeff Johnson <jbj@redhat.com>
- install tmac.mse (FWIW tmac.se looks broken) to fix dangling symlink (#10757).
- add README.A4, how to set up for A4 paper (#8276).
- add other documents to package.

* Thu Mar  2 2000 Jeff Johnson <jbj@redhat.com>
- permit sourcing on regular files within cwd tree (unless -U specified).

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- fix incorrectly installed tmac.m file (#8362).

* Mon Feb  7 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- check if build system is sane again

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- fix description and summary
- man pages are compressed. This is ugly.

* Mon Jan 31 2000 Bill Nottingham <notting@redhat.com>
- put the binaries actually in the package *oops*

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- split perl components into separate subpackage

* Wed Dec 29 1999 Bill Nottingham <notting@redhat.com>
- update to 1.15

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 9)

* Tue Feb 16 1999 Cristian Gafton <gafton@redhat.com>
- glibc 2.1 patch for xditview (#992)

* Thu Oct 22 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide

* Thu Sep 10 1998 Cristian Gafton <gafton@redhat.com>
- fix makefiles to work with bash2

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- use g++ for C++ code

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- manhattan and buildroot

* Mon Nov  3 1997 Michael Fulbright <msf@redhat.com>
- made xdefaults file a config file

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- split perl components into separate subpackage

* Tue Oct 21 1997 Michael Fulbright <msf@redhat.com>
- updated to 1.11a
- added safe troff-to-ps.fpi

* Tue Oct 14 1997 Michael Fulbright <msf@redhat.com>
- removed troff-to-ps.fpi for security reasons.

* Fri Jun 13 1997 Erik Troan <ewt@redhat.com>
- built against glibc

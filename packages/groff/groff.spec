# $Id: Owl/packages/groff/groff.spec,v 1.1 2000/08/09 00:51:27 kad Exp $

%define BUILD_USE_X      'no'

Summary: A document formatting system.
Name: 		groff
Version: 	1.16.1
Release: 	1owl
Copyright: 	GPL
Group: 		Applications/Publishing
Source0: 	ftp://ftp.gnu.org/gnu/groff/groff-%{version}.tar.gz
Source1: 	troff-to-ps.fpi
Source2: 	README.A4
Patch0:		groff-1.16.1-owl-man.diff
Patch1: 	groff-1.16-rh-safer.diff
Requires: 	mktemp
Buildroot:      /var/rpm-buildroot/%{name}-root
Obsoletes: 	groff-tools

%description
Groff is a document formatting system.  Groff takes standard text and
formatting commands as input and produces formatted output.  The
created documents can be shown on a display or printed on a printer.
Groff's formatting commands allow you to specify font type and size,
bold type, italic type, the number and size of columns on a page, and
more.

You should install groff if you want to use it as a document
formatting system.  Groff can also be used to format man pages. If you
are going to use groff with the X Window System, you'll also need to
install the groff-gxditview package.

%package perl
Summary: Parts of the groff formatting system that require Perl.
Group: Applications/Publishing

%description perl
The groff-perl package contains the parts of the groff text processor
package that require Perl. These include the afmtodit font processor
for creating PostScript font files, the grog utility that can be used
to automatically determine groff command-line options, and the
troff-to-ps print filter.

%if "%{BUILD_USE_X}"=="'yes'"
%package gxditview
Summary: An X previewer for groff text processor output.
Group: Applications/Publishing

%description gxditview
Gxditview displays the groff text processor's output on an X Window
System display.

If you are going to use groff as a text processor, you should install
gxditview so that you preview your processed text files in X.  You'll
also need to install the groff package and the X Window System.
%endif

%prep
%setup -q
%patch0 -p0
%patch1 -p1 -b .safer

cp %{SOURCE2} .

%build

%if "%{BUILD_USE_X}"=="'yes'"
PATH=$PATH:%{_prefix}/X11R6/bin
%endif

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

#mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_prefix}/share
ln -s tmac.s	${RPM_BUILD_ROOT}%{_prefix}/share/groff/tmac/tmac.gs
ln -s tmac.mse	${RPM_BUILD_ROOT}%{_prefix}/share/groff/tmac/tmac.gmse
ln -s tmac.m	${RPM_BUILD_ROOT}%{_prefix}/share/groff/tmac/tmac.gm
ln -s troff	${RPM_BUILD_ROOT}%{_prefix}/bin/gtroff
ln -s tbl	${RPM_BUILD_ROOT}%{_prefix}/bin/gtbl
ln -s pic	${RPM_BUILD_ROOT}%{_prefix}/bin/gpic
ln -s eqn	${RPM_BUILD_ROOT}%{_prefix}/bin/geqn
ln -s neqn	${RPM_BUILD_ROOT}%{_prefix}/bin/gneqn
ln -s refer	${RPM_BUILD_ROOT}%{_prefix}/bin/grefer
ln -s lookbib	${RPM_BUILD_ROOT}%{_prefix}/bin/glookbib
ln -s indxbib	${RPM_BUILD_ROOT}%{_prefix}/bin/gindxbib
ln -s soelim	${RPM_BUILD_ROOT}%{_prefix}/bin/gsoelim
ln -s nroff	${RPM_BUILD_ROOT}%{_prefix}/bin/gnroff

# Build system is compressing man-pages
ln -s eqn.1.gz	${RPM_BUILD_ROOT}%{_mandir}/man1/geqn.1.gz
ln -s indxbib.1.gz ${RPM_BUILD_ROOT}%{_mandir}/man1/gindxbib.1.gz
ln -s lookbib.1.gz ${RPM_BUILD_ROOT}%{_mandir}/man1/glookbib.1.gz
ln -s nroff.1.gz 	${RPM_BUILD_ROOT}%{_mandir}/man1/gnroff.1.gz
ln -s pic.1.gz 	${RPM_BUILD_ROOT}%{_mandir}/man1/gpic.1.gz
ln -s refer.1.gz 	${RPM_BUILD_ROOT}%{_mandir}/man1/grefer.1.gz
ln -s soelim.1.gz ${RPM_BUILD_ROOT}%{_mandir}/man1/gsoelim.1.gz
ln -s tbl.1.gz 	${RPM_BUILD_ROOT}%{_mandir}/man1/gtbl.1.gz
ln -s troff.1.gz 	${RPM_BUILD_ROOT}%{_mandir}/man1/gtroff.1.gz

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/rhs/rhs-printfilters
install -m755 %{SOURCE1} ${RPM_BUILD_ROOT}%{_prefix}/share/rhs/rhs-printfilters

find ${RPM_BUILD_ROOT}%{_prefix}/bin ${RPM_BUILD_ROOT}%{_mandir} -type f -o -type l | \
	grep -v afmtodit | grep -v grog | grep -v mdoc.samples |\
	grep -v mmroff |\
	sed "s|${RPM_BUILD_ROOT}||g" | sed "s|\.[0-9]|\.*|g" > groff-files

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f groff-files
%defattr(-,root,root)
%doc	BUG-REPORT NEWS PROBLEMS README README.A4 TODO VERSION
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
* Sun Aug  6 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
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


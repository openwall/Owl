# $Id: Owl/packages/tcsh/tcsh.spec,v 1.7 2001/07/06 20:32:56 mci Exp $

%define	_bindir	/bin

Summary: 	An enhanced version of csh, the C shell.
Name: 		tcsh
Version: 	6.10.01
Release: 	2owl
Copyright: 	BSD
Group: 		System Environment/Shells
Source: 	ftp://ftp.fujitsu.co.jp/pub/misc/shells/tcsh/%{name}-%{version}.tgz
Patch0:		tcsh-6.10.00-rh-utmp.diff
Patch1: 	tcsh-6.09.00-rh-termios_hack.diff
Patch2: 	tcsh-6.09.00-rh-locale.diff
Patch3:		tcsh-6.10.00-suse-owl-shtmp.diff
Patch4:		tcsh-6.10.01-deb-format.diff
Patch5:		tcsh-6.10.01-deb-config.diff
Patch6:		tcsh-6.10.01-deb-locale.diff
Patch7:		tcsh-6.10.01-deb-man.diff
Patch8:		tcsh-6.10.01-deb-time.diff
Provides: 	csh = %{version}
Prereq: 	fileutils grep
URL: 		http://www.primate.wisc.edu/software/csh-tcsh-book/
Buildroot: 	/var/rpm-buildroot/%{name}-root

%description
Tcsh is an enhanced but completely compatible version of csh, the C
shell.  Tcsh is a command language interpreter which can be used both
as an interactive login shell and as a shell script command processor.
Tcsh includes a command line editor, programmable word completion,
spelling correction, a history mechanism, job control and a C language
like syntax.

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
%configure
make LIBES="-lnsl -ltermcap -lcrypt" all catalogs
test -x %{__perl} && %{__perl} tcsh.man2html tcsh.man || :

%install
rm -rf ${RPM_BUILD_ROOT}

install -m 755 -D -s tcsh ${RPM_BUILD_ROOT}%{_bindir}/tcsh
install -m 644 -D tcsh.man ${RPM_BUILD_ROOT}%{_mandir}/man1/tcsh.1
ln -sf tcsh ${RPM_BUILD_ROOT}%{_bindir}/csh
ln -sf tcsh.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/csh.1
nroff -me eight-bit.me > eight-bit.txt

for i in de es fr gr_GR it ja
do
    mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/locale/$i/LC_MESSAGES
done
install -m 644 tcsh.german.cat ${RPM_BUILD_ROOT}%{_datadir}/locale/de/LC_MESSAGES/tcsh
install -m 644 tcsh.spanish.cat ${RPM_BUILD_ROOT}%{_datadir}/locale/es/LC_MESSAGES/tcsh
install -m 644 tcsh.french.cat ${RPM_BUILD_ROOT}%{_datadir}/locale/fr/LC_MESSAGES/tcsh
install -m 644 tcsh.greek.cat ${RPM_BUILD_ROOT}%{_datadir}/locale/gr_GR/LC_MESSAGES/tcsh
install -m 644 tcsh.italian.cat ${RPM_BUILD_ROOT}%{_datadir}/locale/it/LC_MESSAGES/tcsh
install -m 644 tcsh.ja.cat ${RPM_BUILD_ROOT}%{_datadir}/locale/ja/LC_MESSAGES/tcsh

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
if ! grep -qs '^/bin/csh$' /etc/shells; then echo /bin/csh >>/etc/shells; fi
if ! grep -qs '^/bin/tcsh$' /etc/shells; then echo /bin/tcsh >>/etc/shells; fi

%postun
if [ ! -x %{_bindir}/tcsh ]; then
    grep -v '^%{_bindir}/tcsh$' /etc/shells | grep -v '^%{_bindir}/csh$'> /etc/shells.rpm
    mv /etc/shells.rpm /etc/shells
fi

%files
%defattr(-,root,root)
%doc NewThings FAQ eight-bit.txt complete.tcsh Fixes tcsh.html
%{_bindir}/tcsh
%{_bindir}/csh
%{_mandir}/*/*
%{_datadir}/locale/*/LC_MESSAGES/tcsh*

%changelog
* Fri Jul 06 2001 Michail Litvak <mci@owl.openwall.com>
- added some patches from Debian (format bug, etc.)

* Wed Jun 20 2001 Michail Litvak <mci@owl.openwall.com>
- updated to 6.10.01
- some spec cleanups

* Sun Dec 17 2000 Solar Designer <solar@owl.openwall.com>
- Build HTML docs correctly (the script was trying to be too smart and
behaved differently when not run on a tty).

* Fri Dec 15 2000 Solar Designer <solar@owl.openwall.com>
- Updated the mkstemp() patch to actually be correct for 6.10.00 (which
already includes a more portable, but worse fix for the same problem).

* Sat Dec 09 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- 6.10
- security update

* Sat Nov 04 2000 Solar Designer <solar@owl.openwall.com>
- Added a patch by Dr. Werner Fink <werner@suse.de> (and slightly modified)
for the unsafe /tmp access reported on Bugtraq by proton.

* Sun Sep 24 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 15 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- add locale support (#10345).

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies

* Thu Jan 27 2000 Jeff Johnson <jbj@redhat.com>
- append entries to spanking new /etc/shells.

* Mon Jan 10 2000 Jeff Johnson <jbj@redhat.com>
- update to 6.09.
- fix strcoll oddness (#6000, #6244, #6398).

* Sat Sep 25 1999 Michael K. Johnson <johnsonm@redhat.com>
- fix $shell by using --bindir

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 5)

* Wed Feb 24 1999 Cristian Gafton <gafton@redhat.com>
- patch for using PATH_MAX instead of some silly internal #defines for
  variables that handle filenames.

* Fri Nov  6 1998 Jeff Johnson <jbj@redhat.com>
- update to 6.08.00.

* Fri Oct 02 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 6.07.09 from the freebsd
- security fix

* Wed Aug  5 1998 Jeff Johnson <jbj@redhat.com>
- use -ltermcap so that /bin/tcsh can be used in single user mode w/o /usr.
- update url's

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 6.07; added BuildRoot
- cleaned up the spec file; fixed source url

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- added termios hacks for new glibc
- added /bin/csh to file list

* Fri Jun 13 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Fri Feb 07 1997 Erik Troan <ewt@redhat.com>
- Provides csh, adds and removes /bin/csh from /etc/shells if csh package
isn't installed.

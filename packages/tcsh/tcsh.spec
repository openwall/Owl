# $Id: Owl/packages/tcsh/tcsh.spec,v 1.9 2003/10/30 21:15:49 solar Exp $

Summary: An enhanced version of csh, the C shell.
Name: tcsh
Version: 6.10.01
Release: owl2
License: BSD
Group: System Environment/Shells
URL: http://www.primate.wisc.edu/software/csh-tcsh-book/
Source: ftp://ftp.fujitsu.co.jp/pub/misc/shells/tcsh/%name-%version.tgz
Patch0: tcsh-6.10.00-rh-utmp.diff
Patch1: tcsh-6.09.00-rh-termios_hack.diff
Patch2: tcsh-6.09.00-rh-locale.diff
Patch3: tcsh-6.10.00-suse-owl-shtmp.diff
Patch4: tcsh-6.10.01-deb-format.diff
Patch5: tcsh-6.10.01-deb-config.diff
Patch6: tcsh-6.10.01-deb-locale.diff
Patch7: tcsh-6.10.01-deb-man.diff
Patch8: tcsh-6.10.01-deb-time.diff
PreReq: fileutils, grep
Provides: csh = %version
BuildRoot: /override/%name-%version

%description
tcsh is an enhanced but completely compatible version of csh, the C
shell.  tcsh is a command language interpreter which can be used both
as an interactive login shell and as a shell script command processor.
tcsh includes a command line editor, programmable word completion,
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

%define	_bindir	/bin

%build
%configure
make LIBES="-lnsl -ltermcap -lcrypt" all catalogs
test -x %__perl && %__perl tcsh.man2html tcsh.man || :

%install
rm -rf $RPM_BUILD_ROOT

install -m 755 -D -s tcsh $RPM_BUILD_ROOT%_bindir/tcsh
install -m 644 -D tcsh.man $RPM_BUILD_ROOT%_mandir/man1/tcsh.1
ln -sf tcsh $RPM_BUILD_ROOT%_bindir/csh
ln -sf tcsh.1 $RPM_BUILD_ROOT%_mandir/man1/csh.1
nroff -me eight-bit.me > eight-bit.txt

for i in de es fr gr_GR it ja
do
	mkdir -p $RPM_BUILD_ROOT%_datadir/locale/$i/LC_MESSAGES
done
install -m 644 tcsh.german.cat \
	$RPM_BUILD_ROOT%_datadir/locale/de/LC_MESSAGES/tcsh
install -m 644 tcsh.spanish.cat \
	$RPM_BUILD_ROOT%_datadir/locale/es/LC_MESSAGES/tcsh
install -m 644 tcsh.french.cat \
	$RPM_BUILD_ROOT%_datadir/locale/fr/LC_MESSAGES/tcsh
install -m 644 tcsh.greek.cat \
	$RPM_BUILD_ROOT%_datadir/locale/gr_GR/LC_MESSAGES/tcsh
install -m 644 tcsh.italian.cat \
	$RPM_BUILD_ROOT%_datadir/locale/it/LC_MESSAGES/tcsh
install -m 644 tcsh.ja.cat \
	$RPM_BUILD_ROOT%_datadir/locale/ja/LC_MESSAGES/tcsh

%post
if ! grep -qs '^/bin/csh$' /etc/shells; then echo /bin/csh >> /etc/shells; fi
if ! grep -qs '^/bin/tcsh$' /etc/shells; then echo /bin/tcsh >> /etc/shells; fi

%postun
if [ ! -x %_bindir/tcsh ]; then
	grep -Ev '^%_bindir/t{0,1}csh$' /etc/shells > /etc/shells.rpmtmp
	mv /etc/shells.rpmtmp /etc/shells
fi

%files
%defattr(-,root,root)
%doc NewThings FAQ eight-bit.txt complete.tcsh Fixes tcsh.html
%_bindir/tcsh
%_bindir/csh
%_mandir/*/*
%_datadir/locale/*/LC_MESSAGES/tcsh*

%changelog
* Mon Feb 04 2002 Solar Designer <solar@owl.openwall.com> 6.10.01-owl2
- Enforce our new spec file conventions.

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

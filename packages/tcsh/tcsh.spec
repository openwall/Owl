# $Id: Owl/packages/tcsh/tcsh.spec,v 1.13 2005/09/30 19:44:26 solar Exp $

Summary: An enhanced version of csh, the C shell.
Name: tcsh
Version: 6.14.00
Release: owl1
License: BSD
Group: System Environment/Shells
URL: http://www.tcsh.org/Home
Source: ftp://ftp.astron.com/pub/tcsh/%name-%version.tar.gz
Patch0: tcsh-6.14.00-suse-owl-tmp.diff
Patch1: tcsh-6.14.00-owl-config.diff
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

cat > catalogs << EOF
de ISO-8859-1 german
el ISO-8859-7 greek
en ISO-8859-1 C
es ISO-8859-1 spanish
et ISO-8859-1 et
fi ISO-8859-1 finnish
fr ISO-8859-1 french
it ISO-8859-1 italian
ja eucJP ja
ru KOI8-R russian
uk KOI8-U ukrainian
EOF

while read lang charset language; do
	if ! grep -q '^$ codeset=' nls/$language/set1; then
		echo '$ codeset='$charset      >  nls/$language/set1.codeset
		cat nls/$language/set1         >> nls/$language/set1.codeset
		cat nls/$language/set1.codeset >  nls/$language/set1
		rm nls/$language/set1.codeset
	fi
done < catalogs

%define	_bindir	/bin

%build
%configure
make LIBES="-lnsl -ltermcap -lcrypt" all
test -x %__perl && %__perl tcsh.man2html tcsh.man || :
make -C nls catalogs

%install
rm -rf %buildroot

install -m 755 -D -s tcsh %buildroot%_bindir/tcsh
install -m 644 -D tcsh.man %buildroot%_mandir/man1/tcsh.1
ln -sf tcsh %buildroot%_bindir/csh
ln -sf tcsh.1 %buildroot%_mandir/man1/csh.1
nroff -me eight-bit.me > eight-bit.txt

while read lang charset language; do
	dest=%buildroot%_datadir/locale/$lang/LC_MESSAGES
	if test -f tcsh.$language.cat; then
		mkdir -p $dest
		install -m 644 tcsh.$language.cat $dest/tcsh
	fi
done < catalogs

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
* Sun Sep 18 2005 Gremlin from Kremlin <gremlin@owl.openwall.com> 6.14.00-owl1
- Updated to 6.14.00, dropped obsolete patches (only the -tmp patch is left),
disabled AUTOLOGOUT by default.

* Sat Feb 28 2004 Michail Litvak <mci@owl.openwall.com> 6.10.01-owl3
- Fixed building with new glibc (fix from ALT's spec file).

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

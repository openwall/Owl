# $Owl: Owl/packages/tcsh/tcsh.spec,v 1.25 2010/03/05 08:08:59 solar Exp $

Summary: An enhanced version of csh, the C shell.
Name: tcsh
Version: 6.17.00
Release: owl1
License: BSD
Group: System Environment/Shells
URL: http://www.tcsh.org/Home
Source: ftp://ftp.astron.com/pub/tcsh/%name-%version.tar.bz2
Patch0: tcsh-6.17.00-owl-tmp.diff
Patch1: tcsh-6.17.00-owl-config.diff
Patch2: tcsh-6.17.00-rh-printexitvalue.diff
Patch3: tcsh-6.17.00-rh-signal.diff
Patch4: tcsh-6.17.00-owl-warnings.diff
PreReq: fileutils, grep
Requires(postun): sed >= 4.0.9
BuildRequires: perl, groff, libtermcap-devel, glibc-utils
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

%define	_bindir	/bin

%{expand:%%define optflags %optflags -Wall}

%build
%configure
%__make LIBES="-ltermcap -lcrypt" all
test -x %__perl && %__perl tcsh.man2html tcsh.man || :
%__make -C nls catalogs

%install
rm -rf %buildroot

install -m 755 -D tcsh %buildroot%_bindir/tcsh
install -m 644 -D tcsh.man %buildroot%_mandir/man1/tcsh.1
ln -sf tcsh %buildroot%_bindir/csh
ln -sf tcsh.1 %buildroot%_mandir/man1/csh.1
nroff -me eight-bit.me > eight-bit.txt

while read lang language; do
	dest=%buildroot%_datadir/locale/$lang/LC_MESSAGES
	if test -f tcsh.$language.cat; then
		mkdir -p $dest
		install -m 644 tcsh.$language.cat $dest/tcsh
	fi
done << EOF
de german
el greek
en C
es spanish
et et
fi finnish
fr french
it italian
ja ja
pl pl
ru russian
uk ukrainian
EOF

%post
fgrep -qx /bin/csh /etc/shells || echo /bin/csh >> /etc/shells
fgrep -qx /bin/tcsh /etc/shells || echo /bin/tcsh >> /etc/shells

%postun
if [ $1 -eq 0 ]; then
	sed -i '/\/bin\/t\?csh/d' /etc/shells
fi

%files
%defattr(-,root,root)
%doc NewThings FAQ eight-bit.txt complete.tcsh Fixes tcsh.html
%_bindir/tcsh
%_bindir/csh
%_mandir/*/*
%_datadir/locale/*/LC_MESSAGES/tcsh*

%changelog
* Fri Mar 05 2010 Solar Designer <solar-at-owl.openwall.com> 6.17.00-owl1
- Reworked the -tmp patch to always use strings of the regular "char" (not
"Char") for the temporary files directory and temporary file pathnames.
- Changed %post to use "fgrep -x", reverted Gremlin's changes to %postun.
- Corrected a typo in the spec file (6.17.00-owl0 wouldn't build).
- Re-compressed the source tarball from .gz to .bz2.
- Enabled -Wall and fixed the code to build without any warnings again.

* Wed Mar 03 2010 Gremlin from Kremlin <gremlin-at-owl.openwall.com> 6.17.00-owl0
- Updated to 6.17.00

* Thu May 04 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 6.14.00-owl5
- Added glibc-utils to BuildRequires due to gencat.

* Wed Jan 04 2006 Gremlin from Kremlin <gremlin-at-owl.openwall.com> 6.14.00-owl4
- Disabled color output for built-in "ls-F" command, as it caused choke on
newer LS_COLORS options.

* Mon Oct 24 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 6.14.00-owl3
- Adjusted the tcsh.1 patch as suggested by Solar.

* Wed Oct 19 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 6.14.00-owl2
- Replaced 'make' with '%%__make'.
- Dropped the strip option from install in favor of brp- scripts.
- Removed -lnsl from 'LIBES=', since it isn't needed to be specified
explicitly.
- Added BuildRequires on perl, groff, libtermcap-devel.
- Fixed tcsh.1 to mention the correct path for temporary files used for '<<'
redirections (appended to the -suse-owl-tmp patch).
- Optimized the %%postun, avoided the use of the predictable temporary file
name.
- Added Requires(postun) sed >= 4.0.9.

* Sun Sep 18 2005 Gremlin from Kremlin <gremlin-at-owl.openwall.com> 6.14.00-owl1
- Updated to 6.14.00, dropped obsolete patches (only the -tmp patch is left),
disabled AUTOLOGOUT by default.

* Sat Feb 28 2004 Michail Litvak <mci-at-owl.openwall.com> 6.10.01-owl3
- Fixed building with new glibc (fix from ALT's spec file).

* Mon Feb 04 2002 Solar Designer <solar-at-owl.openwall.com> 6.10.01-owl2
- Enforce our new spec file conventions.

* Fri Jul 06 2001 Michail Litvak <mci-at-owl.openwall.com>
- added some patches from Debian (format bug, etc.)

* Wed Jun 20 2001 Michail Litvak <mci-at-owl.openwall.com>
- updated to 6.10.01
- some spec cleanups

* Sun Dec 17 2000 Solar Designer <solar-at-owl.openwall.com>
- Build HTML docs correctly (the script was trying to be too smart and
behaved differently when not run on a tty).

* Fri Dec 15 2000 Solar Designer <solar-at-owl.openwall.com>
- Updated the mkstemp() patch to actually be correct for 6.10.00 (which
already includes a more portable, but worse fix for the same problem).

* Sat Dec 09 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- 6.10
- security update

* Sat Nov 04 2000 Solar Designer <solar-at-owl.openwall.com>
- Added a patch by Dr. Werner Fink <werner at suse.de> (and slightly modified)
for the unsafe /tmp access reported on Bugtraq by proton.

* Sun Sep 24 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH

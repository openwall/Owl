# $Owl: Owl/packages/tcsh/tcsh.spec,v 1.30 2014/07/12 14:19:27 galaxy Exp $

Summary: An enhanced version of csh, the C shell.
Name: tcsh
Version: 6.18.01
Release: owl3
License: BSD
Group: System Environment/Shells
URL: http://www.tcsh.org/Home
# ftp://ftp.astron.com/pub/tcsh/%name-%version.tar.gz
Source0: %name-%version.tar.xz
Source1: csh.login
Source2: csh.cshrc
Source3: skel.tcshrc
Patch0: tcsh-6.18.01-owl-tmp.diff
Patch1: tcsh-6.18.01-owl-config.diff
Patch2: tcsh-6.18.01-owl-warnings.diff
Requires(post,postun): fileutils, grep
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

%define	_bindir	/bin

%{expand:%%define optflags %optflags -Wall}

%build
%configure
%__make LIBES="-ltermcap -lcrypt" all
%__perl tcsh.man2html tcsh.man || :
%__make -C nls catalogs

%install
rm -rf %buildroot

install -m 755 -D tcsh %buildroot%_bindir/tcsh
install -pm 644 -D tcsh.man %buildroot%_mandir/man1/tcsh.1
ln -sf tcsh %buildroot%_bindir/csh
ln -sf tcsh.1 %buildroot%_mandir/man1/csh.1
nroff -me eight-bit.me > eight-bit.txt

while read lang language; do
	dest=%buildroot%_datadir/locale/$lang/LC_MESSAGES
	if test -f nls/$language.cat; then
		mkdir -p $dest
		install -m 644 nls/$language.cat $dest/tcsh.mo
	fi
done << EOF
en C
et et
fi finnish
fr french
de german
el greek
it italian
ja ja
pl pl
ru russian
es spanish
uk ukrainian
EOF

mkdir -p %buildroot/etc/skel
install -pm 644 %_sourcedir/skel.tcshrc %buildroot/etc/skel/.tcshrc
install -pm 644 %_sourcedir/csh.{login,cshrc} %buildroot/etc/

%find_lang %name || :
touch '%name.lang'

%post
fgrep -qx /bin/csh /etc/shells || echo /bin/csh >> /etc/shells
fgrep -qx /bin/tcsh /etc/shells || echo /bin/tcsh >> /etc/shells

%postun
if [ $1 -eq 0 ]; then
	sed -i '/\/bin\/t\?csh/d' /etc/shells
fi

%files -f %name.lang
%defattr(-,root,root)
%doc NewThings FAQ eight-bit.txt complete.tcsh Fixes tcsh.html
%config(noreplace) /etc/csh.*
%config(noreplace) /etc/skel/.tcshrc
%_bindir/tcsh
%_bindir/csh
%_mandir/*/*

%changelog
* Mon Jun 30 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 6.18.01-owl3
- Replaced the deprecated PreReq tag with Requires(post,postun).
- Added %%find_lang.
- Removed the -x test on %%__perl since it breaks the purpose of the tool
macros (where one could re-define the macro).

* Tue Aug 14 2012 Solar Designer <solar-at-owl.openwall.com> 6.18.01-owl2
- Re-introduced the man page patch to reflect the naming of temporary files.
- Revised the default settings to have fewer personal preferences and to be
more consistent with the settings that we use for bash.
- Use xz-compressed Source tarball.

* Mon Jul 23 2012 Gremlin from Kremlin <gremlin-at-owl.openwall.com> 6.18.01-owl1
- Updated to 6.18.01
- Dropped obsolete and recreated actual patches
- Re-enabled color output for built-in "ls-F" command
- Moved most settings from csh.login to csh.cshrc
- Added /etc/skel/.tcshrc file
- Added some examples to the configuration files

* Sat Dec 04 2010 Solar Designer <solar-at-owl.openwall.com> 6.17.00-owl3
- Revised the default shell prompt per gremlin@'s suggestion.

* Tue Mar 30 2010 Solar Designer <solar-at-owl.openwall.com> 6.17.00-owl2
- Moved /etc/csh.login and /etc/csh.cshrc from the owl-etc package to this one.

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

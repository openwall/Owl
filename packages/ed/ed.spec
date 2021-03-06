# $Owl: Owl/packages/ed/ed.spec,v 1.26 2014/07/12 14:08:53 galaxy Exp $

Summary: The GNU line-oriented text editor.
Name: ed
Version: 1.5
Release: owl2
License: GPLv3+
Group: Applications/Text
URL: http://www.gnu.org/software/ed/
Source: ftp://ftp.gnu.org/gnu/ed/ed-%version.tar.gz
# Signature: ftp://ftp.gnu.org/gnu/ed/ed-%version.tar.gz.sig
Patch0: ed-1.5-owl-alt-progname.diff
Patch1: ed-1.5-alt-owl-info.diff
Patch2: ed-1.5-owl-man.diff
Requires(pre): /sbin/install-info
BuildRoot: /override/%name-%version

%description
ed is a line-oriented text editor, used to create, display, and modify
text files (both interactively and via shell scripts).
For most purposes, ed has been replaced in normal usage by full-screen
editors such as vi and emacs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{expand:%%define optflags %optflags -Wall -Dlint}

%build
%configure \
	CC='%__cc' CFLAGS='%optflags' \
	--prefix=/usr --exec-prefix=/ --bindir=/bin
%__make LDFLAGS=-s

%check
%__make check

%install
%makeinstall bindir=%buildroot/bin

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/ed.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/ed.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc NEWS AUTHORS README
/bin/*ed
%_infodir/ed.info*
%_mandir/man1/*ed.*

%changelog
* Sat Jun 28 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.5-owl2
- Regenerated the info and man patches since they were fuzzy.

* Wed Oct 06 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.5-owl1
- Updated to 1.5.
- Updated owl-alt-progname patch.

* Tue Aug 25 2009 Michail Litvak <mci-at-owl.openwall.com> 1.4-owl1
- Updated to 1.4.
- Removed outdated patches (there was significant source changes).

* Thu Nov 15 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.2-owl24
- Synced with ed-0.2-alt6:
- Disabled build of code provided by glibc.
- Fixed program_name initialization.
- Enabled build with -Wall, fixed uncovered compilation warnings.
- Added run of testcase after build.
- Added URL, updated info entry.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.2-owl23
- Corrected info files installation.

* Wed Feb 25 2004 Michail Litvak <mci-at-owl.openwall.com> 0.2-owl22
- Fixed building with new auto* tools.

* Wed Sep 04 2002 Michail Litvak <mci-at-owl.openwall.com> 0.2-owl21
- Replace -owl-mkstemp.diff by more improved -alt-tmp.diff
- add patch to fix man page

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Wed Jan 30 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Nov 23 2000 Michail Litvak <mci-at-owl.openwall.com>
- ed-0.2-deb-tmpnam.diff replaced by ed-0.2-owl-mkstemp.diff
  we must use mkstemp(3)

* Wed Nov 22 2000 Michail Litvak <mci-at-owl.openwall.com>
- imported from RH
- patches from Debian
- ed-0.2-deb-mkfile.diff: don't compile in
  libed.a as it's redundant old code   superseded by code in glibc.
  This reduces the ed binary by 23k.
- ed-0.2-deb-parentheses.diff: parentheses to quiet -Wall
- ed-0.2-deb-tmpnam.diff: Patched buf.c to use tempnam()

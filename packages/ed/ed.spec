# $Owl: Owl/packages/ed/ed.spec,v 1.21 2007/11/16 00:00:52 ldv Exp $

Summary: The GNU line-oriented text editor.
Name: ed
Version: 0.2
Release: owl24
License: GPL
Group: Applications/Text
URL: http://www.gnu.org/software/ed/
Source: ftp://ftp.gnu.org/gnu/ed-%version.tar.gz
Patch0: ed-0.2-alt-configure.diff
Patch1: ed-0.2-alt-error.diff
Patch2: ed-0.2-deb-Makefile.diff
Patch3: ed-0.2-deb-parentheses.diff
Patch4: ed-0.2-alt-tmp.diff
Patch5: ed-0.2-alt-progname.diff
Patch6: ed-0.2-deb-owl-man.diff
Patch7: ed-0.2-alt-owl-info.diff
Patch8: ed-0.2-alt-glibc.diff
Patch9: ed-0.2-alt-warnings.diff
PreReq: /sbin/install-info
Prefix: %_prefix
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
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
rm getopt.h regex.h
rm configure ed.info

%{expand:%%define optflags %optflags -Wall -Dlint}

%build
autoreconf -fis
# glibc does have sigsetjmp, it's just a macro, which confuses autoconf.
export ac_cv_func_sigsetjmp=yes
%configure --exec-prefix=/
make LDFLAGS=-s
make -k check

%install
%makeinstall bindir=%buildroot/bin mandir=%buildroot%_mandir/man1

%post
/sbin/install-info %_infodir/ed.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/ed.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc NEWS POSIX README THANKS
/bin/*ed
%_infodir/ed.info*
%_mandir/man1/*ed.*

%changelog
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

# $Owl: Owl/packages/vim/vim.spec,v 1.47 2010/12/06 05:52:13 solar Exp $

%define BUILD_USE_GPM 0
%define BUILD_USE_PYTHON 0
%define BUILD_USE_X 0

Summary: The VIM editor.
Name: vim
%define major 7
%define minor 3
%define alpha %nil
%define patchlevel 075
%define vimdir vim%major%minor%alpha
Version: %major.%minor%{?patchlevel:.%patchlevel}
Release: owl1
License: Charityware
Group: Applications/Editors
URL: http://www.vim.org
Source0: vim-%major.%minor%alpha.tar.xz
# ftp://ftp.vim.org/pub/vim/unix/vim-%major.%minor%alpha.tar.bz2
Source10: vitmp.c
Source11: vitmp.1
Source12: vimrc
Source13: gvim.desktop
Source14: README
Source15: filelist.syntax-base.rel
Patch0: vim-%major.%minor-%version.xz
# ftp://ftp.vim.org/pub/vim/patches/%major.%minor/
# cat %major.%minor.* | xz > vim-%major.%minor-%version.xz
Patch10: vim-6.4-rh-owl-spec-syntax.diff
Patch11: vim-6.4-rh-paths.diff
Patch12: vim-7.2-owl-tmp.diff
Patch13: vim-7.2-rh-fix-keys.diff
Patch14: vim-7.2-rh-owl-vim-not-vi.diff
Patch15: vim-7.2-rh-owl-xxd-locale.diff
Patch16: vim-7.3-owl-configure.diff
Patch17: vim-7.3-owl-Makefile.diff
Requires: mktemp >= 1:1.3.1
BuildRequires: libtermcap-devel, ncurses-devel, perl
BuildRequires: sed >= 4.0.9
%if %BUILD_USE_GPM
BuildRequires: gpm-devel
%endif
%if %BUILD_USE_PYTHON
BuildRequires: python-devel
%endif
%if %BUILD_USE_X
BuildRequires: gtk+-devel
%endif
BuildRoot: /override/%name-%version

%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  vi was the first real screen-based editor for Unix, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.

%package common
Summary: The common files needed by any version of the VIM editor.
Group: Applications/Editors

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  vi was the first real screen-based editor for Unix, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-common package contains files which every VIM binary will need in
order to run.

%package small
Summary: A small version of the VIM editor.
Group: Applications/Editors
Requires: vim-common
Provides: vim-minimal
Obsoletes: vim, vim-minimal

%description small
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  vi was the first real screen-based editor for Unix, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-small package includes a small version of VIM, which is installed
into /bin/vi for use when only the root partition is present.

%package enhanced
Summary: A feature-rich version of the VIM editor.
Group: Applications/Editors
Requires: vim-common
Obsoletes: vim-color

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  vi was the first real screen-based editor for Unix, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-enhanced package contains a version of VIM with all its features
compiled in.

%if %BUILD_USE_X
%package X11
Summary: A version of the VIM editor for the X Window System.
Group: Applications/Editors
Requires: vim-common

%description X11
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  vi was the first real screen-based editor for Unix, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.
vim-X11 is a version of the VIM editor which will run within the
X Window System.  This package lets you run VIM as an X application
with a graphical interface and mouse support.
%endif

%package spell
Summary: The dictionaries for spell checking.  This package is optional.
Group: Applications/Editors
Requires: vim-common

%description spell
This subpackage contains dictionaries for vim spell checking in
many different languages.

%package lang
Summary: Language files for Vim.  This package is optional.
Group: Applications/Editors
Requires: vim-common

%description lang
This subpackage contains translation files for many different languages.

%package syntax
Summary: Extra syntax files for Vim.  This package is optional.
Group: Applications/Editors
Requires: vim-enhanced

%description syntax
This subpackage contains extra syntax highlighting files for Vim.

%package tutor
Summary: Vim tutorial.  This package is optional.
Group: Applications/Editors
Requires: vim-common

%description tutor
This subpackage contains Vim tutorial files in many different languages.

%prep
%setup -q -n %vimdir
%patch0 -p0
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
rm src/auto/configure
install -pm644 %_sourcedir/README .

%if %BUILD_USE_GPM
%define	gpmflag --enable-gpm
%else
%define	gpmflag --disable-gpm
%endif

%if %BUILD_USE_PYTHON
%define	pythonflag --enable-pythoninterp
%else
%define pythonflag --disable-pythoninterp
%endif

%build
cd src

aclocal
autoconf
sed 's+\./config.log+auto/config.log+' configure > auto/configure
chmod 755 auto/configure

%if %BUILD_USE_X
export ac_cv_func_mkstemp=yes \
%configure \
	--with-features=huge \
	--enable-perlinterp --disable-tclinterp \
	--with-x=yes --enable-gui=gnome \
	--exec-prefix=/usr/X11R6 \
	--enable-xim --enable-multibyte \
	--enable-fontset %pythonflag %gpmflag
%__make VIMRUNTIMEDIR=%_datadir/vim/%vimdir COMPILEDBY=build@%buildhost
mv vim gvim
%__make clean
%endif

export ac_cv_func_mkstemp=yes \
%configure \
	--with-features=huge \
	--disable-netbeans \
	--enable-perlinterp --disable-tclinterp \
	--with-x=no --enable-gui=no \
	--enable-multibyte \
	--enable-fontset %pythonflag %gpmflag
%__make VIMRUNTIMEDIR=%_datadir/vim/%vimdir COMPILEDBY=build@%buildhost
mv vim vim-enhanced
%__make clean

export ac_cv_func_mkstemp=yes \
%configure \
	--with-features=small \
	--disable-netbeans \
	--disable-arabic \
	--disable-farsi \
	--disable-pythoninterp --disable-perlinterp --disable-tclinterp \
	--with-x=no --enable-gui=no \
	--with-tlib=termcap --disable-gpm
%__make VIMRUNTIMEDIR=%_datadir/vim/%vimdir COMPILEDBY=build@%buildhost

gcc %optflags -Wall -s %_sourcedir/vitmp.c -o vitmp

%install
rm -rf %buildroot
mkdir -p %buildroot/bin
mkdir -p %buildroot%_bindir
mkdir -p %buildroot%_datadir/vim
%if %BUILD_USE_X
mkdir -p %buildroot%_prefix/X11R6/bin
%endif

pushd src
%makeinstall installmacros BINDIR=/bin DESTDIR=%buildroot
mv %buildroot/bin/xxd %buildroot%_bindir
install -m755 vim-enhanced %buildroot%_bindir/vim
%if %BUILD_USE_X
install -m755 gvim %buildroot%_prefix/X11R6/bin/
%endif

install -m755 vitmp %buildroot/bin/
install -pm644 %_sourcedir/vitmp.1 %buildroot%_mandir/man1/

pushd %buildroot
mv bin/vim bin/vi
mv bin/rview bin/view bin/vimtutor .%_bindir/
rm bin/ex
mv bin/rvim .%_bindir/
ln -s vi bin/rvi
ln -s vi bin/ex
ln -s vim .%_bindir/vimdiff
sed -i "s,%buildroot,," .%_mandir/man1/{vim,vimtutor}.1
ln -s vim.1 .%_mandir/man1/vi.1
ln -s vim.1 .%_mandir/man1/rvi.1

%if %BUILD_USE_X
ln -s gvim .%_prefix/X11R6/bin/vimx
ln -s gvim .%_prefix/X11R6/bin/gview
ln -s gvim .%_prefix/X11R6/bin/gex
ln -s gvim .%_prefix/X11R6/bin/evim
ln -s vim.1 .%_mandir/man1/gvim.1
ln -s vim.1 .%_mandir/man1/vimx.1
ln -s vim.1 .%_mandir/man1/gview.1
ln -s vim.1 .%_mandir/man1/gex.1
ln -s vim.1 .%_mandir/man1/evim.1
mkdir -p etc/X11/applnk/Applications
cp %_sourcedir/gvim.desktop etc/X11/applnk/Applications/
%else
# XXX: investigate this -- (GM)
rm -r .%_mandir/man1/evim.1*
rm -r .%_mandir/fr*/man1/evim.1*
rm -r .%_mandir/it*/man1/evim.1*
rm -r .%_mandir/pl*/man1/evim.1*
rm -r .%_mandir/ru*/man1/evim.1*
%endif

install -pm644 %_sourcedir/vimrc .%_datadir/vim/
sed -i 's!VIMDIR!%_datadir/vim/%vimdir!' .%_datadir/vim/vimrc

# Compress documentation
pushd .%_datadir/vim/%vimdir/doc/
gzip -9n *.txt
sed -i 's/\t\([a-zA-Z0-9\._-]\+\).txt/\t\1.txt.gz/' tags
popd

# Dependency cleanups
chmod 644 .%_datadir/vim/%vimdir/{doc/vim2html.pl,tools/{*.pl,vim132}}
popd
chmod 644 ../runtime/doc/vim2html.pl
popd

# filelist.syntax-base.rel MUST NOT contain blank lines
# otherwise the whole syntax/ directory is packaged in -enhanced
sed -e 's,^,%_datadir/%name/%name%major%minor/syntax/,' \
	%_sourcedir/filelist.syntax-base.rel | sort > filelist.syntax-base

find %buildroot/%_datadir/%name/%name%major%minor/syntax/ -type f | sed \
	-e 's,^%buildroot/,,' | sort > filelist.syntax-all

comm -13 filelist.syntax-base filelist.syntax-all > filelist.syntax-rest

%files common
%defattr(-,root,root)
%doc README
%_bindir/xxd
%_datadir/vim
%exclude %_datadir/%name/vim*/syntax
%exclude %_datadir/%name/vim*/lang
%exclude %_datadir/%name/vim*/spell
%exclude %_datadir/%name/vim*/tutor
%_mandir/man1/vim.*
%_mandir/fr*/man1/vim.*
%_mandir/it*/man1/vim.*
%_mandir/pl*/man1/vim.*
%_mandir/ru*/man1/vim.*
%_mandir/man1/xxd.*
%_mandir/fr*/man1/xxd.*
%_mandir/it*/man1/xxd.*
%_mandir/pl*/man1/xxd.*
%_mandir/ru*/man1/xxd.*

%files small
%defattr(-,root,root)
/bin/ex
/bin/rvi
/bin/vi
/bin/vitmp
%_mandir/man1/rvi.*
%_mandir/man1/vi.*
%_mandir/man1/vitmp.*

%files enhanced -f filelist.syntax-base
%defattr(-,root,root)
%_bindir/rview
%_bindir/rvim
%_bindir/view
%_bindir/vim
%_bindir/vimdiff
%_mandir/man1/rvim.*
%_mandir/man1/vimdiff.*
%_mandir/fr*/man1/vimdiff.*
%_mandir/it*/man1/vimdiff.*
%_mandir/pl*/man1/vimdiff.*
%_mandir/ru*/man1/vimdiff.*
%dir %_datadir/%name/vim*/syntax/

%files spell
%defattr(-,root,root)
%dir %_datadir/%name/vim*/spell
%_datadir/%name/vim*/spell/*

%files lang
%_datadir/%name/vim*/lang

%files syntax -f filelist.syntax-rest

%files tutor
%defattr(-,root,root)
%_bindir/vimtutor
%dir %_datadir/%name/vim*/tutor
%_datadir/%name/vim*/tutor/*
%_mandir/man1/vimtutor.*
%_mandir/fr*/man1/vimtutor.*
%_mandir/it*/man1/vimtutor.*
%_mandir/pl*/man1/vimtutor.*
%_mandir/ru*/man1/vimtutor.*

%if %BUILD_USE_X
%files X11
%defattr(-,root,root)
%config(missingok) /etc/X11/applnk/Applications/gvim.desktop
%_prefix/X11R6/bin/gvim
%_prefix/X11R6/bin/vimx
%_prefix/X11R6/bin/gview
%_prefix/X11R6/bin/gex
%_prefix/X11R6/bin/evim
%dir %_datadir/%name/vim*/lang
%_datadir/%name/vim*/lang/*
%_mandir/man1/gvim.*
%_mandir/man1/vimx.*
%_mandir/man1/gview.*
%_mandir/man1/gex.*
%_mandir/man1/evim.*
%_mandir/fr*/man1/evim.*
%_mandir/it*/man1/evim.*
%_mandir/pl*/man1/evim.*
%_mandir/ru*/man1/evim.*
%endif

%changelog
* Mon Dec 06 2010 Solar Designer <solar-at-owl.openwall.com> 7.3.075-owl1
- Updated to patchlevel 075.

* Sat Dec 04 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 7.3.021-owl4
- Introduced new subpackages -syntax and -lang.

* Fri Oct 15 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 7.3.021-owl3
- Fixed parallel build.
- Fixed vimrc bug.
- Do not recreate already existing symlinks.

* Wed Oct 13 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 7.3.021-owl2
- Use gzip-compressed doc/* files.
- Removed 'augroup gzip' section from vimrc (we have gzip plugin for this).

* Mon Oct 11 2010 Solar Designer <solar-at-owl.openwall.com> 7.3.021-owl1
- Patchlevel 021.
- Use xz-compressed Source files.

* Wed Oct 06 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 7.3.019-owl1
- Updated to 7.3 patchlevel 019.
- Dropped deb-fixes patch (fixed in upstream).
- Fixed build bug with old autoconf.

* Tue Mar 09 2010 Dmitry V. Levin <ldv-at-owl.openwall.com> 7.2.351-owl2
- vitmp: Updated vi commands required to disable backups in modern VIM.

* Sun Feb 14 2010 Michail Litvak <mci-at-owl.openwall.com> 7.2.351-owl1
- Updated to 7.2 patchlevel 351.
- Introduced new subpackages -spell and -tutor.

* Tue Oct 20 2009 Michail Litvak <mci-at-owl.openwall.com> 7.2.267-owl1
- Updated to 7.2 patchlevel 267.
- Regenerated patches, removed patches included to upstream.

* Thu Aug 30 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 6.4.4-owl3
- Backported upstream patch to disallow system() function in modelines
(CVE-2007-2438).
- Backported upstream fix for format string bug in help-tags tag handling
(CVE-2007-2953).

* Tue Apr 04 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 6.4.4-owl2
- Relocated view and rview from /bin to %_bindir.
- Removed ex from %_bindir, ex in /bin should be enough.
- Packaged rvim and vimdiff symlinks.
- Package manpages according to related binaries.

* Sun Dec 18 2005 Michail Litvak <mci-at-owl.openwall.com> 6.4.4-owl1
- Updated to 6.4 patchlevel 4.
- Reviewed patches, added some patches from Debian.
- Provides vim-minimal for FC4 compatibility.

* Thu Sep 09 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 6.1.386-owl4
- Patched to build with new autotools.
- Spec prepared for FHS moving.

* Tue Jul 20 2004 Michail Litvak <mci-at-owl.openwall.com> 6.1.386-owl3
- Use sed -i instead of perl.

* Thu Jan 29 2004 Solar Designer <solar-at-owl.openwall.com> 6.1.386-owl2
- Included patch by galaxy@ to resolve a name clash with Perl 5.8.3.

* Sat Mar 15 2003 Michail Litvak <mci-at-owl.openwall.com> 6.1.386-owl1
- Updated to patchlevel 386

* Thu Apr 25 2002 Solar Designer <solar-at-owl.openwall.com>
- vitmp moved from /usr/libexec to /bin and now has a man page.
- Additional temporary file handling fixes to vim and its scripts (but not
the documentation yet).
- Run autoconf in the same way that vim Makefiles would.

* Fri Apr 19 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 6.1 patchlevel 18, reviewing the patches in Rawhide and taking
those pieces which make sense.
- No longer install a second copy of the documentation, refer to the runtime
directory instead.
- Provide a vitmp wrapper, to be used by crontab(1) and edquota(8); this is
to make sure the file is overwritten in-place and no swap files are used.

* Sat Feb 02 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Apr 01 2001 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import php,lilo,nocrv patches from RH
- upgrade to 6.0z
- disable modeline's
- alternative languages disabled

* Mon Feb 19 2001 Solar Designer <solar-at-owl.openwall.com>
- "small" feature set for /bin/vi (+visual).
- Renamed vim-minimal package to vim-small, corrected package descriptions.

* Sat Jan 06 2001 Solar Designer <solar-at-owl.openwall.com>
- Enable mkstemp explicitly, not rely on configure (this will make sense
once vim uses mkstemp for real).

* Fri Dec 15 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- disable gpm

* Fri Dec 15 2000 Solar Designer <solar-at-owl.openwall.com>
- More spec file cleanups (no subshell).

* Mon Dec 11 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- Imported from RH.
- 6.0p
- cleanup

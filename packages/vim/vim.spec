# $Id: Owl/packages/vim/vim.spec,v 1.14 2003/10/30 21:15:49 solar Exp $

%define BUILD_USE_GPM 0
%define BUILD_USE_PYTHON 0
%define BUILD_USE_X 0

Summary: The VIM editor.
Name: vim
%define major 6
%define minor 1
%define alpha %nil
%define patchlevel 386
%define vimdir vim%major%minor%alpha
Version: %major.%minor%{?patchlevel:.%patchlevel}
Release: owl1
License: Charityware
Group: Applications/Editors
Source0: ftp://ftp.vim.org/pub/vim/unix/vim-%major.%minor%alpha.tar.bz2
Source1: vim-%major.%minor-%version.bz2
Source2: vitmp.c
Source3: vitmp.1
Source4: vimrc
Source5: gvim.desktop
Source6: README
Patch0: vim-6.1-rh-owl-vim-not-vi.diff
Patch1: vim-6.1-rh-paths.diff
Patch2: vim-6.1-rh-fix-keys.diff
Patch3: vim-6.1-rh-owl-xxd-locale.diff
Patch4: vim-6.1-rh-owl-spec-syntax.diff
Patch5: vim-6.1-owl-tmp.diff
Requires: mktemp >= 1:1.3.1
BuildRequires: perl
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

%prep
%setup -q -n %vimdir
{
	bzcat %SOURCE1 || touch failed
} | patch -p0
test ! -e failed
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
rm src/auto/configure
install -m 644 $RPM_SOURCE_DIR/README .

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

mv configure configure.save
autoconf
sed -e 's+\./config.log+auto/config.log+' configure > auto/configure
chmod 755 auto/configure
mv -f configure.save configure

%if %BUILD_USE_X
export ac_cv_func_mkstemp=yes \
%configure \
	--with-features=huge \
	--enable-perlinterp --disable-tclinterp \
	--with-x=yes --enable-gui=gnome \
	--exec-prefix=/usr/X11R6 \
	--enable-xim --enable-multibyte \
	--enable-fontset %pythonflag %gpmflag
make VIMRUNTIMEDIR=/usr/share/vim/%vimdir COMPILEDBY=build@%buildhost
mv vim gvim
make clean
%endif

export ac_cv_func_mkstemp=yes \
%configure \
	--prefix=/usr \
	--with-features=huge \
	--enable-perlinterp --disable-tclinterp \
	--with-x=no --enable-gui=no \
	--exec-prefix=/usr --enable-multibyte \
	--enable-fontset %pythonflag %gpmflag
make VIMRUNTIMEDIR=/usr/share/vim/%vimdir COMPILEDBY=build@%buildhost
mv vim vim-enhanced
make clean

export ac_cv_func_mkstemp=yes \
%configure \
	--prefix='${DEST}'/usr \
	--with-features=small \
	--disable-pythoninterp --disable-perlinterp --disable-tclinterp \
	--with-x=no --enable-gui=no \
	--with-tlib=termcap --disable-gpm \
	--exec-prefix=/
make VIMRUNTIMEDIR=/usr/share/vim/%vimdir COMPILEDBY=build@%buildhost

gcc $RPM_OPT_FLAGS -Wall -s $RPM_SOURCE_DIR/vitmp.c -o vitmp

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{/bin,/usr/{bin,share/vim}}
%if %BUILD_USE_X
mkdir -p $RPM_BUILD_ROOT/usr/X11R6/bin
%endif

cd src
%makeinstall BINDIR=/bin DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/bin/xxd $RPM_BUILD_ROOT/usr/bin/
make installmacros DESTDIR=$RPM_BUILD_ROOT
install -m 755 vim-enhanced $RPM_BUILD_ROOT/usr/bin/vim
%if %BUILD_USE_X
install -m 755 gvim $RPM_BUILD_ROOT/usr/X11R6/bin/
%endif

install -m 755 vitmp $RPM_BUILD_ROOT/bin/
install -m 644 $RPM_SOURCE_DIR/vitmp.1 $RPM_BUILD_ROOT%_mandir/man1/

pushd $RPM_BUILD_ROOT
mv bin/vim bin/vi
mv bin/vimtutor usr/bin/
rm bin/rvim
ln -sf vi bin/view
ln -sf vi bin/ex
ln -sf vi bin/rvi
ln -sf vi bin/rview
ln -sf vim usr/bin/ex
ln -sf vim usr/bin/rvim
ln -sf vim usr/bin/vimdiff
perl -pi -e "s,$RPM_BUILD_ROOT,," .%_mandir/man1/{vim,vimtutor}.1
rm .%_mandir/man1/rvim.1
ln -sf vim.1 .%_mandir/man1/vi.1
ln -sf vim.1 .%_mandir/man1/rvi.1
ln -sf vim.1 .%_mandir/man1/rvim.1
ln -sf vim.1 .%_mandir/man1/vimdiff.1

%if %BUILD_USE_X
ln -sf gvim usr/X11R6/bin/vimx
ln -sf gvim usr/X11R6/bin/gview
ln -sf gvim usr/X11R6/bin/gex
ln -sf gvim usr/X11R6/bin/evim
ln -sf vim.1 .%_mandir/man1/gvim.1
ln -sf vim.1 .%_mandir/man1/vimx.1
ln -sf vim.1 .%_mandir/man1/gview.1
ln -sf vim.1 .%_mandir/man1/gex.1
ln -sf vim.1 .%_mandir/man1/evim.1
mkdir -p etc/X11/applnk/Applications
cp $RPM_SOURCE_DIR/gvim.desktop etc/X11/applnk/Applications/
%endif

install -m 644 $RPM_SOURCE_DIR/vimrc usr/share/vim/

# Dependency cleanups
chmod 644 usr/share/vim/%vimdir/{doc/vim2html.pl,tools/{*.pl,vim132}}
popd
chmod 644 ../runtime/doc/vim2html.pl

%files common
%defattr(-,root,root)
%doc README
/usr/bin/xxd
/usr/share/vim
%_mandir/man1/vim.*
%_mandir/man1/vi.*
%_mandir/man1/ex.*
%_mandir/man1/view.*
%_mandir/man1/rvi.*
%_mandir/man1/rview.*
%_mandir/man1/xxd.*

%files small
%defattr(-,root,root)
/bin/vi
/bin/ex
/bin/view
/bin/rvi
/bin/rview
/bin/vitmp
%_mandir/man1/vitmp.*

%files enhanced
%defattr(-,root,root)
/usr/bin/vim
/usr/bin/ex
/usr/bin/vimtutor
%_mandir/man1/vimtutor.*

%if %BUILD_USE_X
%files X11
%defattr(-,root,root)
%config(missingok) /etc/X11/applnk/Applications/gvim.desktop
/usr/X11R6/bin/gvim
/usr/X11R6/bin/vimx
/usr/X11R6/bin/gview
/usr/X11R6/bin/gex
/usr/X11R6/bin/evim
%_mandir/man1/gvim.*
%_mandir/man1/vimx.*
%_mandir/man1/gview.*
%_mandir/man1/gex.*
%_mandir/man1/evim.*
%endif

%changelog
* Sat Mar 15 2003 Michail Litvak <mci@owl.openwall.com> 6.1.386-owl1
- Updated to patchlevel 386

* Thu Apr 25 2002 Solar Designer <solar@owl.openwall.com>
- vitmp moved from /usr/libexec to /bin and now has a man page.
- Additional temporary file handling fixes to vim and its scripts (but not
the documentation yet).
- Run autoconf in the same way that vim Makefiles would.

* Fri Apr 19 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 6.1 patchlevel 18, reviewing the patches in Rawhide and taking
those pieces which make sense.
- No longer install a second copy of the documentation, refer to the runtime
directory instead.
- Provide a vitmp wrapper, to be used by crontab(1) and edquota(8); this is
to make sure the file is overwritten in-place and no swap files are used.

* Sat Feb 02 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Apr 01 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import php,lilo,nocrv patches from RH
- upgrade to 6.0z
- disable modeline's
- alternative languages disabled

* Mon Feb 19 2001 Solar Designer <solar@owl.openwall.com>
- "small" feature set for /bin/vi (+visual).
- Renamed vim-minimal package to vim-small, corrected package descriptions.

* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- Enable mkstemp explicitly, not rely on configure (this will make sense
once vim uses mkstemp for real).

* Fri Dec 15 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- disable gpm

* Fri Dec 15 2000 Solar Designer <solar@owl.openwall.com>
- More spec file cleanups (no subshell).

* Mon Dec 11 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- Imported from RH.
- 6.0p
- cleanup

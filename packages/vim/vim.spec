# $Id: Owl/packages/vim/vim.spec,v 1.8 2002/02/03 00:18:04 solar Exp $

%define alpha z
%define vimversion vim60%{alpha}

%define BUILD_USE_GPM 0
%define BUILD_USE_PYTHON 0
%define BUILD_USE_X 0

Summary: The VIM editor.
Name: vim
Version: 6.0
Release: owl0.26
License: Charityware
Group: Applications/Editors
Source0: ftp://ftp.vim.org/pub/vim/unreleased/unix/vim-%{version}%{alpha}-src.tar.bz2
Source1: ftp://ftp.vim.org/pub/vim/unreleased/unix/vim-%{version}%{alpha}-rt.tar.bz2
Source2: vimrc
Source3: gvim.desktop
Patch0: vim-4.2-rh-speed_t.diff
Patch1: vim-5.1-rh-vimnotvi.diff
Patch2: vim-5.6a-rh-perl-paths.diff
Patch3: vim-6.0-rh-fixkeys.diff
Patch4: vim-6.0-rh-specsyntax.diff
Patch5: vim-6.0r-rh-nocrv.diff
Patch6: vim-6.0t-rh-phphighlight.diff
Patch7: vim-6.0v-rh-lilo.diff
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
BuildRoot: /override/%{name}-%{version}

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
%setup -q -b 1 -n %{vimversion}
%patch0 -p1
%patch1 -p1
# fix rogue dependencies from sample code
chmod -x runtime/tools/mve.awk
%patch2 -p1
find . -name '*.paths' -print0 | xargs -r0 rm -f --
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
perl -pi -e 's,bin/nawk,bin/awk,g' runtime/tools/mve.awk

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
perl -pi -e "s,\\\$VIMRUNTIME,/usr/share/vim/%{vimversion},g" os_unix.h
perl -pi -e "s,\\\$VIM,/usr/share/vim/%{vimversion}/macros,g" os_unix.h

%if %BUILD_USE_X
export ac_cv_func_mkstemp=yes \
%configure \
	--with-features=huge \
	--enable-perlinterp --disable-tclinterp \
	--with-x=yes --enable-gui=gnome \
	--exec-prefix=/usr/X11R6 \
	--enable-xim --enable-multibyte \
	--enable-fontset %{pythonflag} %{gpmflag}
make
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
	--enable-fontset %{pythonflag} %{gpmflag}
make
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
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/bin
mkdir -p $RPM_BUILD_ROOT/usr/{bin,share/vim}
%if %BUILD_USE_X
mkdir -p $RPM_BUILD_ROOT/usr/X11R6/bin
%endif

cd src
%makeinstall BINDIR=$RPM_BUILD_ROOT/bin DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/bin/xxd $RPM_BUILD_ROOT/usr/bin/
make installmacros DESTDIR=$RPM_BUILD_ROOT
install -s -m 755 vim-enhanced $RPM_BUILD_ROOT/usr/bin/vim
%if %BUILD_USE_X
install -s -m 755 gvim $RPM_BUILD_ROOT/usr/X11R6/bin/
%endif

pushd $RPM_BUILD_ROOT
mv bin/vim bin/vi
rm bin/rvim
ln -sf vi bin/view
ln -sf vi bin/ex
ln -sf vi bin/rvi
ln -sf vi bin/rview
ln -sf vim usr/bin/ex
perl -pi -e "s,$RPM_BUILD_ROOT,," .%{_mandir}/man1/{vim,vimtutor}.1
rm .%{_mandir}/man1/rvim.1
ln -sf vim.1 .%{_mandir}/man1/vi.1
ln -sf vim.1 .%{_mandir}/man1/rvi.1

%if %BUILD_USE_X
ln -sf gvim usr/X11R6/bin/vimx
ln -sf vim.1 .%{_mandir}/man1/gvim.1
ln -sf vim.1 .%{_mandir}/man1/vimx.1
mkdir -p etc/X11/applnk/Utilities
cp $RPM_SOURCE_DIR/gvim.desktop etc/X11/applnk/Utilities/
%endif

install -m 644 $RPM_SOURCE_DIR/vimrc usr/share/vim/%{vimversion}/macros/
ln -s vimrc usr/share/vim/%{vimversion}/macros/gvimrc

# Dependency cleanups
chmod 644 $RPM_BUILD_ROOT/usr/share/vim/%{vimversion}/doc/vim2html.pl \
	$RPM_BUILD_ROOT/usr/share/vim/%{vimversion}/tools/{*.pl,vim132}
popd
chmod 644 ../runtime/doc/vim2html.pl

%clean
rm -rf $RPM_BUILD_ROOT

%files common
%defattr(-,root,root)
%doc README*.txt runtime/macros/README.txt runtime/tools/README.txt
%doc runtime/doc runtime/syntax runtime/termcap runtime/tutor
%doc runtime/*.vim
/bin/vimtutor
/usr/bin/xxd

/usr/share/vim
%{_mandir}/man1/vim.*
%{_mandir}/man1/vimtutor.*
%{_mandir}/man1/ex.*
%{_mandir}/man1/vi.*
%{_mandir}/man1/view.*
%{_mandir}/man1/rvi.*
%{_mandir}/man1/rview.*
%{_mandir}/man1/xxd.*

%files small
%defattr(-,root,root)
/bin/ex
/bin/vi
/bin/view
/bin/rvi
/bin/rview

%files enhanced
%defattr(-,root,root)
/usr/bin/vim
/usr/bin/ex

%if %BUILD_USE_X
%files X11
%defattr(-,root,root)
%config(missingok) /etc/X11/applnk/Utilities/gvim.desktop
/usr/X11R6/bin/gvim
/usr/X11R6/bin/vimx
%{_mandir}/man1/gvim.*
%{_mandir}/man1/vimx.*
%endif

%changelog
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

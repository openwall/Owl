# $Id: Owl/packages/vim/vim.spec,v 1.6 2001/02/19 08:54:03 solar Exp $

%define vimversion vim60p

%define NEED_PYTHON 	'no'
%define NEED_GPM 	'no'
%define NEED_X11	'no'


%if "%{NEED_PYTHON}"=="'yes'"
%define	pythonflag --enable-pythoninterp
%else
%define pythonflag --disable-pythoninterp
%endif
%if "%{NEED_GPM}"=="'yes'"
%define	gpmflag --enable-gpm
%else
%define	gpmflag --disable-gpm
%endif


Summary: 	The VIM editor.
Name: 		vim
Version: 	6.0
Release: 	0.19owl
Copyright: 	freeware
Group: 		Applications/Editors
Source0: 	ftp://ftp.vim.org/pub/vim/unreleased/unix/vim-%{version}p-src.tar.gz
Source1: 	ftp://ftp.vim.org/pub/vim/unreleased/unix/vim-%{version}p-rt.tar.gz
Source2: 	gvim.desktop
Source3: 	vimrc
Patch0: 	vim-4.2-rh-speed_t.diff
Patch1: 	vim-5.1-rh-vimnotvi.diff
Patch2: 	vim-5.6a-rh-perl-paths.diff
Patch3: 	vim-6.0-rh-fixkeys.diff
Patch4: 	vim-6.0-rh-specsyntax.diff
Buildroot: 	/var/rpm-buildroot/%{name}-root
Buildrequires: 	perl
%if "%{NEED_GPM}"=="'yes'"
Buildrequires: 	gpm-devel
%endif
%if "%{NEED_PYTHON}"=="'yes'"
Buildrequires: 	python-devel
%endif
%if "%{NEED_X11}"=="'yes'"
Buildrequires: 	gtk+-devel
%endif

%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.

%package common
Summary: The common files needed by any version of the VIM editor.
Group: Applications/Editors

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-common package contains files which every VIM binary will need in
order to run.

If you are installing any version of the VIM editor, you'll also need
to have the vim-common package installed.

%package small
Summary: A small version of the VIM editor.
Group: Applications/Editors
Requires: vim-common
Obsoletes: vim, vim-minimal

%description small
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more. The
vim-small package includes a small version of VIM, which is installed
into /bin/vi for use when only the root partition is present.

%package enhanced
Summary: A feature-rich version of the VIM editor.
Group: Applications/Editors
Requires: vim-common
Obsoletes: vim-color

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-enhanced package contains a version of VIM with all its features
compiled in.

%if "%{NEED_X11}"=="'yes'"
%package X11
Summary: The VIM version of the vi editor for the X Window System.
Group: Applications/Editors
Requires: vim-common

%description X11
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.
VIM-X11 is a version of the VIM editor which will run within the
X Window System.  If you install this package, you can run VIM as an X
application with a full GUI interface and mouse support.

Install the vim-X11 package if you'd like to try out a version of vi
with graphics and mouse capabilities.  You'll also need to install the
vim-common package.
%endif

%prep
%setup -q -b 1 -n %{vimversion}
%patch0 -p1 -b .4.2
%patch1 -p1 -b .vim
# fix rogue dependencies from sample code
chmod -x runtime/tools/mve.awk
%patch2 -p1 -b .paths
find . -name \*.paths | xargs rm -f
%patch3 -p1 -b .fixkeys
%patch4 -p1 -b .highlite
perl -pi -e "s,bin/nawk,bin/awk,g" runtime/tools/mve.awk

%build
cd src
perl -pi -e "s,\\\$VIMRUNTIME,/usr/share/vim/%{vimversion},g" os_unix.h
perl -pi -e "s,\\\$VIM,/usr/share/vim/%{vimversion}/macros,g" os_unix.h

%if "%{NEED_X11}"=="'yes'"
export ac_cv_func_mkstemp=yes \
%configure \
	--with-features=huge \
	--enable-perlinterp --disable-tclinterp \
	--with-x=yes --enable-gui=gnome \
	--exec-prefix=/usr/X11R6 \
	--enable-xim --enable-multibyte %{pythonflag} %{gpmflag}
make
cp vim gvim
make clean
%endif

export ac_cv_func_mkstemp=yes \
%configure \
	--prefix=/usr \
	--with-features=huge \
	--enable-perlinterp --disable-tclinterp \
	--with-x=no --enable-gui=no \
	--exec-prefix=/usr --enable-multibyte  %{pythonflag} %{gpmflag}
make
cp vim enhanced-vim
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
%if "%{NEED_X11}"=="'yes'"
mkdir -p $RPM_BUILD_ROOT/usr/
%endif

cd src
%makeinstall BINDIR=$RPM_BUILD_ROOT/bin DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/bin/xxd $RPM_BUILD_ROOT/usr/bin
make installmacros DESTDIR=$RPM_BUILD_ROOT
install -s -m 755 enhanced-vim $RPM_BUILD_ROOT/usr/bin/vim
%if "%{NEED_X11}"=="'yes'"
install -s -m 755 gvim $RPM_BUILD_ROOT/usr/X11R6/bin
%endif

pushd $RPM_BUILD_ROOT
mv ./bin/vim ./bin/vi
rm -f ./bin/rvim
ln -sf vi ./bin/view
ln -sf vi ./bin/ex
ln -sf vi ./bin/rvi
ln -sf vi ./bin/rview
ln -sf vim ./usr/bin/ex
perl -pi -e "s,$RPM_BUILD_ROOT,," \
	.%{_mandir}/man1/vim.1 .%{_mandir}/man1/vimtutor.1
rm -f .%{_mandir}/man1/rvim.1
ln -sf vim.1.gz .%{_mandir}/man1/vi.1.gz
ln -sf vim.1.gz .%{_mandir}/man1/rvi.1.gz
%if "%{NEED_X11}"=="'yes'"
ln -sf vim.1.gz .%{_mandir}/man1/gvim.1.gz
ln -sf gvim ./usr/X11R6/bin/vimx
mkdir -p ./etc/X11/applnk/Utilities
cp %{SOURCE2} ./etc/X11/applnk/Utilities/gvim.desktop
%endif
install -s -m 644 %{SOURCE3} ./usr/share/vim/%{vimversion}/macros/
ln -s vimrc ./usr/share/vim/%{vimversion}/macros/gvimrc
# Dependency cleanups
chmod 644 ./usr/share/vim/%{vimversion}/doc/vim2html.pl \
	./usr/share/vim/%{vimversion}/tools/*.pl \
	./usr/share/vim/%{vimversion}/tools/vim132
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

%if "%{NEED_X11}"=="'yes'"
%files X11
%defattr(-,root,root)
%config(missingok) /etc/X11/applnk/Utilities/gvim.desktop
/usr/X11R6/bin/gvim
/usr/X11R6/bin/vimx
%{_mandir}/man1/gvim.*
%endif

%changelog
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
- 6.0p
- cleanup

* Mon Oct 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 6.0k

* Tue Oct 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 6.0i
- add new desktop file w/ translations

* Thu Aug 31 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 6.0h

* Wed Aug 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 6.0g

* Mon Aug 14 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 6.0f

* Wed Aug  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 6.0e

* Sun Jul 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 6.0c
- get rid of the DESTDIR patch, no longer needed

* Sun Jul 16 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 6.0b

* Mon Jul 10 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 6.0a

* Sun Jun 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.7 release
- some more fixes to .spec file syntax highlighting rules... About time it
  recognizes %%{_mandir}...

* Sun Jun 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.7a

* Sat Jun  3 2000 Bernhard Rosenkränzer <bero@redhat.com>
- patchlevel 74
- add %%makeinstall macro recognition to .spec file syntax highlighting rules
- fix up Makefiles

* Fri Apr 14 2000 Bernhard Rosenkränzer <bero@redhat.com>
- patchlevel 66
- fix compilation with perl 5.6.0

* Mon Mar 20 2000 Bernhard Rosenkränzer <bero@redhat.com>
- patchlevel 12

* Tue Mar 07 2000 Preston Brown <pbrown@redhat.com>
- fix home/end in vimrc (we did a term = rxvt, totally wrong)

* Tue Feb 29 2000 Preston Brown <pbrown@redhat.com>
- change F1-F4 keybindings for xterm builtin terminfo to match real terminfo

* Thu Feb 17 2000 Bill Nottingham <notting@redhat.com>
- kill autoindent

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Sat Feb  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Patchlevel 11
- handle compressed man pages
- fix man page symlinks

* Wed Feb  2 2000 Bill Nottingham <notting@redhat.com>
- eliminate dependencies on X in vim-enhanced, and ncurses/gpm
  in vim-minimal

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- eliminate dependencies on csh and perl in vim-common

* Wed Jan 19 2000 Bernhard Rosenrkänzer <bero@redhat.com>
- Use awk, not nawk

* Tue Jan 18 2000 Bernhard Rosenrkänzer <bero@redhat.com>
- 5.6
- patch 5.6.001
- remove /usr/bin/vi - if you want vim, type vim

* Tue Jan 11 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 5.6a
- Remove dependency on nawk (introduced by base update)
- some tweaks to make updating easier

* Tue Nov  9 1999 Bernhard Rosenkränzer <bero@redhat.com>
- 5.5
- fix path to vimrc

* Tue Jul 27 1999 Michael K. Johnson <johnsonm@redhat.com>
- moved from athena to gtk widgets for X version
- removed vim.1 from X11 filelist because X11 depends on vim-common anyway
- fixed rogue dependencies from sample files

* Tue Jul 27 1999 Jeff Johnson <jbj@redhat.com>
- update to 5.4.

* Thu Jul 22 1999 Jeff Johnson <jbj@redhat.com>
- man page had buildroot pollution (#3629).

* Thu Mar 25 1999 Preston Brown <pbrown@redhat.com>
- with recent termcap/terminfo fixes, regular vim works in xterm/console
- in color, so vim-color package removed.

* Tue Mar 23 1999 Erik Troan <ewt@redhat.com>
- removed "set backupdir=/tmp/vim_backup" from default vimrc

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 5)

* Thu Dec 17 1998 Michael Maher <mike@redaht.com>
- built pacakge for 6.0

* Tue Sep 15 1998 Michael Maher <mike@redhat.com>
- removed '--with-tlib=termcap' so that color-vim works

* Wed Sep  2 1998 Jeff Johnson <jbj@redhat.com>
- update to 5.3.

* Mon Aug 10 1998 Jeff Johnson <jbj@redhat.com>
- merge in Toshio's changes
- color-vim: changed "--disable-p" to "--disable-perlinterp --with-tlib=termcap"
- added minimal rvi/rview and man pages.
- move Obsoletes to same package as executable.

* Thu Aug 06 1998 Toshio Kuratomi <badger@prtr-13.ucsc.edu>
- Break the package apart similar to the way the netscape package was
  broken down to handle navigator or communicator: The vim package is
  Obsolete, now there is vim-common with all the common files, and a
  package for each binary: vim-minimal (has /bin/vi compiled with no
  frills), vim-enhanced (has /usr/bin/vim with extra perl and python
  interpreters), and vim-X11 (has /usr/X11R6/bin/gvim compiled with
  GUI support.)
- Enable the perl and python interpreters in the gui version (gvim).

* Tue Jun 30 1998 Michael Maher <mike@redhat.com>
- Fixed tutor help.
- cvim package added.  Thanks to Stevie Wills for finding this one :-)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri May 01 1998 Donnie Barnes <djb@redhat.com>
- added patch to turn off the "vi compatibility" by default.  You can
  still get it via the -C command line option

* Thu Apr 23 1998 Donnie Barnes <djb@redhat.com>
- removed perl and python interpreters (sorry, but those don't belong
  in a /bin/vi and having two vi's seemed like overkill...complain
  to suggest@redhat.com if you care)

* Fri Apr 17 1998 Donnie Barnes <djb@redhat.com>
- fixed buildroot bug

* Sat Apr 11 1998 Donnie Barnes <djb@redhat.com>
- updated from 4.6 to 5.1
- moved to buildroot

* Sun Nov 09 1997 Donnie Barnes <djb@redhat.com>
- fixed missing man page

* Wed Oct 22 1997 Donnie Barnes <djb@redhat.com>
- added wmconfig entry to vim-X11

* Mon Oct 20 1997 Donnie Barnes <djb@redhat.com>
- upgraded from 4.5 to 4.6

* Fri Jun 13 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Mar 25 1997 Michael K. Johnson <johnsonm@redhat.com>
- Upgraded to 4.5
- Added ex symlinks

* Tue Mar 11 1997 Michael K. Johnson <johnsonm@redhat.com>
- Added view symlink.

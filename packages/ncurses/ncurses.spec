# $Owl: Owl/packages/ncurses/ncurses.spec,v 1.37 2010/10/15 20:22:55 segoon Exp $

%define major 5
%define oldmajor 4

%define patchlevel 20101009

%define BUILD_CXX 0
%define BUILD_GPM 0

Summary: A CRT screen handling and optimization package.
Name: ncurses
Version: 5.7
Release: owl3
License: distributable
Group: System Environment/Libraries
URL: http://dickey.his.com/ncurses/ncurses.html
Source0: %name-%version-%patchlevel.tar.xz
# ftp://invisible-island.net/%name/%name-%version.tar.gz
# ftp://ftp.gnu.org/gnu/%name/%name-%version.tar.gz
# Signature: ftp://invisible-island.net/%name/%name-%version.tar.gz.sig
Source1: ncurses-linux
Source2: ncurses-linux-m
Source3: ncurses-resetall.sh
Patch0: ncurses-5.7-owl-glibc-enable_secure.diff
Patch1: ncurses-5.7-owl-warnings.diff
PreReq: /sbin/ldconfig
BuildRoot: /override/%name-%version

%description
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4BSD classic curses library.

%package devel
Summary: The development files for applications which use ncurses.
Group: Development/Libraries
Requires: %name = %version-%release
AutoReq: false

%description devel
The header files and libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

%ifnarch x86_64
%package compat
Summary: ncurses compatibility for ncurses 4.x
Group: System Environment/Libraries
Requires: %name = %version-%release
Provides: libform.so.%oldmajor, libmenu.so.%oldmajor
Provides: libncurses.so.%oldmajor, libpanel.so.%oldmajor

%description compat
This ncurses package provides compatibility libraries for packages
built against Red Hat Linux 6.2.
%endif

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%prep
%setup -q -n %name-%version-%patchlevel
rm -r doc/html/ada
%patch0 -p1
%patch1 -p1
bzip2 -9k NEWS

%build
export ac_cv_func_mkstemp=yes \
%configure \
	--program-transform-name= \
	--with-normal \
	--with-shared \
	--without-debug \
	--without-profile \
%if %BUILD_CXX
	--with-cxx \
%else
	--without-cxx \
%endif
	--without-ada \
	--disable-root-environ \
	--with-ospeed=speed_t \
	--with-termlib \
%if %BUILD_GPM
	--with-gpm \
%else
	--without-gpm \
%endif
	--enable-symlinks \
	--with-manpage-format=normal \
	--with-manpage-aliases \
	--without-manpage-symlinks \
	--enable-const \
	--enable-hard-tabs \
	--enable-no-padding \
	--enable-sigwinch \
	--enable-echo \
	--enable-warnings \
	--disable-termcap \
	--disable-rpath
%__make

%if %BUILD_CXX
# Build C++ shared library
pushd lib
g++ -shared -Wl,-soname,libncurses++.so.5 -o libncurses++.so.%version \
	-Wl,-whole-archive libncurses++.a -Wl,-no-whole-archive \
	-L. -lform -lmenu -lpanel -lncurses -ltinfo
popd

# Build C++ demonstration program
rm -f c++/demo
%__make -C c++
%endif

%install
rm -rf %buildroot
mkdir -p %buildroot%_prefix/lib
%makeinstall \
	includedir=%buildroot%_includedir/%name \
	ticdir=%buildroot%_datadir/terminfo

ln -s ../l/linux %buildroot%_datadir/terminfo/c/console
ln -s ncurses/curses.h %buildroot%_includedir/ncurses.h
for I in curses unctrl eti form menu panel term; do
	ln -s ncurses/$I.h %buildroot%_includedir/$I.h
done

%ifarch sparc sparcv9 sparc64
# XXX (GM): Warning: I cannot test if this block is necessary for current
# version of ncurses.
install -m 644 %_sourcedir/ncurses-linux \
	%buildroot%_datadir/terminfo/l/linux
install -m 644 %_sourcedir/ncurses-linux-m \
	%buildroot%_datadir/terminfo/l/linux-m
%endif

%if %BUILD_CXX
# Install C++ shared library
install -p -m 755 lib/libncurses++.so.%version %buildroot%_libdir/
ln -s libncurses++.so.%version %buildroot%_libdir/libncurses++.so.5
ln -s libncurses++.so.5 %buildroot%_libdir/libncurses++.so

# Prepare C++ doc directory
mkdir -p rpm-doc/c++
install -p -m 644 c++/{NEWS,PROBLEMS,README-first} rpm-doc/c++/
%endif

# the resetall script
install -m 755 %_sourcedir/ncurses-resetall.sh \
	%buildroot%_bindir/resetall

%ifnarch x86_64
# compat links
ln -s libform.so.%version %buildroot%_libdir/libform.so.%oldmajor
ln -s libmenu.so.%version %buildroot%_libdir/libmenu.so.%oldmajor
ln -s libncurses.so.%version %buildroot%_libdir/libncurses.so.%oldmajor
ln -s libpanel.so.%version %buildroot%_libdir/libpanel.so.%oldmajor
%endif

# remove terminfo entries for screen, since the screen package provides
# more recent versions
rm %buildroot%_datadir/terminfo/s/screen{,-bce,-s}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(755,root,root) %_libdir/lib*.so.%{major}*
%doc ANNOUNCE NEWS.bz2 README TO-DO
%doc doc/html/announce.html
%if %BUILD_CXX
%doc rpm-doc/c++
%endif
%_datadir/terminfo
%_datadir/tabset
%_bindir/*
%_mandir/man1/*
%_mandir/man5/*
%_mandir/man7/*
%_prefix/lib/terminfo

%files devel
%defattr(-,root,root)
%doc doc/html/{hackguide,ncurses-intro}.html
%doc AUTHORS
%if %BUILD_CXX
%doc c++/demo.cc
%endif
%_libdir/lib*.so
%_libdir/lib*.a
%_includedir/*
%_mandir/man3/*

%ifnarch x86_64
%files compat
%defattr(-,root,root)
%_libdir/lib*.so.%{oldmajor}*
%endif

%changelog
* Fri Oct 15 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 5.7-owl3
- Updated to 5.7-20101009.

* Fri Oct 15 2010 Solar Designer <solar-at-owl.openwall.com> 5.7-owl2
- Dropped the erroneous owl-fixes patch (TermType is a pointer, not an array).
- Corrected oldmajor (it was broken with the previous change, which was never
made public).
- Use xz-compressed Source tarball.

* Mon Oct 11 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 5.7-owl1
- Updated to 5.7.
- Updated owl-fixes and owl-glibc-enable_secure patches.
- Fixed compiler warnings.
- Packaged AUTHORS file.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.4-owl3
- Compressed NEWS file.

* Fri May 14 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 5.4-owl2
- Fixed inconsistency when dealing with compat symlinks.
- Removed entries for the screen package from the database.

* Fri May 14 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 5.4-owl1
- Updated patch-set from official site
- Added %_libdir/terminfo symbolic link into filelist

* Wed Mar 17 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 5.4-owl0.3
- Removed unneeded libraries strip -- it will be done by brp- scripts
- Fixed packaging problem for c++ documentation

* Wed Mar 10 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 5.4-owl0.2
- turned off building of C++ library by default.
- turned off linking with gpm by default (we need to review Makefiles to
link this library only where needed, but not to every binary we build).

* Fri Mar 05 2004 Michail Litvak <mci-at-owl.openwall.com> 5.4-owl0.1
- 5.4
- 20040214 + 20040221 + 20040228 patches

* Wed Jan 28 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 5.3-owl0.1
- Cleaned up the spec file (removed unneeded macros)

* Tue Jan 20 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 5.3-owl0
- Updated to the 5.3 version with 20040117 patch
- Cleaned up the spec (by using macros)
- Dropped rh-typo and rh-tput-S patches (already in upstream)
- owl-fixes patch shrinked (all previous owl-fixes already in upstream)

* Wed Oct 29 2003 Solar Designer <solar-at-owl.openwall.com> 5.2-owl10
- Don't keep ESC characters in resetall script source, use echo -e instead.
- Eliminated unneeded curly braces with RPM macros and dropped %clean.

* Wed Feb 06 2002 Michail Litvak <mci-at-owl.openwall.com> 5.2-owl9
- Enforce our new spec file conventions

* Mon Jun 25 2001 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- fix tput -S bug. (RH#44669)

* Fri Jan 26 2001 Solar Designer <solar-at-owl.openwall.com>
- Patch a typo in curs_deleteln(3X).

* Sat Jan 06 2001 Solar Designer <solar-at-owl.openwall.com>
- Enable mkstemp explicitly, not rely on configure.

* Sun Dec 24 2000 Solar Designer <solar-at-owl.openwall.com>
- Autoreq: false for the -devel package to install before perl.

* Sun Dec 10 2000 Solar Designer <solar-at-owl.openwall.com>
- Removed the last remaining RH (security) patch which is now redundant
and had a race, anyway.

* Wed Nov 08 2000 Solar Designer <solar-at-owl.openwall.com>
- ncurses-5.2-20001104 patch which adds --with-ospeed and bugfixes.
- --with-ospeed=speed_t for compatibility with libtermcap.
- optflags_lib support.
- %%defattr(-,root,root) for the compat package.

* Mon Nov 06 2000 Solar Designer <solar-at-owl.openwall.com>
- --disable-root-environ to enable the recent security fixes.
- Added a patch to use glibc's __libc_enable_secure.
- Added a patch to fix potential problems found during a mini-audit.

* Sat Nov 04 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- new compat

* Wed Oct 25 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- ncurses 5.2 and compat.

* Sun Oct 15 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import 5.1 from RH rawhide

# $Id: Owl/packages/ncurses/ncurses.spec,v 1.15 2002/02/06 18:10:41 mci Exp $

%define major 5
%define oldmajor 4

Summary: A CRT screen handling and optimization package.
Name: ncurses
Version: 5.2
Release: owl8.1
License: distributable
Group: System Environment/Libraries
URL: http://dickey.his.com/ncurses/ncurses.html
Source0: ftp://dickey.his.com/ncurses/ncurses-%{version}.tar.gz
Source1: ncurses-linux
Source2: ncurses-linux-m
Source3: ncurses-resetall.sh
Patch0: ftp://dickey.his.com/ncurses/5.2/ncurses-5.2-20001028.patch.gz
Patch1: ftp://dickey.his.com/ncurses/5.2/ncurses-5.2-20001104.patch.gz
Patch2: ncurses-5.2-owl-glibc-enable_secure.diff
Patch3: ncurses-5.2-owl-fixes.diff
Patch4: ncurses-5.2-rh-typo.diff
Patch5: ncurses-5.2-rh-tput-S.diff
BuildRoot: /override/%{name}-%{version}

%description
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4BSD classic curses library.

%package devel
Summary: The development files for applications which use ncurses.
Group: Development/Libraries
AutoReq: false
Requires: ncurses = %{PACKAGE_VERSION}

%description devel
The header files and libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

%package compat
Summary: ncurses compatibility for ncurses 4.x
Group: System Environment/Libraries
Requires: ncurses = %{PACKAGE_VERSION}
Provides: libform.so.%{oldmajor}, libmenu.so.%{oldmajor}
Provides: libncurses.so.%{oldmajor}, libpanel.so.%{oldmajor}

%description compat
This ncurses package provides compatibility libraries for packages
built against Red Hat Linux 6.2.

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%prep
%setup -q -n ncurses-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
CFLAGS="%{optflags} -DPURE_TERMINFO"
%define optflags $CFLAGS
export ac_cv_func_mkstemp=yes \
%configure \
	--with-normal --with-shared --without-debug --without-profile \
	--without-cxx --without-ada \
	--disable-root-environ --with-ospeed=speed_t
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall includedir=$RPM_BUILD_ROOT/usr/include/ncurses \
	ticdir=$RPM_BUILD_ROOT/usr/share/terminfo
ln -s ../l/linux $RPM_BUILD_ROOT/usr/share/terminfo/c/console
ln -s ncurses/curses.h $RPM_BUILD_ROOT/usr/include/ncurses.h
for I in curses unctrl eti form menu panel term ; do
	ln -sf ncurses/$I.h $RPM_BUILD_ROOT/usr/include/$I.h
done

%ifarch sparc sparcv9 sparc64
install -c -m 644 $RPM_SOURCE_DIR/ncurses-linux \
	$RPM_BUILD_ROOT/usr/share/terminfo/l/linux
install -c -m 644 $RPM_SOURCE_DIR/ncurses-linux-m \
	$RPM_BUILD_ROOT/usr/share/terminfo/l/linux-m
%endif

strip -R .comment --strip-unneeded $RPM_BUILD_ROOT/usr/lib/*.so.[0-9].*
make clean -C test

# the resetall script
install -c -m 755 $RPM_SOURCE_DIR/ncurses-resetall.sh \
	$RPM_BUILD_ROOT/usr/bin/resetall

# compat links
ln -s libform.so.%{version} $RPM_BUILD_ROOT/usr/lib/libform.so.%{oldmajor}
ln -s libmenu.so.%{version} $RPM_BUILD_ROOT/usr/lib/libmenu.so.%{oldmajor}
ln -s libncurses.so.%{version} $RPM_BUILD_ROOT/usr/lib/libncurses.so.%{oldmajor}
ln -s libpanel.so.%{version} $RPM_BUILD_ROOT/usr/lib/libpanel.so.%{oldmajor}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(755,root,root) /usr/lib/lib*.so.%{major}*
%doc README ANNOUNCE 
%doc doc/html/announce.html
%{_datadir}/terminfo
%{_datadir}/tabset
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files devel
%defattr(-,root,root)
%doc c++ test
%doc doc/html/hackguide.html
%doc doc/html/ncurses-intro.html
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_includedir}/*
%{_mandir}/man3/*

%files compat
%defattr(-,root,root)
/usr/lib/lib*.so.%{oldmajor}*

%changelog
* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Mon Jun 25 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- fix tput -S bug. (RH#44669)

* Fri Jan 26 2001 Solar Designer <solar@owl.openwall.com>
- Patch a typo in curs_deleteln(3X).

* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- Enable mkstemp explicitly, not rely on configure.

* Sun Dec 24 2000 Solar Designer <solar@owl.openwall.com>
- Autoreq: false for the -devel package to install before perl.

* Sun Dec 10 2000 Solar Designer <solar@owl.openwall.com>
- Removed the last remaining RH (security) patch which is now redundant
and had a race, anyway.

* Wed Nov 08 2000 Solar Designer <solar@owl.openwall.com>
- ncurses-5.2-20001104 patch which adds --with-ospeed and bugfixes.
- --with-ospeed=speed_t for compatibility with libtermcap.
- optflags_lib support.
- %defattr(-,root,root) for the compat package.

* Mon Nov 06 2000 Solar Designer <solar@owl.openwall.com>
- --disable-root-environ to enable the recent security fixes.
- Added a patch to use glibc's __libc_enable_secure.
- Added a patch to fix potential problems found during a mini-audit.

* Sat Nov 04 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- new compat 

* Wed Oct 25 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- ncurses 5.2 and compat.

* Sun Oct 15 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import 5.1 from RH rawhide

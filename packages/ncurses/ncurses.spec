# $Id: Owl/packages/ncurses/ncurses.spec,v 1.3 2000/11/04 08:19:42 kad Exp $

%define 	major		5
%define 	oldmajor	4

Summary: 	A CRT screen handling and optimization package.
Name: 		ncurses
Version: 	5.2
Release: 	2owl
Copyright: 	distributable
Group: 		System Environment/Libraries
URL: 		http://dickey.his.com/ncurses/ncurses.html
Source0: 	ftp://dickey.his.com/ncurses/ncurses-%{version}.tar.gz
Source2: 	ncurses-linux
Source3: 	ncurses-linux-m
Source4: 	ncurses-resetall.sh
Patch0:		ncurses-5.0-rh-setuid2.diff
BuildRoot: 	/var/rpm-buildroot/%{name}-root

%description
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4BSD classic curses library.


%package devel
Summary: The development files for applications which use ncurses.
Group: Development/Libraries
Requires: ncurses = %{PACKAGE_VERSION}

%description devel
The header files and libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.


%package compat
Summary: Ncurses compatibility for ncurses 4.x
Group: System Environment/Libraries
Requires: ncurses = %{PACKAGE_VERSION}
Provides: libform.so.%{oldmajor} libmenu.so.%{oldmajor} libncurses.so.%{oldmajor} libpanel.so.%{oldmajor}

%description compat
This ncurses package provides compatiblity libaries for packages
built against Red Hat Linux 6.2.

%prep
%setup -q -n ncurses-%{version}
%patch0 -p1
find . -name "*.orig" -exec rm -f {} \;

%build
CFLAGS="%{optflags} -DPURE_TERMINFO"
%define optflags $CFLAGS
%configure \
	--with-normal --with-shared --without-debug --without-profile \
	--without-cxx --without-ada
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall includedir=$RPM_BUILD_ROOT/usr/include/ncurses ticdir=$RPM_BUILD_ROOT/usr/share/terminfo
ln -s ../l/linux $RPM_BUILD_ROOT/usr/share/terminfo/c/console
ln -s ncurses/curses.h $RPM_BUILD_ROOT/usr/include/ncurses.h
for I in curses unctrl eti form menu panel term; do
	ln -sf ncurses/$I.h $RPM_BUILD_ROOT/usr/include/$I.h
done

%ifarch sparc
install -c -m644 %SOURCE2 $RPM_BUILD_ROOT/usr/share/terminfo/l/linux
install -c -m644 %SOURCE3 $RPM_BUILD_ROOT/usr/share/terminfo/l/linux-m
%endif

strip -R .comment $RPM_BUILD_ROOT/usr/bin/* || :
strip -R .comment --strip-unneeded $RPM_BUILD_ROOT/usr/lib/*.so.[0-9].*
make clean -C test

# the resetall script
install -c -m 755 %{SOURCE4} $RPM_BUILD_ROOT/usr/bin/resetall

# comapt links
ln -s libform.so.%{version} $RPM_BUILD_ROOT/usr/lib/libform.so.%{oldmajor}
ln -s libmenu.so.%{version} $RPM_BUILD_ROOT/usr/lib/libmenu.so.%{oldmajor}
ln -s libncurses.so.%{version} $RPM_BUILD_ROOT/usr/lib/libncurses.so.%{oldmajor}
ln -s libpanel.so.%{version} $RPM_BUILD_ROOT/usr/lib/libpanel.so.%{oldmajor}

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
/usr/lib/lib*.so.%{oldmajor}*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Nov  4 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- new compat 

* Wed Oct 25 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- ncurses 5.2 and compat.

* Sun Oct 15 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import 5.1 from RH rawhide

* Mon Oct  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update (fixes the "make menuconfig" bug introduced by the security fix)

* Tue Oct  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix security problem (possible buffer overrun)

* Fri Aug  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add the bugfix patches from the ncurses maintainer

* Thu Jul 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.1

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Matt Wilson <msw@redhat.com>
- *don't ship symlinks from lib*.so.5 to lib*.so.4!
- use FHS macros

* Fri Jun  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild for 7.0
- /usr/share/man
- update URL for patches
- misc. fixes to spec file

* Mon Mar 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- use the real library version number
- update to 20000319

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Fri Feb 18 2000 Preston Brown <pbrown@redhat.com>
- xterm terminfo entries from XFree86 3.3.6
- final round of xterm fixes, follow debian policy.

* Sat Feb  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- strip libraries

* Thu Feb  3 2000 Bernhard Rosenkränzer <bero@redhat.com>
- More xterm fixes (Bug #9087)

* Thu Jan 27 2000 Bernhard Rosenkränzer <bero@redhat.com>
- More xterm fixes from Hans de Goede (Bug #8633)

* Sat Jan 15 2000 Bernhard Rosenkränzer <bero@redhat.com>
- remove some broken symlinks (leftovers from libncurses.so.5)
- Use %configure (Bug #8484)

* Tue Jan 11 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Add xterm patch from Hans de Goede <hans@highrise.nl>
- Patch 20000108, this fixes a problem with a header file.

* Wed Jan  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Add 20000101 patch, hopefully finally fixing the xterm description

* Wed Dec 22 1999 Cristian Gafton <gafton@redhat.com>
- revert to the old major number - because the ABI is not changed (and we
  should be handling the changes via symbol versioning anyway)

* Fri Nov 12 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix a typo in spec
- Add the 19991006 patch, fixing some C++ STL compatibility problems.
- get rid of profiling and debugging versions - we need to save space...

* Thu Nov  4 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.0
- some spec cleanups to make updating easier
- add links *.so.5 to *.so.4 - they are fully binary compatible.
  (Why did they change the invocation number???)

* Wed Sep 22 1999 Cristian Gafton <gafton@redhat.com>
- make clean in the test dir - don't ship any binaries at all.

* Mon Sep 13 1999 Preston Brown <pbrown@redhat.com>
- fixed stripping of test programs.

* Sun Aug 29 1999 Preston Brown <pbrown@redhat.com>
- removed 'flash' capability for xterm; see bug #2820 for details.

* Fri Aug 27 1999 Cristian Gafton <gafton@redhat.com>
- add the resetall script from Marc Merlin <marc@merlins.org>

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- added iris-ansi-net as alias for iris-ansi (bug #2561)

* Fri Jul 30 1999 Michael K. Johnson <johnsonm@redhat.com>
- added ncurses-intro.hmtl and hackguide.html to -devel package [bug #3929]

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- make sure ALL binaries are stripped (incl. test binaries)

* Thu Mar 25 1999 Preston Brown <pbrown@redhat.com>
- made xterm terminfo stuff MUCH better.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 16)

* Sat Mar 13 1999 Cristian Gafton <gafton@redhat.com>
- fixed header for C++ compiles

* Fri Mar 12 1999 Jeff Johnson <jbj@redhat.com>
- add terminfo entries for linux/linux-m on sparc (obsolete termfile_sparc).

* Thu Feb 18 1999 Cristian Gafton <gafton@redhat.com>
- updated patchset from original site

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- don't build the C++ demo code
- update patch set to the current as of today (redid all the individual
  patches in a single one)

* Wed Oct 14 1998 Cristian Gafton <gafton@redhat.com>
- make sure to strip the binaries

* Wed Sep 23 1998 Cristian Gafton <gafton@redhat.com>
- added another zillion of patches. The spec file *is* ugly
- defattr

* Mon Jul 20 1998 Cristian Gafton <gafton@redhat.com>
- added lots of patches. This spec file is starting to look ugly

* Wed Jul 01 1998 Alan Cox <alan@redhat.com>
- Fix setuid trusting. Open termcap/info files as the real user.

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- added terminfo entry for the poor guys using lat1 and/or lat-2 on their
  consoles... Enjoy linux-lat ! Thanks, Erik !

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- new patch to get xterm-color and nxterm terminfo entries
- aliased them to rxvt, as that seems to satisfy everybody

* Sun Apr 12 1998 Cristian Gafton <gafton@redhat.com>
- added %clean section

* Tue Apr 07 1998 Cristian Gafton <gafton@redhat.com>
- removed /usr/lib/terminfo symlink - we shouldn't need that

* Mon Apr 06 1998 Cristian Gafton <gafton@redhat.com>
- updated to 4.2 + patches
- added BuildRoot

* Sat Apr 04 1998 Cristian Gafton <gafton@redhat.com>
- rebuilt with egcs on alpha

* Wed Dec 31 1997 Erik Troan <ewt@redhat.com>
- version 7 didn't rebuild properly on the Alpha somehow -- no real changes
  are in this version

* Tue Dec 09 1997 Erik Troan <ewt@redhat.com>
- TIOCGWINSZ wasn't used properly

* Tue Jul 08 1997 Erik Troan <ewt@redhat.com>
- built against glibc, linked shared libs against -lc


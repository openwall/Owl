# $Id: Owl/packages/gpm/gpm.spec,v 1.1 2001/01/05 16:37:53 kad Exp $

# this defines the library version that this package builds.
%define 	LIBVER 1.18.0

Summary:	A mouse server for the Linux console.
Name: 	 	gpm
Version:	1.19.3
Release: 	5owl
License: 	GPL
Group: 		System Environment/Daemons
Source0: 	ftp://ftp.systemy.it/pub/develop/%{name}-%{version}.tar.gz
Source1: 	gpm.init
Patch0: 	gpm-1.19.3-rh-nops.diff
Patch1: 	gpm-1.17.5-rh-docfix.diff
Patch2: 	gpm-1.19.3-rh-noroot.diff
Patch3: 	gpm-1.19.2-rh-initgroups.diff
Patch4: 	gpm-1.19.1-rh-gpm-node-chmod.diff
Patch5: 	gpm-1.19.2-rh-limits.diff
Patch6:		gpm-1.19.3-immunix-owl-mktemp.diff
Prereq: 	/sbin/chkconfig /sbin/ldconfig /sbin/install-info /etc/rc.d/init.d
BuildRoot: 	/var/rpm-buildroot/%{name}-root

%description
Gpm provides mouse support to text-based Linux applications like the
Emacs editor and the Midnight Commander file management system.  Gpm
also provides console cut-and-paste operations using the mouse and
includes a program to allow pop-up menus to appear at the click of a
mouse button.

Gpm should be installed if you intend to use a mouse with your Red Hat
Linux system.

%package devel
Requires: gpm
Summary: Libraries and header files for developing mouse driven programs.
Group: Development/Libraries

%description devel
The gpm-devel program contains the libraries and header files needed
for the development of mouse driven programs for the console.  This
package allows you to develop text-mode programs which use the mouse.

Install gpm-devel if you need to develop text-mode programs which will
use the mouse.  You'll also need to install the gpm package.

%prep
%setup -q
%patch0 -p1 
%patch1 -p1 
%patch2 -p1
%patch3 -p1 
%patch4 -p1 
%patch5 -p1 
%patch6 -p1 

%build
autoconf
CFLAGS="-D_GNU_SOURCE $RPM_OPT_FLAGS" \
    lispdir=%{buildroot}%{_datadir}/emacs/site-lisp \
    %configure
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}

PATH=/sbin:$PATH:/usr/sbin:$PATH

mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp
%makeinstall lispdir=%{buildroot}%{_datadir}/emacs/site-lisp

install -m644 doc/gpm-root.1 %{buildroot}%{_mandir}/man1
install -m644 gpm-root.conf %{buildroot}%{_sysconfdir}
install -s -m755 hltest %{buildroot}%{_bindir}
make t-mouse.el t-mouse.elc
cp t-mouse.el* %{buildroot}%{_datadir}/emacs/site-lisp

pushd %{buildroot}
chmod +x .%{_libdir}/libgpm.so.%{LIBVER}
ln -sf libgpm.so.%{LIBVER} .%{_libdir}/libgpm.so
gzip -9nf .%{_infodir}/gpm.info*
popd


mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d  
install -m 755 $RPM_SOURCE_DIR/gpm.init %{buildroot}%{_sysconfdir}/rc.d/init.d/gpm

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add gpm
/sbin/ldconfig
/sbin/install-info %{_infodir}/gpm.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
    /sbin/install-info %{_infodir}/gpm.info.gz --delete %{_infodir}/dir
    service gpm stop >/dev/null 2>&1
    /sbin/chkconfig --del gpm
fi

%postun
if [ "$1" -ge "1" ]; then
  service gpm condrestart >/dev/null 2>&1
fi
/sbin/ldconfig

%files
%defattr(-,root,root)
%config %{_sysconfdir}/gpm-root.conf

%{_bindir}/mev
%{_bindir}/gpm-root
%{_bindir}/hltest
/usr/sbin/gpm
%{_datadir}/emacs/site-lisp/t-mouse.el
%{_datadir}/emacs/site-lisp/t-mouse.elc
%{_infodir}/gpm.info*
%{_mandir}/man1/mev.1*
%{_mandir}/man1/gpm-root.1*
%{_mandir}/man8/gpm.8*
%{_libdir}/libgpm.so.%{LIBVER}
%config %{_sysconfdir}/rc.d/init.d/gpm

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libgpm.a
%{_libdir}/libgpm.so

%changelog
* Fri Jan  5 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import mktemp patch from Immunix, fix strncpy

* Sun Dec 24 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

* Fri Jul 28 2000 Preston Brown <pbrown@redhat.com>
- cleaned up post section

* Wed Jul 26 2000 Preston Brown <pbrown@redhat.com>
- clarification: pam requirement added to fix permissions on /dev/gpmctl (#12849)

* Sat Jul 22 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.19.3

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 30 2000 Matt Wilson <msw@redhat.com>
- use sysconf(_SC_OPEN_MAX)

* Tue Jun 27 2000 Preston Brown <pbrown@redhat.com>
- don't prereq, only require initscripts

* Mon Jun 26 2000 Preston Brown <pbrown@redhat.com>
- fix up and move initscript
- prereq initscripts >= 5.20

* Sat Jun 17 2000 Bill Nottingham <notting@redhat.com>
- fix %config tag for initscript

* Thu Jun 15 2000 Bill Nottingham <notting@redhat.com>
- move it back

* Thu Jun 15 2000 Preston Brown <pbrown@redhat.com>
- move init script

* Wed Jun 14 2000 Preston Brown <pbrown@redhat.com>
- security patch on socket descriptor from Chris Evans.  Thanks Chris.
- include limits.h for OPEN_MAX

* Mon Jun 12 2000 Preston Brown <pbrown@redhat.com>
- 1.19.2, fix up root (setuid) patch
- FHS paths

* Thu Apr  6 2000 Jakub Jelinek <jakub@redhat.com>
- 1.19.1
- call initgroups in gpm-root before spawning command as user
- make gpm-root work on big endian

* Sun Mar 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- call ldconfig directly in postun

* Wed Mar 22 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with new libncurses

* Sat Mar 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.19.0
- fix build on systems that don't have emacs
  (configure built t-mouse* only if emacs was installed)

* Tue Feb 29 2000 Preston Brown <pbrown@redhat.com>
- important fix: improperly buildrooted for /usr/share/emacs/site-lisp, fixed.

* Tue Feb 15 2000 Jakub Jelinek <jakub@redhat.com>
- avoid cluttering of syslog with gpm No data messages

* Mon Feb 14 2000 Preston Brown <pbrown@redhat.com>
- disable-paste and mouse-test removed, they seem broken.

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- updated gpm.init to have better shutdown and descriptive messages
- strip lib

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description
- man pages are compressed

* Wed Jan 12 2000 Preston Brown <pbrown@redhat.com>
- 1.18.1.

* Tue Sep 28 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 1.18, hopefully fixes sparc protocol issues

* Fri Sep 24 1999 Bill Nottingham <notting@redhat.com>
- install-info sucks, and then you die.

* Fri Sep 10 1999 Bill Nottingham <notting@redhat.com>
- chkconfig --del in %preun, not %postun

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 1.17.9
- the maintainers are taking care of .so version now, removed patch

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Wed Jun  2 1999 Jeff Johnson <jbj@redhat.com>
- disable-paste need not be setuid root in Red Hat 6.0 (#2654)

* Tue May 18 1999 Michael K. Johnson <johnsonm@redhat.com>
- gpm.init had wrong pidfile name in comments; confused linuxconf

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- make sure all binaries are stripped, make init stuff more chkconfig style
- removed sparc-specific mouse stuff
- bumped libver to 1.17.5
- fixed texinfo source

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Thu Mar  4 1999 Matt Wilson <msw@redhat.com>
- updated to 1.75.5

* Tue Feb 16 1999 Cristian Gafton <gafton@redhat.com>
- avoid using makedev for internal functions (it is a #define in the system
  headers)

* Wed Jan 13 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 1.17.2.

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- enforce the use of -D_GNU_SOURCE so that it will compile on the ARM
- build against glibc 2.1

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 22 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced initscript

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- recompiled for manhattan

* Wed Apr 08 1998 Erik Troan <ewt@redhat.com>
- updated to 1.13

* Mon Nov 03 1997 Donnie Barnes <djb@redhat.com>
- added patch from Richard to get things to build on the SPARC

* Tue Oct 28 1997 Donnie Barnes <djb@redhat.com>
- fixed the emacs patch to install the emacs files in the right
  place (hopefully).

* Mon Oct 13 1997 Erik Troan <ewt@redhat.com>
- added chkconfig support
- added install-info

* Thu Sep 11 1997 Donald Barnes <djb@redhat.com>
- upgraded from 1.10 to 1.12
- added status/restart functionality to init script
- added define LIBVER 1.11

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

# $Id: Owl/packages/psmisc/psmisc.spec,v 1.1 2000/08/09 00:51:27 kad Exp $

Summary: Utilities for managing processes on your system.
Name: 		psmisc
Version: 	19
Release: 	4owl
Copyright: 	distributable
Group: 		Applications/System
Source: 	ftp://lrcftp.epfl.ch/pub/linux/local/psmisc/psmisc-%{version}.tar.gz
Patch: 		psmisc-17-rh-buildroot.diff
Patch1: 	psmisc-19-rh-noroot.diff
Buildroot: 	/var/rpm-buildroot/%{name}-root


%description
The psmisc package contains utilities for managing processes on your
system: pstree, killall and fuser.  The pstree command displays a tree
structure of all of the running processes on your system.  The killall
command sends a specified signal (SIGTERM if nothing is specified) to
processes identified by name.  The fuser command identifies the PIDs
of processes that are using specified files or filesystems.

%prep
%setup -q -n psmisc
%patch -p1 -b .br
%patch1 -p1 -b .noroot

%build
make 'LDFLAGS=-s' CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -DPSMISC_VERSION=\\\"`cat VERSION`\\\""
strip -R .comments fuser killall pstree

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/bin
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
make INSTPREFIX="$RPM_BUILD_ROOT" MANDIR="%{_mandir}/man1" install
mv $RPM_BUILD_ROOT/bin/fuser $RPM_BUILD_ROOT/sbin
chmod 0755 $RPM_BUILD_ROOT/sbin/fuser $RPM_BUILD_ROOT/usr/bin/killall $RPM_BUILD_ROOT/usr/bin/pstree

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/sbin/fuser
/usr/bin/killall
/usr/bin/pstree
%{_mandir}/man1/fuser.1*
%{_mandir}/man1/killall.1*
%{_mandir}/man1/pstree.1*

%changelog
* Sun Aug  6 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- FHS man paths
- patch makefile to enable non-root builds

* Sat Feb  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Deal with compressed man pages

* Sun Nov 21 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- update to v19
- handle RPM_OPT_FLAGS

* Mon Sep 27 1999 Bill Nottingham <notting@redhat.com>
- move fuser to /sbin

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Sat Mar 13 1999 Michael Maher <mike@redhat.com>
- updated package

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- renamed the patch file .patch instead of .spec

* Thu Apr 09 1998 Erik Troan <ewt@redhat.com>
- updated to psmisc version 17
- buildrooted

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from version 11 to version 16
- spec file cleanups

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc

# $Id: Owl/packages/psmisc/psmisc.spec,v 1.6 2004/11/23 22:40:49 mci Exp $

Summary: Utilities for managing processes on your system.
Name: psmisc
Version: 19
Release: owl5
License: BSD
Group: Applications/System
Source: ftp://lrcftp.epfl.ch/pub/linux/local/psmisc/psmisc-%version.tar.gz
Patch0: psmisc-19-owl-Makefile.diff
Patch1: psmisc-19-owl-by-user.diff
BuildRoot: /override/%name-%version

%description
The psmisc package contains utilities for managing processes on your
system: pstree, killall and fuser.  The pstree command displays a tree
structure of all of the running processes on your system.  The killall
command sends a specified signal (SIGTERM if nothing is specified) to
processes identified by name.  The fuser command identifies the PIDs
of processes that are using specified files or filesystems.

%prep
%setup -q -n psmisc
%patch0 -p1
%patch1 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" make

%install
rm -rf %buildroot
make install \
	DESTDIR=%buildroot \
	EBINDIR=/sbin BINDIR=%_bindir MANDIR=%_mandir

%files
%defattr(-,root,root)
%doc CHANGES COPYING README psmisc-%version.lsm
/sbin/fuser
%_bindir/killall
%_bindir/pstree
%_mandir/man1/fuser.1*
%_mandir/man1/killall.1*
%_mandir/man1/pstree.1*

%changelog
* Wed Dec 25 2002 Solar Designer <solar@owl.openwall.com> 19-owl5
- Fixed the segfault in pstree(1) when asked to report information for a
user, but entry with PID 1 (init) is inaccessible, thanks to (GalaxyMaster).
- Replaced two RH-derived Makefile patches with a much cleaner one.

* Wed Feb 06 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.
- Package the documentation.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

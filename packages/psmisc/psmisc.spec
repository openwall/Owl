# $Id: Owl/packages/psmisc/psmisc.spec,v 1.8 2005/02/18 23:48:08 galaxy Exp $

Summary: Utilities for managing processes on your system.
Name: psmisc
Version: 21.5
Release: owl0
License: BSD
Group: Applications/System
Source: ftp://prdownloads.sourceforge.net/psmisc/psmisc-%version.tar.gz
Patch0: psmisc-21.5-owl-termcap.diff
Patch1: psmisc-21.5-owl-restricted-proc.diff
BuildRoot: /override/%name-%version

%description
The psmisc package contains utilities for managing processes on your
system: pstree, killall and fuser.  The pstree command displays a tree
structure of all of the running processes on your system.  The killall
command sends a specified signal (SIGTERM if nothing is specified) to
processes identified by name.  The fuser command identifies the PIDs
of processes that are using specified files or filesystems.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure --disable-rpath
%__make all

%install
rm -rf %buildroot
%makeinstall
%find_lang %name

%files -f %name.lang
%defattr(-,root,root)
%doc ChangeLog COPYING README AUTHORS
%_bindir/fuser
%_bindir/killall
%_bindir/pstree*
%_mandir/man1/fuser.1*
%_mandir/man1/killall.1*
%_mandir/man1/pstree.1*

%changelog
* Sat Feb 19 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 21.5-owl0
- Updated to 21.5.
- Dropped unneeded Makefile patch.
- Regenerated restricted proc patch.
- Temporary workaround for termcap.

* Sat Jan 15 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 19-owl6
- Implemented support for restricted proc kernel patch.

* Wed Dec 25 2002 Solar Designer <solar@owl.openwall.com> 19-owl5
- Fixed the segfault in pstree(1) when asked to report information for a
user, but entry with PID 1 (init) is inaccessible, thanks to (GalaxyMaster).
- Replaced two RH-derived Makefile patches with a much cleaner one.

* Wed Feb 06 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.
- Package the documentation.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

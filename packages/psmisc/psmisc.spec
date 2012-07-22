# $Owl: Owl/packages/psmisc/psmisc.spec,v 1.18 2012/07/22 18:37:45 segoon Exp $

Summary: Utilities for managing processes on your system.
Name: psmisc
Version: 21.5
Release: owl5
License: GPL
Group: Applications/System
URL: http://psmisc.sourceforge.net
Source: http://prdownloads.sourceforge.net/psmisc/psmisc-%version.tar.gz
Patch0: psmisc-21.5-owl-termcap.diff
Patch1: psmisc-21.5-owl-restricted-proc.diff
Patch2: psmisc-21.5-up-Makefile.diff
BuildRequires: ncurses-devel
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
%patch2 -p1
bzip2 -9k ChangeLog

%build
%configure --disable-rpath
%__make all LDFLAGS=-ltinfo

%install
rm -rf %buildroot
%makeinstall

%find_lang %name

cd %buildroot
mkdir sbin
mv .%_bindir/fuser sbin/

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog.bz2 README
/sbin/fuser
%_bindir/killall
%_bindir/pstree*
%_mandir/man1/fuser.1*
%_mandir/man1/killall.1*
%_mandir/man1/pstree.1*

%changelog
* Sun Jul 22 2012 Vasiliy Kulikov <segoon-at-owl.openwall.com> 21.5-owl5
- Added -ltinfo into LDFLAGS to fix build error under binutils >= 2.21.

* Tue Jun 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 21.5-owl4
- Backported upstream change to fix build with new GNU make.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 21.5-owl3
- Compressed ChangeLog file.

* Fri Apr 08 2005 Solar Designer <solar-at-owl.openwall.com> 21.5-owl2
- Updated the License tag - this code is now GPL'ed.

* Mon Feb 21 2005 Solar Designer <solar-at-owl.openwall.com> 21.5-owl1
- Added URL tag, corrected Source URL.
- Moved fuser back to /sbin for RHL compatibility and since our current
/etc/rc.d/init.d/netfs depends on that.

* Sat Feb 19 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 21.5-owl0
- Updated to 21.5.
- Dropped unneeded Makefile patch.
- Regenerated restricted proc patch.
- Temporary workaround for termcap.

* Sat Jan 15 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 19-owl6
- Implemented support for restricted proc kernel patch.

* Wed Dec 25 2002 Solar Designer <solar-at-owl.openwall.com> 19-owl5
- Fixed the segfault in pstree(1) when asked to report information for a
user, but entry with PID 1 (init) is inaccessible, thanks to (GalaxyMaster).
- Replaced two RH-derived Makefile patches with a much cleaner one.

* Wed Feb 06 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.
- Package the documentation.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH

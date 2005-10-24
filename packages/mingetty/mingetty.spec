# $Id: Owl/packages/mingetty/mingetty.spec,v 1.13 2005/10/24 03:06:27 solar Exp $

Summary: A compact getty program for virtual consoles only.
Name: mingetty
Version: 0.9.4
Release: owl15
License: GPL
Group: System Environment/Base
Source0: ftp://jurix.jura.uni-sb.de/pub/linux/source/system/daemons/mingetty-0.9.4.tar.gz
Patch0: mingetty-0.9.4-suse.diff
Patch1: mingetty-0.9.4-owl-bound.diff
Patch2: mingetty-0.9.4-owl-logname.diff
Patch3: mingetty-0.9.4-owl-syslog.diff
Requires: SimplePAMApps >= 0.60-owl13
BuildRoot: /override/%name-%version

%description
The mingetty program is a lightweight, minimalist getty program for
use only on virtual consoles.  mingetty lacks certain functionality
needed for serial lines (you may use the mgetty program in that case).

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%__make CC="%__cc" CFLAGS="-D_GNU_SOURCE -Wall %optflags"

%install
rm -rf %buildroot
mkdir -p %buildroot/sbin
mkdir -p %buildroot%_mandir/man8

install -m 755 mingetty %buildroot/sbin/
install -m 644 mingetty.8 %buildroot%_mandir/man8/

%files
%defattr(-,root,root)
%doc ANNOUNCE COPYING CHANGES
/sbin/mingetty
%_mandir/man8/mingetty.8*

%changelog
* Mon Jan 10 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.9.4-owl15
- Made use of %%__cc and %%__make macros.

* Thu Dec 18 2003 Michail Litvak <mci-at-owl.openwall.com> 0.9.4-owl14
- Fix Y2K bug in -suse.diff (Thanks to Ilya Andreiv)

* Mon Feb 04 2002 Solar Designer <solar-at-owl.openwall.com> 0.9.4-owl13
- Enforce our new spec file conventions.

* Mon Sep 25 2000 Solar Designer <solar-at-owl.openwall.com>
- Replaced the error()/USE_SYSLOG code to fix a "format bug" reported by
Jarno Huuskonen on security-audit.

* Sun Jul 09 2000 Solar Designer <solar-at-owl.openwall.com>
- Imported this spec file from RH, replaced all their patches with one
from SuSE, and added a patch of my own (that backs out some of the RH/
SuSE changes and adds some bound checking).  This package is indeed still
just a hack.
- Now passes the username to login via LOGNAME, so requires the patched
SimplePAMApps as well.

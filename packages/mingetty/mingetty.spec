# $Id: Owl/packages/mingetty/mingetty.spec,v 1.7 2003/10/30 21:15:46 solar Exp $

Summary: A compact getty program for virtual consoles only.
Name: mingetty
Version: 0.9.4
Release: owl13
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
make CFLAGS="-D_GNU_SOURCE -Wall $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT%_mandir/man8

install -m 755 mingetty $RPM_BUILD_ROOT/sbin/
install -m 644 mingetty.8 $RPM_BUILD_ROOT%_mandir/man8/

%files
%defattr(-,root,root)
%doc ANNOUNCE COPYING CHANGES
/sbin/mingetty
%_mandir/man8/mingetty.8*

%changelog
* Mon Feb 04 2002 Solar Designer <solar@owl.openwall.com> 0.9.4-owl13
- Enforce our new spec file conventions.

* Mon Sep 25 2000 Solar Designer <solar@owl.openwall.com>
- Replaced the error()/USE_SYSLOG code to fix a "format bug" reported by
Jarno Huuskonen on security-audit.

* Sun Jul 09 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file from RH, replaced all their patches with one
from SuSE, and added a patch of my own (that backs out some of the RH/
SuSE changes and adds some bound checking).  This package is indeed still
just a hack.
- Now passes the username to login via LOGNAME, so requires the patched
SimplePAMApps as well.

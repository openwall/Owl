Summary: A compact getty program for virtual consoles only.
Name: mingetty
Version: 0.9.4
Copyright: GPL
Release: 13owl
Group: System Environment/Base
Source0: ftp://jurix.jura.uni-sb.de/pub/linux/source/system/daemons/mingetty-0.9.4.tar.gz
Patch0: mingetty-0.9.4-suse.diff
Patch1: mingetty-0.9.4-owl-bound.diff
Patch2: mingetty-0.9.4-owl-logname.diff
Patch3: mingetty-0.9.4-owl-syslog.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: SimplePAMApps >= 0.60-1owl

%description
The mingetty program is a lightweight, minimalist getty program for
use only on virtual consoles.  Mingetty is not suitable for serial
lines (you should use the mgetty program in that case).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
make CFLAGS="-D_GNU_SOURCE -Wall $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{sbin,usr/man/man8}

install -m 0755 -s mingetty $RPM_BUILD_ROOT/sbin/
install -m 0644 mingetty.8 $RPM_BUILD_ROOT/usr/man/man8/
gzip -9nf $RPM_BUILD_ROOT/usr/man/man8/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ANNOUNCE COPYING CHANGES
/sbin/mingetty
/usr/man/man8/mingetty.*

%changelog
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

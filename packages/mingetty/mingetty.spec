Summary: A compact getty program for virtual consoles only.
Name: mingetty
Version: 0.9.4
Copyright: GPL
Release: 12owl
Group: System Environment/Base
Source0: ftp://jurix.jura.uni-sb.de/pub/linux/source/system/daemons/mingetty-0.9.4.tar.gz
Patch0: mingetty-0.9.4-suse.diff
Patch1: mingetty-0.9.4-owl-bound.diff
Patch2: mingetty-0.9.4-owl-logname.diff
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
* Sun Jul  9 2000 Solar Designer <solar@false.com>
- Imported this spec file from RH, replaced all their patches with one
from SuSE, and added a patch of my own (that backs out some of the RH/
SuSE changes and adds some bound checking).  This package is indeed still
just a hack.
- Now passes the username to login via LOGNAME, so requires the patched
SimplePAMApps as well.

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 10)

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- fixed build problems on intel and alpha for manhattan

* Tue Oct 21 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

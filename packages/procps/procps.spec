# $Id: Owl/packages/procps/Attic/procps.spec,v 1.3 2000/12/02 03:01:33 solar Exp $

Summary: Utilities for monitoring your system and processes on your system.
Name: procps
Version: 2.0.7
Release: 1owl
Copyright: GPL and LGPL
Group: System Environment/Base
Source: ftp://sunsite.unc.edu/pub/Linux/system/status/ps/procps-%{version}.tar.gz
Patch0: procps-2.0.6-owl-alt-stale.diff
Patch1: procps-2.0.7-owl-locale.diff
Patch2: procps-2.0.7-owl-meminfo-fixes.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}

%description
The procps package contains a set of system utilities which provide
system information.  procps includes ps, free, skill, snice, tload,
top, pgrep, pkill, uptime, vmstat, w, and watch.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make CC="gcc $RPM_OPT_FLAGS" LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{bin,lib,sbin,usr/{bin,X11R6/bin,man/{man1,man5,man8}}}
make DESTDIR=$RPM_BUILD_ROOT OWNERGROUP= install

chmod 755 $RPM_BUILD_ROOT/{lib,bin,sbin,usr/bin}/*
strip $RPM_BUILD_ROOT/{bin,sbin,usr/bin/*} || :
gzip -9nf $RPM_BUILD_ROOT/usr/man/man[158]/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc NEWS BUGS TODO
/lib/libproc.so.%{version}
/bin/ps
/sbin/sysctl
/usr/bin/oldps
/usr/bin/uptime
/usr/bin/tload
/usr/bin/free
/usr/bin/w
/usr/bin/top
/usr/bin/vmstat
/usr/bin/watch
/usr/bin/skill
/usr/bin/snice
/usr/bin/pgrep
/usr/bin/pkill

/usr/man/man1/free.1.gz
/usr/man/man1/ps.1.gz
/usr/man/man1/oldps.1.gz
/usr/man/man1/skill.1.gz
/usr/man/man1/snice.1.gz
/usr/man/man1/pgrep.1.gz
/usr/man/man1/pkill.1.gz
/usr/man/man1/tload.1.gz
/usr/man/man1/top.1.gz
/usr/man/man1/uptime.1.gz
/usr/man/man1/w.1.gz
/usr/man/man1/watch.1.gz
/usr/man/man5/sysctl.conf.5.gz
/usr/man/man8/vmstat.8.gz
/usr/man/man8/sysctl.8.gz

%changelog
* Sat Dec 02 2000 Solar Designer <solar@owl.openwall.com>
- Updated to 2.0.7, removed 3 patches which are now obsolete.
- Added a C-locale-for-sscanf patch similar to one found in RH 7.0.
- Fixed a new long long / meminfo bug.

* Mon Nov 13 2000 Solar Designer <solar@owl.openwall.com>
- Added a patch from Red Hat to prevent divide by zero on big-endian.

* Wed Jul 05 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec from iNs/Linux, cleaned it up a bit, and added the
patch for alternative stale utmp entry checking.

* Thu Feb 17 2000  Francis J. Lacoste <francis.lacoste@iNsu.COM> 
  [2.0.6-1i]
- Changed group.
- Removed wmconfig file.
- Updated to version 2.0.6.
- Drop XConsole and sessreg from file list.
- Added sysctl program.
- Compressed man pages.

* Mon Mar 15 1999  Francis J. Lacoste <francis@Contre.COM> 
- Removed setuid bit on XConsole.
- Handled non root build.
- Fix perms.
- Stripped binaries.

* Fri Mar 12 1999 Michael Maher <mike@redhat.com>
- added changelog

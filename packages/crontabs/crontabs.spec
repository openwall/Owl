# $Id: Owl/packages/crontabs/crontabs.spec,v 1.11 2005/01/14 03:27:50 galaxy Exp $

Summary: System crontab files used to schedule the execution of programs.
Name: crontabs
Version: 2.0
Release: owl5
License: GPL
Group: System Environment/Base
Source0: run-parts-1.15.tar.gz
Source1: crontab
Patch0: run-parts-1.15-owl-umask.diff
Patch1: run-parts-1.15-owl-races.diff
Patch2: run-parts-1.15-owl-write_loop.diff
Patch3: run-parts-1.15-owl-fixes.diff
BuildRoot: /override/%name-%version

%description
This package contains the system crontab file and provides the
following directories:

/etc/cron.hourly
/etc/cron.daily
/etc/cron.weekly
/etc/cron.monthly

As these directory names say, the files within them are executed by
cron on an hourly, daily, weekly, or monthly basis, respectively.

The crontabs package handles a basic system function, so it should be
installed on your system.

%prep
%setup -q -n run-parts-1.15
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%__cc run-parts.c -o run-parts $RPM_OPT_FLAGS -Wall

%install
rm -rf %buildroot
mkdir -p %buildroot/etc/cron.{hourly,daily,weekly,monthly}
mkdir -p %buildroot%_bindir
mkdir -p %buildroot%_mandir/man8/

install -m 644 $RPM_SOURCE_DIR/crontab %buildroot/etc/
install -m 755 run-parts %buildroot%_bindir/
install -m 644 run-parts.8 %buildroot%_mandir/man8/

%files
%defattr(-,root,root)
%config /etc/crontab
%_bindir/run-parts
%_mandir/man8/*
%dir /etc/cron.hourly
%dir /etc/cron.daily
%dir /etc/cron.weekly
%dir /etc/cron.monthly

%changelog
* Fri Jan 07 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.0-owl5
- Added fixes patch to deal with issues after gcc upgrade.
- Used %%__cc to chose C compiler.
- Removed "-s" option from compilation process since we are using brp- scripts.

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com> 2.0-owl4
- Enforce our new spec file conventions.

* Fri May 25 2001 Solar Designer <solar@owl.openwall.com>
- Fixed SIGCHLD races in run-parts (the code is still far from clean).

* Thu May 16 2001 Michail Litvak <mci@owl.openwall.com>
- run-parts source archive renamed to name with version
- umask patching extracted to separate patch (and improved)
- use gcc instead of make

* Thu May 15 2001 Michail Litvak <mci@owl.openwall.com>
- basically imported from RH, but run-parts imported
  from Debian (debianutils)
- run-parts patched to use write_loop() instead of just write()

# $Id: Owl/packages/crontabs/crontabs.spec,v 1.6 2002/02/07 01:41:15 solar Exp $

Summary: System crontab files used to schedule the execution of programs.
Name: crontabs
Version: 2.0
Release: owl4
License: GPL
Group: System Environment/Base
Source0: run-parts-1.15.tar.gz
Source1: crontab
Patch0: run-parts-1.15-owl-umask.diff
Patch1: run-parts-1.15-owl-races.diff
Patch2: run-parts-1.15-owl-write_loop.diff
BuildRoot: /override/%{name}-%{version}

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

%build
gcc run-parts.c -o run-parts $RPM_OPT_FLAGS -Wall -s

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/cron.{hourly,daily,weekly,monthly}
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8/

install -m 644 $RPM_SOURCE_DIR/crontab $RPM_BUILD_ROOT/etc/
install -m 755 run-parts $RPM_BUILD_ROOT/usr/bin/
install -m 644 run-parts.8 $RPM_BUILD_ROOT%{_mandir}/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config /etc/crontab
/usr/bin/run-parts
%{_mandir}/man8/*
%dir /etc/cron.hourly
%dir /etc/cron.daily
%dir /etc/cron.weekly
%dir /etc/cron.monthly

%changelog
* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
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

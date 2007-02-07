# $Owl: Owl/packages/crontabs/crontabs.spec,v 1.16.2.1 2007/02/07 17:19:59 ldv Exp $

Summary: System crontab files used to schedule the execution of programs.
Name: crontabs
Version: 2.1
Release: owl1
License: GPL
Group: System Environment/Base
Source0: run-parts.c
Source1: run-parts.8
Source2: crontab
Requires: crond
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
%setup -qcT
install -pm644 %_sourcedir/run-parts.{c,8} .

%build
%__cc run-parts.c -o run-parts %optflags -Wall -W

%install
rm -rf %buildroot
mkdir -p %buildroot/etc/cron.{hourly,daily,weekly,monthly}
mkdir -p %buildroot%_bindir
mkdir -p %buildroot%_mandir/man8/

install -m600 %_sourcedir/crontab %buildroot/etc/
install -m755 run-parts %buildroot%_bindir/
install -m644 run-parts.8 %buildroot%_mandir/man8/

%files
%defattr(-,root,root,700)
%config /etc/crontab
%_bindir/run-parts
%_mandir/man8/*
%dir /etc/cron.hourly
%dir /etc/cron.daily
%dir /etc/cron.weekly
%dir /etc/cron.monthly

%changelog
* Tue Dec 26 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.1-owl1
- Updated run-parts from debianutils-2.17.4.

* Mon Jun 26 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.0-owl7
- Changed /etc/cron.* access permissions to 0700.
- Changed /etc/crontab access permissions to 0600.

* Sat Sep 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.0-owl6
- Added crond to the package requirements.

* Fri Jan 07 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.0-owl5
- Added fixes patch to deal with issues after gcc upgrade.
- Use %%__cc macro to choose C compiler.
- Removed "-s" option from compilation process since we are using brp- scripts.

* Thu Jan 24 2002 Solar Designer <solar-at-owl.openwall.com> 2.0-owl4
- Enforce our new spec file conventions.

* Fri May 25 2001 Solar Designer <solar-at-owl.openwall.com>
- Fixed SIGCHLD races in run-parts (the code is still far from clean).

* Thu May 16 2001 Michail Litvak <mci-at-owl.openwall.com>
- run-parts source archive renamed to name with version
- umask patching extracted to separate patch (and improved)
- use gcc instead of make

* Thu May 15 2001 Michail Litvak <mci-at-owl.openwall.com>
- basically imported from RH, but run-parts imported
  from Debian (debianutils)
- run-parts patched to use write_loop() instead of just write()

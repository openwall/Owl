# $Id: Owl/packages/crontabs/crontabs.spec,v 1.2 2001/05/16 17:45:25 mci Exp $

Summary: System crontab files used to schedule the execution of programs.
Name: crontabs
Version: 2.0
Release: 2owl
Copyright: GPL
Group: System Environment/Base
Source0: run-parts-1.15.tar.gz
Source1: crontab
Patch0: run-parts-1.15-owl-writeloop.diff
Patch1: run-parts-1.15-owl-ulimit.diff
BuildRoot: /var/rpm-buildroot/%{name}-%{version}

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
%setup -n run-parts-1.15
%patch0 -p1
%patch1 -p1

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
* Thu May 16 2001 Michail Litvak <mci@owl.openwall.com>
- run-parts source archive renamed to name with version
- ulimit patching extracted to separate patch (and improved)
- use gcc instead of make

* Thu May 15 2001 Michail Litvak <mci@owl.openwall.com>
- basically imported from RH, but run-parts imported
  from Debian (debianutils)
- run-parts patched to use write_loop() instead of just write()

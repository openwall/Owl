# $Id: Owl/packages/logrotate/logrotate.spec,v 1.2 2001/06/04 01:01:14 solar Exp $

Summary: Rotates, compresses, removes and mails system log files.
Name: logrotate
Version: 3.5.2
Release: 2owl
Copyright: GPL
Group: System Environment/Base
Source: ftp://ftp.redhat.com/pub/redhat/code/logrotate/logrotate-%{version}.tar.gz
Patch0: logrotate-3.5.2-owl-fixes.diff
Patch1: logrotate-3.5.2-owl-commands-paths.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: crontabs
BuildPreReq: popt

%description
The logrotate utility is designed to simplify the administration of
log files on a system which generates a lot of log files.  logrotate
allows for the automatic rotation, compression, removal and mailing of
log files.  logrotate can be set to handle a log file daily, weekly,
monthly or when the log file gets to a certain size.  Normally,
logrotate runs as a daily cron job.

Install the logrotate package if you need a utility to deal with the
log files on your system.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
make CC=gcc RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
make PREFIX=$RPM_BUILD_ROOT MANDIR=%{_mandir} install
mkdir -p $RPM_BUILD_ROOT/etc/{logrotate.d,cron.daily}
mkdir -p $RPM_BUILD_ROOT/var/lib/logrotate

install -m 600 examples/logrotate-default $RPM_BUILD_ROOT/etc/logrotate.conf
install -m 700 examples/logrotate.cron $RPM_BUILD_ROOT/etc/cron.daily/logrotate

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lib/logrotate.status ]; then
	mv -f /var/lib/logrotate.status /var/lib/logrotate/status
fi

%preun
if [ $1 -eq 0 ]; then
	rm -f /var/lib/logrotate/status
fi

%files
%attr(0700,root,root) /usr/sbin/logrotate
%attr(0644,root,root) %{_mandir}/man8/logrotate.8*
%attr(0600,root,root) %config /etc/logrotate.conf
%attr(0700,root,root) %dir /etc/logrotate.d
%attr(0700,root,root) /etc/cron.daily/logrotate
%attr(0700,root,root) /var/lib/logrotate

%changelog
* Mon Jun 04 2001 Solar Designer <solar@owl.openwall.com>
- Enabled the daily cron job now that we have /etc/cron.daily (finally).
- Moved /var/lib/logrotate.status to /var/lib/logrotate/status
- If log compression is requested, use gzip at its default compression
level (no "-9").

* Sat Nov 04 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file for Owl.
- Added a patch to fix some security/reliability issues.

* Tue Aug 15 2000 Erik Troan <ewt@redhat.com>
- see CHANGES

* Sun Jul 23 2000 Erik Troan <ewt@redhat.com>
- see CHANGES

* Tue Jul 11 2000 Erik Troan <ewt@redhat.com>
- support spaces in filenames
- added sharedscripts

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- use %%{_mandir} for man pages

* Thu Feb 24 2000 Erik Troan <ewt@redhat.com>
- don't rotate lastlog

* Thu Feb 03 2000 Erik Troan <ewt@redhat.com>
- gzipped manpages

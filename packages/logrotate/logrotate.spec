# $Id: Owl/packages/logrotate/logrotate.spec,v 1.5 2002/02/05 20:07:13 mci Exp $

Summary: Rotates, compresses, removes and mails system log files.
Name: logrotate
Version: 3.5.9
Release: owl2
License: GPL
Group: System Environment/Base
Source: logrotate-%{version}.tar.bz2
Patch0: logrotate-3.5.9-cvs-20011126.diff
Patch1: logrotate-3.5.9-owl-commands-paths.diff
Patch2: logrotate-3.5.9-owl-man.diff
Patch3: logrotate-3.5.9-owl-fchmod-fchown-race.diff
Patch4: logrotate-3.5.9-owl-tmp.diff
Requires: crontabs
BuildPreReq: popt
BuildRoot: /override/%{name}-%{version}

%description
The logrotate utility is designed to simplify the administration of
log files on a system which generates a lot of log files.  logrotate
allows for the automatic rotation, compression, removal and mailing of
log files.  logrotate can be set to handle a log file daily, weekly,
monthly or when the log file gets to a certain size.  Normally,
logrotate runs as a daily cron job.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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
* Tue Feb 05 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Tue Nov 27 2001 Solar Designer <solar@owl.openwall.com>
- Corrected the man page for our status file path.
- Use $TMPDIR.

* Mon Nov 26 2001 Michail Litvak <mci@owl.openwall.com>
- 3.5.9
- Patch from CVS to fix zero-length state files.
- Wrote in man page about use of wildcards.
- fix race in case fchmod->fchown.

* Mon Jun 04 2001 Solar Designer <solar@owl.openwall.com>
- Enabled the daily cron job now that we have /etc/cron.daily (finally).
- Moved /var/lib/logrotate.status to /var/lib/logrotate/status
- If log compression is requested, use gzip at its default compression
level (no "-9").

* Sat Nov 04 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file for Owl.
- Added a patch to fix some security/reliability issues.

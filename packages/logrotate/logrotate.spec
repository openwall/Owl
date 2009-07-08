# $Owl: Owl/packages/logrotate/logrotate.spec,v 1.13 2009/07/08 00:53:05 solar Exp $

Summary: Rotates, compresses, removes and mails system log files.
Name: logrotate
Version: 3.6.2
Release: owl2
License: GPL
Group: System Environment/Base
URL: https://fedorahosted.org/logrotate/
# https://fedorahosted.org/releases/l/o/logrotate/
# http://svn.fedorahosted.org/svn/logrotate/
Source: logrotate-%version.tar.bz2
Patch0: logrotate-3.6.2-owl-commands-paths.diff
Patch1: logrotate-3.6.2-owl-man.diff
Patch2: logrotate-3.6.2-owl-fchmod-fchown-race.diff
Patch3: logrotate-3.6.2-owl-tmp.diff
Requires: crontabs
BuildRequires: popt
BuildRoot: /override/%name-%version

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

%build
%__make CC="%__cc" RPM_OPT_FLAGS="%optflags"

%install
%__make PREFIX="%buildroot" MANDIR="%_mandir" install
mkdir -p %buildroot/etc/{logrotate.d,cron.daily}
mkdir -p %buildroot/var/lib/logrotate

install -m 600 examples/logrotate-default %buildroot/etc/logrotate.conf
install -m 700 examples/logrotate.cron %buildroot/etc/cron.daily/logrotate

%post
if [ -f /var/lib/logrotate.status ]; then
	mv -f /var/lib/logrotate.status /var/lib/logrotate/status
fi

%preun
if [ $1 -eq 0 ]; then
	rm -f /var/lib/logrotate/status
fi

%files
%attr(0755,root,root) %_sbindir/logrotate
%attr(0644,root,root) %_mandir/man8/logrotate.8*
%attr(0600,root,root) %config(noreplace) /etc/logrotate.conf
%attr(0700,root,root) %dir /etc/logrotate.d
%attr(0700,root,root) /etc/cron.daily/logrotate
%attr(0700,root,root) /var/lib/logrotate

%changelog
* Sun Oct 09 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.6.2-owl2
- Changed the permissions for %%_sbindir/logrotate from 0700 to 0755.
- Replaced 'make' with '%%__make' and 'gcc' with '%%__cc'.
- Replaced '/usr/sbin' with '%%_sbindir'.

* Mon Mar 11 2002 Michail Litvak <mci-at-owl.openwall.com> 3.6.2-owl1
- 3.6.2
- noreplace config file

* Tue Feb 05 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Tue Nov 27 2001 Solar Designer <solar-at-owl.openwall.com>
- Corrected the man page for our status file path.
- Use $TMPDIR.

* Mon Nov 26 2001 Michail Litvak <mci-at-owl.openwall.com>
- 3.5.9
- Patch from CVS to fix zero-length state files.
- Wrote in man page about use of wildcards.
- fix race in case fchmod->fchown.

* Mon Jun 04 2001 Solar Designer <solar-at-owl.openwall.com>
- Enabled the daily cron job now that we have /etc/cron.daily (finally).
- Moved /var/lib/logrotate.status to /var/lib/logrotate/status
- If log compression is requested, use gzip at its default compression
level (no "-9").

* Sat Nov 04 2000 Solar Designer <solar-at-owl.openwall.com>
- Imported this spec file for Owl.
- Added a patch to fix some security/reliability issues.

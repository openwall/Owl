# $Id: Owl/packages/utempter/Attic/utempter.spec,v 1.2 2001/02/25 18:25:38 solar Exp $

Summary: A privileged helper for utmp/wtmp updates.
Name: utempter
Version: 0.5.2
Release: 5owl
License: GPL
Group: System Environment/Base
Source: utempter-%{version}.tar.gz
Prereq: grep, /usr/sbin/groupadd, /sbin/ldconfig
Prefix: %{_prefix}
BuildRoot: /var/rpm-buildroot/%{name}-root

%description
utempter is a privileged helper which allows terminal emulators such
as screen and xterm to record user sessions to utmp and wtmp files.

%prep
%setup -q

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT install
strip $RPM_BUILD_ROOT/usr/sbin/utempter
mkdir -p $RPM_BUILD_ROOT/usr/sbin/utempter.d/
mv $RPM_BUILD_ROOT/usr/sbin/utempter $RPM_BUILD_ROOT/usr/sbin/utempter.d/
ln -s utempter.d/utempter $RPM_BUILD_ROOT/usr/sbin/utempter

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep ^utempter: /etc/group &>/dev/null || groupadd -g 162 utempter

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(710,root,utempter) %dir /usr/sbin/utempter.d/
%attr(2711,root,utmp) /usr/sbin/utempter.d/utempter
%doc COPYING
/usr/lib/libutempter.so*
/usr/include/utempter.h
/usr/sbin/utempter

%changelog
* Sun Feb 25 2001 Solar Designer <solar@owl.openwall.com>
- Various spec file cleanups.
- Corrected the package description.

* Wed Feb 21 2001 Michail Litvak <mci@owl.openwall.com>
- imported from RH
- added utempter group
- utempter binary moved to /usr/sbin/utempter.d/
  owned by group utempter with 710 permissions

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Matt Wilson <msw@redhat.com>
- defattr root

* Thu Feb 24 2000 Erik Troan <ewt@redhat.com>
- added LGPL notice

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip utempter

* Mon Aug 30 1999 Bill Nottingham <notting@redhat.com>
- add utmp as group 22

* Fri Jun  4 1999 Jeff Johnson <jbj@redhat.com>
- ignore SIGCHLD while processing utmp.

# $Id: Owl/packages/utempter/Attic/utempter.spec,v 1.5 2002/05/19 03:56:03 solar Exp $

Summary: A privileged helper for utmp/wtmp updates.
Name: utempter
Version: 0.5.2
Release: owl6
License: GPL
Group: System Environment/Base
Source: utempter-%{version}.tar.gz
Patch0: utempter-0.5.2-owl-helper-path-hack.diff
PreReq: /sbin/ldconfig, grep, /usr/sbin/groupadd
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
utempter is a privileged helper which allows terminal emulators such
as screen and xterm to record user sessions to utmp and wtmp files.

%prep
%setup -q
%patch0 -p1

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT install
strip $RPM_BUILD_ROOT%{_libexecdir}/utempter/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%pre
grep -q ^utempter: /etc/group || groupadd -g 162 utempter

%files
%defattr(-,root,root)
%doc COPYING
%attr(710,root,utempter) %dir %{_libexecdir}/utempter
%attr(2711,root,utmp) %{_libexecdir}/utempter/utempter
/usr/lib/libutempter.so*
/usr/include/utempter.h

%changelog
* Sun May 19 2002 Solar Designer <solar@owl.openwall.com>
- Moved the utempter directory to /usr/libexec.
- Try an alternate utempter helper binary location for screen.

* Mon Feb 04 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Feb 25 2001 Solar Designer <solar@owl.openwall.com>
- Various spec file cleanups.
- Corrected the package description.

* Wed Feb 21 2001 Michail Litvak <mci@owl.openwall.com>
- imported from RH
- added utempter group
- utempter binary moved to /usr/sbin/utempter.d/
  owned by group utempter with 710 permissions

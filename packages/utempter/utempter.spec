# $Id: Owl/packages/utempter/Attic/utempter.spec,v 1.3 2002/02/04 08:07:29 solar Exp $

Summary: A privileged helper for utmp/wtmp updates.
Name: utempter
Version: 0.5.2
Release: owl5
License: GPL
Group: System Environment/Base
Source: utempter-%{version}.tar.gz
PreReq: grep, /usr/sbin/groupadd, /sbin/ldconfig
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

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
mkdir -p $RPM_BUILD_ROOT/usr/sbin/utempter.d/
mv $RPM_BUILD_ROOT/usr/sbin/utempter $RPM_BUILD_ROOT/usr/sbin/utempter.d/
ln -s utempter.d/utempter $RPM_BUILD_ROOT/usr/sbin/utempter

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep -q ^utempter: /etc/group || groupadd -g 162 utempter

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

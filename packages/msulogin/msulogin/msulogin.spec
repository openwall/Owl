# $Id: Owl/packages/msulogin/msulogin/msulogin.spec,v 1.1 2003/04/27 02:26:29 solar Exp $

Summary: The single user mode login program (sulogin).
Name: msulogin
Version: 0.9
Release: owl1
License: relaxed BSD and (L)GPL-compatible
Group: System Environment/Base
URL: http://www.openwall.com/msulogin/
Source: ftp://ftp.openwall.com/pub/projects/msulogin/%{name}-%{version}.tar.gz
Conflicts: SysVinit < 2.85-owl4
BuildRoot: /override/%{name}-%{version}

%description
sulogin is a program to force the console user to login under a root
account before a shell is started.  Unlike other implementations of
sulogin, this one supports having multiple root accounts on a system.

%prep
%setup -q

%build
make CFLAGS="-c -Wall $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE
/sbin/sulogin
%{_mandir}/man8/sulogin.8*

%changelog
* Sun Apr 27 2003 Solar Designer <solar@owl.openwall.com> 0.9-owl1
- Wrote this program and the accompanying files.

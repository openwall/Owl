# $Id: Owl/packages/quota/quota.spec,v 1.13 2002/02/05 15:33:42 solar Exp $

Summary: System administration tools for monitoring users' disk usage.
Name: quota
Version: 2.00
Release: owl6
License: BSD
Group: System Environment/Base
Source: ftp://ftp.cistron.nl/pub/people/mvw/quota/%{name}-%{version}.tar.gz
Patch0: quota-2.00-pld-owl-man.diff
Patch1: quota-2.00-owl-install-no-root.diff
Patch2: quota-2.00-owl-tmp.diff
BuildRequires: e2fsprogs-devel
BuildRoot: /override/%{name}-%{version}

%description
The quota package contains system administration tools for monitoring
and limiting users' and or groups' disk usage, per filesystem.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure
make CC=gcc

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,2,3,8}

%makeinstall root_sbindir=$RPM_BUILD_ROOT/sbin DEF_BIN_MODE=755

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/*.html
%doc warnquota.conf
/sbin/*
%{_bindir}/*
%{_sbindir}/edquota
%{_sbindir}/quotastats
%{_sbindir}/repquota
%{_sbindir}/setquota
%{_sbindir}/warnquota
%{_mandir}/man1/quota.1*
%{_mandir}/man2/quotactl.2*
%{_mandir}/man8/edquota.8*
%{_mandir}/man8/quotacheck.8*
%{_mandir}/man8/quotaon.8*
%{_mandir}/man8/repquota.8*
%{_mandir}/man8/setquota.8*

%changelog
* Tue Feb 05 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Jul 06 2001 Solar Designer <solar@owl.openwall.com>
- New release number for upgrades after building against glibc >= 2.1.3-17owl
which includes corrected declaration of struct dqstats in <sys/quota.h>.

* Sun Jul 01 2001 Michail Litvak <mci@owl.openwall.com>
- pack only *.html in doc/
- man pages fixes
- added TMPDIR support to edquota
- put warnquota.conf in doc

* Wed Jun 27 2001 Michail Litvak <mci@owl.openwall.com>
- more fixes in mans and docs
- patch to catch error from mkstemp
- include doc/ subdir into package

* Mon Jun 25 2001 Michail Litvak <mci@owl.openwall.com>
- some spec cleanups
- patch to allow building to non-root user

* Sun Jun 24 2001 Michail Litvak <mci@owl.openwall.com>
- Imported from RH
- man patch from PLD

# $Id: Owl/packages/stmpclean/stmpclean.spec,v 1.3 2002/04/01 21:38:56 solar Exp $

Summary: A safe temporary directory cleaner.
Name: stmpclean
Version: 0.1
Release: owl2
License: BSD
Group: System Environment/Base
Source0: ftp://ftp.mccme.ru/users/shalunov/stmpclean-%{version}.tar.gz
Source1: stmpclean.cron
Patch0: stmpclean-0.1-owl-fixes.diff
PreReq: /etc/cron.daily
Provides: tmpwatch
Obsoletes: tmpwatch
BuildRoot: /override/%{name}-%{version}

%description
The stmpclean utility removes old files (and old empty directories)
from the specified directory.  Its typical use is to clean directories
such as /tmp where old files tend to accumulate.

%prep
%setup -q
%patch0 -p1

%build
make CFLAGS="$RPM_OPT_FLAGS -Wall" stmpclean

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT SBINDIR=%{_sbindir} MANDIR=%{_mandir}
cd $RPM_BUILD_ROOT
mkdir -p etc/cron.daily
install -m 700 $RPM_SOURCE_DIR/stmpclean.cron etc/cron.daily/stmpclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README
%{_sbindir}/*
%{_mandir}/*
/etc/cron.daily/stmpclean

%changelog
* Sun Mar 31 2002 Solar Designer <solar@owl.openwall.com>
- Corrected the tmpwatch emulation to accept the time in hours.

* Sat Mar 30 2002 Solar Designer <solar@owl.openwall.com>
- Packaged stmpclean 0.1 with minor fixes and modifications to switch
supplementary groups as well as euid/egid, make use of O_DIRECTORY and
O_NOFOLLOW to avoid possible side effects on open(2) when raced, and
provide some limited tmpwatch emulation.

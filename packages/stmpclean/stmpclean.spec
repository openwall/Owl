# $Id: Owl/packages/stmpclean/stmpclean.spec,v 1.6 2003/10/30 21:15:49 solar Exp $

Summary: A safe temporary directory cleaner.
Name: stmpclean
Version: 0.3
Release: owl1
License: BSD
Group: System Environment/Base
URL: http://www.internet2.edu/~shalunov/stmpclean/
Source0: http://www.internet2.edu/~shalunov/stmpclean/%name-%version.tar.gz
Source1: stmpclean.cron
Patch0: stmpclean-0.3-owl-fixes.diff
PreReq: /etc/cron.daily
Provides: tmpwatch
Obsoletes: tmpwatch
BuildRoot: /override/%name-%version

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
make install DESTDIR=$RPM_BUILD_ROOT SBINDIR=%_sbindir MANDIR=%_mandir
cd $RPM_BUILD_ROOT
mkdir -p etc/cron.daily
install -m 700 $RPM_SOURCE_DIR/stmpclean.cron etc/cron.daily/stmpclean

%files
%defattr(-,root,root)
%doc README FAQ
%_sbindir/*
%_mandir/*
/etc/cron.daily/stmpclean

%changelog
* Thu Jun 12 2003 Solar Designer <solar@owl.openwall.com> 0.3-owl1
- Updated to 0.3 which will refuse to process relative pathnames.

* Thu Apr 25 2002 Solar Designer <solar@owl.openwall.com> 0.1-owl3
- Dereference symlinks for directories specified on the command line.
- Install the binary mode 700 as it's not usable by regular users.

* Sun Mar 31 2002 Solar Designer <solar@owl.openwall.com>
- Corrected the tmpwatch emulation to accept the time in hours.

* Sat Mar 30 2002 Solar Designer <solar@owl.openwall.com>
- Packaged stmpclean 0.1 with minor fixes and modifications to switch
supplementary groups as well as euid/egid, make use of O_DIRECTORY and
O_NOFOLLOW to avoid possible side effects on open(2) when raced, and
provide some limited tmpwatch emulation.

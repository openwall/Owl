# $Owl: Owl/packages/stmpclean/stmpclean.spec,v 1.16 2010/09/02 21:30:07 solar Exp $

Summary: A safe temporary directory cleaner.
Name: stmpclean
Version: 0.3
Release: owl5
License: BSD
Group: System Environment/Base
URL: http://shlang.com/stmpclean/
Source0: http://shlang.com/stmpclean/%name-%version.tar.gz
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
make CFLAGS="%optflags -Wall" stmpclean

%install
rm -rf %buildroot
make install DESTDIR=%buildroot SBINDIR=%_sbindir MANDIR=%_mandir
cd %buildroot
mkdir -p etc/cron.daily
install -m 700 %_sourcedir/stmpclean.cron etc/cron.daily/stmpclean

%files
%defattr(-,root,root)
%doc README FAQ
%_sbindir/*
%_mandir/man8/*
/etc/cron.daily/stmpclean

%changelog
* Thu Sep 02 2010 Solar Designer <solar-at-owl.openwall.com> 0.3-owl5
- Only run stmpclean on /var/tmp if it is not a symlink to /tmp.

* Mon Nov 08 2004 Michail Litvak <mci-at-owl.openwall.com> 0.3-owl4
- Updated stmpclean.cron according to FHS 2.2 man pages cache location.

* Mon Jun 28 2004 Solar Designer <solar-at-owl.openwall.com> 0.3-owl3
- Silently continue on ENOENT from lstat() on a directory entry.

* Fri Mar 19 2004 Solar Designer <solar-at-owl.openwall.com> 0.3-owl2
- Package only man8/*, not the entire man8 directory (that was a bug).

* Thu Jun 12 2003 Solar Designer <solar-at-owl.openwall.com> 0.3-owl1
- Updated to 0.3 which will refuse to process relative pathnames.

* Thu Apr 25 2002 Solar Designer <solar-at-owl.openwall.com> 0.1-owl3
- Dereference symlinks for directories specified on the command line.
- Install the binary mode 700 as it's not usable by regular users.

* Sun Mar 31 2002 Solar Designer <solar-at-owl.openwall.com>
- Corrected the tmpwatch emulation to accept the time in hours.

* Sat Mar 30 2002 Solar Designer <solar-at-owl.openwall.com>
- Packaged stmpclean 0.1 with minor fixes and modifications to switch
supplementary groups as well as euid/egid, make use of O_DIRECTORY and
O_NOFOLLOW to avoid possible side effects on open(2) when raced, and
provide some limited tmpwatch emulation.

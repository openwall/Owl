Summary: Utilities for monitoring your system and processes on your system.
Name: procps
Version: 2.0.6
Release: 1owl
Copyright: GPL and LGPL
Group: System Environment/Base
Source: ftp://sunsite.unc.edu/pub/Linux/system/status/ps/procps-%{version}.tar.gz
Patch0: procps-2.0.6-ins-noroot.diff
Patch1: procps-2.0.6-owl-alt-stale.diff
Patch2: procps-2.0.6-owl-glibc-2.1.3-hack.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}

%description
The procps package contains a set of system utilities which provide
system information.  Procps includes ps, free, skill, snice, tload,
top, uptime, vmstat, w, and watch.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make CC="gcc $RPM_OPT_FLAGS" LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{bin,lib,sbin,usr/{bin,man/{man1,man5,man8}}}
make DESTDIR=$RPM_BUILD_ROOT install

install -m644 sysctl.conf.5 $RPM_BUILD_ROOT/usr/man/man5

# Fix perms
chmod 644 $RPM_BUILD_ROOT/usr/man/man1/*
chmod 755 $RPM_BUILD_ROOT/{lib,bin,usr/bin}/*
strip $RPM_BUILD_ROOT/{bin,sbin,usr/bin/*} || :

gzip -9f $RPM_BUILD_ROOT/usr/man/man[158]/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc NEWS BUGS TODO
/lib/libproc.so.2.0.6
/bin/ps
/sbin/sysctl
/usr/bin/oldps
/usr/bin/uptime
/usr/bin/tload
/usr/bin/free
/usr/bin/w
/usr/bin/top
/usr/bin/vmstat
/usr/bin/watch
/usr/bin/skill
/usr/bin/snice

/usr/man/man1/free.1.gz
/usr/man/man1/ps.1.gz
/usr/man/man1/oldps.1.gz
/usr/man/man1/skill.1.gz
/usr/man/man1/snice.1.gz
/usr/man/man1/tload.1.gz
/usr/man/man1/top.1.gz
/usr/man/man1/uptime.1.gz
/usr/man/man1/w.1.gz
/usr/man/man1/watch.1.gz
/usr/man/man5/sysctl.conf.5.gz
/usr/man/man8/vmstat.8.gz
/usr/man/man8/sysctl.8.gz

%changelog
* Wed Jul  5 2000 Solar Designer <solar@false.com>
- Imported this spec from iNs/Linux, cleaned it up a bit, and added the
  patch for alternative stale utmp entry checking.

* Thu Feb 17 2000  Francis J. Lacoste <francis.lacoste@iNsu.COM> 
  [2.0.6-1i]
- Changed group.
- Removed wmconfig file.
- Updated to version 2.0.6.
- Drop XConsole and sessreg from file list.
- Added sysctl program.
- Compressed man pages.

* Mon Mar 15 1999  Francis J. Lacoste <francis@Contre.COM> 
- Removed setuid bit on XConsole.
- Handled non root build.
- Fix perms.
- Stripped binaries.

* Fri Mar 12 1999 Michael Maher <mike@redhat.com>
- added changelog

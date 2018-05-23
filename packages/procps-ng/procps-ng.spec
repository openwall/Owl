# $Owl: Owl/packages/procps-ng/procps-ng.spec,v 1.2.2.2 2018/05/23 17:37:01 solar Exp $

Summary: Utilities for monitoring your system and processes on your system.
Name: procps-ng
Version: 3.3.14
Release: owl1
License: GPL and LGPL
Group: System Environment/Base
URL: https://sourceforge.net/projects/procps-ng/
# Also https://gitlab.com/procps-ng
Source: https://netcologne.dl.sourceforge.net/project/procps-ng/Production/procps-ng-3.3.14.tar.xz
Patch0: procps-ng-3.3.14-qualys-fixes.diff
Patch1: procps-ng-3.3.14-owl-portability.diff
Requires(post,postun): /sbin/ldconfig
Provides: procps
Obsoletes: procps
BuildRequires: ncurses-devel
BuildRoot: /override/%name-%version

%description
The procps-ng package contains a set of system utilities which provide
system information.  These include: free, pgrep, pkill, pmap, ps, pwdx,
skill, slabtop, snice, sysctl, tload, top, uptime, vmstat, w, and watch.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{expand:%%define optflags %optflags -Wall}

%build
%configure \
	--exec-prefix=/ \
	--docdir=/unwanted \
	--disable-static \
	--disable-w-from \
	--disable-kill \
	--enable-skill \
	--enable-sigwinch \
	--disable-modern-top
%__make LDFLAGS=-ltinfo

%check
%__make check

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot
# For compatibility with scripts that might refer to /bin/ps and /sbin/sysctl
mkdir %buildroot/{bin,sbin}
ln -s ..%_bindir/ps %buildroot/bin/
ln -s ..%_sbindir/sysctl %buildroot/sbin/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS NEWS Documentation/FAQ Documentation/TODO
%_libdir/libprocps.so.*
%_bindir/*
%_sbindir/*
/bin/ps
/sbin/sysctl
%_mandir/man[158]/*
%_datadir/locale/*/LC_MESSAGES/*.mo
%exclude /unwanted
%exclude %_libdir/libprocps.la
# Fedora has the below in -devel subpackage
%exclude %_libdir/libprocps.so
%exclude %_libdir/pkgconfig/libprocps.pc
%exclude %_includedir/proc
%exclude %_mandir/man3

%changelog
* Wed May 23 2018 Solar Designer <solar-at-owl.openwall.com> 3.3.14-owl1
- Created this spec file for procps-ng based on Owl's spec file for procps,
but with configure options and list of files to package based on Fedora's.
- Dropped all of our patches, replacing them with a cumulative Qualys patch
(combining their 126 patches into one) fixing the security issues and more,
and a new Owl patch for portability to our old glibc.

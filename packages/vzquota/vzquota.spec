# $Owl: Owl/packages/vzquota/vzquota.spec,v 1.1 2009/10/27 16:18:22 ldv Exp $

Summary: OpenVZ disk quota control utilities.
Name: vzquota
Version: 3.0.12
Release: owl1
License: GPLv2+
Group: System Environment/Kernel
URL: http://openvz.org/
Source: http://download.openvz.org/utils/%name/%version/src/%name-%version.tar.bz2
Patch: vzquota-3.0.12-up-20090519.diff
BuildRoot: /override/%name-%version

%description
This package contains utilities to control OpenVZ disk quotas:
+ vzdqcheck: counts disk usage,
+ vzdqdump: dumps user/group quotas,
+ vzdqload: loads user/group quotas,
+ vzquota: manipulates disk quotas.

%prep
%setup -q
%patch -p1

%build
CFLAGS="%optflags" %__make VARDIR=/var/lib

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot MANDIR=%_mandir VARDIR=/var/lib

%files
%defattr(-,root,root)
%_sbindir/vz*
%_mandir/man8/vz*
/var/lib/vz*

%changelog
* Tue Oct 27 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.0.12-owl1
- Initial revision.

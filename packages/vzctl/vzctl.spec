# $Owl: Owl/packages/vzctl/vzctl.spec,v 1.9 2012/02/27 06:51:50 solar Exp $

Summary: OpenVZ containers control utility.
Name: vzctl
Version: 3.0.23
Release: owl8
License: GPLv2+
Group: System Environment/Kernel
URL: http://openvz.org/
Source: http://download.openvz.org/utils/%name/%version/src/%name-%version.tar.bz2
Patch0: vzctl-3.0.23-owl-PATH.diff
Patch1: vzctl-3.0.23-owl-config.diff
Patch2: vzctl-3.0.23-owl-startup.diff
Patch3: vzctl-3.0.23-owl-veip.diff
Patch4: vzctl-3.0.23-alt-postcreate.diff
Patch5: vzctl-3.0.23-owl-cron.diff
Patch6: vzctl-3.0.23-owl-mtab-mode.diff
Patch7: vzctl-3.0.23-owl-vps-create.diff
PreReq: /sbin/chkconfig
Requires: vzquota
BuildRoot: /override/%name-%version

%description
vzctl utility allows system administator to control OpenVZ containers,
i.e. create, start, shutdown, set various options and limits etc.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%{expand:%%define optflags %optflags -fno-strict-aliasing}

%build
%configure \
	--disable-bashcomp \
	--enable-logrotate \
	--disable-udev \
	--disable-static
%__make

%install
make install install-redhat DESTDIR=%buildroot initddir=%_initrddir
rm %buildroot%_libdir/libvzctl.*
mkdir -p %buildroot/etc/cron.d/
touch %buildroot/etc/cron.d/vz

%post
if [ $1 -eq 1 ]; then
        /sbin/chkconfig --add vz
fi

%preun
if [ $1 = 0 ]; then
	/sbin/chkconfig --del vz
fi

%files
%defattr(-,root,root,700)
%config %_initrddir/vz
%config(noreplace) /etc/logrotate.d/*
%_sbindir/*
%_libdir/lib*
%_libdir/vzctl
%_datadir/vzctl
%_mandir/man?/*
%dir /etc/vz
%dir /etc/vz/names
%config(noreplace) /etc/vz/vz.conf
%config(noreplace) /etc/vz/cron
%config /etc/vz/conf
%config /etc/vz/dists
%config /etc/sysconfig/network-scripts/*
%ghost /etc/cron.d/vz
/var/run/vzctl
/vz
%dev(c,126,0) %attr(600,root,root) /dev/vzctl

%changelog
* Mon Feb 27 2012 Solar Designer <solar-at-owl.openwall.com> 3.0.23-owl8
- Don't enable the "vz" service by default, but initialize OpenVZ even when no
containers are configured to start if the service is started anyway (this
reverts the change made in 3.0.23-owl3).
- In the quota file update cron job, pass the "-t" option to "vzquota stat"
such that per-user and per-group disk usage and quotas are actually updated.

* Sun Oct 09 2011 Solar Designer <solar-at-owl.openwall.com> 3.0.23-owl7
- No longer set MODULES_DISABLED=yes in the default config since our new
kernels use modules for OpenVZ stuff just like OpenVZ's official kernels do.

* Mon Dec 06 2010 Solar Designer <solar-at-owl.openwall.com> 3.0.23-owl6
- Corrected the way /etc/cron.d/vz is created such that /etc/cron.d's mtime
is changed, which is needed for our crond to actually notice the file.
- Added a cron job to update quota files (in case the system crashes).
- Staggered the cron jobs (don't run more than one on a given minute).
- When creating a new container, pass the "--numeric-owner -Sp" options to tar
extracting the template, in addition to the options that were used previously.
- Set the new container's root directory permissions to 755 regardless of the
current umask and of permissions for "." or "/" that might be in the tarball.
- In *set_ugid_quota.sh scripts, set the permissions on /etc/mtab to 644
regardless of the current umask.

* Mon Nov 30 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.0.23-owl5
- Imported ALT's enhancements to the postcreate.sh script.

* Sat Nov 28 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.0.23-owl4
- Moved veip runtime directory from /var/lib/vzctl/ to /var/run/vzctl/.

* Mon Nov 23 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.0.23-owl3
- Changed startup script to skip OpenVZ initialization if there are no
containers to start.

* Mon Nov 23 2009 Solar Designer <solar-at-owl.openwall.com> 3.0.23-owl2
- Set MODULES_DISABLED=yes in the default config to match our default kernel.

* Sun Nov 22 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.0.23-owl1
- Initial revision.

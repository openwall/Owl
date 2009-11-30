# $Owl: Owl/packages/vzctl/vzctl.spec,v 1.5 2009/11/30 12:49:00 ldv Exp $

Summary: OpenVZ containers control utility.
Name: vzctl
Version: 3.0.23
Release: owl5
License: GPLv2+
Group: System Environment/Kernel
URL: http://openvz.org/
Source: http://download.openvz.org/utils/%name/%version/src/%name-%version.tar.bz2
Patch0: vzctl-3.0.23-owl-PATH.diff
Patch1: vzctl-3.0.23-owl-config.diff
Patch2: vzctl-3.0.23-owl-startup.diff
Patch3: vzctl-3.0.23-owl-veip.diff
Patch4: vzctl-3.0.23-alt-postcreate.diff
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

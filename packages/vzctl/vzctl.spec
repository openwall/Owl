# $Owl: Owl/packages/vzctl/vzctl.spec,v 1.1 2009/11/22 21:27:21 ldv Exp $

Summary: OpenVZ containers control utility.
Name: vzctl
Version: 3.0.23
Release: owl1
License: GPLv2+
Group: System Environment/Kernel
URL: http://openvz.org/
Source: http://download.openvz.org/utils/%name/%version/src/%name-%version.tar.bz2
Patch: vzctl-3.0.23-owl-PATH.diff
PreReq: /sbin/chkconfig
Requires: vzquota
BuildRoot: /override/%name-%version

%description
vzctl utility allows system administator to control OpenVZ containers,
i.e. create, start, shutdown, set various options and limits etc.

%prep
%setup -q
%patch -p1

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
/var/lib/vzctl
/vz
%dev(c,126,0) %attr(600,root,root) /dev/vzctl

%changelog
* Sun Nov 22 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.0.23-owl1
- Initial revision.

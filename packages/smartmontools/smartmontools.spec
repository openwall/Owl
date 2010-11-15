# $Owl: Owl/packages/smartmontools/smartmontools.spec,v 1.4 2010/11/15 21:50:30 solar Exp $

Summary: Control and monitor storage systems using S.M.A.R.T.
Name: smartmontools
Version: 5.40
Release: owl2
License: GPL
Group: System Environment/Daemons
URL: http://smartmontools.sourceforge.net/
Source0: smartmontools-%version.tar.xz
# http://prdownloads.sourceforge.net/smartmontools/smartmontools-%version.tar.gz
Source1: smartd.init
Source2: smartd.sysconfig
Patch0: smartmontools-5.40-up-megaraid-segfault.diff
PreReq: /sbin/chkconfig
Requires: mailx
BuildRequires: sed >= 4.1
BuildRoot: /override/%name-%version

%description
This package contains two utility programs (smartctl and smartd) to
control and monitor storage systems using the Self-Monitoring, Analysis
and Reporting Technology System (S.M.A.R.T.) built into most modern
ATA and SCSI hard disks.  It is derived from the smartsuite package,
and includes support for ATA/ATAPI-5 disks.

%prep
%setup -q
%patch0 -p2
fgrep -lZ /usr/local/bin/mail *.in |
	xargs -r0 sed -i 's,/usr/local/bin/mail,/bin/mail,g' --

%{expand:%%define optflags %optflags -Wall}

%build
%configure \
	--with-docdir=%buildroot/%_docdir/%name-%version
%__make

%install
rm -rf %buildroot
%makeinstall

# remove upstream init scripts
rm -r %buildroot/etc/rc.d

chmod 600 %buildroot/etc/smartd.conf
install -pD -m700 %_sourcedir/smartd.init \
	%buildroot/etc/rc.d/init.d/smartd
install -pD -m600 %_sourcedir/smartd.sysconfig \
	%buildroot/etc/sysconfig/smartd

%pre
rm -f /var/run/smartd.restart
if [ $1 -ge 2 ] && /etc/rc.d/init.d/smartd status; then
	touch /var/run/smartd.restart || :
	/etc/rc.d/init.d/smartd stop || :
fi

%post
/sbin/chkconfig --add smartd
if [ -f /var/run/smartd.restart ]; then
	/etc/rc.d/init.d/smartd start
elif [ -f /var/run/smartd.pid ]; then
	/etc/rc.d/init.d/smartd restart
fi
rm -f /var/run/smartd.restart

%preun
if [ $1 -eq 0 ]; then
	/etc/rc.d/init.d/smartd stop || :
	/sbin/chkconfig --del smartd
fi

%files
%defattr(-,root,root)
%_sbindir/*
%exclude %_sbindir/update-smart-drivedb
%_mandir/man?/*
%config /etc/rc.d/init.d/smartd
%config(noreplace) /etc/smartd.conf
%config(noreplace) /etc/sysconfig/smartd
%_datadir/%name/
%_docdir/%name-%version/
%exclude %_docdir/%name-%version/CHANGELOG
%exclude %_docdir/%name-%version/INSTALL

%changelog
* Mon Nov 15 2010 Solar Designer <solar-at-owl.openwall.com> 5.40-owl2
- Added upstream's change:
"Linux megaraid: Fix segfault on non-data commands (Ticket #78)".

* Fri Nov 12 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 5.40-owl1
- Updated to 5.40.
- Dropped all patches (fixed in upstream).

* Mon Jun 12 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.36-owl1
- Initial revision, based on smartmontools-5.36-alt2 package from Sisyphus.

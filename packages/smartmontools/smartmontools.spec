# $Owl: Owl/packages/smartmontools/smartmontools.spec,v 1.2 2006/06/12 22:16:51 ldv Exp $

Summary: Control and monitor storage systems using S.M.A.R.T.
Name: smartmontools
Version: 5.36
Release: owl1
License: GPL
Group: System Environment/Daemons
URL: http://smartmontools.sourceforge.net/
Source0: http://prdownloads.sourceforge.net/smartmontools/smartmontools-%version.tar.gz
Source1: smartd.init
Source2: smartd.sysconfig
Patch0: smartmontools-5.36-cvs-20060414-wd-attr-190.diff
Patch1: smartmontools-5.36-cvs-20060415-vpd-page-0x83-size.diff
Patch2: smartmontools-5.36-cvs-20060415-libata-2.6.17-id.diff
Patch3: smartmontools-5.36-cvs-20060609-seagate-momentus.diff
Patch4: smartmontools-5.36-deb-cciss.diff
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
fgrep -lZ /usr/local/bin/mail *.in |
	xargs -r0 sed -i 's,/usr/local/bin/mail,/bin/mail,g' --

%{expand:%%define optflags %optflags -Wall}

%build
%configure
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

%define docdir %_docdir/%name-%version
bzip2 -9 %buildroot%docdir/CHANGELOG
rm %buildroot%docdir/INSTALL

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
%_mandir/man?/*
%config /etc/rc.d/init.d/smartd
%config(noreplace) /etc/smartd.conf
%config(noreplace) /etc/sysconfig/smartd
%docdir

%changelog
* Mon Jun 12 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.36-owl1
- Initial revision, based on smartmontools-5.36-alt2 package from Sisyphus.

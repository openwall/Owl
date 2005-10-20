Summary: NTP Time Synchronization Client 
Name: openntpd
Version: 3.7p1
Release: owl1
License: BSD License
Group: System Environment/Daemons
URL: http://www.openntpd.org
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenNTPD/%name-%version.tar.gz
Source1: %name.init
Source2: %name.control
Prefix: %_prefix
BuildRoot: /override/%name-%version

BuildRequires: openssl-devel
PreReq: /var/empty
PreReq: shadow-utils
PreReq: coreutils
PreReq: owl-control >= 0.4, owl-control <= 2.0
Requires: chkconfig
Requires: openssl

%description
NTP Time Synchronization Server and Client - http://www.openntpd.org

%prep
%setup -q

%build
%configure \
	--with-privsep-user=ntpd \
	--with-privsep-dir=/var/empty

%__make

%install
rm -rf "%buildroot"
%__make install DESTDIR="%buildroot" INSTALL="install -p"
mkdir -p "%buildroot%_sysconfdir/init.d"
install -p -m755 "%SOURCE1" "%buildroot%_sysconfdir/init.d/ntpd"
mkdir -p "%buildroot%_sysconfdir/control.d/facilities"
install -p -m755 "%SOURCE2" "%buildroot%_sysconfdir/control.d/facilities/ntpd"

%pre
if [ \
	0"$(/usr/bin/id -u xntpd 2>/dev/null)" -eq 185 -a \
	0"$(/usr/bin/id -g xntpd 2>/dev/null)" -eq 185 -a \
	-z "$(/usr/bin/id -un ntpd 2>/dev/null)" -a \
	-z "$(/bin/grep '^ntpd:' %_sysconfdir/group 2>/dev/null)" \
]; then
	echo -n "Renaming the 'xntpd' group to 'ntpd' ... "
	/usr/sbin/groupmod -n ntpd xntpd && echo "Done"
	echo -n "Renaming the 'xntpd' user to 'ntpd' ... "
	/usr/sbin/usermod -l ntpd xntpd && echo "Done"
fi

/bin/grep '^ntpd:' %_sysconfdir/group &>/dev/null || groupadd -g 185 ntpd
/usr/bin/id ntpd &>/dev/null || /usr/sbin/useradd -u 185 -g ntpd -s /bin/false -d / ntpd

if [ $1 -ge 2 ]; then
	%_sbindir/control-dump ntpd
	if /sbin/service ntpd status &>/dev/null; then
		touch /var/run/ntpd.restart || :
		/sbin/service ntpd stop || :
	fi
fi

%post
if [ $1 -eq 2 ]; then
	%_sbindir/control-restore ntpd
fi
/sbin/chkconfig --add ntpd
test -f /var/run/ntpd.restart && /sbin/service ntpd start || :
rm -f /var/run/ntpd.restart

%preun
if [ $1 -eq 0 ]; then
	/sbin/service ntpd stop || :
	/sbin/chkconfig --del ntpd
fi

%files
%defattr(-,root,root,0755)
%doc ChangeLog CREDITS README LICENCE
%config(noreplace) %_sysconfdir/ntpd.conf
%config %_sysconfdir/init.d/ntpd
%_sysconfdir/control.d/facilities/ntpd
%_sbindir/*
%_mandir/man?/*

%changelog
* Wed Oct 19 2005 (GalaxyMaster) <galaxy at owl.openwall.com> 3.7p1-owl1
- Added a logic to rename the 'xntpd' account to 'ntpd'.
- Added openntpd.control to put ntpd under the control of owl-control.

* Fri Sep 09 2005 (GalaxyMaster) <galaxy at owl.openwall.com> 3.7p1-owl0
- Initial release for Owl.


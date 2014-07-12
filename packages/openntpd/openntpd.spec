# $Owl: Owl/packages/openntpd/openntpd.spec,v 1.15 2014/07/12 14:14:50 galaxy Exp $

Summary: NTP time synchronization server and client.
Name: openntpd
Version: 3.7p1
Release: owl6
License: BSD License
Group: System Environment/Daemons
URL: http://www.openntpd.org
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenNTPD/%name-%version.tar.gz
Source1: openntpd.init
Source2: openntpd.control
Patch0: openntpd-3.7p1-owl-chroot.diff
Patch1: openntpd-3.7p1-cvs-20050524-listen_all-skip-NULL.diff
Prefix: %_prefix
Requires(pre): /var/empty, shadow-utils, coreutils, grep
Requires(pre,post): owl-control >= 0.4, owl-control < 2.0
Requires(post,preun): chkconfig
Requires: openssl
BuildRequires: rpm-build >= 0:4.11
BuildRequires: openssl-devel
BuildRoot: /override/%name-%version

%description
NTP time synchronization server and client - http://www.openntpd.org

The ntpd daemon synchronizes the local clock to one or more remote NTP
servers, and can also act as an NTP server itself, redistributing the
local time.  It implements the Simple Network Time Protocol version 4, as
described in RFC 2030, and the Network Time Protocol version 3, as
described in RFC 1305.

%prep
%setup -q
%patch0 -p1
%patch1 -p3
bzip2 -9k ChangeLog

%build
autoreconf -f
%configure \
	--with-privsep-user=ntpd \
	--with-privsep-path=/var/empty

%__make

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot INSTALL="install -p"
mkdir -p %buildroot%_initddir
install -p -m755 %_sourcedir/openntpd.init %buildroot%_initddir/ntpd
mkdir -p %buildroot%_sysconfdir/control.d/facilities
install -p -m755 %_sourcedir/openntpd.control \
	%buildroot%_sysconfdir/control.d/facilities/ntpd

%pre
if [ \
	0"$(id -u xntpd 2>/dev/null)" -eq 185 -a \
	0"$(id -g xntpd 2>/dev/null)" -eq 185 -a \
	-z "$(id -un ntpd 2>/dev/null)" -a \
	-z "$(grep -q '^ntpd:' /etc/group)" \
]; then
	echo -n "Renaming the 'xntpd' group to 'ntpd' ... "
	groupmod -n ntpd xntpd && echo "Done"
	echo -n "Renaming the 'xntpd' user to 'ntpd' ... "
	usermod -l ntpd xntpd && echo "Done"
fi

grep -q '^ntpd:' /etc/group || groupadd -g 185 ntpd
id ntpd &>/dev/null || useradd -u 185 -g ntpd -s /bin/false -d / ntpd

if [ $1 -ge 2 ]; then
	%_sbindir/control-dump ntpd
	if /sbin/service ntpd status &>/dev/null; then
		touch /var/run/ntpd.restart
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
%doc CREDITS ChangeLog.bz2 LICENCE README
%config(noreplace) %_sysconfdir/ntpd.conf
%config %_initddir/ntpd
%_sysconfdir/control.d/facilities/ntpd
%_sbindir/*
%_mandir/man?/*

%changelog
* Mon Jun 30 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.7p1-owl6
- Replaced the deprecated PreReq tag with Requires().
- Replaced the deprecated %%_initrddir macro with %%_initddir.

* Mon Sep 18 2006 Solar Designer <solar-at-owl.openwall.com> 3.7p1-owl5
- Use the %%_initrddir macro.
- Adjusted the init script for consistency with the majority of other ones
in Owl.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.7p1-owl4
- Compressed ChangeLog file.

* Wed Jan 18 2006 Solar Designer <solar-at-owl.openwall.com> 3.7p1-owl3
- Back-ported a fix from the OpenBSD CVS to skip address-less interfaces
with "listen on *"; thanks to Bernhard Fischer for reporting this to us.

* Fri Oct 21 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.7p1-owl2
- Fixed a typo in the configure option name.
- Applied a patch to honor --with-privsep-path in configure.

* Wed Oct 19 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.7p1-owl1
- Added a logic to rename the 'xntpd' account to 'ntpd'.
- Added openntpd.control to put ntpd under the control of owl-control.

* Fri Sep 09 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.7p1-owl0
- Initial release for Owl.

# $Id: Owl/packages/scanlogd/Attic/scanlogd.spec,v 1.1 2001/07/12 01:54:57 solar Exp $

Summary: A tool to detect and log TCP port scans
Name: scanlogd
Version: 2.2
Release: 1owl
License: relaxed BSD and (L)GPL-compatible
Group: System Environment/Daemons
URL: http://www.openwall.com/scanlogd/
Source0: ftp://ftp.openwall.com/pub/projects/scanlogd/scanlogd-%{version}.tar.gz
Source1: scanlogd.init
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Prereq: /sbin/chkconfig, /dev/null, grep, shadow-utils

%description
scanlogd detects port scans and writes one line per scan via the syslog(3)
mechanism.  If a source address sends multiple packets to different ports
in a short time, the event will be logged.

%prep
%setup -q

%build
make linux CFLAGS="-c -Wall $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%_sbindir,%_mandir/man8,etc/rc.d/init.d}

install -m 700 scanlogd $RPM_BUILD_ROOT/%_sbindir
install -m 644 scanlogd.8 $RPM_BUILD_ROOT/%_mandir/man8
install -m 700 $RPM_SOURCE_DIR/scanlogd.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/scanlogd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep -q ^scanlogd: /etc/group || groupadd -g 199 scanlogd
grep -q ^scanlogd: /etc/passwd ||
	useradd -g scanlogd -u 199 -d / -s /bin/false -M scanlogd
rm -f /var/run/scanlogd.restart
if [ $1 -ge 2 ]; then
	/etc/rc.d/init.d/scanlogd status && touch /var/run/scanlogd.restart || :
	/etc/rc.d/init.d/scanlogd stop || :
fi

%post
test -f /var/run/scanlogd.restart && /etc/rc.d/init.d/scanlogd start || :
rm -f /var/run/scanlogd.restart

%preun
if [ $1 -eq 0 ]; then
	/etc/rc.d/init.d/scanlogd stop || :
	/sbin/chkconfig --del scanlogd
fi

%files
%defattr(-,root,root)
%_sbindir/scanlogd
%_mandir/man8/scanlogd.8*
%config /etc/rc.d/init.d/scanlogd

%changelog
* Thu Jul 12 2001 Solar Designer <solar@owl.openwall.com>
- Packaged scanlogd for Owl.

# $Id: Owl/packages/xinetd/xinetd.spec,v 1.5.2.1 2001/06/29 20:40:56 solar Exp $

%define NEED_PYTHON 'no'

Summary: The extended Internet services daemon
Name: xinetd
Version: 2.3.0
Release: 1owl
License: BSD with minor restrictions
Group: System Environment/Daemons
Source0: http://www.xinetd.org/xinetd-%{version}.tar.gz
Source1: xinetd.init
Source2: xinetd.conf
Source3: xinetd-inetdconvert
Source4: xinetd-ttime
Source5: xinetd-utime
Source6: xinetd-tdtime
Source7: xinetd-udtime
Source8: xinetd-echo
Source9: xinetd-uecho
Source10: xinetd-chargen
Source11: xinetd-uchargen
Provides: inetd
Prereq: /sbin/chkconfig /etc/init.d
BuildRequires: tcp_wrappers
URL: http://www.xinetd.org/
BuildRoot: /var/rpm-buildroot/%{name}-root
Obsoletes: inetd

%description
xinetd performs the same function as inetd: it starts programs that
provide Internet services.  Instead of having such servers started at
system initialization time, and be dormant until a connection request
arrives, xinetd is the only daemon process started and it listens on
all service ports for the services listed in its configuration file.
When a request comes in, xinetd starts the appropriate server.  Because
of the way it operates, xinetd (as well as inetd) is also referred to
as a super-server.

xinetd has access control machanisms, extensive logging capabilities,
the ability to make services available based on time, and can place
limits on the number of servers that can be started, among other things.

%prep
%setup -q

%build
autoconf
%configure --with-libwrap
make CC=gcc

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
%makeinstall \
	DAEMONDIR=$RPM_BUILD_ROOT/usr/sbin MANDIR=$RPM_BUILD_ROOT/%{_mandir}
mkdir -p $RPM_BUILD_ROOT/etc/xinetd.d/
install -m 755 %SOURCE1 $RPM_BUILD_ROOT/etc/rc.d/init.d/xinetd
install -m 644 %SOURCE2 $RPM_BUILD_ROOT/etc/xinetd.conf
%if "%{NEED_PYTHON}"=="'yes'"
install -m 755 %SOURCE3 $RPM_BUILD_ROOT/usr/sbin/inetdconvert
%endif
install -m 644 %SOURCE4 $RPM_BUILD_ROOT/etc/xinetd.d/time
install -m 644 %SOURCE5 $RPM_BUILD_ROOT/etc/xinetd.d/time-udp
install -m 644 %SOURCE6 $RPM_BUILD_ROOT/etc/xinetd.d/daytime
install -m 644 %SOURCE7 $RPM_BUILD_ROOT/etc/xinetd.d/daytime-udp
install -m 644 %SOURCE8 $RPM_BUILD_ROOT/etc/xinetd.d/echo
install -m 644 %SOURCE9 $RPM_BUILD_ROOT/etc/xinetd.d/echo-udp
install -m 644 %SOURCE10 $RPM_BUILD_ROOT/etc/xinetd.d/chargen
install -m 644 %SOURCE11 $RPM_BUILD_ROOT/etc/xinetd.d/chargen-udp

rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/itox*
rm -f $RPM_BUILD_ROOT/usr/sbin/itox
rm -f $RPM_BUILD_ROOT/usr/sbin/xconv.pl

%clean
rm -rf $RPM_BUILD_ROOT

%pre
rm -f /var/run/xinetd.restart
if [ $1 -ge 2 ]; then
	/etc/rc.d/init.d/xinetd status && touch /var/run/xinetd.restart || :
	/etc/rc.d/init.d/xinetd stop || :
fi

%post
if [ $1 -eq 1 ]; then
	/sbin/chkconfig --add xinetd
fi
if [ -f /var/run/xinetd.restart ]; then
	/etc/rc.d/init.d/xinetd start
fi
rm -f /var/run/xinetd.restart

%preun
if [ $1 -eq 0 ]; then
	/etc/rc.d/init.d/xinetd stop || :
	/sbin/chkconfig --del xinetd
fi

%files
%defattr(-,root,root)
%doc INSTALL xinetd/CHANGELOG xinetd/COPYRIGHT README xinetd/sample.conf

%config /etc/xinetd.conf
/usr/sbin/*
%{_mandir}/*/*
%config /etc/rc.d/init.d/xinetd
%config /etc/xinetd.d/*

%changelog
* Fri Jun 29 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 2.3.0, which fixes the problem with xinetd's string handling
routines discovered by Sebastian Krahmer of SuSE Security Team.
- Dropped the 2.1.8.9pre15 patches (incorporated into 2.1.8.9pre16+).

* Tue Jun 12 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 2.1.8.9pre15.
- With includedir, skip all files with names containing a dot ('.') or
ending with a tilde ('~'); this replaces the Red Hat Linux derived patch.
- Minor man page fixes.

* Wed May 30 2001 Solar Designer <solar@owl.openwall.com>
- Ensure the umask is no less restrictive than 022.

* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- Corrected the use of "--" in the startup script.

* Fri Dec 15 2000 Solar Designer <solar@owl.openwall.com>
- Changed the default xinetd.conf.
- Startup script cleanups.
- Restart after package upgrades in an owl-startup compatible way.

* Mon Dec 11 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import
- xinetd.init -> owl-startup
- 2.1.8.9pre13

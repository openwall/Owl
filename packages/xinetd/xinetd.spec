# $Id: Owl/packages/xinetd/xinetd.spec,v 1.16 2002/08/10 21:31:25 solar Exp $

Summary: The extended Internet services daemon.
Name: xinetd
Version: 2.3.6
Release: owl1
License: BSD with minor restrictions
Group: System Environment/Daemons
URL: http://www.xinetd.org
Source0: http://www.xinetd.org/xinetd-%{version}.tar.gz
Source1: xinetd.init
Source2: xinetd.conf
Source3: xinetd-ttime
Source4: xinetd-utime
Source5: xinetd-tdtime
Source6: xinetd-udtime
Source7: xinetd-echo
Source8: xinetd-uecho
Source9: xinetd-chargen
Source10: xinetd-uchargen
Patch0: xinetd-2.3.6-owl-fixes.diff
PreReq: /sbin/chkconfig
Provides: inetd
Obsoletes: inetd
BuildRequires: tcp_wrappers
BuildRoot: /override/%{name}-%{version}

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
%patch0 -p1

%{expand:%%define optflags %optflags -Wall -Wno-unused -Wno-switch}

%build
%configure --with-libwrap
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/{rc.d/init.d,xinetd.d}
%makeinstall \
	DAEMONDIR=$RPM_BUILD_ROOT/usr/sbin MANDIR=$RPM_BUILD_ROOT%{_mandir}

cd $RPM_BUILD_ROOT

install -m 755 $RPM_SOURCE_DIR/xinetd.init etc/rc.d/init.d/xinetd
install -m 644 $RPM_SOURCE_DIR/xinetd.conf etc/
install -m 644 $RPM_SOURCE_DIR/xinetd-ttime etc/xinetd.d/time
install -m 644 $RPM_SOURCE_DIR/xinetd-utime etc/xinetd.d/time-udp
install -m 644 $RPM_SOURCE_DIR/xinetd-tdtime etc/xinetd.d/daytime
install -m 644 $RPM_SOURCE_DIR/xinetd-udtime etc/xinetd.d/daytime-udp
install -m 644 $RPM_SOURCE_DIR/xinetd-echo etc/xinetd.d/echo
install -m 644 $RPM_SOURCE_DIR/xinetd-uecho etc/xinetd.d/echo-udp
install -m 644 $RPM_SOURCE_DIR/xinetd-chargen etc/xinetd.d/chargen
install -m 644 $RPM_SOURCE_DIR/xinetd-uchargen etc/xinetd.d/chargen-udp

rm usr/sbin/{itox,xconv.pl} .%{_mandir}/man8/{itox,xconv.pl}.8*

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
%doc README AUDIT xinetd/CHANGELOG xinetd/COPYRIGHT xinetd/sample.conf
%config /etc/xinetd.conf
/usr/sbin/*
%{_mandir}/*/*
%config /etc/rc.d/init.d/xinetd
%config /etc/xinetd.d/*

%changelog
* Sun Aug 11 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 2.3.6 adding fixes or workarounds for issues introduced after
2.3.3 including the signal pipe leak into child processes (a security hole
with 2.3.4+).
- Made xinetd also unlink its PID file when exiting on reload.

* Sat Feb 02 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.
- Dropped the unused xinetd-inetdconvert.

* Mon Nov 05 2001 Solar Designer <solar@owl.openwall.com>
- /etc/init.d -> /etc/rc.d/init.d for consistency.

* Thu Aug 30 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 2.3.3.
- Dropped the big -audit patch all of which went into xinetd 2.3.1+.
- Added the unlinking of PID file when exiting due to no services.

* Sat Jul 28 2001 Solar Designer <solar@owl.openwall.com>
- Handle the case of nonexistent /etc/sysconfig/network correctly.
- Don't -stayalive, we may invent a reload-or-start option instead.

* Sun Jul 22 2001 Solar Designer <solar@owl.openwall.com>
- Updated the -audit patch based on results of testing by Michail Litvak
<mci@owl.openwall.com>, by ALT Linux Team, and at DataForce ISP.

* Thu Jul 05 2001 Solar Designer <solar@owl.openwall.com>
- Applied _many_ security and reliability fixes (in fact so many that
there have to be new bugs as well and testing is needed), see AUDIT.
The patch is 100 KB large.

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

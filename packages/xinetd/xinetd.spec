# $Id: Owl/packages/xinetd/xinetd.spec,v 1.4 2000/12/15 03:59:50 solar Exp $

%define NEED_PYTHON 'no'

Summary: 	A secure replacement for inetd.
Name: 		xinetd
Version: 	2.1.8.9pre13
Release: 	3owl
License: 	Distributable (BSD-like)
Group: 		System Environment/Daemons
Source: 	http://www.xinetd.org/xinetd-%{version}.tar.gz
Source1: 	xinetd.init
Source2: 	xinetd.conf
Source3:	xinetd-inetdconvert
Source4: 	xinetd-ttime
Source5: 	xinetd-utime
Source6: 	xinetd-tdtime
Source7: 	xinetd-udtime
Source8: 	xinetd-echo
Source9: 	xinetd-uecho
Source10: 	xinetd-chargen
Source11: 	xinetd-uchargen
Patch0: 	xinetd-2.1.8.9pre10-rh-skipjunkfiles.diff
Provides: 	inetd
Prereq: 	/sbin/chkconfig /etc/init.d
BuildRequires: 	tcp_wrappers
URL: 		http://www.xinetd.org/
BuildRoot: 	/var/rpm-buildroot/%{name}-root
Obsoletes: 	inetd

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

%build
autoconf
%configure --with-libwrap
make

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
* Fri Dec 15 2000 Solar Designer <solar@owl.openwall.com>
- Changed the default xinetd.conf.
- Startup script cleanups.
- Restart after package upgrades in an owl-startup compatible way.

* Mon Dec 11 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import
- xinetd.init -> owl-startup
- 2.1.8.9pre13

* Tue Oct 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.8.9pre11, which includes the previous bugfixes.
- don't convert the internal services, include 
  such files with xinetd (#17331, #18899)

* Mon Oct 09 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Add patch to fix segfault problem (#18686)

* Fri Oct 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- apply patch from nalin@redhat.com for handling tcp
  connections with wait=yes properly

* Tue Sep 26 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add explicit dependency on a modern version of initscripts 
  (#17533)

* Wed Aug 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.8.9pre10 - remove tcpwrapper and pidfile patches,
  as they are now in.
- change default startup position to 56, so it 
  starts after bind (#17047)

* Thu Aug 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use the server name not the service name for libwrap
  checking (#16516). The new way was better, but
  this is sacrificed so old systems will continue to work
  and the documentation for tcp_wrappers can be correct.

* Wed Aug 16 2000 Than Ngo <than@redhat.com>
- fix initscript, test network file before source it (Bug #16247)

* Tue Aug 15 2000 Trond Eivind Glomsrød <teg@redhat.com
- make the pidfile 0644, not 0300 (#16256)

* Tue Aug 08 2000 Trond Eivind Glomsrød <teg@redhat.com>
- added support for "-pidfile" option (#15531)

* Fri Aug 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- added patch to ignore .rpmsave, .rpmorig, .rpmnew, ~ 
  suffixed files (#15304)

* Thu Aug 03 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.8.9pre9, old patches are now integrated.

* Wed Aug 02 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix converting of "wait" argument (#13884) 
- remove tcpd and /usr/sbin/tcpd from inetd.conf services
  before converting - xinetd is linked against tcp_wrappers 

* Mon Jul 31 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix linuxconf restart problem (#14856)
- fix conditional restart
- mark /etc/xinetd.conf as a configuration file

* Tue Jul 25 2000 Bill Nottingham <notting@redhat.com>
- um, we *need* to prereq /etc/init.d

* Mon Jul 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't require /etc/init.d

* Sat Jul 22 2000 Bill Nottingham <notting@redhat.com>
- rebuild

* Tue Jul 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix the sections of the man pages (#14244)

* Tue Jul 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove itox, as it wouldn't do the right thing with our
  configuration
- same with xconv.pl
- some changes to the installation process

* Mon Jul 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- move initscript back to /etc/rc.d/init.d

* Fri Jul 14 2000 Trond Eivind Glomsrød <teg@redhat.com>
- change process name in init file

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- start the daemon with the "-reuse" flag

* Thu Jul 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- "Prereq:", not "Requires:" for /etc/init.d

* Wed Jul 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- require /etc/init.d

* Wed Jul  5 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- upper the number of instances to 60

* Sun Jul  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix a memory-allocation bug

* Wed Jun 28 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.8.9pre8

* Wed Jun 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- moved to /etc/init.d

* Wed Jun 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- changed specfile and initfile to implement conditional
  restart

* Sun Jun 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.8.9pre7
- now obsoletes inetd
- use %%{_tmppath}

* Sun Jun 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.8.9pre6
- added converter script which can convert specified or 
  remaing uncoverted services
- use %%{_mandir}
- removed +x on xinetd.conf

* Wed May 24 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.8.9pre4
- authpriv patch no longer needed

* Tue May 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- /etc/xinetd.d is now part of the filesystem package
- more fixes to xinetd.init

* Mon May 22 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fixed some obvious bugs in xinetd.init
- added a default xinetd.conf
- patched xinetd to understand LOG_AUTHPRIV

* Fri May 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- updated version
- removed a define %ver (we already have %version)
- removed some extra CFLAGS declarations
- added configuration directory, /etc/xinetd.d

* Mon Feb 21 2000 Tim Powers <timp@redhat.com>
- fixed broken postun sections, should have been *preun*
- fixed broken gzip of manpages

* Wed Jan 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.1.8.8p8
- Fix the init script (Bug #7277)
- remove our patches (no longer required)

* Tue Sep 21 1999 Bill Nottingham <notting@redhat.com>
- add -lnsl

* Tue Sep 7 1999 Tim Powers <timp@redhat.com>
- modification top install routine

* Mon Jul 26 1999 Tim Powers <timp@redhat.com>
- updated source to 2.1.8.6b6
- built for 6.1

* Mon Apr 26 1999 Bill Nottingham <notting@redhat.com>
- update to 2.1.8.6b5
- build for PowerTools

* Mon Jan 10 1999 Bill Nottingham <notting@redhat.com>
- update to 2.1.8.5p2

* Tue Dec  1 1998 Bill Nottingham <notting@redhat.com>
- intial build

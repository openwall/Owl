# $Id: Owl/packages/net-tools/net-tools.spec,v 1.2 2000/09/07 21:42:41 solar Exp $

Summary: The basic tools for setting up networking.
Name: 		net-tools
Version: 	1.57
Release: 	1owl
Copyright: 	GPL
Group: 		System Environment/Base
Source0: 	http://www.tazenda.demon.co.uk/phil/net-tools/net-tools-%{version}.tar.bz2
Source1: 	net-tools-1.57-config.h
Source2: 	net-tools-1.57-config.make
Patch0: 	net-tools-1.56-rh-fhs.diff
BuildRoot: 	/var/rpm-buildroot/%{name}-root

%description
The net-tools package contains the basic tools needed for setting up
networking:  ethers, route and others.

%prep
%setup -q
%patch0 -p 1 -b .fhs

cp %SOURCE1 ./config.h
cp %SOURCE2 ./config.make

%build
make COPTS="$RPM_OPT_FLAGS -D_GNU_SOURCE -Wall"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{bin,sbin}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{1,5,8}

make BASEDIR=$RPM_BUILD_ROOT mandir=%{_mandir} install

{ cd $RPM_BUILD_ROOT
  strip ./sbin/* ./bin/* || :
} 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/bin/dnsdomainname
/bin/domainname
/bin/hostname
/bin/netstat
/bin/nisdomainname
/bin/ypdomainname
/sbin/arp
/sbin/ifconfig
/sbin/ipmaddr
/sbin/iptunnel
/sbin/mii-tool
/sbin/plipconfig
/sbin/rarp
/sbin/route
/sbin/slattach
%{_mandir}/man[158]/*
%lang(cs)	%{_datadir}/locale/cs/LC_MESSAGES/net-tools.mo
%lang(de)	%{_mandir}/de_DE/man[158]/*
%lang(de)	%{_datadir}/locale/de/LC_MESSAGES/net-tools.mo
%lang(et)	%{_datadir}/locale/et_EE/LC_MESSAGES/net-tools.mo
%lang(fr)	%{_mandir}/fr_FR/man[158]/*
%lang(fr)	%{_datadir}/locale/fr/LC_MESSAGES/net-tools.mo
%lang(pt_BR)	%{_mandir}/pt_BR/man[18]/*
%lang(pt_BR)	%{_datadir}/locale/pt_BR/LC_MESSAGES/net-tools.mo

%changelog
* Thu Sep 07 2000 Solar Designer <solar@owl.openwall.com>
- Use RPM_OPT_FLAGS.

* Wed Aug 09 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- upgrade to 1.57

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun  6 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.56.
- FHS packaging.

* Sat Apr 15 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.55.

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Fri Jan 14 2000 Jeff Johnson <jbj@redhat.com>
- fix "netstat -ci" (#6904).
- document more netstat options (#7429).

* Thu Jan 13 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.54.
- enable "everything but DECnet" including IPv6.

* Sun Aug 29 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.53.

* Wed Jul 28 1999 Jeff Johnson <jbj@redhat.com>
- plug "netstat -c" fd leak (#3620).

* Thu Jun 17 1999 Jeff Johnson <jbj@redhat.com>
- plug potential buffer overruns.

* Sat Jun 12 1999 John Hardin <jhardin@wolfenet.com>
- patch to recognize ESP and GRE protocols for VPN masquerade

* Fri Apr 23 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.52.

* Thu Mar 25 1999 Jeff Johnson <jbj@redhat.com>
- update interface statistics continuously (#1323)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.51.
- strip binaries.

* Tue Feb  2 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.50.
- added slattach/plipconfig/ipmaddr/iptunnel commands.
- enabled translated man pages.

* Tue Dec 15 1998 Jakub Jelinek <jj@ultra.linux.cz>
- update to 1.49.

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.48.

* Thu Nov 12 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.47.

* Wed Sep  2 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.46

* Thu Jul  9 1998 Jeff Johnson <jbj@redhat.com>
- build root
- include ethers.5

* Thu Jun 11 1998 Aron Griffis <agriffis@coat.com>
- upgraded to 1.45
- patched hostname.c to initialize buffer
- patched ax25.c to use kernel headers

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Feb 27 1998 Jason Spangler <jasons@usemail.com>
- added config patch

* Fri Feb 27 1998 Jason Spangler <jasons@usemail.com>
- changed to net-tools 1.432
- removed old glibc 2.1 patch
 
* Wed Oct 22 1997 Erik Troan <ewt@redhat.com>
- added extra patches for glibc 2.1

* Tue Oct 21 1997 Erik Troan <ewt@redhat.com>
- included complete set of network protocols (some were removed for
  initial glibc work)

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- updated glibc patch for glibc 2.0.5

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- updated to 1.33

# $Id: Owl/packages/dhcp/dhcp.spec,v 1.20 2003/09/29 22:54:06 solar Exp $

%define BUILD_DHCP_CLIENT 0

Summary: Dynamic Host Configuration Protocol (DHCP) distribution.
Name: dhcp
Version: 3.0pl2
Release: owl4
License: ISC License
Group: System Environment/Daemons
URL: http://www.isc.org/products/DHCP/
Source0: ftp://ftp.isc.org/isc/dhcp/dhcp-%{version}.tar.gz
Source1: dhcpd.init
Source2: dhcpd.conf.sample
Patch0: dhcp-3.0pl2-owl-man.diff
Patch1: dhcp-3.0pl2-owl-drop-root.diff
Patch2: dhcp-3.0pl2-rh-owl-script.diff
Patch3: dhcp-3.0pl2-owl-warnings.diff
BuildRoot: /override/%{name}-%{version}

%description
The ISC Dynamic Host Configuration Protocol distribution provides a
freely redistributable reference implementation of all aspects of the
DHCP protocol.

%if %BUILD_DHCP_CLIENT
%package client
Summary: The ISC DHCP client.
Group: System Enviroment/Base
PreReq: dhcp = %{version}-%{release}
Obsoletes: dhcpcd

%description client
The Internet Software Consortium DHCP Client, dhclient, provides a
means for configuring one or more network interfaces using the Dynamic
Host Configuration Protocol, BOOTP protocol, or if these protocols
fail, by statically assigning an address.
%endif

%package server
Summary: The ISC DHCP server daemon.
Group: System Environment/Daemons
PreReq: dhcp = %{version}-%{release}
PreReq: /sbin/chkconfig
Obsoletes: dhcpd

%description server
The Internet Software Consortium DHCP Server, dhcpd, implements the
Dynamic Host Configuration Protocol (DHCP) and the Internet Bootstrap
Protocol (BOOTP).  DHCP allows hosts on a TCP/IP network to request
and be assigned IP addresses, and also to discover information about
the network to which they are attached.  BOOTP provides similar
functionality, with certain restrictions.

%package relay
Summary: The ISC DHCP relay.
Group: System Environment/Daemons
PreReq: dhcp = %{version}-%{release}

%description relay
DHCP relay is the Internet Software Consortium (ISC) relay agent for
DHCP packets.  It is used on a subnet with DHCP clients to "relay"
their requests to a subnet that has a DHCP server on it.  Because DHCP
packets can be broadcast, they will not be routed off of the local
subnet.  The DHCP relay takes care of this for the client.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%{expand:%%define optflags %optflags -Wall -Wno-unused}

%ifarch alpha alphaev5 alphaev56 alphapca56 alphaev6 alphaev67
%{expand:%%define optflags %optflags -DPTRSIZE_64BIT}
%endif

%build
./configure --copts "$RPM_OPT_FLAGS"
make CC=gcc DEBUG=

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/{rc.d/init.d}
make install DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}

cd $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
mkdir -p $RPM_BUILD_ROOT/var/lib/dhcp/{dhcpd,dhclient}/state

install -m 700 $RPM_SOURCE_DIR/dhcpd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcpd
install -m 644 $RPM_SOURCE_DIR/dhcpd.conf.sample $RPM_BUILD_ROOT/

touch $RPM_BUILD_ROOT/var/lib/dhcp/dhcpd/state/dhcpd.leases
touch $RPM_BUILD_ROOT/var/lib/dhcp/dhclient/state/dhclient.leases

cat <<EOF > $RPM_BUILD_ROOT/etc/sysconfig/dhcpd
# Additional command line options here
DHCPDARGS=
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep -q ^dhcp: /etc/group || groupadd -g 188 dhcp
grep -q ^dhcp: /etc/passwd ||
	useradd -g dhcp -u 188 -d / -s /bin/false -M dhcp

%pre server
rm -f /var/run/dhcp.restart
if [ $1 -ge 2 ]; then
	/etc/rc.d/init.d/dhcpd status && touch /var/run/dhcp.restart || :
	/etc/rc.d/init.d/dhcpd stop || :
fi

%post server
if [ -f /var/run/dhcp.restart ]; then
	/etc/rc.d/init.d/dhcpd start
fi
rm -f /var/run/dhcp.restart

%preun server
if [ $1 -eq 0 ]; then
	/etc/rc.d/init.d/dhcpd stop || :
	/sbin/chkconfig --del dhcpd
fi

%files
%defattr(-,root,root)
%doc README RELNOTES CHANGES COPYRIGHT $RPM_BUILD_ROOT/dhcpd.conf.sample
%{_mandir}/man1/omshell.1*
%{_mandir}/man3/dhcpctl.3*
%{_mandir}/man5/dhcp-eval.5*
%{_mandir}/man5/dhcp-options.5*

%if %BUILD_DHCP_CLIENT
%files client
%defattr(-,root,root)
/sbin/dhclient
/sbin/dhclient-script
%{_mandir}/man5/dhclient.conf.5*
%{_mandir}/man5/dhclient.leases.5*
%{_mandir}/man8/dhclient.8*
%{_mandir}/man8/dhclient-script.8*
%attr(0700,root,dhcp) %dir /var/lib/dhcp/dhclient
%attr(0700,root,dhcp) %dir /var/lib/dhcp/dhclient/state
%attr(0600,root,dhcp) %config /var/lib/dhcp/dhclient/state/dhclient.leases
%endif

%files server
%defattr(-,root,root)
%config /etc/sysconfig/dhcpd
%config /etc/rc.d/init.d/dhcpd
/usr/sbin/dhcpd
%{_mandir}/man5/dhcpd.conf.5*
%{_mandir}/man5/dhcpd.leases.5*
%{_mandir}/man8/dhcpd.8*
%attr(0750,root,dhcp) %dir /var/lib/dhcp/dhcpd
%attr(1770,root,dhcp) %dir /var/lib/dhcp/dhcpd/state
%attr(0600,dhcp,dhcp) %config /var/lib/dhcp/dhcpd/state/dhcpd.leases

%files relay
%defattr(-,root,root)
/usr/sbin/dhcrelay
%{_mandir}/man8/dhcrelay.8*

%changelog
* Tue Sep 30 2003 Solar Designer <solar@owl.openwall.com> 3.0pl2-owl4
- Define PTRSIZE_64BIT when building for Alpha.

* Fri Sep 19 2003 Matthias Schmidt <schmidt@owl.openwall.com> 3.0pl2-owl3
- Fixed another four warnings on sparc.

* Mon Sep 15 2003 Solar Designer <solar@owl.openwall.com> 3.0pl2-owl2
- Don't set dhcpd to be started at system boot by default.
- dhcrelay chroots now to /var/empty.

* Mon Sep 15 2003 Solar Designer <solar@owl.openwall.com> 3.0pl2-owl1
- Create the pseudo-user/group in the common package.

* Sun Sep 14 2003 Matthias Schmidt <schmidt@owl.openwall.com> 3.0pl2-owl0.4
- Create three subdirectories for dhcpd and dhclient under /var/lib/dhcp

* Tue Sep 09 2003 Matthias Schmidt <schmidt@owl.openwall.com> 3.0pl2-owl0.3
- Minor changes in the drop-root patch
- Set the permissions for /var/lib/dhcp correctly
- Passing options to dhcpd via /etc/sysconfig/dhcpd
- Fix for the remaining 34 warnings

* Tue Sep 09 2003 Solar Designer <solar@owl.openwall.com> 3.0pl2-owl0.2
- Applied the initial set of corrections.
- Pass the optflags correctly.
- Changed -Wall to -Wall -Wno-unused, this reduces the number of warnings
from 418 to 34; the remaining warnings need to be dealt with.

* Mon May 05 2003 Matthias Schmidt <schmidt@owl.openwall.com> 3.0pl2-owl0.1
- Initial release (3.0pl2)
- chroot patch for dhcpd and dhcrelay
- Modified a client-patch from Red Hat

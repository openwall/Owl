# $Id: Owl/packages/dhcp/dhcp.spec,v 1.29 2005/01/12 15:55:50 galaxy Exp $

%define BUILD_DHCP_CLIENT 0

Summary: Dynamic Host Configuration Protocol (DHCP) distribution.
Name: dhcp
Version: 3.0pl2
Release: owl9
License: ISC License
Group: System Environment/Daemons
URL: http://www.isc.org/products/DHCP/
Source0: ftp://ftp.isc.org/isc/dhcp/dhcp-%version.tar.gz
Source1: dhcpd.init
Source2: dhcpd.conf.sample
Patch0: dhcp-3.0pl2-owl-man.diff
Patch1: dhcp-3.0pl2-owl-drop-root.diff
Patch2: dhcp-3.0pl2-rh-owl-script.diff
Patch3: dhcp-3.0pl2-owl-warnings.diff
Patch4: dhcp-3.0pl2-owl-bound.diff
Patch5: dhcp-3.0pl2-owl-gcc343-fixes.diff
BuildRoot: /override/%name-%version

%description
The ISC Dynamic Host Configuration Protocol distribution provides a
freely redistributable reference implementation of all aspects of the
DHCP protocol.

%if %BUILD_DHCP_CLIENT
%package client
Summary: The ISC DHCP client.
Group: System Environment/Base
PreReq: %name = %version-%release
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
PreReq: %name = %version-%release
PreReq: /sbin/chkconfig
Requires: %_var/empty
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
PreReq: %name = %version-%release
Requires: %_var/empty

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
%patch4 -p1
%patch5 -p1

%{expand:%%define optflags %optflags -Wall -Wno-unused}

%ifarch alpha alphaev5 alphaev56 alphapca56 alphaev6 alphaev67
%{expand:%%define optflags %optflags -DPTRSIZE_64BIT}
%endif

%build
./configure --copts "$RPM_OPT_FLAGS -D_GNU_SOURCE"
%__make CC="%__cc" DEBUG=

%install
rm -rf %buildroot
mkdir -p %buildroot/etc/{rc.d/init.d}
%__make install \
	DESTDIR="%buildroot" \
	ADMMANDIR="%_mandir/man8" \
	FFMANDIR="%_mandir/man5" \
	LIBMANDIR="%_mandir/man3" \
	USRMANDIR="%_mandir/man1"

cd %buildroot

mkdir -p %buildroot%_sysconfdir/{rc.d/init.d,sysconfig}
mkdir -p %buildroot%_var/lib/dhcp/{dhcpd,dhclient}/state

install -m 700 $RPM_SOURCE_DIR/dhcpd.init %buildroot%_sysconfdir/rc.d/init.d/dhcpd

touch %buildroot%_var/lib/dhcp/dhcpd/state/dhcpd.leases
touch %buildroot%_var/lib/dhcp/dhclient/state/dhclient.leases

cat <<EOF > %buildroot%_sysconfdir/sysconfig/dhcpd
# Additional command line options here
DHCPDARGS=
EOF

# Remove unpackaged files
rm %buildroot%_bindir/omshell
rm %buildroot%_mandir/man3/omapi.3*
rm %buildroot%_mandir/man3/omshell.3*
rm %buildroot/usr/local/include/dhcpctl.h
rm %buildroot/usr/local/include/isc-dhcp/boolean.h
rm %buildroot/usr/local/include/isc-dhcp/dst.h
rm %buildroot/usr/local/include/isc-dhcp/int.h
rm %buildroot/usr/local/include/isc-dhcp/lang.h
rm %buildroot/usr/local/include/isc-dhcp/list.h
rm %buildroot/usr/local/include/isc-dhcp/result.h
rm %buildroot/usr/local/include/isc-dhcp/types.h
rm %buildroot/usr/local/include/omapip/alloc.h
rm %buildroot/usr/local/include/omapip/buffer.h
rm %buildroot/usr/local/include/omapip/omapip.h
rm %buildroot/usr/local/lib/libdhcpctl.a
rm %buildroot/usr/local/lib/libomapi.a
%if !%BUILD_DHCP_CLIENT
rm %buildroot/sbin/dhclient
rm %buildroot/sbin/dhclient-script
rm %buildroot%_mandir/man5/dhclient.conf.5*
rm %buildroot%_mandir/man5/dhclient.leases.5*
rm %buildroot%_mandir/man8/dhclient.8*
rm %buildroot%_mandir/man8/dhclient-script.8*
rm %buildroot/var/lib/dhcp/dhclient/state/dhclient.leases
%endif

%pre
grep -q ^dhcp: %_sysconfdir/group || groupadd -g 188 dhcp
grep -q ^dhcp: %_sysconfdir/passwd ||
	useradd -g dhcp -u 188 -d / -s /bin/false -M dhcp

%pre server
rm -f %_var/run/dhcp.restart
if [ $1 -ge 2 ]; then
	%_sysconfdir/rc.d/init.d/dhcpd status && touch %_var/run/dhcp.restart || :
	%_sysconfdir/rc.d/init.d/dhcpd stop || :
fi

%post server
if [ -f %_var/run/dhcp.restart ]; then
	%_sysconfdir/rc.d/init.d/dhcpd start
fi
rm -f %_var/run/dhcp.restart

%preun server
if [ $1 -eq 0 ]; then
	%_sysconfdir/rc.d/init.d/dhcpd stop || :
	/sbin/chkconfig --del dhcpd
fi

%files
%defattr(-,root,root)
%doc README RELNOTES CHANGES COPYRIGHT $RPM_SOURCE_DIR/dhcpd.conf.sample
%_mandir/man1/omshell.1*
%_mandir/man3/dhcpctl.3*
%_mandir/man5/dhcp-eval.5*
%_mandir/man5/dhcp-options.5*

%if %BUILD_DHCP_CLIENT
%files client
%defattr(-,root,root)
/sbin/dhclient
/sbin/dhclient-script
%_mandir/man5/dhclient.conf.5*
%_mandir/man5/dhclient.leases.5*
%_mandir/man8/dhclient.8*
%_mandir/man8/dhclient-script.8*
%attr(0700,root,dhcp) %dir %_var/lib/dhcp/dhclient
%attr(0700,root,dhcp) %dir %_var/lib/dhcp/dhclient/state
%attr(0600,root,dhcp) %config %verify(not size md5 mtime) %_var/lib/dhcp/dhclient/state/dhclient.leases
%endif

%files server
%defattr(-,root,root)
%config %_sysconfdir/sysconfig/dhcpd
%config %_sysconfdir/rc.d/init.d/dhcpd
%_sbindir/dhcpd
%_mandir/man5/dhcpd.conf.5*
%_mandir/man5/dhcpd.leases.5*
%_mandir/man8/dhcpd.8*
%attr(0750,root,dhcp) %dir %_var/lib/dhcp/dhcpd
%attr(1770,root,dhcp) %dir %_var/lib/dhcp/dhcpd/state
%attr(0600,dhcp,dhcp) %config %verify(not size md5 mtime) /var/lib/dhcp/dhcpd/state/dhcpd.leases

%files relay
%defattr(-,root,root)
%_sbindir/dhcrelay
%_mandir/man8/dhcrelay.8*

%changelog
* Fri Jan 07 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 3.0pl2-owl9
- Added gcc343-fixes patch to deal with gcc post-upgrade issues.
- Cleaned up the spec.

* Tue Nov 02 2004 Solar Designer <solar@owl.openwall.com> 3.0pl2-owl8
- Remove unpackaged files.

* Sun Jun 13 2004 Solar Designer <solar@owl.openwall.com> 3.0pl2-owl7
- Added a bounds checking patch covering sprintf() calls with "%s" format
specifier and non-constant strings and forcing the use of snprintf() and
vsnprintf() in all places where that was previously supported.

* Mon Feb 09 2004 Michail Litvak <mci@owl.openwall.com> 3.0pl2-owl6
- Use RPM macros instead of explicit paths.

* Sun Oct 12 2003 Solar Designer <solar@owl.openwall.com> 3.0pl2-owl5
- Require /var/empty in server and relay subpackages (from Maxim Timofeyev).

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

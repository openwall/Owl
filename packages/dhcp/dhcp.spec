# $Owl: Owl/packages/dhcp/dhcp.spec,v 1.54 2009/07/16 20:28:29 solar Exp $

# We do not officially support the DHCP client because it is rather
# complicated, yet it runs entirely as root, which we find an
# unacceptable and unjustified security risk.  If you enable this
# setting, then you're essentially running your own revision of this
# package, and you're on your own with possible vulnerabilities.
%define BUILD_DHCP_CLIENT 0

Summary: Dynamic Host Configuration Protocol (DHCP) distribution.
Name: dhcp
Version: 3.0.7
Release: owl1
License: ISC License
Group: System Environment/Daemons
URL: https://www.isc.org/software/dhcp
Source0: ftp://ftp.isc.org/isc/dhcp/dhcp-%version.tar.gz
Source1: dhcpd.init
Source2: dhcpd.conf.sample
Patch0: dhcp-3.0.7-alt-owl-fixes.diff
Patch1: dhcp-3.0.6-owl-alt-errwarn.diff
Patch2: dhcp-3.0.6-alt-daemonize.diff
Patch3: dhcp-3.0.6-alt-defaults.diff
Patch4: dhcp-3.0.6-rh-owl-script.diff
Patch5: dhcp-3.0.7-owl-support-contact.diff
Patch6: dhcp-3.0.6-owl-bound.diff
Patch7: dhcp-3.0.6-alt-Makefile.diff
Patch8: dhcp-3.0.6-rh-dhcpctl-man.diff
Patch9: dhcp-3.0.6-rh-memory.diff
Patch10: dhcp-3.0.6-rh-failover-ports.diff
Patch11: dhcp-3.0.6-rh-man.diff
Patch12: dhcp-3.0.7-owl-alt-drop-root.diff
Patch13: dhcp-3.0.7-alt-format.diff
Patch14: dhcp-3.0.7-up-dhclient-bound.diff
Patch15: dhcp-3.0.7-deb-CVE-2009-1892.diff
PreReq: grep, shadow-utils
BuildRequires: groff, libcap-devel
BuildRoot: /override/%name-%version

%description
The ISC Dynamic Host Configuration Protocol distribution provides a
freely redistributable reference implementation of all aspects of the
DHCP protocol.

Note that most of the actual functionality is provided by dhcp-client,
dhcp-server, and dhcp-relay subpackages, while this package provides a
handful of miscellaneous files only.

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
PreReq: /sbin/chkconfig, fileutils
Requires: /var/empty
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
Requires: /var/empty

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
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

find server -type f -not -name Makefile\* -print0 |
	xargs -r0 grep -FZl DBDIR -- |
	xargs -r0 sed -i s,DBDIR,/var/lib/dhcp/dhcpd/state,g --
%if %BUILD_DHCP_CLIENT
find client -type f -not -name Makefile\* -print0 |
	xargs -r0 grep -FZl DBDIR -- |
	xargs -r0 sed -i s,DBDIR,/var/lib/dhcp/dhclient/state,g --
%endif

%{expand:%%define optflags %optflags -fno-strict-aliasing -Wall -Wno-unused -D_GNU_SOURCE}

%build
./configure --copts '%optflags'
%__make CC="%__cc" DEBUG=

%install
rm -rf %buildroot
mkdir -p %buildroot/etc/sysconfig
%__make install \
	INSTALL='install -pm644' \
	MANINSTALL='$(INSTALL)' \
	DESTDIR='%buildroot' \
	LIBDIR='%_libdir' \
	INCDIR='%_includedir' \
	ADMMANDIR='%_mandir/man8' \
	FFMANDIR='%_mandir/man5' \
	LIBMANDIR='%_mandir/man3' \
	USRMANDIR='%_mandir/man1'

cd %buildroot

mkdir -p var/lib/dhcp/{dhcpd,dhclient}/state

install -pD -m700 %_sourcedir/dhcpd.init .%_initrddir/dhcpd
install -p -m600 %_sourcedir/dhcpd.conf.sample etc/

touch var/lib/dhcp/dhcpd/state/dhcpd.leases
touch var/lib/dhcp/dhclient/state/dhclient.leases

cat << EOF > etc/sysconfig/dhcpd
# Additional command line options here
DHCPDARGS=
EOF

# Remove unpackaged files - development stuff
rm -r .%_includedir
rm -r .%_libdir/lib*.a
rm -r .%_mandir/man3

%if !%BUILD_DHCP_CLIENT
# Remove unpackaged files - the DHCP client
rm sbin/dhclient
rm sbin/dhclient-script
rm .%_mandir/man5/dhclient.conf.5*
rm .%_mandir/man5/dhclient.leases.5*
rm .%_mandir/man8/dhclient.8*
rm .%_mandir/man8/dhclient-script.8*
rm var/lib/dhcp/dhclient/state/dhclient.leases
%endif

%pre
grep -q ^dhcp: /etc/group || groupadd -g 188 dhcp
grep -q ^dhcp: /etc/passwd ||
	useradd -g dhcp -u 188 -d / -s /bin/false -M dhcp

%pre server
rm -f /var/run/dhcp.restart
if [ $1 -ge 2 ]; then
	%_initrddir/dhcpd status && touch /var/run/dhcp.restart || :
	%_initrddir/dhcpd stop || :
fi

%post server
/sbin/chkconfig --add dhcpd
if [ -f /var/run/dhcp.restart ]; then
	%_initrddir/dhcpd start
fi
rm -f /var/run/dhcp.restart

%preun server
if [ $1 -eq 0 ]; then
	%_initrddir/dhcpd stop || :
	/sbin/chkconfig --del dhcpd
fi

%files
%defattr(-,root,root)
%doc README RELNOTES LICENSE
%_bindir/omshell
%_mandir/man1/omshell.1*
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
%attr(0700,root,dhcp) %dir /var/lib/dhcp/dhclient
%attr(0700,root,dhcp) %dir /var/lib/dhcp/dhclient/state
%attr(0600,root,dhcp) %config %verify(not size md5 mtime) /var/lib/dhcp/dhclient/state/dhclient.leases
%endif

%files server
%defattr(-,root,root)
%config(noreplace) /etc/sysconfig/dhcpd
%config %_initrddir/dhcpd
/etc/dhcpd.conf.sample
%_sbindir/dhcpd
%_mandir/man5/dhcpd.conf.5*
%_mandir/man5/dhcpd.leases.5*
%_mandir/man8/dhcpd.8*
%attr(0750,root,dhcp) %dir /var/lib/dhcp/dhcpd
%attr(1770,root,dhcp) %dir /var/lib/dhcp/dhcpd/state
%attr(0600,dhcp,dhcp) %config %verify(not size md5 mtime) /var/lib/dhcp/dhcpd/state/dhcpd.leases

%files relay
%defattr(-,root,root)
%_sbindir/dhcrelay
%_mandir/man8/dhcrelay.8*

%changelog
* Wed Jul 15 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.0.7-owl1
- Updated to 3.0.7.
- Fixed potential DHCP server crash in certain configurations
(CVE-2009-1892; patch by Christoph Biedl).
- Backported upstream fix for potential stack-based buffer overflow in
DHCP client (CVE-2009-0692; although we're not supporting dhclient
officially and not building it by default).

* Thu Oct 18 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.0.6-owl2
- Simplified lowering privileges algorithm.

* Sun Oct 14 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.0.6-owl1
- Updated to 3.0.6.

* Tue Sep 26 2006 Juan M. Bello Rivas <jmbr-at-owl.openwall.com> 3.0.4-owl1
- Updated to version 3.0.4.

* Tue Sep 19 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.0pl2-owl12
- Fixed init script to properly handle "reload" mode.
- Updated init script to new conventions.
- Use the %%_initrddir macro.

* Fri Apr 29 2005 Solar Designer <solar-at-owl.openwall.com> 3.0pl2-owl11
- Do register dhcpd with chkconfig, but don't enable it for any runlevels
by default.
- Added "PreReq: grep, shadow-utils" to the common "dhcp" subpackage (for
grep, groupadd, useradd), "PreReq: fileutils" to the server subpackage (for
rm, touch).

* Sun Apr 10 2005 Solar Designer <solar-at-owl.openwall.com> 3.0pl2-owl10
- Re-worked the drop-root patch such that dhcpd and dhcrelay will drop
privileges by default, adjusted the man pages accordingly.
- Corrected the packaging of dhcpd.conf.sample, install it under /etc,
have the startup script point the user at the sample file when needed.
- Provide the proper support contact (owl-users mailing list) since the ISC
folks don't want to be bothered with questions on software that includes
third-party modifications and that might not be based off their latest code.
- Updated the lists of files to (not) package.
- Build this package without optimizations based on strict aliasing rules
(there were 33 gcc warnings).

* Fri Jan 07 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.0pl2-owl9
- Added fixes patch to deal with gcc post-upgrade issues.
- Cleaned up the spec.

* Tue Nov 02 2004 Solar Designer <solar-at-owl.openwall.com> 3.0pl2-owl8
- Remove unpackaged files.

* Sun Jun 13 2004 Solar Designer <solar-at-owl.openwall.com> 3.0pl2-owl7
- Added a bounds checking patch covering sprintf() calls with "%%s" format
specifier and non-constant strings and forcing the use of snprintf() and
vsnprintf() in all places where that was previously supported.

* Mon Feb 09 2004 Michail Litvak <mci-at-owl.openwall.com> 3.0pl2-owl6
- Use RPM macros instead of explicit paths.

* Sun Oct 12 2003 Solar Designer <solar-at-owl.openwall.com> 3.0pl2-owl5
- Require /var/empty in server and relay subpackages (from Maxim Timofeyev).

* Tue Sep 30 2003 Solar Designer <solar-at-owl.openwall.com> 3.0pl2-owl4
- Define PTRSIZE_64BIT when building for Alpha.

* Fri Sep 19 2003 Matthias Schmidt <schmidt-at-owl.openwall.com> 3.0pl2-owl3
- Fixed another four warnings on sparc.

* Mon Sep 15 2003 Solar Designer <solar-at-owl.openwall.com> 3.0pl2-owl2
- Don't set dhcpd to be started at system boot by default.
- dhcrelay chroots now to /var/empty.

* Mon Sep 15 2003 Solar Designer <solar-at-owl.openwall.com> 3.0pl2-owl1
- Create the pseudo-user/group in the common package.

* Sun Sep 14 2003 Matthias Schmidt <schmidt-at-owl.openwall.com> 3.0pl2-owl0.4
- Create three subdirectories for dhcpd and dhclient under /var/lib/dhcp

* Tue Sep 09 2003 Matthias Schmidt <schmidt-at-owl.openwall.com> 3.0pl2-owl0.3
- Minor changes in the drop-root patch
- Set the permissions for /var/lib/dhcp correctly
- Passing options to dhcpd via /etc/sysconfig/dhcpd
- Fix for the remaining 34 warnings

* Tue Sep 09 2003 Solar Designer <solar-at-owl.openwall.com> 3.0pl2-owl0.2
- Applied the initial set of corrections.
- Pass the optflags correctly.
- Changed -Wall to -Wall -Wno-unused, this reduces the number of warnings
from 418 to 34; the remaining warnings need to be dealt with.

* Mon May 05 2003 Matthias Schmidt <schmidt-at-owl.openwall.com> 3.0pl2-owl0.1
- Initial release (3.0pl2)
- chroot patch for dhcpd and dhcrelay
- Modified a client-patch from Red Hat

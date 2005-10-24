# $Id: Owl/packages/iproute2/iproute2.spec,v 1.20 2005/10/24 02:22:11 solar Exp $

%define ver 2.4.7
%define snapshot ss020116

Summary: Enhanced IP routing and network devices configuration tools.
Name: iproute2
Version: %ver.%snapshot
Release: owl3
License: GPL
Group: Applications/System
Source0: ftp://ftp.inr.ac.ru/ip-routing/%name-%ver-now-%snapshot-try.tar.gz
Source1: %name-%ver-%snapshot-ps.tar.bz2
Source2: ip.8
Source3: tc.8
Source4: tc-htb.8
Source5: tc-pbfifo.8
Source6: tc-pfifo_fast.8
Source7: tc-prio.8
Source8: tc-red.8
Source9: tc-sfq.8
Source10: tc-tbf.8
Source11: tc-cbq.8
Patch0: iproute2-2.4.7-rh-promisc-allmulti.diff
Patch1: iproute2-2.4.7-owl-socketbits.diff
Patch2: iproute2-2.4.7-owl-warnings.diff
Patch3: iproute2-2.4.7-deb-netlink.diff
Patch4: iproute2-2.4.7-owl-nstat-bound.diff
Patch5: iproute2-2.4.7-devik-htb.diff
Provides: iproute = %version
Obsoletes: iproute
BuildRequires: db4-devel, bison
BuildRoot: /override/%name-%version

%description
Linux 2.2+ maintains compatibility with the basic configuration utilities
of the network (ifconfig, route) but a new utility is required to exploit
the new characteristics and features of the kernel, such as policy
routing, fast NAT and packet scheduling.  This package includes the new
utilities (ip, tc, rtmon, rtacct, ifstat, nstat, rtstat, ss).

%prep
%setup -q -n %name -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%{expand:%%define optflags %optflags -Wall -Wstrict-prototypes}

%build
make \
	KERNEL_INCLUDE=/usr/include \
	CCOPTS="%optflags -D_GNU_SOURCE"

%install
rm -rf %buildroot

mkdir -p %buildroot{/sbin,%_sbindir,/etc/iproute2,%_mandir/man8}

install -m 755 ip/{ip,ifcfg,rtmon} tc/tc %buildroot/sbin/
install -m 755 misc/{ifstat,nstat,rtacct,rtstat,ss} %buildroot%_sbindir/
install -m 644 etc/iproute2/* %buildroot/etc/iproute2/
install -m 644 %_sourcedir/ip.8 %buildroot%_mandir/man8/
install -m 644 %_sourcedir/tc.8 %buildroot%_mandir/man8/
install -m 644 %_sourcedir/tc-htb.8 %buildroot%_mandir/man8/
install -m 644 %_sourcedir/tc-pbfifo.8 %buildroot%_mandir/man8/
install -m 644 %_sourcedir/tc-pfifo_fast.8 %buildroot%_mandir/man8/
install -m 644 %_sourcedir/tc-prio.8 %buildroot%_mandir/man8/
install -m 644 %_sourcedir/tc-red.8 %buildroot%_mandir/man8/
install -m 644 %_sourcedir/tc-sfq.8 %buildroot%_mandir/man8/
install -m 644 %_sourcedir/tc-tbf.8 %buildroot%_mandir/man8/
install -m 644 %_sourcedir/tc-cbq.8 %buildroot%_mandir/man8/

gzip -9nf iproute2-ps/*.ps

%files
%defattr(-,root,root)
%doc README* RELNOTES examples iproute2-ps/*.ps*
%dir /etc/iproute2
%attr(644,root,root) %config(noreplace) /etc/iproute2/*
/sbin/*
%_sbindir/*
%_mandir/man8/*

%changelog
* Sat Mar 05 2005 Michail Litvak <mci@owl.openwall.com> 2.4.7.ss020116-owl3
- Added patch to support HTB qdisc.

* Sun Apr 18 2004 Solar Designer <solar@owl.openwall.com> 2.4.7.ss020116-owl2
- Fixed the potential buffer overflow in nstat discovered by Steve Grubb,
and a number of other related potential issues in nstat.

* Sat Nov 22 2003 Michail Litvak <mci@owl.openwall.com> 2.4.7.ss020116-owl1
- reduce -owl-socketbits.diff to include only sockaddr_storage
definition.
- Added patch from Herbert Xu to prevent a local denial of service attack
via sending unicast netlink messages to any process on the system.

* Sun Oct 12 2003 Michail Litvak <mci@owl.openwall.com> 2.4.7-owl5
- ss020116
- Fixed building with kernel >= 2.4.22.
- Dropped some obsolete patches.
- Include some new tools (ifstat, nstat, rtstat, ss)

* Mon Apr 01 2002 Solar Designer <solar@owl.openwall.com>
- More formatting fixes to ip.8; the tc*.8 man pages remain _very_ dirty.
- Compilation warning fixes on Alpha (builds with -Wall cleanly now).

* Mon Feb 11 2002 Michail Litvak <mci@owl.openwall.com>
- add manpages
- add PostScript documentation

* Thu Feb 07 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Dec 28 2001 Michail Litvak <mci@owl.openwall.com>
- spec-file based on RH's

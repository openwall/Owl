# $Owl: Owl/packages/iproute2/iproute2.spec,v 1.27 2012/02/27 08:51:31 solar Exp $

Summary: Enhanced IP routing and network devices configuration tools.
Name: iproute2
Version: 2.6.38
Release: owl3
License: GPL
Group: Applications/System
Source0: http://devresources.linuxfoundation.org/dev/iproute2/download/%name-%version.tar.bz2
# Signature: http://devresources.linuxfoundation.org/dev/iproute2/download/%name-%version.tar.bz2.sig
Patch0: iproute2-2.4.7-alt-rtacct_daemon.diff
Patch1: iproute2-2.6.18-alt-ifcfg.diff
Patch2: iproute2-2.6.18-alt-ip-man.diff
Patch3: iproute2-2.6.28-alt-format.diff
Patch4: iproute2-2.6.38-owl-warnings.diff
Patch5: iproute2-2.6.38-owl-tmp.diff
Patch6: iproute2-2.6.38-owl-configure.diff
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
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%{expand:%%define optflags %optflags -Wall -Wstrict-prototypes}

%build
%__make \
	KERNEL_INCLUDE=/usr/include \
	CCOPTS="%optflags -D_GNU_SOURCE"

%install
rm -rf %buildroot

%__make install \
	DESTDIR=%buildroot \
	SBINDIR=/sbin/ \
	MANDIR=%_mandir \
	DOCDIR=%_docdir/%name-%version

mkdir -p %buildroot/%_sbindir
rm %buildroot/sbin/rtstat
mv %buildroot/sbin/{arpd,lnstat,ifstat,nstat,rtacct,ss} %buildroot/%_sbindir/
ln -sf lnstat %buildroot/%_sbindir/rtstat
ln -sf lnstat %buildroot/%_sbindir/ctstat

%files
%defattr(-,root,root)
%doc RELNOTES examples
%doc README.distribution  README.iproute2+tc  README.lnstat
%dir /etc/iproute2
%attr(644,root,root) %config(noreplace) /etc/iproute2/*
/sbin/*
%exclude /sbin/rtpr
%exclude %_sbindir/arpd
%exclude /sbin/genl
%_sbindir/*
/usr/lib/tc/
%_mandir/man*/*

%changelog
* Mon Feb 27 2012 Solar Designer <solar-at-owl.openwall.com> 2.6.38-owl3
- Search for the iptables library directory under /lib64 before /lib.

* Wed Feb 15 2012 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.38-owl2
- Fixed arbitrary file overwrite at build stage and in dhclient sample script.

* Wed Apr 13 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.38-owl1
- Updated to 2.6.38.
- Dropped obsoleted patches (fixed in upstream).
- Imported some patches from ALT.

* Sun Sep 20 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.4.7.ss020116-owl4
- Disabled build time kernel headers check.

* Sat Mar 05 2005 Michail Litvak <mci-at-owl.openwall.com> 2.4.7.ss020116-owl3
- Added patch to support HTB qdisc.

* Sun Apr 18 2004 Solar Designer <solar-at-owl.openwall.com> 2.4.7.ss020116-owl2
- Fixed the potential buffer overflow in nstat discovered by Steve Grubb,
and a number of other related potential issues in nstat.

* Sat Nov 22 2003 Michail Litvak <mci-at-owl.openwall.com> 2.4.7.ss020116-owl1
- reduce -owl-socketbits.diff to include only sockaddr_storage
definition.
- Added patch from Herbert Xu to prevent a local denial of service attack
via sending unicast netlink messages to any process on the system.

* Sun Oct 12 2003 Michail Litvak <mci-at-owl.openwall.com> 2.4.7-owl5
- ss020116
- Fixed building with kernel >= 2.4.22.
- Dropped some obsolete patches.
- Include some new tools (ifstat, nstat, rtstat, ss)

* Mon Apr 01 2002 Solar Designer <solar-at-owl.openwall.com>
- More formatting fixes to ip.8; the tc*.8 man pages remain _very_ dirty.
- Compilation warning fixes on Alpha (builds with -Wall cleanly now).

* Mon Feb 11 2002 Michail Litvak <mci-at-owl.openwall.com>
- add manpages
- add PostScript documentation

* Thu Feb 07 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Dec 28 2001 Michail Litvak <mci-at-owl.openwall.com>
- spec-file based on RH's

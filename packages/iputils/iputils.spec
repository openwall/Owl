# $Id: Owl/packages/iputils/iputils.spec,v 1.4 2002/05/30 11:23:21 mci Exp $

Summary: Utilities for IPv4/IPv6 networking.
Name: iputils
Version: ss020124
Release: owl1
License: mostly BSD, some GPL
Group: Applications/Internet
Source0: ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{version}.tar.gz
Source1: iputils-ss020124-doc.tar.bz2 
Source2: bonding-0.2.tar.bz2
Source3: ping.control
Patch0: iputils-ss020124-rh-owl-cache-reverse-lookups.diff
Patch1: iputils-ss020124-owl-warnings.diff
Requires: owl-control < 2.0
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
The iputils package contains a set of IPv4/IPv6 networking utilities,
and most importantly ping.  The ping command sends a series of ICMP
protocol ECHO_REQUEST packets to a specified network host and can tell
you if that machine is alive and receiving network traffic.

%prep
%setup -q -n %{name} -a 1 -a 2
mv -f bonding-0.2/README bonding-0.2/README.ifenslave
%patch0 -p1
%patch1 -p1

%build
mv rdisc.c rdisc.c.orig
sed 's/in\.rdiscd/rdiscd/' < rdisc.c.orig > rdisc.c
mv Makefile Makefile.orig
make CCOPTS="-D_GNU_SOURCE $RPM_OPT_FLAGS -Wall" \
	IPV4_TARGETS="tracepath ping clockdiff rdisc arping" # no tftpd
gcc $RPM_OPT_FLAGS -Wall -s bonding-0.2/ifenslave.c -o bonding-0.2/ifenslave

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/{bin,sbin}
install -m 755 arping clockdiff ping6 tracepath tracepath6 traceroute6 \
	${RPM_BUILD_ROOT}%{_sbindir}/
install -m 755 rdisc ${RPM_BUILD_ROOT}%{_sbindir}/rdiscd
install -m 700 ping $RPM_BUILD_ROOT/bin/
install -m 755 bonding-0.2/ifenslave $RPM_BUILD_ROOT/sbin/

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
install -m 644 iputils-doc/{arping,clockdiff,ping,tracepath,traceroute6}.8 \
	${RPM_BUILD_ROOT}%{_mandir}/man8/

sed 's/rdisc/rdiscd/' \
	< iputils-doc/rdisc.8 > ${RPM_BUILD_ROOT}%{_mandir}/man8/rdiscd.8

mkdir -p $RPM_BUILD_ROOT/etc/control.d/facilities
install -m 700 $RPM_SOURCE_DIR/ping.control \
	$RPM_BUILD_ROOT/etc/control.d/facilities/ping

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc RELNOTES bonding*/README.ifenslave
%{_sbindir}/arping
%{_sbindir}/clockdiff
%attr(4711,root,root) /bin/ping
/sbin/ifenslave
%{_sbindir}/ping6
%{_sbindir}/tracepath
%{_sbindir}/tracepath6
%{_sbindir}/traceroute6
%{_sbindir}/rdiscd
%{_mandir}/man8/*
/etc/control.d/facilities/ping

%changelog
* Wed May 30 2002 Michail Litvak <mci@owl.openwall.com>
- ss020124
- include man pages precompiled from sgml sources

* Mon Feb 04 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Tue Apr 10 2001 Solar Designer <solar@owl.openwall.com>
- Reviewed patches and RPM spec files of the iputils package in RH, CAEN,
and PLD distributions.
- Updated two RH-derived patches.
- Patched some unimportant gcc warnings.
- Wrote ping.control.
- Wrote this spec file.

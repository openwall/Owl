# $Id: Owl/packages/iputils/iputils.spec,v 1.2 2002/02/04 13:43:31 mci Exp $

Summary: Utilities for IPv4/IPv6 networking.
Name: iputils
Version: ss001110
Release: owl1
License: mostly BSD, some GPL
Group: Applications/Internet
Source0: ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{version}.tar.gz
Source1: bonding-0.2.tar.bz2
Source2: ping.control
Patch0: iputils-ss001110-rh-owl-doc.diff
Patch1: iputils-ss001110-rh-owl-cache-reverse-lookups.diff
Patch2: iputils-ss001110-owl-warnings.diff
Requires: owl-control < 2.0
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
The iputils package contains a set of IPv4/IPv6 networking utilities,
and most importantly ping.  The ping command sends a series of ICMP
protocol ECHO_REQUEST packets to a specified network host and can tell
you if that machine is alive and receiving network traffic.

%prep
%setup -q -n %{name} -a 1
mv -f bonding-0.2/README bonding-0.2/README.ifenslave
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
mv rdisc.c rdisc.c.orig
sed 's/in\.rdiscd/rdiscd/' < rdisc.c.orig > rdisc.c
mv Makefile Makefile.orig
sed "s/-O2 -Wall -g/$RPM_OPT_FLAGS -Wall/" < Makefile.orig > Makefile
make IPV4_TARGETS="tracepath ping clockdiff rdisc arping" # no tftpd
gcc $RPM_OPT_FLAGS -Wall -s bonding-0.2/ifenslave.c -o bonding-0.2/ifenslave

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/{bin,sbin}
install -c arping clockdiff ping6 tracepath tracepath6 traceroute6 \
	${RPM_BUILD_ROOT}%{_sbindir}/
install -c rdisc ${RPM_BUILD_ROOT}%{_sbindir}/rdiscd
install -c ping	$RPM_BUILD_ROOT/bin/
install -c bonding-0.2/ifenslave $RPM_BUILD_ROOT/sbin/
strip ${RPM_BUILD_ROOT}%{_sbindir} $RPM_BUILD_ROOT/{bin,sbin}/* || :

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
install -c {arping,clockdiff,ping,tracepath}.8 \
	${RPM_BUILD_ROOT}%{_mandir}/man8/
sed 's/in\.rdisc/rdiscd/' \
	< in.rdisc.8c > ${RPM_BUILD_ROOT}%{_mandir}/man8/rdiscd.8

mkdir -p $RPM_BUILD_ROOT/etc/control.d/facilities
install -m 700 $RPM_SOURCE_DIR/ping.control $RPM_BUILD_ROOT/etc/control.d/facilities/ping

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README RELNOTES bonding*/README.ifenslave
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
* Mon Feb 04 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Tue Apr 10 2001 Solar Designer <solar@owl.openwall.com>
- Reviewed patches and RPM spec files of the iputils package in RH, CAEN,
and PLD distributions.
- Updated two RH-derived patches.
- Patched some unimportant gcc warnings.
- Wrote ping.control.
- Wrote this spec file.

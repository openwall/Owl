# $Id: Owl/packages/iputils/iputils.spec,v 1.14 2003/10/22 00:08:25 solar Exp $

Summary: Utilities for IPv4/IPv6 networking.
Name: iputils
Version: ss020927
Release: owl2
License: mostly BSD, some GPL
Group: Applications/Internet
Source0: ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{version}.tar.gz
Source1: bonding-0.2.tar.bz2
Source2: ping.control
Patch0: iputils-ss020927-rh-owl-cache-reverse-lookups.diff
Patch1: iputils-ss020927-owl-warnings.diff
Patch2: iputils-ss020927-owl-socketbits.diff
Patch3: bonding-0.2-owl-ioctl.diff
PreReq: owl-control >= 0.4, owl-control < 2.0
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
%patch3 -p0

%{expand:%%define optflags %optflags -Wall}

%build
make \
	CCOPT="-D_GNU_SOURCE $RPM_OPT_FLAGS" \
	IPV4_TARGETS="tracepath ping clockdiff rdisc arping" # no tftpd, rarpd
gcc $RPM_OPT_FLAGS -s bonding-0.2/ifenslave.c -o bonding-0.2/ifenslave

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/{bin,sbin}
install -m 755 arping clockdiff ping6 tracepath tracepath6 traceroute6 \
	$RPM_BUILD_ROOT%{_sbindir}/
install -m 755 rdisc $RPM_BUILD_ROOT%{_sbindir}/rdiscd
install -m 700 ping $RPM_BUILD_ROOT/bin/
install -m 755 bonding-0.2/ifenslave $RPM_BUILD_ROOT/sbin/

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
install -m 644 doc/{arping,clockdiff,ping,tracepath,traceroute6}.8 \
	$RPM_BUILD_ROOT%{_mandir}/man8/

sed 's/rdisc/rdiscd/' \
	< doc/rdisc.8 > $RPM_BUILD_ROOT%{_mandir}/man8/rdiscd.8

mkdir -p $RPM_BUILD_ROOT/etc/control.d/facilities
install -m 700 $RPM_SOURCE_DIR/ping.control \
	$RPM_BUILD_ROOT/etc/control.d/facilities/ping

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ $1 -ge 2 ]; then
	/usr/sbin/control-dump ping
fi

%post
if [ $1 -ge 2 ]; then
	/usr/sbin/control-restore ping
else
	/usr/sbin/control ping public
fi

%files
%defattr(-,root,root)
%doc RELNOTES bonding*/README.ifenslave
%{_sbindir}/arping
%{_sbindir}/clockdiff
/sbin/ifenslave
%attr(700,root,root) /bin/ping
%{_sbindir}/ping6
%{_sbindir}/tracepath
%{_sbindir}/tracepath6
%{_sbindir}/traceroute6
%{_sbindir}/rdiscd
%{_mandir}/man8/*
/etc/control.d/facilities/ping

%changelog
* Thu Oct 21 2003 Michail Litvak <mci@owl.openwall.com> ss020927-owl2
- reduce -owl-socketbits.diff to include only sockaddr_storage
difinition, because previous version broke tracepath.

* Thu Oct 16 2003 Michail Litvak <mci@owl.openwall.com> ss020927-owl1
- ss020927
- Fixed building with kernel >= 2.4.22.
- Source archive now contains precompiled man pages, so don't include
them as another archive.

* Sun Nov 03 2002 Solar Designer <solar@owl.openwall.com>
- Dump/restore the owl-control setting for ping on package upgrades.
- Keep ping at mode 700 ("restricted") in the package, but default it to
"public" in %post when the package is first installed.  This avoids a
race and fail-open behavior where a "restricted" ping could be "public"
during package upgrades.

* Mon Jun 03 2002 Solar Designer <solar@owl.openwall.com>
- Patched ifenslave to use the SIOCBOND* ioctl's instead of the obsolete
BOND_* ones when building with Linux 2.4+ kernel headers.

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

# $Owl: Owl/packages/iputils/iputils.spec,v 1.33.2.1 2015/01/03 06:58:38 solar Exp $

Summary: Utilities for IPv4/IPv6 networking.
Name: iputils
Version: s20101006
Release: owl1
Epoch: 1
License: mostly BSD, some GPL
Group: Applications/Internet
Source0: http://www.skbuff.net/iputils/%name-%version.tar.bz2
Source1: ifenslave-20080602.tar.gz
Source2: ping.control
Source3: ping6.control
Source4: arping.8
Source5: clockdiff.8
Source6: ping.8
Source7: rdisc.8
Source8: tracepath.8
Patch0: iputils-ss020927-rh-owl-cache-reverse-lookups.diff
Patch1: iputils-s20101006-owl-SO_MARK.diff
Patch2: iputils-s20101006-owl-libsysfs.diff
Patch3: iputils-s20101006-owl-pingsock.diff
Patch4: iputils-20001007-rh-bug23844.diff
Patch5: iputils-s20101006-gentoo-owl-bindnow.diff
Patch6: iputils-s20101006-rh-ping_cleanup.diff
Patch7: iputils-s20101006-alt-perror-newline.diff
Patch8: iputils-s20071127-alt-datalen-fix.diff
Patch9: iputils-s20101006-owl-warnings.diff
PreReq: owl-control >= 0.4, owl-control < 2.0
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
The iputils package contains a set of IPv4/IPv6 networking utilities,
and most importantly ping.  The ping command sends a series of ICMP
protocol ECHO_REQUEST packets to a specified network host and can tell
you if that machine is alive and receiving network traffic.

%prep
%setup -q -a 1
mv -f README.bonding README.ifenslave
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

%{expand:%%define optflags %optflags -Wall}

%build
%__make \
	CCOPT="-D_GNU_SOURCE %optflags" \
	IPV4_TARGETS="tracepath ping clockdiff rdisc arping" # no tftpd, rarpd
%__cc %optflags -s ifenslave.c -o ifenslave

%install
rm -rf %buildroot

mkdir -p %buildroot%_sbindir
mkdir -p %buildroot/{bin,sbin}
install -m 755 arping clockdiff %buildroot%_sbindir/
install -m 755 rdisc %buildroot%_sbindir/rdiscd
install -m 700 ping ping6 %buildroot/bin/
install -m 755 tracepath tracepath6 %buildroot/bin/
install -m 755 ifenslave %buildroot/sbin/

mkdir -p %buildroot%_mandir/man1
mkdir -p %buildroot%_mandir/man8
install -pD -m644 %_sourcedir/ping.8 %buildroot%_mandir/man1/ping.1
ln -sf ping.1 %buildroot%_mandir/man1/ping6.1
ln -sf tracepath.1 %buildroot%_mandir/man1/tracepath6.1
ln -sf tracepath.8 %buildroot%_mandir/man8/tracepath6.8
install -pD -m644 %_sourcedir/tracepath.8 \
	%buildroot%_mandir/man1/tracepath.1
install -m 644 %_sourcedir/{arping,clockdiff}.8 \
	%buildroot%_mandir/man8/
sed 's/rdisc/rdiscd/' \
	< %_sourcedir/rdisc.8 > %buildroot%_mandir/man8/rdiscd.8

mkdir -p %buildroot/etc/control.d/facilities
install -m 700 %_sourcedir/ping.control \
	%buildroot/etc/control.d/facilities/ping
install -m 700 %_sourcedir/ping6.control \
	%buildroot/etc/control.d/facilities/ping6

%pre
if [ $1 -ge 2 ]; then
	%_sbindir/control-dump ping ping6
fi
grep -q ^_icmp: /etc/group || groupadd -g 111 _icmp

%post
if [ $1 -ge 2 ]; then
	%_sbindir/control-restore ping ping6
else
	%_sbindir/control ping dgramsocket
fi

%files
%defattr(-,root,root)
%doc RELNOTES README.ifenslave
%_sbindir/arping
%_sbindir/clockdiff
/sbin/ifenslave
%attr(700,root,root) %verify(not mode group) /bin/ping
%attr(700,root,root) %verify(not mode group) /bin/ping6
/bin/tracepath
/bin/tracepath6
%_sbindir/rdiscd
%_mandir/man?/*
/etc/control.d/facilities/ping
/etc/control.d/facilities/ping6

%changelog
* Mon Mar 28 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1:s20101006-owl1
- Updated to s20101006.
- Dropped obsoleted patches.
- Updated owl-pingsock and owl-warnings patches.
- Imported patches from ALT, RH and gentoo.
- Removed usages of SO_MARK (because of the kernel version) and libsysfs.
- Introduced lost "ping6.control".

* Tue Feb 01 2011 Solar Designer <solar-at-owl.openwall.com> ss020927-owl10
- Add group _icmp (if it does not exist yet) on package install.
- Revised the control(8) settings for ping(1): added dgramsocket, turned public
into an alias for dgramsocket (for upgrades of systems that used public),
renamed old public into traditional.
- "control ping dgramsocket" by default.

* Mon Jan 31 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> ss020927-owl9
- Added patch for ICMP sockets (no control mode yet).

* Fri Sep 03 2010 Solar Designer <solar-at-owl.openwall.com> ss020927-owl8
- Install ping as "restricted" by default.

* Mon Jan 04 2010 Solar Designer <solar-at-owl.openwall.com> ss020927-owl7
- Added a patch by Simon Baker to make ping6 and tracepath6 work with our new
kernel version.  As a side effect, this breaks builds with Linux 2.4 kernel
headers.  Reference:
http://www.openwall.com/lists/owl-users/2009/12/10/3

* Sun Sep 20 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> ss020927-owl6
- Disabled build time kernel headers check.

* Thu Nov 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> ss020927-owl5
- Added owl-control facility for ping6.
- Relocated ping6, tracepath and tracepath6 to /bin.
- Relocated manual pages for commands to the first section.

* Mon Nov 14 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> ss020927-owl4
- Removed traceroute6 in favour of the traceroute package.

* Sun Jun 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> ss020927-owl3
- Removed verifying permissions and group owner for ping since it's
controlled by owl-control facility.
- Cleaned up the spec.

* Tue Oct 21 2003 Michail Litvak <mci-at-owl.openwall.com> ss020927-owl2
- reduce -owl-socketbits.diff to include only sockaddr_storage
definition, because previous version broke tracepath.

* Thu Oct 16 2003 Michail Litvak <mci-at-owl.openwall.com> ss020927-owl1
- ss020927
- Fixed building with kernel >= 2.4.22.
- Source archive now contains precompiled man pages, so don't include
them as another archive.

* Sun Nov 03 2002 Solar Designer <solar-at-owl.openwall.com>
- Dump/restore the owl-control setting for ping on package upgrades.
- Keep ping at mode 700 ("restricted") in the package, but default it to
"public" in %post when the package is first installed.  This avoids a
race and fail-open behavior where a "restricted" ping could be "public"
during package upgrades.

* Mon Jun 03 2002 Solar Designer <solar-at-owl.openwall.com>
- Patched ifenslave to use the SIOCBOND* ioctl's instead of the obsolete
BOND_* ones when building with Linux 2.4+ kernel headers.

* Thu May 30 2002 Michail Litvak <mci-at-owl.openwall.com>
- ss020124
- include man pages precompiled from sgml sources

* Mon Feb 04 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Tue Apr 10 2001 Solar Designer <solar-at-owl.openwall.com>
- Reviewed patches and RPM spec files of the iputils package in RH, CAEN,
and PLD distributions.
- Updated two RH-derived patches.
- Patched some unimportant gcc warnings.
- Wrote ping.control.
- Wrote this spec file.

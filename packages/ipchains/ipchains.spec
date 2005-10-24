# $Id: Owl/packages/ipchains/Attic/ipchains.spec,v 1.18 2005/10/24 03:06:24 solar Exp $

Summary: Tools for managing ipchains packet filtering rules.
Name: ipchains
Version: 1.3.10
Release: owl13
License: GPL
Group: System Environment/Base
URL: http://netfilter.samba.org/ipchains/
Source0: http://netfilter.samba.org/ipchains/%name-%version.tar.gz
Source1: http://netfilter.samba.org/ipchains/ipchains-scripts-1.1.2.tar.gz
Source2: http://netfilter.samba.org/ipchains/HOWTO.txt.gz
Source3: ipchains.init
Patch0: ipchains-1.3.10-rh-install-no-root.diff
Patch1: ipchains-1.3.10-rh-owl-man.diff
Patch2: ipchains-1.3.10-rh-RETURN.diff
Patch3: ipchains-1.3.10-owl-fixes.diff
PreReq: chkconfig
Requires: fileutils, sh-utils, textutils, grep, sed
Obsoletes: ipfwadm, ipchains-scripts
BuildRoot: /override/%name-%version

%description
Tools found in this package are used to set up, maintain, and inspect the
ipchains-based IP packet filtering rules in the Linux kernel.

ipchains-based filtering is used on Linux 2.2.x kernels and is supported
for backwards compatibility on Linux 2.4.x kernels when they're built with
a non-default configuration option.

%prep
%setup -q -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
install -m 644 %_sourcedir/HOWTO.txt.gz .

%build
%__make clean
%__make CC="%__cc" COPTS="%optflags"

%install
rm -rf %buildroot
mkdir -p %buildroot/sbin
mkdir -p %buildroot%_mandir/man{4,8}

%__make install SBIN=%buildroot/sbin MANDIR=%buildroot%_mandir
pushd ipchains-scripts-1.1.2
cp ipchains-restore ipchains-save %buildroot/sbin/
cp ipfwadm-wrapper %buildroot/sbin/ipfwadm
ln -s ipfwadm %buildroot/sbin/ipfwadm-wrapper
cp *.8 %buildroot%_mandir/man8/
popd

mkdir -p %buildroot/etc/rc.d/init.d
install -m 755 %_sourcedir/ipchains.init \
	%buildroot/etc/rc.d/init.d/ipchains

gzip -9nf ipchains-quickref.ps

%post
/sbin/chkconfig --add ipchains

%preun
if [ $1 -eq 0 ]; then
	/sbin/chkconfig --del ipchains
fi

%files
%defattr(-,root,root)
%doc *.txt*
%doc COPYING README ipchains-quickref.ps.gz
%attr(755,root,root) %config /etc/rc.d/init.d/ipchains
/sbin/*
%_mandir/man*/*

%changelog
* Fri Jan 07 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.3.10-owl13
- Added a patch to deal with "label at end of compound statement" issue.
- Cleaned up the spec.

* Mon Sep 15 2003 Solar Designer <solar-at-owl.openwall.com> 1.3.10-owl12
- In "stop", only try to do anything if ipchains is supported by kernel.

* Fri Aug 22 2003 Solar Designer <solar-at-owl.openwall.com> 1.3.10-owl11
- Corrected the package summary and description to note the difference
from iptables.
- Removed the redirect of ipchains-save output to /dev/null, let's see
if it has anything to say.
- In the config file, only treat lines starting with a '#' and empty
lines as comments; no longer allow for an arbitrary number of spaces
before the '#'.
- PreReq: chkconfig
- Requires: fileutils, sh-utils, textutils, grep, sed

* Mon Feb 04 2002 Michail Litvak <mci-at-owl.openwall.com> 1.3.10-owl10
- Enforce our new spec file conventions

* Mon Dec 10 2001 Solar Designer <solar-at-owl.openwall.com>
- More cleanups to the startup script.
- Corrected the package description.
- Compressed the HOWTO.

* Thu Dec 09 2001 Michail Litvak <mci-at-owl.openwall.com>
- imported from RH
- some spec and ipchains.init cleanups

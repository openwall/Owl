# $Id: Owl/packages/ipchains/Attic/ipchains.spec,v 1.9 2003/08/22 01:44:39 solar Exp $

Summary: Tools for managing ipchains packet filtering rules.
Name: ipchains
Version: 1.3.10
Release: owl11
License: GPL
Group: System Environment/Base
URL: http://netfilter.samba.org/ipchains/
Source0: http://netfilter.samba.org/ipchains/%{name}-%{version}.tar.gz
Source1: http://netfilter.samba.org/ipchains/ipchains-scripts-1.1.2.tar.gz
Source2: http://netfilter.samba.org/ipchains/HOWTO.txt.gz
Source3: ipchains.init
Patch0: ipchains-1.3.10-rh-install-no-root.diff
Patch1: ipchains-1.3.10-rh-owl-man.diff
Patch2: ipchains-1.3.10-rh-RETURN.diff
PreReq: chkconfig
Requires: fileutils, sh-utils, textutils, grep, sed
Obsoletes: ipfwadm, ipchains-scripts
BuildRoot: /override/%{name}-%{version}

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
install -m 644 $RPM_SOURCE_DIR/HOWTO.txt.gz .

%build
make clean
make COPTS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{4,8}

make install SBIN=$RPM_BUILD_ROOT/sbin MANDIR=$RPM_BUILD_ROOT%{_mandir}
pushd ipchains-scripts-1.1.2
cp ipchains-restore ipchains-save $RPM_BUILD_ROOT/sbin/
cp ipfwadm-wrapper $RPM_BUILD_ROOT/sbin/ipfwadm
ln -s ipfwadm $RPM_BUILD_ROOT/sbin/ipfwadm-wrapper
cp *.8 $RPM_BUILD_ROOT%{_mandir}/man8/
popd

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 755 $RPM_SOURCE_DIR/ipchains.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/ipchains

gzip -9nf ipchains-quickref.ps

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_mandir}/man*/*

%changelog
* Fri Aug 22 2003 Solar Designer <solar@owl.openwall.com> 1.3.10-owl11
- Corrected the package summary and description to note the difference
from iptables.
- Removed the redirect of ipchains-save output to /dev/null, let's see
if it has anything to say.
- In the config file, only treat lines starting with a '#' and empty
lines as comments; no longer allow for an arbitrary number of spaces
before the '#'.
- PreReq: chkconfig
- Requires: fileutils, sh-utils, textutils, grep, sed

* Mon Feb 04 2002 Michail Litvak <mci@owl.openwall.com> 1.3.10-owl10
- Enforce our new spec file conventions

* Mon Dec 10 2001 Solar Designer <solar@owl.openwall.com>
- More cleanups to the startup script.
- Corrected the package description.
- Compressed the HOWTO.

* Thu Dec 09 2001 Michail Litvak <mci@owl.openwall.com>
- imported from RH
- some spec and ipchains.init cleanups

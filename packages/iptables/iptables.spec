# $Id: Owl/packages/iptables/iptables.spec,v 1.9 2004/07/26 22:42:59 mci Exp $

Summary: Tools for managing Netfilter/iptables packet filtering rules.
Name: iptables
Version: 1.2.11
Release: owl1
License: GPL
Group: System Environment/Base
URL: http://www.netfilter.org
Source0: http://www.netfilter.org/files/%name-%version.tar.bz2
Source1: iptables.init
PreReq: chkconfig
Requires: fileutils, textutils, grep
BuildRequires: kernel-headers >= 2.4.0
BuildRoot: /override/%name-%version

%description
Tools found in this package are used to set up, maintain, and inspect the
iptables-based IP packet filtering rules in the Linux kernel.

iptables-based filtering is used on Linux 2.4.x and newer kernels.

%prep
%setup -q

%build
OPT="$RPM_OPT_FLAGS"
make iptables-save iptables-restore all \
	COPT_FLAGS="$RPM_OPT_FLAGS" LIBDIR=/%_lib

%install
make install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=/%_lib BINDIR=/sbin MANDIR=%_mandir
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 755 $RPM_SOURCE_DIR/iptables.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/iptables

%post
/sbin/chkconfig --add iptables

%preun
if [ $1 -eq 0 ]; then
	/sbin/chkconfig --del iptables
fi

%files
%defattr(-,root,root)
%attr(755,root,root) %config /etc/rc.d/init.d/iptables
/sbin/iptables*
%_mandir/*/iptables*
%dir /%_lib/iptables
/%_lib/iptables/libipt*

%changelog
* Thu Jul 22 2004 Michail Litvak <mci@owl.openwall.com> 1.2.11-owl1
- 1.2.11

* Mon Sep 15 2003 Solar Designer <solar@owl.openwall.com> 1.2.8-owl2
- In "stop", only try to do anything if iptables is supported by kernel.

* Fri Aug 22 2003 Solar Designer <solar@owl.openwall.com> 1.2.8-owl1
- Further cleanups and changes for consistency with the ipchains package.

* Wed Aug 20 2003 Michail Litvak <mci@owl.openwall.com>
- initial package for Owl.
- startup script cleanups.

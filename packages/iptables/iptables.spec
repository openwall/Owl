# $Id: Owl/packages/iptables/iptables.spec,v 1.1 2003/08/20 13:18:00 mci Exp $

Summary: Tools for managing Linux kernel packet filtering capabilities.
Name: iptables
Version: 1.2.8
Release: owl1
License: GPL
Group: System Environment/Base
URL: http://www.netfilter.org/
Source0: http://www.netfilter.org/files/%{name}-%{version}.tar.bz2
Source1: iptables.init
Requires: chkconfig
BuildRequires: kernel-headers >= 2.4.0
BuildRoot: /override/%{name}-%{version}

%description
The iptables utility controls the network packet filtering code in the
Linux kernel.

%prep
%setup -q

# XXX Fix NETLINK script detection name
mv extensions/.NETLINK.test extensions/.NETLINK-test

%build
OPT="$RPM_OPT_FLAGS"
make COPT_FLAGS="$RPM_OPT_FLAGS" LIBDIR=/%{_lib} iptables-save iptables-restore all

%install
make install DESTDIR=%{buildroot} LIBDIR=/%{_lib} BINDIR=/sbin MANDIR=%{_mandir}
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 755 $RPM_SOURCE_DIR/iptables.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/iptables

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_mandir}/*/iptables*
%dir /%{_lib}/iptables
/%{_lib}/iptables/libipt*

%changelog
* Wed Aug 20 2003 Michail Litvak <mci@owl.openwall.com> 1.2.8-owl1
- initial package for Owl.
- startup script cleanups.

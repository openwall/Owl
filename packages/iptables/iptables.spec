# $Id: Owl/packages/iptables/iptables.spec,v 1.12 2005/01/12 16:13:51 galaxy Exp $

%define BUILD_STATIC 0
%define BUILD_IPV6 0

Summary: Tools for managing Netfilter/iptables packet filtering rules.
Name: iptables
Version: 1.2.11
Release: owl2
License: GPL
Group: System Environment/Base
URL: http://www.netfilter.org
Source0: http://www.netfilter.org/files/%name-%version.tar.bz2
Source1: iptables.init
PreReq: chkconfig
Requires: fileutils, textutils, grep
BuildRequires: kernel-headers >= 2.4.4
BuildRoot: /override/%name-%version

%description
Tools found in this package are used to set up, maintain, and inspect the
iptables-based IP packet filtering rules in the Linux kernel.

iptables-based filtering is used on Linux 2.4.x and newer kernels.

%package -n iptables6
Summary: Tools for managing Netfilter/iptables packet filtering (IPv6).
Group: System Environment/Base
URL: http://www.netfilter.org
PreReq: chkconfig
Requires: fileutils, textutils, grep

%description -n iptables6
Tools found in this package are used to set up, maintain, and inspect the
iptables-based IP packet filtering rules in the Linux kernel. This is an
IPv6 version of iptables.

iptables-based filtering is used on Linux 2.4.x and newer kernels.

%prep
%setup -q

%build

%__make iptables-save iptables-restore all \
	CC="%__cc" \
	COPT_FLAGS="$RPM_OPT_FLAGS" \
%if %BUILD_STATIC
	NO_SHARED_LIBS="1" \
%endif
%if %BUILD_IPV6
	DO_IPV6="1" \
%endif
	IPT_LIBDIR=/%_lib/%name

%install
rm -rf %buildroot

%__make install \
	DESTDIR=%buildroot \
	PREFIX="%_prefix" \
	LIBDIR="/%_lib" \
	BINDIR="/sbin" \
	MANDIR="%_mandir" \
	INCDIR="%_includedir"

mkdir -p %buildroot%_sysconfdir/rc.d/init.d
install -m 755 $RPM_SOURCE_DIR/iptables.init \
	%buildroot%_sysconfdir/rc.d/init.d/iptables

%if !%BUILD_IPV6
rm %buildroot/%_lib/iptables/libip6t*
rm %buildroot/sbin/ip6tables
rm %buildroot%_mandir/man8/ip6tables.8*
%endif

%if %BUILD_STATIC
rm -rf -- %buildroot/%_lib/iptables
%endif

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
%if !%BUILD_STATIC
%dir /%_lib/iptables
/%_lib/iptables/libipt*
%endif

%if %BUILD_IPV6
%files -n iptables6
%defattr(-,root,root)
%if !%BUILD_STATIC
%dir /%_lib/iptables
/%_lib/iptables/libip6t*
%endif
/sbin/ip6tables*
%_mandir/*/ip6tables.8*
%endif

%changelog
* Mon Jan 10 2005 (GalaxyMaster) <galaxy@openwall.com> 1.2.11-owl2
- Corrected kernel requirement to 2.4.4 as mentioned by iptables'
INSTALL.
- Made use of %__cc and %__make macros.
- Added iptables6 package and BUILD_IPV6 macro to control its building.
This need to be revised to add %_sysconfig/etc/init.d/iptables6. NOTE:
I've introduced dual owning of /%_lib/iptables directory by iptables
and iptables6 packages. I think this is ok to share owning of some files
or directories between several related packages which were built from
one parent source package.
- Added BUILD_STATIC macro to allow build all statically, although only
package building was tested in this mode.
- Cleaned up the spec.

* Thu Jul 22 2004 Michail Litvak <mci@owl.openwall.com> 1.2.11-owl1
- 1.2.11

* Mon Sep 15 2003 Solar Designer <solar@owl.openwall.com> 1.2.8-owl2
- In "stop", only try to do anything if iptables is supported by kernel.

* Fri Aug 22 2003 Solar Designer <solar@owl.openwall.com> 1.2.8-owl1
- Further cleanups and changes for consistency with the ipchains package.

* Wed Aug 20 2003 Michail Litvak <mci@owl.openwall.com>
- initial package for Owl.
- startup script cleanups.

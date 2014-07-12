# $Owl: Owl/packages/iptables/iptables.spec,v 1.29 2014/07/12 14:09:13 galaxy Exp $

%define BUILD_IPV6 0

Summary: Tools for managing Netfilter/iptables packet filtering rules.
Name: iptables
Version: 1.4.10
Release: owl3
License: GPLv2+
Group: System Environment/Base
URL: http://www.netfilter.org/projects/iptables/
Source0: ftp://ftp.netfilter.org/pub/iptables/%name-%version.tar.bz2
Source1: iptables.init
Source2: iptables-config
Patch1: iptables-1.4.10-alt-link.diff
Patch2: iptables-1.4.10-alt-modprobe.diff
Patch3: iptables-1.4.9.1-alt-configure.diff
Patch4: iptables-1.4.5-rh-alt-eperm.diff
Patch5: iptables-1.4.10-owl-Makefile.diff
Patch6: iptables-1.4.9.1-owl-nfnetlink.diff
Requires(post,preun): chkconfig
Requires: coreutils, grep, mktemp
BuildRequires: kernel-headers >= 2.4.4
BuildRoot: /override/%name-%version

%description
Tools found in this package are used to set up, maintain, and inspect the
iptables-based IP packet filtering rules in the Linux kernel.

iptables-based filtering is used on Linux 2.4.x and newer kernels.

%if %BUILD_IPV6
%package -n iptables6
Summary: Tools for managing Netfilter/iptables packet filtering (IPv6).
Group: System Environment/Base
URL: http://www.netfilter.org
Requires(post,preun): chkconfig
Requires: coreutils, grep, mktemp
Requires: %name = %version-%release

%description -n iptables6
Tools found in this package are used to set up, maintain, and inspect the
iptables-based IP packet filtering rules in the Linux kernel.  This is an
IPv6 version of iptables.

iptables-based filtering is used on Linux 2.4.x and newer kernels.
%endif

%prep
%setup -q
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p1
%patch6 -p0

%define _libdir /%_lib
%{expand:%%define optflags %optflags -fno-strict-aliasing}

%build
autoreconf
%configure \
	--sbindir=/sbin \
	--with-xtlibdir=/%_lib/iptables \
%if !%BUILD_IPV6
	--disable-ipv6 \
%endif
	#

# Build libraries first
printf '\n%s\n' 'build-libLTLIBRARIES: $(lib_LTLIBRARIES)' >>Makefile
%__make V=1 LDFLAGS=-Wl,--as-needed build-libLTLIBRARIES
%__make V=1 LDFLAGS=-Wl,--as-needed

%if %BUILD_IPV6
sed s/iptables/ip6tables/g <%_sourcedir/iptables.init >ip6tables.init
sed s/iptables/ip6tables/g <%_sourcedir/iptables-config >ip6tables-config
%endif

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot

# Do not package .la files.
rm %buildroot%_libdir/lib*.la

mkdir -p %buildroot/etc/rc.d/init.d %buildroot/etc/sysconfig
install -pm755 %_sourcedir/iptables.init \
	%buildroot/etc/rc.d/init.d/iptables
install -pm600 %_sourcedir/iptables-config \
	%buildroot/etc/sysconfig/
%if %BUILD_IPV6
install -pm755 ip6tables.init \
	%buildroot/etc/rc.d/init.d/ip6tables
install -pm600 ip6tables-config \
	%buildroot/etc/sysconfig/
%endif

%post
/sbin/chkconfig --add iptables

%preun
if [ $1 -eq 0 ]; then
	/sbin/chkconfig --del iptables
fi

%if %BUILD_IPV6
%post -n iptables6
/sbin/chkconfig --add ip6tables

%preun -n iptables6
if [ $1 -eq 0 ]; then
	/sbin/chkconfig --del ip6tables
fi
%endif

%files
%defattr(-,root,root)
%config /etc/rc.d/init.d/iptables
%config(noreplace) /etc/sysconfig/iptables-config
/sbin/iptables*
%_mandir/man8/iptables*
/%_lib/libip4tc.so.*
/%_lib/libxtables.so.*
%dir /%_lib/iptables
/%_lib/iptables/libipt*
/%_lib/iptables/libxt*
%exclude %_bindir/iptables-xml
%exclude %_libdir/lib*.so
%exclude %_includedir/*
%exclude %_libdir/pkgconfig/*.pc
%doc iptables.xslt

%if %BUILD_IPV6
%files -n iptables6
%defattr(-,root,root)
%config /etc/rc.d/init.d/ip6tables
%config(noreplace) /etc/sysconfig/ip6tables-config
/sbin/ip6tables*
%_mandir/*/ip6tables*
/%_lib/libip6tc.so.*
%dir /%_lib/iptables
/%_lib/iptables/libip6t*
%endif

%changelog
* Sat Jun 28 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.4.10-owl3
- Replaced deprecated PreReq with Requires(post,preun).
- Excluded a newly detected unpackaged file (iptables-xml).

* Mon Mar 14 2011 Solar Designer <solar-at-owl.openwall.com> 1.4.10-owl2
- Changed the default for IPTABLES_STATUS_ARGS to "-nv".

* Tue Nov 09 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.4.10-owl1
- Updated to 1.4.10.
- Updated patches alt-link, alt-modprobe and owl-Makefile.

* Sat Aug 21 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.4.9.1-owl1
- Updated to 1.4.9.1.
- Updated patches -alt-link and -alt-configure.
- Dropped patch -alt-fixes (fixed in upstream).
- Dropped patch -owl-warnings.
- Made configure.ac not to use PKG_CONFIG_MODULES.

* Wed Sep 23 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.5-owl1
- Updated to 1.4.5.
- Updated patches from ALT's iptables-1.4.5-alt1 package.
- Dropped BUILD_STATIC support.

* Sat May 20 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.3.5-owl2
- Fixed broken logic for unsupported extensions in extensions/Makefile.
From now on, all unsupported target/matches are marked as such.
- Introduced section PATCH-O-MATIC in iptables.8/ip6tables.8.

* Tue Feb 28 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.3.5-owl1
- Updated to 1.3.5.
- Applied upstream fixes from svn snapshot 6466.
- Imported a bunch of patches from ALT's iptables-1.3.5-alt1 package.
- Reworked startup script, introduced /etc/sysconfig/iptables-config
for tuning it, changed default behaviour to load rules without restoring
byte and package counters.

* Mon Jan 10 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.2.11-owl2
- Corrected kernel requirement to 2.4.4 as mentioned by iptables' INSTALL.
- Made use of %%__cc and %%__make macros.
- Added iptables6 package and BUILD_IPV6 macro to control its building.
This needs to be revised to add /etc/init.d/iptables6.
NOTE: I've introduced joint ownership of /lib/iptables directory by iptables
and iptables6 packages.  I think it's OK to share ownership of some files or
directories between several related packages which were built from one parent
source package.
- Added BUILD_STATIC macro to allow to build all statically, although only
(main) iptables package building was tested in this mode.
- Cleaned up the spec.

* Thu Jul 22 2004 Michail Litvak <mci-at-owl.openwall.com> 1.2.11-owl1
- 1.2.11

* Mon Sep 15 2003 Solar Designer <solar-at-owl.openwall.com> 1.2.8-owl2
- In "stop", only try to do anything if iptables is supported by kernel.

* Fri Aug 22 2003 Solar Designer <solar-at-owl.openwall.com> 1.2.8-owl1
- Further cleanups and changes for consistency with the ipchains package.

* Wed Aug 20 2003 Michail Litvak <mci-at-owl.openwall.com>
- initial package for Owl.
- startup script cleanups.

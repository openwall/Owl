# $Owl: Owl/packages/iptables/iptables.spec,v 1.24 2006/05/20 22:42:58 galaxy Exp $

%define BUILD_STATIC 0
%define BUILD_IPV6 0

Summary: Tools for managing Netfilter/iptables packet filtering rules.
Name: iptables
Version: 1.3.5
Release: owl2
License: GPL
Group: System Environment/Base
URL: http://www.netfilter.org/projects/iptables/
Source0: ftp://ftp.netfilter.org/pub/iptables/%name-%version.tar.bz2
Source1: iptables.init
Source2: iptables-config
Patch0: iptables-1.3.5-svn-r6466.diff
Patch1: iptables-1.3.5-alt-link.diff
Patch2: iptables-1.3.5-alt-modprobe.diff
Patch3: iptables-1.3.5-alt-iptc-defs.diff
Patch4: iptables-1.3.5-rh-alt-eperm.diff
Patch5: iptables-1.3.5-owl-warnings.diff
Patch6: iptables-1.3.5-owl-man.diff
PreReq: chkconfig
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
PreReq: chkconfig
Requires: coreutils, grep, mktemp

%description -n iptables6
Tools found in this package are used to set up, maintain, and inspect the
iptables-based IP packet filtering rules in the Linux kernel.  This is an
IPv6 version of iptables.

iptables-based filtering is used on Linux 2.4.x and newer kernels.
%endif

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%__make all \
	CC="%__cc" \
	COPT_FLAGS="%optflags" \
%if %BUILD_STATIC
	NO_SHARED_LIBS="1" \
%else
	LDLIBS="-ldl" \
%endif
%if %BUILD_IPV6
	experimental \
%endif
	DO_IPV6="%BUILD_IPV6" \
	PREFIX="%_prefix" \
	LIBDIR="/%_lib" \
	BINDIR="/sbin"

%if %BUILD_IPV6
sed s/iptables/ip6tables/g <%_sourcedir/iptables.init >ip6tables.init
sed s/iptables/ip6tables/g <%_sourcedir/iptables-config >ip6tables-config
%endif

%install
rm -rf %buildroot
%__make install \
%if %BUILD_STATIC
	NO_SHARED_LIBS="1" \
%endif
%if %BUILD_IPV6
	install-experimental \
%endif
	DO_IPV6="%BUILD_IPV6" \
	DESTDIR=%buildroot \
	PREFIX="%_prefix" \
	LIBDIR="/%_lib" \
	BINDIR="/sbin" \
	MANDIR="%_mandir" \
	INCDIR="%_includedir"

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
%_mandir/*/iptables*
%if !%BUILD_STATIC
%dir /%_lib/iptables
/%_lib/iptables/libipt*
%endif

%if %BUILD_IPV6
%files -n iptables6
%defattr(-,root,root)
%config /etc/rc.d/init.d/ip6tables
%config(noreplace) /etc/sysconfig/ip6tables-config
/sbin/ip6tables*
%_mandir/*/ip6tables*
%if !%BUILD_STATIC
%dir /%_lib/iptables
/%_lib/iptables/libip6t*
%endif
%endif

%changelog
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

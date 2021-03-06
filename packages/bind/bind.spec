# $Owl: Owl/packages/bind/bind.spec,v 1.33 2016/10/21 03:12:55 solar Exp $

%{?!BUILD_DEVEL:   %define BUILD_DEVEL 0}
%{?!BUILD_IPV6:    %define BUILD_IPV6 0}
%{?!BUILD_OPENSSL: %define BUILD_OPENSSL 0}

Summary: ISC BIND - DNS server.
Name: bind
Version: 9.3.5
Release: owl11
License: BSD-style
URL: http://www.isc.org/products/BIND/
Group: System Environment/Daemons

# ftp://ftp.isc.org/isc/bind9/%version/bind-%version-P2.tar.gz
Source0: bind-%version-P2.tar.bz2
Source1: rfc1912.txt.bz2
Source2: bind-debug.control
Source3: bind-slave.control
Source4: resolver.5
Source5: bind.init
Source6: rndc.key
Source7: rndc.conf
Source8: bind.named.conf
Source9: bind.options.conf
Source10: bind.rndc.conf
Source11: bind.local.conf
Source12: bind.rfc1912.conf
Source13: bind.rfc1918.conf
Source14: bind.localhost
Source15: bind.localdomain
Source16: bind.127.in-addr.arpa
Source17: bind.empty

Patch0: bind-9.3.5-owl-warnings.diff
Patch1: bind-9.3.5-openbsd-owl-pidfile.diff
Patch2: bind-9.3.5-openbsd-owl-chroot-defaults.diff
Patch3: bind-9.3.5-alt-owl-chroot.diff
Patch4: bind-9.3.5-owl-checkconf-chroot.diff
Patch5: bind-9.3.5-rh-h_errno.diff
Patch6: bind-9.3.1-alt-isc-config.diff
Patch7: bind-9.3.5-alt-man.diff
Patch8: bind-9.3.1-alt-owl-rndc-confgen.diff
Patch9: bind-9.3.1-owl-rfc-index.diff
Patch10: bind-9.3.5-openbsd-owl-expand_fdsets.diff
Patch11: bind-9.3.5-owl-CVE-2008-5077.diff
Patch12: bind-9.3.6-up-CVE-2009-0696.diff
Patch13: bind-9.3.5-P2-rh-owl-CVE-2010-3613.diff
Patch14: bind-9.3.5-P2-rh-CVE-2011-4313.diff
Patch15: bind-9.3.5-P2-rh-CVE-2012-1667.diff
Patch16: bind-9.3.5-P2-rh-CVE-2012-4244.diff
Patch17: bind-9.3.5-P2-rh-CVE-2012-5166.diff
Patch18: bind-9.3.5-P2-rh-CVE-2015-5477.diff
Patch19: bind-9.3.5-P2-rh-CVE-2015-5722.diff
Patch20: bind-9.3.5-P2-rh-CVE-2015-8000.diff
Patch21: bind-9.3.5-P2-rh-CVE-2015-8704.diff
Patch22: bind-9.3.5-P2-rh-CVE-2016-1285-CVE-2016-1286.diff
Patch23: bind-9.3.5-P2-rh-CVE-2016-2776.diff
Patch24: bind-9.3.5-P2-rh-CVE-2016-2848.diff

Requires: %name-libs = %version-%release
Requires: owl-startup
Requires: sysklogd >= 1.4.1-owl9
Requires(pre,post): owl-control >= 0.4, owl-control < 2.0
%if %BUILD_OPENSSL
BuildRequires: openssl-devel
%endif
BuildRequires: gcc, gcc-c++, glibc-devel >= 2.3.2, libtool, tar
BuildRequires: rpm-build >= 0:4.11
BuildRoot: /override/%name-%version

%define _localstatedir	/var
%define _chrootdir	%_localstatedir/lib/bind
%define docdir		%_docdir/%name-%version

%description
ISC BIND (Berkeley Internet Name Domain) is an implementation of the DNS
(Domain Name System) protocols.  BIND is the most widely used name server
software on the Internet, and is supported by the Internet Software
Consortium (ISC).

This package provides the server and related configuration files.

%package utils
Summary: Utilities for querying DNS name servers.
Group: Applications/System
Requires: %name-libs = %version-%release

%description utils
This package contains a collection of utilities for querying DNS (Domain
Name System) name servers to find out information about Internet hosts.
These tools will provide you with the IP addresses for given host names,
as well as other information about registered domains and network
addresses.

%package doc
Summary: Documentation for ISC BIND.
Group: Documentation
Requires: %name = %version-%release

%description doc
This package provides various documents that are useful for maintaining a
working BIND installation.

%package libs
Summary: Shared library used by ISC BIND.
Group: System Environment/Libraries

%description libs
This package contains shared libraries used by BIND's daemons
and utilities.

%if %BUILD_DEVEL
%package devel
Summary: Files for building applications with ISC BIND libraries.
Group: Development/Libraries
Requires: %name-libs = %version-%release

%description devel
This package contains development libraries and include files required
for building applications with ISC BIND libraries.
%endif

%prep
%setup -q -n bind-%version-P2
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
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1

install -pm644 %_sourcedir/rfc1912.txt.bz2 doc/rfc/
find doc -type f -name '*.txt' -print0 |
	xargs -r0 bzip2 -9q --

mkdir addon
install -pm644 %_sourcedir/bind.init addon/
install -pm644 %_sourcedir/bind.{named,options,rndc,local,rfc1912,rfc1918}.conf \
	addon/
install -pm644 %_sourcedir/bind.{localhost,localdomain,127.in-addr.arpa,empty} \
	addon/
install -pm644 %_sourcedir/rndc.{conf,key} addon/

sed -i '
s,@ROOT@,%_chrootdir,g;
s,@DOCDIR@,%docdir,g;
s,@SYSCONFDIR@,/etc,g;
s,@SBINDIR@,%_sbindir,g;
' \
	bin/check/named-checkconf.* \
	bin/named/include/named/globals.h \
	bin/named/named.8 bin/rndc/rndc.8 \
	addon/*

%build

# This usage of CPP is a hack, we should fix configure instead -- (GM)
CPP="%__cpp"; export CPP
%configure \
	--enable-shared \
%if %BUILD_DEVEL
	--enable-static \
%else
	--disable-static \
%endif
%if %BUILD_IPV6
	--enable-ipv6 \
%else
	--disable-ipv6 \
%endif
%if %BUILD_OPENSSL
	--with-openssl \
	--disable-openssl-version-check \
%else
	--without-openssl \
%endif
	--disable-threads \
	--disable-linux-caps \
	--with-randomdev=/dev/urandom \
	--with-libtool \
	--with-pic

%__make

%install
rm -rf %buildroot

%__make install DESTDIR=%buildroot

# Install missing man pages
install -pm644 %_sourcedir/resolver.5 %buildroot%_mandir/man5/

# Install startup script for ISC BIND daemon
install -pD -m700 addon/bind.init %buildroot%_initddir/named

# Install control files
install -pD -m700 %_sourcedir/bind-debug.control \
	%buildroot/etc/control.d/facilities/bind-debug
install -pD -m700 %_sourcedir/bind-slave.control \
	%buildroot/etc/control.d/facilities/bind-slave

# Install configurations files
install -pm600 addon/rndc.conf %buildroot/etc/

# Create a chrooted environment ===
mkdir -p %buildroot%_chrootdir/{dev,etc,var/{run,tmp},zone/slave}
for n in named options rndc local rfc1912 rfc1918; do
	install -pm640 addon/bind.$n.conf \
		%buildroot%_chrootdir/etc/$n.conf
done
for n in localhost localdomain 127.in-addr.arpa empty; do
	install -pm640 "addon/bind.$n" %buildroot%_chrootdir/zone/$n
	sed -i 's,YYYYMMDDNN,%(date +%%s),' %buildroot%_chrootdir/zone/$n
done
install -pm640 addon/rndc.key %buildroot%_chrootdir/etc/
ln -s ..%_chrootdir/etc/named.conf %buildroot/etc/

# Make use of the /etc/syslog.d/ feature
touch %buildroot%_chrootdir/dev/log
mkdir %buildroot/etc/syslog.d
ln -s %_chrootdir/dev/log %buildroot/etc/syslog.d/named
# === end of the chroot configuration

# Package documentation files
mkdir -p %buildroot%docdir
cp -a CHANGES COPYRIGHT FAQ README* doc/{arm,draft,misc,rfc} \
	%buildroot%docdir/
bzip2 -9q -- %buildroot%docdir/{CHANGES,FAQ}
rm -- %buildroot%docdir/*/{Makefile*,README-SGML,*.xml}

# Create ghost file
touch %buildroot/var/run/named.pid

# Remove lwresd files
rm %buildroot%_sbindir/lwresd %buildroot%_mandir/man8/lwresd.*

# Remove libtool .la files if any
rm -f %buildroot%_libdir/lib*.la

%pre
grep -q ^named: /etc/group ||
	/usr/sbin/groupadd -g 25 named
grep -q ^named: /etc/passwd ||
	/usr/sbin/useradd -g named -u 25 -d / -s /bin/false \
		-c 'Domain Name Server' -M named
if [ $1 -ge 2 ]; then
	%_sbindir/control-dump bind-debug bind-slave
	if %_initddir/named status; then
		touch /var/run/named.restart
		%_initddir/named stop || :
	fi
fi

%post
if [ $1 -ge 2 ]; then
	%_sbindir/control-restore bind-debug bind-slave
fi
/sbin/chkconfig --add named
test -f /var/run/named.restart && %_initddir/named start || :
rm -f /var/run/named.restart

%preun
if [ $1 -eq 0 ]; then
	%_initddir/named stop || :
	/sbin/chkconfig --del named
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %docdir
%docdir/README*
%docdir/FAQ*
%docdir/misc

/etc/control.d/facilities/*
/etc/named.conf
%config %_initddir/named
%config(noreplace) /etc/rndc.conf
/etc/syslog.d/named

%_sbindir/dnssec-*
%_sbindir/named*
%_sbindir/rndc*

%_mandir/man5/named.conf.5*
%_mandir/man5/rndc.conf.5*
%_mandir/man8/dnssec-*.8*
%_mandir/man8/named*.8*
%_mandir/man8/rndc*.8*

%ghost %attr(644,root,root) /var/run/named.pid

# chroot
%defattr(640,root,named,710)
%dir %_chrootdir
%dir %_chrootdir/dev
%dir %_chrootdir/etc
%dir %_chrootdir/zone
%dir %attr(700,root,named) %verify(not mode) %_chrootdir/zone/slave
%dir %attr(700,root,named) %verify(not mode) %_chrootdir/var
%dir %attr(1770,root,named) %_chrootdir/var/run
%dir %attr(1770,root,named) %_chrootdir/var/tmp
%config(noreplace) %_chrootdir/etc/*.conf
%config(noreplace) %verify(not md5 mtime size) %_chrootdir/etc/rndc.key
%config %_chrootdir/zone/localhost
%config %_chrootdir/zone/localdomain
%config %_chrootdir/zone/127.in-addr.arpa
%config %_chrootdir/zone/empty
%ghost %attr(666,root,root) %_chrootdir/dev/log

%files doc
%defattr(-,root,root)
%docdir
%exclude %docdir/COPYRIGHT
%exclude %docdir/README*
%exclude %docdir/FAQ*
%exclude %docdir/misc

%files libs
%defattr(-,root,root)
%dir %docdir
%docdir/COPYRIGHT
%_libdir/*.so.*

%if %BUILD_DEVEL
%files devel
%defattr(-,root,root)
%_bindir/isc-config.sh
%_includedir/*
%_libdir/*.a
%_libdir/*.so
%_mandir/man3/*
%else
%exclude %_bindir/isc-config.sh
%exclude %_includedir/*
%exclude %_libdir/*.so
%exclude %_mandir/man3/*
%endif

%files utils
%defattr(-,root,root)
%_bindir/dig
%_bindir/host
%_bindir/nslookup
%_bindir/nsupdate
%_mandir/man1/dig.1*
%_mandir/man1/host.1*
%_mandir/man1/nslookup.1*
%_mandir/man5/resolver.5*
%_mandir/man8/nsupdate.8*

%changelog
* Fri Oct 21 2016 Solar Designer <solar-at-owl.openwall.com> 9.3.5-owl11
- Added a patch from bind-9.3.6-25.P1.el5_11.10 for CVE-2016-2848.

* Mon Oct 17 2016 Solar Designer <solar-at-owl.openwall.com> 9.3.5-owl10
- Added patches from bind-9.3.6-25.P1.el5_11.9 for CVE-2015-5722 (likely
unneeded since DNSSEC-specific), CVE-2015-8000, CVE-2015-8704, CVE-2016-1285
and CVE-2016-1286, CVE-2016-2776.

* Fri Jul 31 2015 Solar Designer <solar-at-owl.openwall.com> 9.3.5-owl9
- Reviewed the patches in bind-9.3.6-25.P1.el5_11.3 and added those for
CVE-2010-3613, CVE-2011-4313 (probably unneeded here, as per the discussion
on oss-security back in 2011), CVE-2012-1667, CVE-2012-4244, CVE-2012-5166,
CVE-2015-5477.  Some other patches were not added for being DNSSEC-specific,
or too invasive (most notably, the one for CVE-2014-8500, which hasn't been
tested separately from the complex patch for RH bug 572848), or fixing too
minor issues (CVE-2012-1033, which isn't even included in ISC's matrix).

* Mon Jun 30 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 9.3.5-owl8
- Replaced the deprecated PreReq tag with Requires(pre,post).
- Replaced the deprecated %%_initrddir macro with %%_initddir.

* Thu Dec 09 2010 Solar Designer <solar-at-owl.openwall.com> 9.3.5-owl7
- Disallow zone transfers by default and provide more comments and samples for
other settings in options.conf (suggested by galaxy@ and gremlin@).
- Added a comment on our "chroot by default" into the startup script (suggested
by gremlin@).

* Tue Jul 28 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.5-owl6
- Backported upstream fix for a remote DoS bug (CVE-2009-0696).

* Fri Mar 06 2009 Solar Designer <solar-at-owl.openwall.com> 9.3.5-owl5
- Dropped the root-delegation-only directive from options.conf, made minor
updates to comments in that file.

* Mon Jan 12 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.5-owl4
- Built without openssl by default, thus disabled DNSSEC support.

* Thu Jan 08 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.5-owl3
- Backported upstream fixes of incorrect checks for malformed
DSA signatures (CVE-2008-5077).

* Sun Aug 10 2008 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.5-owl2
- Updated to 9.3.5-P2.
- Implemented automatic fdsets expansion to overcome FD_SETSIZE limit.

* Tue Jul 08 2008 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.5-owl1
- Updated to 9.3.5-P1.  This release additionally randomizes UDP query
ports to improve forgery resilience (VU#800113/CVE-2008-1447).

* Thu Nov 08 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.4-owl4
- Updated L.ROOT-SERVERS.NET address.

* Sun Oct 07 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.4-owl3
- Added recursing-file directive to option.conf file, to make
"rndc recursing" work in "control bind-debug enabled" mode, reported
by galaxy@owl.
- Changed startup script to use /dev/urandom as a source of randomness
during rndc key generation.
- Replaced "rndc stop" with killproc in startup script.

* Mon Jul 30 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.4-owl2
- Updated to 9.3.4-P1.  This release fixes a weakness in DNS query
ids generator which could be used to perform DNS cache poisoning
(CVE-2007-2926).

* Mon Jan 29 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.4-owl1
- Updated to 9.3.4.

* Wed Sep 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.2-owl2
- Updated to 9.3.2-P1.

* Tue Jun 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.2-owl1
- Updated to 9.3.2.

* Thu Oct 27 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 9.3.1-owl5
- Adjusted bind.init to not execute named on system startup by default.

* Fri Oct 21 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 9.3.1-owl4
- Removed '|| :' from touch in %%pre.

* Tue Sep 27 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.1-owl3
- Removed syslog restart code from the %%post script.

* Mon Sep 26 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.1-owl2
- Made build of -devel subpackage conditional and disabled it by default.
- Fixed /etc/syslog.d/named symlink.
- In %%post script, restart syslog service instead of reload, to make
syslogd start listening on the additional socket.

* Fri Sep 23 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 9.3.1-owl1
- Initial release, based on ALT's bind-9.3.1-alt1 package and initial
packaging made by (GalaxyMaster).

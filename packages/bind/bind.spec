# $Id: Owl/packages/bind/bind.spec,v 1.10 2005/10/20 23:30:07 galaxy Exp $

%{?!BUILD_DEVEL:   %define BUILD_DEVEL 0}
%{?!BUILD_IPV6:    %define BUILD_IPV6 0}
%{?!BUILD_OPENSSL: %define BUILD_OPENSSL 1}

Summary: ISC BIND - DNS server.
Name: bind
Version: 9.3.1
Release: owl4
License: BSD-like
URL: http://www.isc.org/products/BIND/
Group: System Environment/Daemons

Source0: ftp://ftp.isc.org/isc/bind9/%{version}/bind-%{version}.tar.gz
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

Patch0: bind-9.3.1-owl-warnings.diff
Patch1: bind-9.3.1-openbsd-owl-pidfile.diff
Patch2: bind-9.3.1-openbsd-owl-chroot-defaults.diff
Patch3: bind-9.3.1-alt-owl-chroot.diff
Patch4: bind-9.3.1-owl-checkconf-chroot.diff
Patch5: bind-9.3.1-rh-owl-bsdcompat.diff
Patch6: bind-9.3.1-rh-dig-lwres_conf_parse.diff
Patch7: bind-9.3.1-rh-h_errno.diff
Patch8: bind-9.3.1-suse-lwres-leak.diff
Patch9: bind-9.3.1-alt-isc-config.diff
Patch10: bind-9.3.1-alt-man.diff
Patch11: bind-9.3.1-alt-owl-rndc-confgen.diff
Patch12: bind-9.3.1-suse-Makefile.diff
Patch13: bind-9.3.1-owl-rfc-index.diff

Requires: %name-libs = %version-%release
Requires: owl-startup
Requires: sysklogd >= 1.4.1-owl9
PreReq: owl-control >= 0.4, owl-control < 2.0
%if %BUILD_OPENSSL
BuildRequires: openssl-devel
%endif
BuildRequires: gcc, gcc-c++, glibc-devel >= 2.3.2, libtool, tar
BuildRequires: rpm-build >= 0:4
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
%setup -q -n %name-%version
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

sed -i -e \
	'
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
install -pD -m700 addon/bind.init %buildroot%_initrddir/named

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
	sed -i -e 's,YYYYMMDDNN,%(date +%%s),' %buildroot%_chrootdir/zone/$n
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
rm -- %buildroot%docdir/*/{Makefile*,README-SGML,*.dsl*,*.sh*,*.xml}

# Create ghost files
mkdir %buildroot/var/run
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
	if %_initrddir/named status; then
		touch /var/run/named.restart
		%_initrddir/named stop || :
	fi
fi

%post
if [ $1 -ge 2 ]; then
	%_sbindir/control-restore bind-debug bind-slave
fi
/sbin/chkconfig --add named
test -f /var/run/named.restart && %_initrddir/named start || :
rm -f /var/run/named.restart

%preun
if [ $1 -eq 0 ]; then
	%_initrddir/named stop || :
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
%config %_initrddir/named
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
* Thu Oct 21 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 9.3.1-owl4
- Removed '|| :' from touch in %%pre.

* Tue Sep 27 2005 Dmitry V. Levin <ldv@owl.openwall.com> 9.3.1-owl3
- Removed syslog restart code from the %%post script.

* Mon Sep 26 2005 Dmitry V. Levin <ldv@owl.openwall.com> 9.3.1-owl2
- Made build of -devel subpackage conditional and disabled it by default.
- Fixed /etc/syslog.d/named symlink.
- In %%post script, restart syslog service instead of reload, to make
syslogd start listening on the additional socket.

* Fri Sep 23 2005 Dmitry V. Levin <ldv@owl.openwall.com> 9.3.1-owl1
- Initial release, based on ALT's bind-9.3.1-alt1 package and initial
packaging made by (GalaxyMaster).

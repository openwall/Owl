# $Id: Owl/packages/tcp_wrappers/tcp_wrappers.spec,v 1.2 2000/11/17 08:22:22 solar Exp $

Summary: A security tool which acts as a wrapper for network services.
Name: tcp_wrappers
Version: 7.6
Release: 1owl
Copyright: Distributable
Group: System Environment/Daemons
Source: ftp.porcupine.org/pub/security/tcp_wrappers_7.6.tar.gz
Patch0: tcp_wrappers_7.6-owl-Makefile.diff
Patch1: tcp_wrappers_7.6-openbsd-owl-cleanups.diff
Patch2: tcp_wrappers_7.6-openbsd-owl-ip-options.diff
Patch3: tcp_wrappers_7.6-owl-safe_finger.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}

%description
This package provides daemon programs and a development library which
can monitor and filter incoming requests for network services.

%prep
%setup -q -n tcp_wrappers_7.6
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%ifarch sparc sparcv9 sparc64
make linux RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC"
%else
make linux RPM_OPT_FLAGS="$RPM_OPT_FLAGS"
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{include,lib,man/man3,man/man5,man/man8,sbin}

cp hosts_access.3 $RPM_BUILD_ROOT/usr/man/man3
cp hosts_access.5 hosts_options.5 $RPM_BUILD_ROOT/usr/man/man5
cp tcpd.8 tcpdchk.8 tcpdmatch.8 $RPM_BUILD_ROOT/usr/man/man8
ln -sf hosts_access.5 $RPM_BUILD_ROOT/usr/man/man5/hosts.allow.5
ln -sf hosts_access.5 $RPM_BUILD_ROOT/usr/man/man5/hosts.deny.5
cp libwrap.a $RPM_BUILD_ROOT/usr/lib
cp tcpd.h $RPM_BUILD_ROOT/usr/include
install -m 755 safe_finger $RPM_BUILD_ROOT/usr/sbin
install -m 755 tcpd $RPM_BUILD_ROOT/usr/sbin
install -m 755 tcpdchk $RPM_BUILD_ROOT/usr/sbin
install -m 755 tcpdmatch $RPM_BUILD_ROOT/usr/sbin
install -m 755 try-from $RPM_BUILD_ROOT/usr/sbin

strip $RPM_BUILD_ROOT/usr/sbin/* || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc BLURB CHANGES README* DISCLAIMER Banners.Makefile
/usr/man/man[358]/*
/usr/include/tcpd.h
/usr/lib/libwrap.a
/usr/sbin/safe_finger
/usr/sbin/tcpd
/usr/sbin/tcpdchk
/usr/sbin/tcpdmatch
/usr/sbin/try-from

%changelog
* Mon Oct 02 2000 Solar Designer <solar@owl.openwall.com>
- Based this spec file on Red Hat's, did some cleanups.
- Replaced all of the RH patches with own and OpenBSD-derived ones.

# $Id: Owl/packages/tcp_wrappers/tcp_wrappers.spec,v 1.3 2002/02/04 09:44:23 solar Exp $

Summary: A security tool which acts as a wrapper for network services.
Name: tcp_wrappers
Version: 7.6
Release: owl1
License: distributable
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
mkdir -p $RPM_BUILD_ROOT/usr/{sbin,lib,include}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{3,5,8}

install -m 755 safe_finger tcpd tcpdchk tcpdmatch try-from \
	$RPM_BUILD_ROOT/usr/sbin/
install -m 644 libwrap.a $RPM_BUILD_ROOT/usr/lib/
install -m 644 tcpd.h $RPM_BUILD_ROOT/usr/include/
install -m 644 hosts_access.3 ${RPM_BUILD_ROOT}%{_mandir}/man3/
install -m 644 hosts_access.5 hosts_options.5 ${RPM_BUILD_ROOT}%{_mandir}/man5/
install -m 644 tcpd.8 tcpdchk.8 tcpdmatch.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/
ln -s hosts_access.5 ${RPM_BUILD_ROOT}%{_mandir}/man5/hosts.allow.5
ln -s hosts_access.5 ${RPM_BUILD_ROOT}%{_mandir}/man5/hosts.deny.5

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc BLURB CHANGES README* DISCLAIMER Banners.Makefile
/usr/sbin/*
/usr/lib/libwrap.a
/usr/include/tcpd.h
%{_mandir}/man*/*

%changelog
* Mon Feb 04 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.
- Use the _mandir macro.

* Mon Oct 02 2000 Solar Designer <solar@owl.openwall.com>
- Based this spec file on Red Hat's, did some cleanups.
- Replaced all of the RH patches with own and OpenBSD-derived ones.

# $Id: Owl/packages/tcp_wrappers/tcp_wrappers.spec,v 1.11 2004/11/02 04:07:08 solar Exp $

Summary: A security tool which acts as a wrapper for network services.
Name: tcp_wrappers
Version: 7.6
Release: owl5
License: distributable
Group: System Environment/Daemons
Source: ftp.porcupine.org/pub/security/tcp_wrappers_7.6.tar.gz
Patch0: tcp_wrappers_7.6-owl-Makefile.diff
Patch1: tcp_wrappers_7.6-openbsd-owl-cleanups.diff
Patch2: tcp_wrappers_7.6-openbsd-owl-ip-options.diff
Patch3: tcp_wrappers_7.6-owl-safe_finger.diff
Patch4: tcp_wrappers_7.6-steveg-owl-match.diff
Patch5: tcp_wrappers_7.6-alt-fix_options.diff
Patch6: tcp_wrappers_7.6-alt-shared.diff
BuildRoot: /override/%name-%version

%description
This package provides daemon programs and a development library which
can monitor and filter incoming requests for network services.

%prep
%setup -q -n tcp_wrappers_7.6
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
make linux EXTRA_CFLAGS="$RPM_OPT_FLAGS -fPIC -DPIC -D_REENTRANT"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{sbin,lib,include}
mkdir -p $RPM_BUILD_ROOT%_mandir/man{3,5,8}

install -m 755 safe_finger tcpd tcpdchk tcpdmatch try-from \
	$RPM_BUILD_ROOT%_sbindir/
install -m 644 libwrap.a $RPM_BUILD_ROOT%_libdir/
cp -a libwrap.so* $RPM_BUILD_ROOT%_libdir/
install -m 644 tcpd.h $RPM_BUILD_ROOT%_includedir/
install -m 644 hosts_access.3 $RPM_BUILD_ROOT%_mandir/man3/
install -m 644 hosts_access.5 hosts_options.5 $RPM_BUILD_ROOT%_mandir/man5/
install -m 644 tcpd.8 tcpdchk.8 tcpdmatch.8 $RPM_BUILD_ROOT%_mandir/man8/
ln -s hosts_access.5 $RPM_BUILD_ROOT%_mandir/man5/hosts.allow.5
ln -s hosts_access.5 $RPM_BUILD_ROOT%_mandir/man5/hosts.deny.5

%files
%defattr(-,root,root)
%doc BLURB CHANGES README* DISCLAIMER Banners.Makefile
%_sbindir/*
%_libdir/libwrap.a
%_libdir/libwrap.so*
%_includedir/tcpd.h
%_mandir/man*/*

%changelog
* Thu Sep 09 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 7.6-owl5
- Re-enabled the patch for building with new glibc.

* Wed May 19 2004 Solar Designer <solar@owl.openwall.com> 7.6-owl4
- Do not apply the patch for building with new glibc just yet as it breaks
things for glibc 2.1.3.

* Wed Apr 21 2004 Michail Litvak <mci@owl.openwall.com> 7.6-owl3.2
- Build shared library (patch from ALT).

* Fri Feb 27 2004 Michail Litvak <mci@owl.openwall.com> 7.6-owl3.1
- Patch from ALT to fix building with glibc 2.3.2.

* Sun Dec 07 2003 Solar Designer <solar@owl.openwall.com> 7.6-owl3
- Don't use a file under /tmp during builds, spotted by (GalaxyMaster).

* Thu Dec 19 2002 Solar Designer <solar@owl.openwall.com> 7.6-owl2
- Handle error conditions with table matching, patch from Steve Grubb.

* Mon Feb 04 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.
- Use the _mandir macro.

* Mon Oct 02 2000 Solar Designer <solar@owl.openwall.com>
- Based this spec file on Red Hat's, did some cleanups.
- Replaced all of the RH patches with own and OpenBSD-derived ones.

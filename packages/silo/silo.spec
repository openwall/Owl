# $Id: Owl/packages/silo/silo.spec,v 1.6 2002/02/05 16:38:35 solar Exp $

Summary: The SILO boot loader for SPARCs.
Name: silo
Version: 0.9.9
Release: owl3
License: GPL
Group: System Environment/Base
Source: ftp://sunsite.mff.cuni.cz/OS/Linux/Sparc/local/silo/silo-%{version}.tgz
Patch: silo-0.9.9-owl-nocat.diff
ExclusiveArch: sparc sparcv9 sparc64
BuildRoot: /override/%{name}-%{version}

%description
The silo package installs the Sparc Improved boot LOader (SILO), which
you'll need to boot Linux on a SPARC.  SILO installs onto your system's
boot block and can be configured to boot Linux, Solaris and SunOS.

%prep
%setup -q -n silo-%{version}
%patch -p1

%build
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{boot,sbin,usr/sbin}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{5,8}

install -m 755 sbin/silo $RPM_BUILD_ROOT/sbin/silo
install -m 644 boot/first.b $RPM_BUILD_ROOT/boot/first.b
install -m 644 boot/ultra.b $RPM_BUILD_ROOT/boot/ultra.b
install -m 644 boot/cd.b $RPM_BUILD_ROOT/boot/cd.b
install -m 644 boot/fd.b $RPM_BUILD_ROOT/boot/fd.b
install -m 644 boot/ieee32.b $RPM_BUILD_ROOT/boot/ieee32.b
install -m 644 boot/second.b $RPM_BUILD_ROOT/boot/second.b
install -m 644 boot/silotftp.b $RPM_BUILD_ROOT/boot/silotftp.b
install -m 755 misc/silocheck $RPM_BUILD_ROOT/usr/sbin/silocheck
install -m 644 man/silo.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5/silo.conf.5
install -m 644 man/silo.8 $RPM_BUILD_ROOT%{_mandir}/man8/silo.8

%clean
rm -rf $RPM_BUILD_ROOT

%post
test -f /etc/silo.conf -a "$SILO_INSTALL" = "yes" && /sbin/silo $SILO_FLAGS || :

%files
%defattr(-,root,root)
%doc docs COPYING ChangeLog
/sbin/silo
/boot/first.b
/boot/ultra.b
/boot/cd.b
/boot/fd.b
/boot/ieee32.b
/boot/silotftp.b
/boot/second.b
/usr/sbin/silocheck
%{_mandir}/man5/silo.conf.5*
%{_mandir}/man8/silo.8*

%changelog
* Tue Feb 05 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Jan 18 2001 Solar Designer <solar@owl.openwall.com>
- Run silo in %post if enabled via $SILO_INSTALL.

* Fri Jan 05 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- disable cat command

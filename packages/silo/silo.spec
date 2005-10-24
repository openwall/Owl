# $Id: Owl/packages/silo/silo.spec,v 1.12 2005/10/24 03:06:29 solar Exp $

Summary: Sparc Improved boot LOader.
Name: silo
Version: 1.4.9
Release: owl1
License: GPL
Group: System Environment/Base
Source: http://www.ultralinux.nl/silo/download/silo-%version.tar.bz2
Patch0: silo-1.2.5-owl-Makefile.diff
Patch1: silo-1.2.5-owl-man.diff
Patch2: silo-1.2.4-aurora-ext3.diff
ExclusiveArch: sparc sparcv9 sparc64
BuildRequires: elftoaout, e2fsprogs-devel
BuildRoot: /override/%name-%version

%description
The silo package installs the Sparc Improved boot LOader (SILO), which
you'll need to boot Linux on a SPARC.  SILO installs onto your system's
boot block and can be configured to boot Linux, Solaris and SunOS.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0

%build
%__make 

%install
rm -rf %buildroot
make install DESTDIR=%buildroot MANDIR=%_mandir
rm -f %buildroot/etc/silo.conf

%post
test -f /etc/silo.conf -a "$SILO_INSTALL" = "yes" && /sbin/silo $SILO_FLAGS || :

%files
%defattr(-,root,root)
%doc docs COPYING ChangeLog etc/silo.conf
/sbin/silo
/usr/bin/tilo
/usr/bin/maketilo
/boot/first.b
/boot/ultra.b
/boot/generic.b
/boot/fd.b
/boot/ieee32.b
/boot/isofs.b
/boot/silotftp.b
/boot/second.b
/usr/sbin/silocheck
%_mandir/man1/*tilo.1*
%_mandir/man5/silo.conf.5*
%_mandir/man8/silo.8*

%changelog
* Tue Oct 18 2005 Alexandr D. Kanevskiy <kad-at-owl.openwall.com> 1.4.9-owl1
- Updated to latest stable version.
- Added patch from Aurora Linux for support unclean ext3, and a little
more debugging info wrt unclean ext2 fs.
- Packaged example silo.conf as documentation.

* Mon Jun 03 2002 Solar Designer <solar-at-owl.openwall.com> 1.2.5-owl1
- Updated to 1.2.5.
- Don't disable cat anymore; anyone who wants boot loader security
should use the proper measures to achieve it.

* Tue Feb 05 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Jan 18 2001 Solar Designer <solar-at-owl.openwall.com>
- Run silo in %post if enabled via $SILO_INSTALL.

* Fri Jan 05 2001 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH
- disable cat command

# $Id: Owl/packages/lilo/lilo.spec,v 1.10 2002/02/15 10:33:57 mci Exp $

Summary: The boot loader for Linux and other operating systems.
Name: lilo
Version: 22.1
Release: owl1
License: MIT
Group: System Environment/Base
Source0: ftp://sunsite.unc.edu/pub/Linux/system/boot/lilo/%{name}-%{version}.tar.gz
Source1: keytab-lilo.c
Patch0: lilo-22.1-rh-broken-headers.diff
Patch1: lilo-22.1-alt-part.diff
Patch2: lilo-22.1-alt-owl-fixes.diff
Patch3: lilo-22.1-alt-owl-getopt.diff
Patch4: lilo-22.1-deb-owl-man.diff
BuildRequires: fileutils, dev86
ExclusiveArch: %ix86
BuildRoot: /override/%{name}-%{version}

%description
LILO (LInux LOader) is a basic system program which boots your Linux
system.  LILO loads the Linux kernel from a floppy or a hard drive,
boots the kernel and passes control of the system to the kernel.  LILO
can also boot other operating systems.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
make CC=gcc OPT="$RPM_OPT_FLAGS -Wall"
gcc $RPM_OPT_FLAGS -Wall -s -o keytab-lilo $RPM_SOURCE_DIR/keytab-lilo.c

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}
make install ROOT=$RPM_BUILD_ROOT MAN_DIR=%{_mandir}
install -m 755 keytab-lilo $RPM_BUILD_ROOT/usr/bin/

%clean
rm -rf $RPM_BUILD_ROOT

%post
test -f /etc/lilo.conf && /sbin/lilo || :

%files
%defattr(-,root,root)
%doc README README.bitmaps README.common.problems README.raid1
%doc CHANGES COPYING INCOMPAT QuickInst
%doc doc
/usr/bin/keytab-lilo
/boot/boot*
/boot/chain.b
/boot/os2_d.b
/sbin/lilo
%{_mandir}/*/*

%changelog
* Thu Feb 14 2002 Michail Litvak <mci@owl.openwall.com>
- 22.1
- removed non-actual patches
- added patches from ALT Linux and Debian

* Tue Feb 05 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Mon Jul 23 2001 Solar Designer <solar@owl.openwall.com>
- Use RPM_OPT_FLAGS.

* Mon Dec 11 2000 Solar Designer <solar@owl.openwall.com>
- Run lilo in %post in case the (physical) location of /boot/boot.b or
whatever else LILO depends on has changed with our upgrade.

* Mon Dec 04 2000 Solar Designer <solar@owl.openwall.com>
- No longer require mkinitrd.

* Sun Nov 19 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- 21.6
- import from RH

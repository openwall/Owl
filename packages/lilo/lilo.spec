# $Id: Owl/packages/lilo/lilo.spec,v 1.7 2002/02/05 19:57:09 mci Exp $

Summary: The boot loader for Linux and other operating systems.
Name: lilo
Version: 21.6
Release: owl5
License: MIT
Group: System Environment/Base
Source0: ftp://sunsite.unc.edu/pub/Linux/system/boot/lilo/%{name}-%{version}.tar.gz
Source1: keytab-lilo.c
Patch1: lilo-21-rh-broken-headers.diff
Patch2: lilo-21.4.4-rh-sa5300.diff
Patch3: lilo-21.4.4-rh-i2o.diff
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
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
make CC=gcc CFLAGS="$RPM_OPT_FLAGS -Wall"
gcc $RPM_OPT_FLAGS -Wall -s -o keytab-lilo $RPM_SOURCE_DIR/keytab-lilo.c
#make -C doc || :
#dvips doc/user.dvi -o doc/User_Guide.ps
#dvips doc/tech.dvi -o doc/Technical_Guide.ps
#rm -f doc/*.aux doc/*.log doc/*.toc

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
make install ROOT=$RPM_BUILD_ROOT MAN_DIR=%{_mandir}
mv $RPM_BUILD_ROOT/usr/sbin $RPM_BUILD_ROOT/usr/bin
install -m 755 keytab-lilo $RPM_BUILD_ROOT/usr/bin

%clean
rm -rf $RPM_BUILD_ROOT

%post
test -f /etc/lilo.conf && /sbin/lilo || :

%files
%defattr(-,root,root)
%doc README CHANGES COPYING INCOMPAT QuickInst
%doc doc
/usr/bin/keytab-lilo
/boot/boot*
/boot/chain.b
/boot/message
/boot/os2_d.b
/sbin/lilo
%{_mandir}/*/*

%changelog
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

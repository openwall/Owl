# $Id: Owl/packages/lilo/lilo.spec,v 1.5 2001/07/23 14:25:48 solar Exp $

Summary: The boot loader for Linux and other operating systems.
Name: lilo
Version: 21.6
Release: 4owl
ExclusiveArch: %ix86
License: MIT
Group: System Environment/Base
Source0: ftp://sunsite.unc.edu/pub/Linux/system/boot/lilo/%{name}-%{version}.tar.gz
Source1: keytab-lilo.c
Patch0: lilo-21.6-owl-loop-floppy.diff
Patch1: lilo-21-rh-broken-headers.diff
Patch2: lilo-21.4.4-rh-sa5300.diff
Patch3: lilo-21.4.4-rh-i2o.diff
Buildroot: /var/rpm-buildroot/%{name}-root
BuildRequires: fileutils dev86

%description
LILO (LInux LOader) is a basic system program which boots your Linux
system.  LILO loads the Linux kernel from a floppy or a hard drive,
boots the kernel and passes control of the system to the kernel.  LILO
can also boot other operating systems.

%prep
%setup -q
%patch0 -p1
# work around broken kernel headers
%patch1 -p1 -b .broken
%patch2 -p1 -b .sa5300
%patch3 -p1 -b .i2o

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
install -m755 keytab-lilo $RPM_BUILD_ROOT/usr/bin
install -m644 %{SOURCE1} $RPM_BUILD_ROOT/boot/message

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
* Mon Jul 23 2001 Solar Designer <solar@owl.openwall.com>
- Support 1.44 MB floppy disk images via loopback block devices such that
no physical floppy disk is needed when preparing bootable CD's with LILO.
- Use RPM_OPT_FLAGS.

* Mon Dec 11 2000 Solar Designer <solar@owl.openwall.com>
- Run lilo in %post in case the (physical) location of /boot/boot.b or
whatever else LILO depends on has changed with our upgrade.

* Mon Dec 04 2000 Solar Designer <solar@owl.openwall.com>
- No longer require mkinitrd.

* Sun Nov 19 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- 21.6
- import from RH 

* Sun Aug 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- added tetex-latex, fileutils and dev86 as build requirements
- use %%{_tmppath}
- include man-pages (#16984)

* Wed Aug 23 2000 Michael K. Johnson <johnsonm@redhat.com>
- Fix up "unsafe" (Bug #14855)

* Tue Aug 22 2000 Michael K. Johnson <johnsonm@redhat.com>
- added lilo-21.4.4-i2o.patch to add i2o boot support

* Tue Aug 08 2000 Karsten Hopp <karsten@redhat.de>
- changed major number of SA5300 controller to 104

* Mon Aug  7 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- (oops only did half of the work)
- add bug-fix to not have lilo core-dump on some config files

* Tue Aug 01 2000 Karsten Hopp <karsten@redhat.de>
- added patches for Compaqs SA5300 controller

* Tue Jul 25 2000 Matt Wilson <msw@redhat.com>
- push through again, stale .src.rpm

* Fri Jul 21 2000 Bill Nottingham <notting@redhat.com>
- require mkinitrd

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul 03 2000 Preston Brown <pbrown@redhat.com>
- 21.4.4
- loopdev, "second" patches fall away (now incl. upstream)
- regenerate graphical patch against new tree
- remove patch hacking around compiler screwups
- much improved boot screen.  thanks msw.

* Mon Jun 19 2000 Preston Brown <pbrown@redhat.com>
- new boot graphic.
- work around broken 2.4 kernel headers.

* Fri Jun 02 2000 Preston Brown <pbrown@redhat.com>
- slightly better graphic, enable flame for the beta. :)
- remove volatile compiler keywords, it breaks the new gcc

* Tue May 16 2000 Preston Brown <pbrown@redhat.com>
- adopted graphical hacks from Stormix/Debian

* Wed Mar 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 21.4.1

* Wed Feb  2 2000 Bill Nottingham <notting@redhat.com>
- add %defattr

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- keytab-lilo is now a c program

* Thu Jan 20 2000 Cristian Gafton <gafton@redhat.com>
- oot added the loopdev patches
- revert the raid patch

* Mon Jan 17 2000 Cristian Gafton <gafton@redhat.com>
- slightly modify the raid patch so we can check for invalid 
  devices before opening them
- add -second patch to fix parsing the command line args

* Tue Sep 21 1999 Doug Ledford <dledford@redhat.com>
- Remove the EBDA patch from zab and put in the EBDA patch
  from the VA Research RPM.  This fixes the EBDA issues.
- Added ONE_SHOT to the compile options so that the lilo
  prompt won't timeout once you hit a key at the boot prompt

* Sat Sep 11 1999 Cristian Gafton <gafton@redhat.com>
- don't run lilo in the %post (why was that necesary?)

* Tue Apr 13 1999 Matt Wilson <msw@redhat.com>
- added patch to make Compaq SmartArrays bootable

* Wed Mar 24 1999 Bill Nottingham <notting@redhat.com>
- add EBDA patch from zab

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- add keytab-lilo.pl to the file list

* Sun Dec  6 1998 Matt Wilson <msw@redhat.com>
- updated to release 0.21
- patched to build on 2.1.x kernels

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- updated to release 0.20
- uses a build root

* Tue Jul 08 1997 Erik Troan <ewt@redhat.com>
- built against glibc

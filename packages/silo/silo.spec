# $Id: Owl/packages/silo/silo.spec,v 1.5 2001/01/18 03:25:47 solar Exp $

%define 	SILO_NO_CAT	'yes'

Summary: 	The SILO boot loader for SPARCs.
Name: 		silo
Version: 	0.9.9
Release: 	3owl
Copyright: 	GPL
Group: 		System Environment/Base
Source: 	ftp://sunsite.mff.cuni.cz/OS/Linux/Sparc/local/silo/silo-%{version}.tgz
Patch:		silo-0.9.9-owl-nocat.diff
ExclusiveArch: 	sparc sparcv9 sparc64
BuildRoot: 	/var/rpm-buildroot/%{name}-root

%description
The silo package installs the Sparc Improved boot LOader (SILO), which
you'll need to boot Linux on a SPARC.  SILO installs onto your system's
boot block and can be configured to boot Linux, Solaris and SunOS.

%prep
%setup -q -n silo-%{version}

%if "%{SILO_NO_CAT}"=="'yes'"
%patch -p1
%endif

%build
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{boot,sbin,usr/sbin}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{5,8}

install -m755 sbin/silo		$RPM_BUILD_ROOT/sbin/silo
install -m644 boot/first.b	$RPM_BUILD_ROOT/boot/first.b
install -m644 boot/ultra.b	$RPM_BUILD_ROOT/boot/ultra.b
install -m644 boot/cd.b		$RPM_BUILD_ROOT/boot/cd.b
install -m644 boot/fd.b		$RPM_BUILD_ROOT/boot/fd.b
install -m644 boot/ieee32.b	$RPM_BUILD_ROOT/boot/ieee32.b
install -m644 boot/second.b	$RPM_BUILD_ROOT/boot/second.b
install -m644 boot/silotftp.b	$RPM_BUILD_ROOT/boot/silotftp.b
install -m755 misc/silocheck	$RPM_BUILD_ROOT/usr/sbin/silocheck
install -m644 man/silo.conf.5	$RPM_BUILD_ROOT%{_mandir}/man5/silo.conf.5
install -m644 man/silo.8	$RPM_BUILD_ROOT%{_mandir}/man8/silo.8

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
* Thu Jan 18 2001 Solar Designer <solar@owl.openwall.com>
- Run silo in %post if enabled via $SILO_INSTALL.

* Fri Jan 05 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- disable cat command

* Fri Jul 14 2000 Jakub Jelinek <jakub@redhat.com>
- use %%{_mandir}

* Fri Jul 14 2000 Jakub Jelinek <jakub@redhat.com>
- Pete Zaitcev's JavaStation flash patch
- work around 2.4 kernel headers

* Tue Mar  7 2000 Jakub Jelinek <jakub@redhat.com>
- Set partat0 correctly

* Tue Feb 15 2000 Jakub Jelinek <jakub@redhat.com>
- RAID1 fixes
- package ieee32 bootblock

* Mon Feb 14 2000 Jakub Jelinek <jakub@redhat.com>
- fix -J operation (hopefully)

* Fri Feb  4 2000 Jakub Jelinek <jakub@redhat.com>
- RAID1 support
- man pages are compressed

* Thu Nov 11 1999 Jakub Jelinek <jakub@redhat.com>
- fix reading above 4GB

* Wed Nov  3 1999 Jakub Jelinek <jakub@redhat.com>
- for new kernels, put initial ramdisk right after
  their _end if it fits, should fix many problems with
  initrd loading.
- removed bootfile patch - it was not working anyway
  and AFAIK noone used it

* Tue Oct 12 1999 Jakub Jelinek <jakub@redhat.com>
- fixed a horrible bug introduced in the last release.
  Thanks DaveM.

* Mon Oct 11 1999 Jakub Jelinek <jakub@redhat.com>
- fix support for less buggy PROMs (those which are able
  to read above 1GB, but not 2GB).

* Fri Oct  8 1999 Jakub Jelinek <jakub@redhat.com>
- use some partition device and not whole device if
  possible for masterboot installs
- remove a lot of old cruft, including -d, -o and -O
  options
- no longer do any heuristic about where to put
  the bootblock, simply if -t is not given, it goes
  to bootblock at cylinder 0, otherwise to the
  partition bootblock
- make silotftp.b work

* Wed Oct  6 1999 Jakub Jelinek <jakub@redhat.com>
- brown paper bag bugfix to get cd booting of
  gzipped images working

* Mon Oct  4 1999 Jakub Jelinek <jakub@redhat.com>
- fix bug on traversing non-absolute symlinks

* Tue Sep 28 1999 Jakub Jelinek <jakub@redhat.com>
- don't install silo in %post.

* Thu Sep 23 1999 Jakub Jelinek <jakub@redhat.com>
- actually install the new man page.

* Mon Sep 20 1999 Jakub Jelinek <jakub@redhat.com>
- update to 0.8.8.

* Fri Sep 17 1999 Jakub Jelinek <jakub@redhat.com>
- update to 0.8.7.

* Tue Apr 20 1999 Jakub Jelinek <jj@ultra.linux.cz>
- update to 0.8.6.

* Tue Apr 13 1999 Jeff Johnson <jbj@redhat.com>
- update to pre0.8.6-1.

* Mon Mar 22 1999 Bill Nottingham <notting@redhat.com>
- fix password checking (bug #1054)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Fri Mar 12 1999 Jeff Johnson <jbj@redhat.com>
- add -lc to work around mis-built libext2fs.so

* Thu Dec 17 1998 Jeff Johnson <jbj@redhat.com>
- update to 0.8.5.

* Thu Nov  5 1998 Jeff Johnson <jbj@redhat.com>
- update to 0.8.2.

* Mon Oct 19 1998 Jeff Johnson <jbj@redhat.com>
- update to 0.8.1.

* Wed Sep 30 1998 Jeff Johnson <jbj@redhat.com>
- update to 0.8.
- run silo automagically on install.

* Wed Sep 23 1998 Jeff Johnson <jbj@redhat.com>
- update to pre-0.7.3-3.

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- build root

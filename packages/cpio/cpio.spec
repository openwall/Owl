# $Id: Owl/packages/cpio/cpio.spec,v 1.3 2000/11/29 16:01:06 kad Exp $

Summary: A GNU archiving program.
Name: cpio
Version: 2.4.2
Release: 22owl
Copyright: GPL
Group: Archiving/Backup
conflicts: mt-st
Source: ftp://ftp.gnu.org/gnu/cpio-2.4.2.tar.gz
Patch1:  cpio-2.4.2-deb-cpio.diff
Patch2:  cpio-2.4.2-deb-mt_scsi.diff
Patch3:  cpio-2.4.2-deb-rmt.diff
Patch4:  cpio-2.4.2-deb-glibc21.diff
Patch5:  cpio-2.4.2-deb-cpio_man.diff
Patch6:  cpio-2.4.2-deb-cpio_info.diff
Patch7:  cpio-2.4.2-deb-mt_man.diff
Patch8:  cpio-2.4.2-deb-rmt_man.diff
Patch9:  cpio-2.4.2-rh-fhs.diff
Patch10: cpio-2.4.2-rh-glibc.diff
Patch11: cpio-2.4.2-rh-man.diff
Patch12: cpio-2.4.2-rh-mtime.diff
Patch13: cpio-2.4.2-rh-svr4compat.diff
Patch14: cpio-2.4.2-rh-emptylink.diff
Patch15: cpio-2.4.2-rh-longlongdev.diff
Prereq: /sbin/install-info
Prefix: %{_prefix}
Buildroot: /var/rpm-buildroot/%{name}-root

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

Install cpio if you need a program to manage file archives.

%prep
%setup -q
%patch1  -p1
%patch2  -p1
%patch3  -p1
%patch4  -p1
%patch5  -p1
%patch6  -p1
%patch7  -p1
%patch8  -p1
%patch9  -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

%build
%configure

make LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=$RPM_BUILD_ROOT/bin mandir=$RPM_BUILD_ROOT/%{_mandir}/

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 rmt.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/cpio.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/cpio.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc README NEWS
/bin/cpio
/bin/mt
/usr/libexec/rmt
%{_infodir}/cpio.*
%{_mandir}/man1/cpio.1*
%{_mandir}/man8/rmt.8*

%changelog
* Wed Nov 29 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- imported 2 patch from RH7

* Sun Nov 26 2000 Michail Litvak <mci@owl.openwall.com>
- Imported from RH
- added some patches from Debian
  (many bug fixes in cpio, mt and rmt improvements)
- man page for rmt

* Tue Aug  8 2000 Jeff Johnson <jbj@redhat.com>
- update man page with decription of -c behavior (#10581).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Preston Brown <pbrown@redhat.com>
- patch from HJ Lu for better error codes upon exit

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- missing defattr.

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Fri Dec 17 1999 Jeff Johnson <jbj@redhat.com>
- revert the stdout patch (#3358), restoring original GNU cpio behavior
  (#6376, #7538), the patch was dumb.

* Tue Aug 31 1999 Jeff Johnson <jbj@redhat.com>
- fix infinite loop unpacking empty files with hard links (#4208).
- stdout should contain progress information (#3358).

* Sun Mar 21 1999 Crstian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- longlong dev wrong with "-o -H odc" headers (formerly "-oc").

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to compile on glibc 2.1, where strdup is a macro

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump package.
- Don't include /bin/mt -- use the mt from mt-st package.
- Add prereq's

* Tue Jun 30 1998 Jeff Johnson <jbj@redhat.com>
- fix '-c' to duplicate svr4 behavior (problem #438)
- install support programs & info pages

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot
- removed "(used by RPM)" comment in Summary

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- no longer statically linked as RPM doesn't use cpio for unpacking packages

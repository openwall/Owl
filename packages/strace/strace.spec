# $Id: Owl/packages/strace/strace.spec,v 1.2 2001/01/25 13:57:17 mci Exp $

Summary: Tracks and displays system calls associated with a running process.
Name: strace
Version: 4.2
Release: 11owl 
Copyright: distributable
Group: Development/Debuggers
Source: http://www.liacs.nl/~wichert/strace/strace-%{version}.tar.gz
Patch0: strace-4.1-rh-sparc.diff
Patch1: strace-4.2-deb-lfs.diff
Patch2: strace-4.2-owl-timex.diff
Patch3: strace-4.2-rh-stat64.diff
Patch4: strace-4.2-rh-putmsg.diff
Patch5: strace-4.2-owl-printsock.diff
Prefix: %{_prefix}
Buildroot: /var/rpm-buildroot/%{name}-root

# ExcludeArch: ia64

%description
The strace program intercepts and records the system calls called and
received by a running process.  Strace can print a record of each
system call, its arguments and its return value.  Strace is useful for
diagnosing problems and debugging, as well as for instructional
purposes.

Install strace if you need a tool to track the system calls made and
received by a process.

%prep
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
libtoolize --copy --force
aclocal
autoheader
autoconf

%configure
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
%makeinstall man1dir=${RPM_BUILD_ROOT}%{_mandir}/man1
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/strace

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}/bin/strace
%{_mandir}/man1/strace.1*

%changelog
* Thu Jan 25 2001 Michail Litvak <mci@owl.openwall.com>
- Added patch to fix printsock 

* Mon Jan 23 2001 Michail Litvak <mci@owl.openwall.com>
- Imported from RH
- Removed most of 2.4 related patches...
- Added patch to compile on 2.2 kernels (strace-4.2-owl-timex.diff)
 
* Sat Aug 19 2000 Jakub Jelinek <jakub@redhat.com>
- doh, actually apply the 2.4 syscalls patch
- make it compile with 2.4.0-test7-pre4+ headers, add
  getdents64 and fcntl64

* Thu Aug  3 2000 Jakub Jelinek <jakub@redhat.com>
- add a bunch of new 2.4 syscalls (#14036)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild
- excludearch ia64

* Fri Jun  2 2000 Matt Wilson <msw@redhat.com>
- use buildinstall for FHS

* Wed May 24 2000 Jakub Jelinek <jakub@redhat.com>
- make things compile on sparc
- fix sigreturn on sparc

* Fri Mar 31 2000 Bill Nottingham <notting@redhat.com>
- fix stat64 misdef (#10485)

* Tue Mar 21 2000 Michael K. Johnson <johnsonm@redhat.com>
- added ia64 patch

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- version 4.2 (why are we keeping all these patches around?)

* Sat Nov 27 1999 Jeff Johnson <jbj@redhat.com>
- update to 4.1 (with sparc socketcall patch).

* Fri Nov 12 1999 Jakub Jelinek <jakub@redhat.com>
- fix socketcall on sparc.

* Thu Sep 02 1999 Cristian Gafton <gafton@redhat.com>
- fix KERN_SECURELVL compile problem

* Tue Aug 31 1999 Cristian Gafton <gafton@redhat.com>
- added alpha patch from HJLu to fix the osf_sigprocmask interpretation

* Sat Jun 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.99.1.

* Wed Jun  2 1999 Jeff Johnson <jbj@redhat.com>
- add (the other :-) jj's sparc patch.

* Wed May 26 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to 3.99 in order to
-    add new 2.2.x open flags (#2955).
-    add new 2.2.x syscalls (#2866).
- strace 3.1 patches carried along for now.

* Sun May 16 1999 Jeff Johnson <jbj@redhat.com>
- don't rely on (broken!) rpm %patch (#2735)

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binary

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 16)

* Tue Feb  9 1999 Jeff Johnson <jbj@redhat.com>
- vfork est arrive!

* Tue Feb  9 1999 Christopher Blizzard <blizzard@redhat.com>
- Add patch to follow clone() syscalls, too.

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- patch to build alpha/sparc with glibc 2.1.

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to build on ARM

* Wed Sep 30 1998 Jeff Johnson <jbj@redhat.com>
- fix typo (printf, not tprintf).

* Sat Sep 19 1998 Jeff Johnson <jbj@redhat.com>
- fix compile problem on sparc.

* Tue Aug 18 1998 Cristian Gafton <gafton@redhat.com>
- buildroot

* Mon Jul 20 1998 Cristian Gafton <gafton@redhat.com>
- added the umoven patch from James Youngman <jay@gnu.org>
- fixed build problems on newer glibc releases

* Mon Jun 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

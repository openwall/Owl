# $Id: Owl/packages/man-pages/man-pages.spec,v 1.4 2001/05/03 07:05:35 mci Exp $

Summary: Man (manual) pages from the Linux Documentation Project.
Name: man-pages
Version: 1.35
Release: 3owl
Copyright: distributable
Group: Documentation
Source0: ftp://ftp.win.tue.nl/pub/linux-local/manpages/man-pages-%{version}.tar.gz 
Source1: rpcgen.1
Source2: ldd.1
Source3: getent.1
Source4: iconv.1
Source5: locale.1
Source6: localedef.1
Source7: sprof.1
Source8: getcontext.2
Source9: setcontext.2
Source10: sigaltstack.2
Source11: ld-linux.so.8
Source12: ldconfig.8
Source13: rpcinfo.8
Patch1: man-pages-1.35-deb-misc.diff
Patch2: man-pages-1.35-rh-ctype.diff
# temporarily disabled, we don't yet have these paths
# Patch3: man-pages-1.35-rh-pathupdate.diff
Patch4: man-pages-1.35-rh-unicodeurl.diff
Patch5: man-pages-1.35-rh-roffix.diff
Patch6: man-pages-1.35-rh-mssync.diff
Patch7: man-pages-1.35-owl-ccldso.diff
Patch8: man-pages-1.35-owl-uselib.diff
Buildroot: /var/rpm-buildroot/%{name}-root
Autoreqprov: false
BuildArchitectures: noarch

%description
A large collection of man pages (documentation) from the Linux
Documentation Project (LDP).  The man pages are organized into the
following sections: Section 1, user commands (intro only); Section 2,
system calls; Section 3, libc calls; Section 4, devices (e.g., hd,
sd); Section 5, file formats and protocols (e.g., wtmp, /etc/passwd,
nfs); Section 6, games (intro only); Section 7, conventions, macro
packages, etc. (e.g., nroff, ascii); and Section 8, system
administration (intro only).

%prep
%setup -q

cp %{SOURCE1} man1
cp %{SOURCE2} man1
cp %{SOURCE3} man1
cp %{SOURCE4} man1
cp %{SOURCE5} man1
cp %{SOURCE6} man1
cp %{SOURCE7} man1

cp %{SOURCE8} man2
cp %{SOURCE9} man2
cp %{SOURCE10} man2

cp %{SOURCE11} man8
cp %{SOURCE12} man8
cp %{SOURCE13} man8

%patch1 -p1 
%patch2 -p1
# %patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
rm -fv man1/README
mv -fv man1/COPYING .

# These are parts of fileutils
rm -fv man1/{chgrp,chmod,chown,cp,dd,df,dircolors,du,install}.1
rm -fv man1/{ln,ls,mkdir,mkfifo,mknod,mv,rm,rmdir,touch}.1
rm -fv man1/{dir,vdir}.1

# Part of quota
rm -fv man2/quotactl.2

# Part of modutils
rm -fv man2/get_kernel_syms.2
rm -fv man2/{create,delete,init,query}_module.2

# Part of console-tools
rm -fv man4/console.4

# part of nfs-utils
rm -fv man5/exports.5
rm -fv man5/nfs.5

# Part of bind-utils
rm -fv man5/resolver.5
rm -fv man5/resolv.conf.5

# Obsolete
rm -f man3/infnan.3

# Part of mount
rm -fv man5/fstab.5

# Part of time
rm -fv man1/time.1

# find . -name "*sudo*" -exec rm {} \;

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mandir}
for n in 1 2 3 4 5 6 7 8; do
	mkdir $RPM_BUILD_ROOT%{_mandir}/man$n
done
for n in man?/*; do
	cp -a $n $RPM_BUILD_ROOT%{_mandir}/$n
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc README man-pages-%{version}.Announce
%{_mandir}/man*/*

%changelog
* Wed May 02 2001 Michail Litvak <mci@owl.openwall.com>
- use cp instead of cp -a in spec
- uselib.2 patch

* Mon Apr 30 2001 Michail Litvak <mci@owl.openwall.com>
- Disabled patch 3 (we don't yet have these paths)
- added man for ld-linux.so
- remove time.1 (it is in time package)
- man-pages-extralocale.tar.bz2, man2.tar.gz replaced
  by just non packed files (is better for storing in CVS) 
- patch to replace cc(1) -> gcc(1), ld.so -> ld-linux.so

* Fri Apr 27 2001 Michail Litvak <mci@owl.openwall.com>
- Imported from RH 7.1
- added patch from Debian
- removed man page for ld.so as obsolete

* Wed Apr  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- use MS_SYNCHRONOUS instead of MS_SYNC in mount(2) (#34665)

* Tue Apr  3 2001 Trond Eivind Glomsrød <teg@redhat.com>
- roff fixes to multiple man pages

* Mon Apr  2 2001 Trond Eivind Glomsrød <teg@redhat.com>
- correct the URL for unicode in the charset manpage (#34291)
- roff fixes
- redo iconv patch, so we don't get a .orig from patch because of
  a two line offset

* Fri Mar 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- remove resolv.conf (bind-utils) and infnan (obsolete - #34171)

* Wed Mar 28 2001 Trond Eivind Glomsrød <teg@redhat.com>
- resurrect getnetent(3)

* Sun Mar 25 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.35, obsoletes patch for strsep
- move rpcinfo to section 8 (#33114)

* Fri Mar  9 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Include man-pages on locales (#29713)

* Tue Feb 13 2001 Trond Eivind Glomsrød <teg@redhat.com>
- fix return value of strsep(3) call (#24789)

* Mon Jan 15 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.34

* Fri Dec 15 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 1.33
- obsolete some old, now included patches
- remove netman-cvs, it's now older than the mainstream

* Tue Nov 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Identify two of the macros in stat(2) as GNU, not POSIX. (#21169)

* Wed Nov 08 2000 Trond Eivind Glomsrød <teg@redhat.com>
- don't delete the man pages for dlopen() and friends, 
  they are no longer part of another package
- include man pages for ld*

* Thu Oct 24 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove const from iconv function prototype (#19486)

* Tue Aug 29 2000 Trond Eivind Glomsrød <teg@redhat.com>
- reference wctype(3) instead of non-existing ctype(3)
  from regex(7) (#17037)
- 1.31

* Sun Aug 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove lilo man pages (now included in package)
  (#16984)

* Fri Aug 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fixed bad header specification (#15364)
- removed obsolete patches from package
- updated the rest

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Matt Wilson <msw@redhat.com>
- defattr before docs in filelist

* Sun Jun 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- updated to 1.30

* Tue Jun 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}

* Wed May 31 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove resolv.conf(5) - part of bind-utils

* Tue May 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Remove resolver, dlclose, dlerror, dlopen, dlsym as these
  are included in other packages.

* Tue May 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_mandir) instead of /usr/man
- verify and fix bug in mmap man page (#7382)
- verify and fix missing data in recvfrom man page (#1736)
- verify and fix missing data in putw man page (#10104)
- fixed sendfile(2) man page (#5599)
- fixed tzset man page (#11623)

* Mon May 15 2000 Trond Eivind Glomsrød <teg@redhat.com>
- updated to 1.29
- split off other languages into separate RPMS 

* Thu Mar 16 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- do not use group "man"

* Fri Mar 03 2000 Cristian Gafton <gafton@redhat.com>
- don't apply the netman-cvs man pages anymore, as they seem to be really
  out of date

* Sat Feb 05 2000 Cristian Gafton <gafton@redhat.com>
- put back man3/resolver.3

* Fri Feb 04 2000 Cristian Gafton <gafton@redhat.com>
- remove non-man pages (#7814)

* Fri Feb  4 2000 Matt Wilson <msw@redhat.com>
- exclude dir.1 and vdir.1 (these are in the fileutils package)

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- version 1.28

* Fri Nov 05 1999 Michael K. Johnson <johnsonm@redhat.com>
- Fixed SIGILL, SIGQUIT in signals.7

* Wed Oct 06 1999 Cristian Gafton <gafton@redhat.com>
- fix man page for getcwd

* Wed Sep 22 1999 Cristian Gafton <gafton@redhat.com>
- added man pages for set/getcontext

* Tue Sep 14 1999 Bill Nottingham <notting@redhat.com>
- remove some bad man pages

* Mon Sep 13 1999 Preston Brown <pbrown@redhat.com>
- czech, german, spanish, russian man pages

* Thu Sep 09 1999 Cristian Gafton <gafton@redhat.com>
- version 1.26
- add french man pages
- add italian man pages

* Fri Jul 23 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.25.

* Fri Apr 16 1999 Cristian Gafton <gafton@redhat.com>
- fiox man page fro ftw

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- spellnig fixse

* Tue Mar 30 1999 Bill Nottingham <notting@redhat.com>
- updated to 1.23

* Thu Mar 25 1999 Cristian Gafton <gafton@redhat.com>
- added kernel net manpages

* Mon Mar 22 1999 Erik Troan <ewt@redhat.com>
- updated printf man page
- added rpcgen man page

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- leave the lilo man pages alone (oops)

* Fri Feb 12 1999 Michael Maher <mike@redhat.com>
- fixed bug #413

* Mon Jan 18 1999 Cristian Gafton <gafton@redhat.com>
- remove lilo man pages too
- got rebuilt for 6.0

* Tue Sep 08 1998 Cristian Gafton <gafton@redhat.com>
- version 1.21

* Sat Jun 20 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.20

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- get rid of the modutils man pages
- updated to 1.19

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Erik Troan <ewt@redhat.com>
- updated to 1.18

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- updated to 1.17
- moved build root to /var

* Thu Jul 31 1997 Erik Troan <ewt@redhat.com>
- made a noarch package

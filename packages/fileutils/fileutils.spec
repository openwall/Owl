# $Id: Owl/packages/fileutils/Attic/fileutils.spec,v 1.4 2000/11/30 20:16:50 solar Exp $

Summary: 	The GNU versions of common file management utilities.
Name: 		fileutils
Version: 	4.0.27
Release: 	4owl
License: 	GPL
Group: 		Applications/File
Source0: 	ftp://alpha.gnu.org/gnu/fetish/%{name}-%{version}.tar.gz
Source1: 	DIR_COLORS
Source2: 	colorls.sh
Source3: 	colorls.csh
Source4:	shred.1
Patch0: 	fileutils-4.0-rh-spacedir.diff
Patch1: 	fileutils-4.0-rh-samefile.diff
Patch2: 	fileutils-4.0-rh-C-option.diff
Patch3: 	fileutils-4.0p-rh-strip.diff
Patch4: 	fileutils-4.0x-rh-force-chmod.diff
Patch5: 	fileutils-4.0x-rh-overwrite.diff
Patch6: 	fileutils-4.0-rh-ls-dumbterm.diff
Buildroot: 	/var/rpm-buildroot/%{name}-root
Prereq: 	/sbin/install-info

%description
The fileutils package includes a number of GNU versions of common and
popular file management utilities.  Fileutils includes the following
tools: chgrp (changes a file's group ownership), chown (changes a
file's ownership), chmod (changes a file's permissions), cp (copies
files), dd (copies and converts files), df (shows a filesystem's disk
usage), dir (gives a brief directory listing), dircolors (the setup
program for the color version of the ls command), du (shows disk
usage), install (copies files and sets permissions), ln (creates file
links), ls (lists directory contents), mkdir (creates directories),
mkfifo (creates FIFOs or named pipes), mknod (creates special files),
mv (renames files), rm (removes/deletes files), rmdir (removes empty
directories), sync (synchronizes memory and disk), touch (changes file
timestamps), and vdir (provides long directory listings).

You should install the fileutils package, because it includes many
file management utilities that you'll use frequently.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
unset LINGUAS || :
%ifos linux
%define _exec_prefix /
%endif
%configure

make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

cd $RPM_BUILD_ROOT

%ifos linux
mkdir -p .%{_prefix}/bin
for i in dir dircolors du install mkfifo shred vdir
do
  mv -f ./bin/$i .%{_prefix}/bin/$i
done
strip -R .comment ./bin/* || :
%endif

strip .%{_prefix}/bin/* || :
gzip -9nf .%{_infodir}/fileutils*

mkdir -p ./etc/profile.d
install -c -m 644 %SOURCE1 ./etc
install -c -m 755 %SOURCE2 ./etc/profile.d
install -c -m 755 %SOURCE3 ./etc/profile.d

install -c -m 644 %SOURCE4 $RPM_BUILD_ROOT/%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/fileutils.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/fileutils.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%config %{_sysconfdir}/DIR_COLORS
%config %{_sysconfdir}/profile.d/*

%ifos linux
%{_exec_prefix}/bin/*
%endif
%{_prefix}/bin/*
%{_mandir}/man*/*

%{_infodir}/fileutils*
%{_prefix}/share/locale/*/*/*

%changelog
* Thu Nov 30 2000 Solar Designer <solar@owl.openwall.com>
- Avoid listing %{_sysconfdir}/profile.d (the directory itself).

* Wed Nov 29 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- add warning to shred(1) man.

* Thu Oct 19 2000 Solar Designer <solar@owl.openwall.com>
- Fixed a bug in RH patch to mv (don't exit if lstat on a file fails).

* Sun Oct  1 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- v4.0.27

* Sun Sep 24 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH

* Fri Aug 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up the dircolors initialization script (Bug #16918)

* Mon Aug 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix a bad optimization that broke du ("du -sk . *")

* Thu Aug  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to 4.0x, this fixes cp -r DIR1/ DIR2

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Preston Brown <pbrown@redhat.com>
- colorls scripts evaluate ~/.dircolors (#12634)

* Mon Jul  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up colorls.{c,}sh (Bug #13384)
- 4.0w (this fixes a relatively critical cp -R bug)

* Sat Jun 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Replace a reference to %%{_prefix}/share/info with
  %%{_infodir} for backwards compatibility
  (Bug #12817)
- Fix compilation with current glibc

* Sat Jun 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 4.0u (2 bugfixes)

* Thu Jun  1 2000 Matt Wilson <msw@redhat.com>
- fix usage of configure and makeinstall macros
- use _infodir macros
- fixed filelist to be more generic

* Wed May 31 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 4.0s (important bugfixes + interesting new chown option --from=)
- some tweaks to spec file
- fix up filesystem layout for new FSSTND (/usr/share/man ...)
- fix build on sparc
- fix up installation with the new configure macro

* Sat Apr  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 4.0q

* Tue Mar 07 2000 Cristian Gafton <gafton@redhat.com>
- get rid of 'ls -C' crap. It breaks pipes

* Fri Mar  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't use color-ls on dumb terminals

* Thu Feb 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up mv behavior when overwriting a write-protected file without -f
  (Bug #6246)

* Wed Feb 16 2000 Cristian Gafton <gafton@redhat.com>
- take out the default -F argument to ls (the extra chars are breaking
  scripts)

* Wed Feb  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Back out the cp -x fix, as it breaks cp -r.
  I'll look into really fixing it when I have the time; for now, -r
  is more important than -x.

* Mon Feb  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up the cp -x option (Bug #8726)

* Sun Feb  6 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- don't produce a fatal error on -s when strip fails
- handle special bits with install -m (Bug #7080)

* Wed Feb  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 4.0p stuff: quote multibyte characters correctly.

* Tue Feb 01 2000 Cristian Gafton <gafton@redhat.com>
- add patch to disable st_size computation for devices (hjl)

* Fri Jan 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable DOOR type, which makes tcsh unhappy
- gzipped man pages

* Wed Jan  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fixes from 4.0m

* Sun Dec 12 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix output of mkdir --verbose -p (Bug #7770)

* Thu Nov 18 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix a typo in colorls.sh
- Add the -C option to install for compatibility with *BSD
- unset LINGUAS in spec file to fix build on most 6.1 installations

* Wed Nov 17 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Add colorls.sh/colorls.csh to /etc/profile.d
  (Newbies are likely to like them, professionals who don't will know
  how to remove them. Also, they're compatible with DLD)
- Modify /etc/DIR_COLORS:
  - recognize .bz2, .bz, .tz, .png, .sh, .csh, .rpm, .cpio, .tif
  - recognize color_xterm, dtterm, rxvt and cons25 as colorizable

* Fri Sep 24 1999 Cristian Gafton <gafton@redhat.com>
- don't apply the samefile patch anymore (breaks globbing). Patch still
  included in the src.rpm for a later day fix

* Mon Sep 13 1999 Cristian Gafton <gafton@redhat.com>
- fix my patch some more and use lstat instead

* Sat Sep 11 1999 Bill Nottingham <notting@redhat.com>
- fix gafton's patch ;)

* Fri Sep 10 1999 Cristian Gafton <gafton@redhat.com>
- patch to stop "mv b b" from creating a stupid b/b directory.

* Tue Aug 31 1999 Jeff Johnson <jbj@redhat.com>
- install -D should create DEST not SOURCE filename (#3339).

* Mon Aug 23 1999 Preston Brown <pbrown@redhat.com>
- fixed display of symlinked directories in ls (#4561)

* Wed Jul 28 1999 Cristian Gafton <gafton@redhat.com>
- correctly display mount points that have spaces in them (#3317)

* Tue Mar 23 1999 Cristian Gafton <gafton@redhat.com>
- version 4.0

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Thu Aug 06 1998 Erik Troan <ewt@redhat.com>
- got install-info stuff working in %post/%pre

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- manhattan rebuild
- added %clean

* Wed Oct 22 1997 Erik Troan <ewt@redhat.com>
- minor patch for glibc 2.1

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- install-info turned off, as it creates a prereq loop

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- install-info turned on
- added BuildRoot

* Mon Sep 15 1997 Erik Troan <ewt@redhat.com>
- can't use install-info until %post -p allows argument passing

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- uses install-info

* Fri May 16 1997 Erik Troan <ewt@redhat.com>
- rebuilt for glibc.

* Tue Feb 25 1997 Erik Troan <ewt@redhat.com>
- Hacked at mktime() test to work on 64 bit machines w/ broken mktime(). I
  told Ulrich Drepper and Richard Henderson about this, so hopefully glibc
  will get fixed.

* Thu Feb 20 1997 Michael Fulbright <msf@redhat.com>
- Updated to version 3.16.

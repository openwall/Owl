# $Owl: Owl/packages/man-pages/man-pages.spec,v 1.22 2006/03/30 02:36:25 galaxy Exp $

Summary: Manual (man) pages from the Linux Documentation Project.
Name: man-pages
Version: 2.16
Release: owl2
License: distributable
Group: Documentation
Source0: ftp://ftp.win.tue.nl/pub/linux-local/manpages/man-pages-%version.tar.gz
Source1: rpcgen.1
Source2: getent.1
Source3: iconv.1
Source4: locale.1
Source5: localedef.1
Source6: sprof.1
Source7: ld-linux.so.8
Source8: ldconfig.8
Source9: rpcinfo.8
Patch0: man-pages-2.16-deb-owl-misc.diff
Patch1: man-pages-2.16-rh-owl-roff-fixes.diff
Patch2: man-pages-2.16-rh-misc.diff
Patch3: man-pages-2.16-owl-cc-ld.so.diff
Patch4: man-pages-2.16-owl-uselib.diff
AutoReqProv: false
BuildArchitectures: noarch
BuildRoot: /override/%name-%version

%description
A large collection of man pages (documentation) from the Linux
Documentation Project (LDP).  The man pages are organized into the
following sections: Section 1, user commands (intro only); Section 2,
system calls; Section 3, libc calls; Section 4, devices (e.g., hd,
sd); Section 5, file formats and protocols (e.g., wtmp, /etc/passwd,
nfs); Section 6, games (intro only); Section 7, conventions, macro
packages, etc. (e.g., nroff, ascii); and Section 8, system
administration (intro only).

%package posix
Summary: Man (manual) pages from the IEEE and The Open Group.
Group: Documentation
License: for reprint only
Requires: %name = %version-%release

%description posix
A large collection of man pages (reference material) from the
IEEE Std 1003.1, 2003 Edition, Standard for Information Technology --
Portable Operating System Interface (POSIX), The Open Group Base
Specifications Issue 6, Copyright (C) 2001-2003 by the Institute of
Electrical and Electronics Engineers, Inc and The Open Group.003.1,
2003 Edition, Standard for Information Technology -- Portable Operating
System Interface (POSIX), The Open Group Base Specifications Issue 6,
Copyright (C) 2001-2003 by the Institute of Electrical and Electronics
Engineers, Inc and The Open Group.  The man pages are organized into
the following sections:
	0p: POSIX headers
	1p: POSIX utilities
	3p: POSIX functions

%prep
%setup -q

cp %_sourcedir/rpcgen.1 man1/
cp %_sourcedir/getent.1 man1/
cp %_sourcedir/iconv.1 man1/
cp %_sourcedir/locale.1 man1/
cp %_sourcedir/localedef.1 man1/
cp %_sourcedir/sprof.1 man1/

cp %_sourcedir/ld-linux.so.8 man8/
cp %_sourcedir/ldconfig.8 man8/
cp %_sourcedir/rpcinfo.8 man8/

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
rm man1/README

# These are parts of fileutils
rm man1/{chgrp,chmod,chown,cp,dd,df,dircolors,du,install}.1
rm man1/{ln,ls,mkdir,mkfifo,mknod,mv,rm,rmdir,touch}.1
rm man1/{dir,vdir}.1

# Part of quota
rm man2/quotactl.2

# Part of glibc (crypt_blowfish)
rm man3/crypt.3

# Part of bind-utils
rm man5/resolver.5
rm man5/resolv.conf.5

# Part of shadow-utils
rm man3/getspnam.3

# Obsolete
rm man3/infnan.3

# Part of time
rm man1/time.1

# We don't package it
rm man5/nscd.conf.5
rm man8/nscd.8

%install
rm -rf %buildroot

mkdir -p %buildroot%_mandir
for n in 0p 1 1p 2 3 3p 4 5 6 7 8 9; do
	mkdir %buildroot%_mandir/man$n
done
for n in man*/*; do
	cp -a $n %buildroot%_mandir/$n
done

%files
%defattr(0644,root,root,0755)
%doc README HOWTOHELP man-pages-%version.Announce
%_mandir/man?/*

%files posix
%defattr(0644,root,root,0755)
%doc POSIX-COPYRIGHT
%dir %_mandir/man?p
%_mandir/man?p/*

%changelog
* Thu Mar 30 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.16-owl2
- Added the ?p sections to the POSIX man-pages filelist.

* Thu Dec 08 2005 Michail Litvak <mci-at-owl.openwall.com> 2.16-owl1
- 2.16.
- Make separate subpackage for POSIX man-pages due to licensing restrictions.
- Updated patches.

* Thu Apr 17 2003 Solar Designer <solar-at-owl.openwall.com> 1.52-owl3
- console-tools has been replaced with kbd, so let's package console(4)
from here now.

* Tue Jul 30 2002 Michail Litvak <mci-at-owl.openwall.com>
- 1.52
- Obsolete patches removed
- Don't package nscd* man pages

* Wed Feb 06 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Fri Sep 14 2001 Solar Designer <solar-at-owl.openwall.com>
- Corrected .Bl/.El usage in mdoc.samples.7
- Dropped the RH paths patch entirely, it will need to be updated once we
fix our paths anyway.

* Wed Sep 05 2001 Michail Litvak <mci-at-owl.openwall.com>
- updated to 1.39
- patch to add reference pwrite.2 -> pread.2

* Mon Jun 18 2001 Michail Litvak <mci-at-owl.openwall.com>
- updated to 1.38

* Fri May 04 2001 Solar Designer <solar-at-owl.openwall.com>
- crypt.3 is now a part of our glibc package due to crypt_blowfish.

* Wed May 02 2001 Michail Litvak <mci-at-owl.openwall.com>
- use cp instead of cp -a in spec
- uselib.2 patch

* Mon Apr 30 2001 Michail Litvak <mci-at-owl.openwall.com>
- Disabled patch 3 (we don't yet have these paths)
- added man for ld-linux.so
- remove time.1 (it is in time package)
- man-pages-extralocale.tar.bz2, man2.tar.gz replaced
  by just non packed files (is better for storing in CVS)
- patch to replace cc(1) -> gcc(1), ld.so -> ld-linux.so

* Fri Apr 27 2001 Michail Litvak <mci-at-owl.openwall.com>
- Imported from RH 7.1
- added patch from Debian
- removed man page for ld.so as obsolete

# $Id: Owl/packages/man-pages/man-pages.spec,v 1.16 2003/10/30 21:15:46 solar Exp $

Summary: Manual (man) pages from the Linux Documentation Project.
Name: man-pages
Version: 1.52
Release: owl3
License: distributable
Group: Documentation
Source0: ftp://ftp.win.tue.nl/pub/linux-local/manpages/man-pages-%version.tar.gz
Source1: rpcgen.1
Source2: getent.1
Source3: iconv.1
Source4: locale.1
Source5: localedef.1
Source6: sprof.1
Source7: setcontext.2
Source8: ld-linux.so.8
Source9: ldconfig.8
Source10: rpcinfo.8
Patch0: man-pages-1.52-deb-owl-misc.diff
Patch1: man-pages-1.52-rh-owl-roff-fixes.diff
Patch2: man-pages-1.52-owl-cc-ld.so.diff
Patch3: man-pages-1.52-owl-uselib.diff
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

%prep
%setup -q

cp $RPM_SOURCE_DIR/rpcgen.1 man1/
cp $RPM_SOURCE_DIR/getent.1 man1/
cp $RPM_SOURCE_DIR/iconv.1 man1/
cp $RPM_SOURCE_DIR/locale.1 man1/
cp $RPM_SOURCE_DIR/localedef.1 man1/
cp $RPM_SOURCE_DIR/sprof.1 man1/

cp $RPM_SOURCE_DIR/setcontext.2 man2/

cp $RPM_SOURCE_DIR/ld-linux.so.8 man8/
cp $RPM_SOURCE_DIR/ldconfig.8 man8/
cp $RPM_SOURCE_DIR/rpcinfo.8 man8/

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
rm -fv man1/README

# These are parts of fileutils
rm -fv man1/{chgrp,chmod,chown,cp,dd,df,dircolors,du,install}.1
rm -fv man1/{ln,ls,mkdir,mkfifo,mknod,mv,rm,rmdir,touch}.1
rm -fv man1/{dir,vdir}.1

# Part of quota
rm -fv man2/quotactl.2

# Part of glibc (crypt_blowfish)
rm -fv man3/crypt.3

# Part of bind-utils
rm -fv man5/resolver.5
rm -fv man5/resolv.conf.5

# Obsolete
rm -f man3/infnan.3

# Part of time
rm -fv man1/time.1

# We don't package it
rm -fv man5/nscd.conf.5
rm -fv man8/nscd.8

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%_mandir
for n in 1 2 3 4 5 6 7 8; do
	mkdir $RPM_BUILD_ROOT%_mandir/man$n
done
for n in man?/*; do
	cp -a $n $RPM_BUILD_ROOT%_mandir/$n
done

%files
%defattr(0644,root,root,0755)
%doc README man-pages-%version.Announce
%_mandir/man*/*

%changelog
* Thu Apr 17 2003 Solar Designer <solar@owl.openwall.com> 1.52-owl3
- console-tools has been replaced with kbd, so let's package console(4)
from here now.

* Tue Jul 30 2002 Michail Litvak <mci@owl.openwall.com>
- 1.52
- Obsolete patches removed
- Don't package nscd* man pages

* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Fri Sep 14 2001 Solar Designer <solar@owl.openwall.com>
- Corrected .Bl/.El usage in mdoc.samples.7
- Dropped the RH paths patch entirely, it will need to be updated once we
fix our paths anyway.

* Wed Sep 05 2001 Michail Litvak <mci@owl.openwall.com>
- updated to 1.39
- patch to add reference pwrite.2 -> pread.2

* Mon Jun 18 2001 Michail Litvak <mci@owl.openwall.com>
- updated to 1.38

* Fri May 04 2001 Solar Designer <solar@owl.openwall.com>
- crypt.3 is now a part of our glibc package due to crypt_blowfish.

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

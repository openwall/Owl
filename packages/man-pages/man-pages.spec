# $Owl: Owl/packages/man-pages/man-pages.spec,v 1.23 2009/06/28 17:54:59 mci Exp $

%define posix_version 2003
%define posix_release a

Summary: Manual (man) pages from the Linux Documentation Project.
Name: man-pages
Version: 3.21
Release: owl1
License: distributable
Group: Documentation
Source0: http://www.kernel.org/pub/linux/docs/manpages/man-pages-%version.tar.bz2
# Signature: http://www.kernel.org/pub/linux/docs/manpages/man-pages-%version.tar.bz2.sign
Source1: http://www.kernel.org/pub/linux/docs/man-pages/man-pages-posix/man-pages-posix-%posix_version-%posix_release.tar.bz2
# Signature: http://www.kernel.org/pub/linux/docs/man-pages/man-pages-posix/man-pages-posix-%posix_version-%posix_release.tar.bz2.sign
Source2: rpcgen.1
Source3: getent.1
Source4: iconv.1
Source5: locale.1
Source6: localedef.1
Source7: sprof.1
Source8: rpcinfo.8
Patch0: man-pages-3.21-deb-owl-misc.diff
Patch1: man-pages-3.21-rh-owl-roff-fixes.diff
Patch2: man-pages-3.21-owl-cc.diff
Patch3: man-pages-3.21-owl-uselib.diff
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
%setup -q -a 1

mv  man-pages-posix-%{posix_version}-%{posix_release}/* ./
rmdir man-pages-posix-%{posix_version}-%{posix_release}

cp %_sourcedir/rpcgen.1 man1/
cp %_sourcedir/getent.1 man1/
cp %_sourcedir/iconv.1 man1/
cp %_sourcedir/locale.1 man1/
cp %_sourcedir/localedef.1 man1/
cp %_sourcedir/sprof.1 man1/

cp %_sourcedir/rpcinfo.8 man8/

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

# Part of modutils
rm man2/create_module.2
rm man2/delete_module.2
rm man2/get_kernel_syms.2
rm man2/init_module.2
rm man2/query_module.2

# Part of quota
rm man2/quotactl.2

# Part of glibc (crypt_blowfish)
rm man3/crypt.3
rm man3/crypt_r.3

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
%doc README man-pages-%version.Announce
%_mandir/man?/*

%files posix
%defattr(0644,root,root,0755)
%doc POSIX-COPYRIGHT
%dir %_mandir/man?p
%_mandir/man?p/*

%changelog
* Thu Jun 23 2009 Michail Litvak <mci-at-owl.openwall.com> 3.21-owl1
- 3.21
- Updated patches.

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

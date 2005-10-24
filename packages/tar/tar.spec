# $Id: Owl/packages/tar/tar.spec,v 1.20 2005/10/24 01:56:48 solar Exp $

Summary: A GNU file archiving program.
Name: tar
Version: 1.13.19
Release: owl5
License: GPL
Group: Applications/Archiving
Source0: ftp://alpha.gnu.org/pub/gnu/tar/tar-%version.tar.gz
Source1: tar.1
Patch0: tar-1.13.19-owl-verify-looping-fix.diff
Patch1: tar-1.13.19-mdk-Iy.diff
Patch2: tar-1.13.19-rh-fail.diff
Patch3: tar-1.13.19-rh-owl-unreadable-segfault.diff
Patch4: tar-1.13.19-rh-autoconf.diff
Patch5: tar-1.13.19-rh-owl-no-librt.diff
Patch6: tar-1.13.19-owl-info.diff
Patch7: tar-1.13.19-owl-dot-dot.diff
Patch8: tar-1.13.19-owl-symlinks.diff
Patch9: tar-1.13.19-up-relativize-links.diff
Patch10: tar-1.13.19-owl-autotools.diff
Patch11: tar-1.13.19-owl-po.diff
PreReq: /sbin/install-info, grep
BuildRequires: automake, autoconf, texinfo, gettext
BuildRequires: rpm-build >= 0:4
BuildRoot: /override/%name-%version

%description
The GNU tar program saves many files together into one archive and can
restore individual files (or all of the files) from the archive.  tar
can also be used to add supplemental files to an archive and to update
or list files in the archive.  tar includes multivolume support,
automatic archive compression/decompression, the ability to perform
remote archives and the ability to perform incremental and full
backups.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

%{expand:%%define optflags %optflags -Wall -Dlint}

%build
rm doc/tar.info
unset LINGUAS || :
aclocal
automake -a
autoconf
%define _bindir /bin
%define _libexecdir /sbin
%configure
%__make LIBS=-lbsd all check

%install
rm -rf %buildroot

%makeinstall
ln -sf tar %buildroot/bin/gtar

mkdir -p %buildroot%_mandir/man1
install -m 644 %_sourcedir/tar.1 %buildroot%_mandir/man1/

%post
# Get rid of an old, incorrect info entry when replacing older versions
# of the package.
INFODIRFILE=%_infodir/dir
if grep -q '^Tar: ' $INFODIRFILE; then
	if test -L $INFODIRFILE; then
		INFODIRFILE="`find %_infodir -name dir -printf '%%l'`"
	fi
	cp -p $INFODIRFILE $INFODIRFILE.rpmtmp &&
	grep -v '^Tar: ' $INFODIRFILE > $INFODIRFILE.rpmtmp &&
	mv $INFODIRFILE.rpmtmp $INFODIRFILE
fi

/sbin/install-info %_infodir/tar.info.gz %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/tar.info.gz %_infodir/dir
fi

%files
%defattr(-,root,root)
/bin/tar
/bin/gtar
%_mandir/man1/tar.1*
%_infodir/tar.info*
%_prefix/share/locale/*/LC_MESSAGES/*
%exclude /sbin/rmt
%exclude %_infodir/dir

%changelog
* Tue Mar 02 2004 Michail Litvak <mci@owl.openwall.com> 1.13.19-owl5
- Fixed building with new gettext.

* Fri Feb 27 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 1.13.19-owl4.1
- Fixed building with new autotools.

* Sat Sep 28 2002 Solar Designer <solar@owl.openwall.com> 1.13.19-owl4
- Fixed the contains_dot_dot() bug introduced in 1.13.19 and discovered by
3APA3A; thanks to Mark J Cox of Red Hat and Bencsath Boldizsar for further
analysis:
http://marc.theaimsgroup.com/?l=bugtraq&m=99496364810666
http://mail.gnu.org/pipermail/bug-gnu-utils/2002-May/000827.html
http://marc.theaimsgroup.com/?l=bugtraq&m=103314336129887
http://cve.mitre.org/cgi-bin/cvename.cgi?name=CAN-2001-1267
1.13.17 and 1.13.18 had this right.  CVE CAN-2002-0399 applies to the
implementation bug in 1.13.19 to 1.13.25, but isn't yet public.
- Fixed another 1.13.19's bug which effectively disabled the symlink safety
introduced in 1.13.18; this avoids the problem described by Willy TARREAU
where tar could be made to follow a symlink it just extracted and place a
file outside of the intended directory tree:
http://marc.theaimsgroup.com/?l=bugtraq&m=90674255917321
- Finally, back-ported the fix for the hard link storage bug with 1.13.19
discovered by Jose Pedro Oliveira (at least not security this time):
https://listman.redhat.com/pipermail/roswell-list/2001-August/001286.html

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Mon Aug 05 2002 Michail Litvak <mci@owl.openwall.com>
- Fixed incorrect dir entry in info file.

* Mon Feb 04 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Jul 10 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 1.13.19.
- Fixed the looping on verify bug.
- Store the man page separately, not as a patch.
- Dropped obsolete patches (all of them, actually; checked the testcase
for RH bug #9201 to make sure it doesn't occur with the new version, so
the patch can really be dropped).
- Imported relevant patches from Rawhide and Mandrake (via ALT).

* Thu Sep 07 2000 Solar Designer <solar@owl.openwall.com>
- Fixed the passing of %optflags into configure.

* Sun Aug 06 2000 Alexandr D. Kanevsiy <kad@owl.openwall.com>
- import from RH
- fix URL

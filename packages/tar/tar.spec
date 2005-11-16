# $Owl: Owl/packages/tar/tar.spec,v 1.26 2005/11/16 13:32:45 solar Exp $

Summary: A GNU file archiving program.
Name: tar
Version: 1.15.1
Release: owl3
License: GPL
Group: Applications/Archiving
URL: http://www.gnu.org/software/tar/
Source0: ftp://ftp.gnu.org/gnu/tar/tar-%version.tar.bz2
Source1: tar.1
Source2: append.at
Patch0: tar-1.15.1-cvs-20050105-parse_opt.diff
Patch1: tar-1.15.1-cvs-20050113-name_size.diff
Patch2: tar-1.15.1-cvs-20050303-seekable.diff
Patch3: tar-1.15.1-cvs-20050303-newer-verbose.diff
Patch4: tar-1.15.1-cvs-20050512-pad.diff
Patch5: tar-1.15.1-cvs-20050613-is_avoided_name.diff
Patch6: tar-1.15.1-cvs-20050801-sparse-totals.diff
Patch7: tar-1.15.1-cvs-20051105-tests.diff
Patch8: tar-1.15.1-up-savedir.diff
Patch10: tar-1.15.1-alt-parse_opt-Iy.diff
Patch11: tar-1.15.1-owl-info.diff
Patch12: tar-1.15.1-owl-without-librt.diff
Patch13: tar-1.15.1-alt-contains_dot_dot.diff
Patch14: tar-1.15.1-rh-owl-unreadable-segfault.diff
Patch15: tar-1.15.1-mdk-optimize-ignored.diff
Patch16: tar-1.15.1-deb-doc.diff
Patch17: tar-1.15.1-deb-lone-zero-block-warning.diff
Patch18: tar-1.15.1-alt-warnings.diff
PreReq: /sbin/install-info, grep
BuildRequires: automake, autoconf, cvs, gettext, texinfo
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
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
install -pm644 %_sourcedir/append.at tests/

%{expand:%%define optflags %optflags -Wall -Dlint}

%build
rm doc/tar.info
autoreconf -fisv
export tar_cv_path_RSH=%_bindir/ssh
%configure --bindir=/bin --with-rmt=/sbin/rmt
%__make
%__make -k check
bzip2 -9fk ChangeLog

%install
rm -rf %buildroot

%makeinstall bindir=%buildroot/bin
ln -sf tar %buildroot/bin/gtar

mkdir -p %buildroot%_mandir/man1
install -m 644 %_sourcedir/tar.1 %buildroot%_mandir/man1/

# Remove unpackaged files if any
rm -f %buildroot%_infodir/dir

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

/sbin/install-info %_infodir/tar.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/tar.info %_infodir/dir
fi

%files
%defattr(-,root,root)
/bin/tar
/bin/gtar
%_mandir/man1/tar.1*
%_infodir/tar.info*
%_prefix/share/locale/*/LC_MESSAGES/*
%doc AUTHORS NEWS THANKS

%changelog
* Wed Nov 16 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.15.1-owl3
- Backported savedir() fix from gnulib CVS.

* Mon Nov 14 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.15.1-owl2
- Backported fix to options parser from tar CVS.

* Sat Nov 12 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.15.1-owl1
- Updated to 1.15.1.
- Backported a few fixes from tar CVS.
- Reviewed Owl patches, removed obsolete ones.
- Added missing tests/append.at and enabled testsuite by default.
- Imported fixes from Debian's and ALT's tar packages.

* Tue Mar 02 2004 Michail Litvak <mci-at-owl.openwall.com> 1.13.19-owl5
- Fixed building with new gettext.

* Fri Feb 27 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.13.19-owl4.1
- Fixed building with new autotools.

* Sat Sep 28 2002 Solar Designer <solar-at-owl.openwall.com> 1.13.19-owl4
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

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Mon Aug 05 2002 Michail Litvak <mci-at-owl.openwall.com>
- Fixed incorrect dir entry in info file.

* Mon Feb 04 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Jul 10 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 1.13.19.
- Fixed the looping on verify bug.
- Store the man page separately, not as a patch.
- Dropped obsolete patches (all of them, actually; checked the testcase
for RH bug #9201 to make sure it doesn't occur with the new version, so
the patch can really be dropped).
- Imported relevant patches from Rawhide and Mandrake (via ALT).

* Thu Sep 07 2000 Solar Designer <solar-at-owl.openwall.com>
- Fixed the passing of %optflags into configure.

* Sun Aug 06 2000 Alexandr D. Kanevsiy <kad-at-owl.openwall.com>
- import from RH
- fix URL

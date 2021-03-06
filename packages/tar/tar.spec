# $Owl: Owl/packages/tar/tar.spec,v 1.55 2014/07/12 14:19:21 galaxy Exp $

Summary: A GNU file archiving program.
Name: tar
Version: 1.23
Release: owl5
License: GPLv3+
Group: Applications/Archiving
URL: http://www.gnu.org/software/tar/
# http://savannah.gnu.org/projects/tar
Source0: ftp://ftp.gnu.org/gnu/tar/tar-%version.tar.bz2
# Signature: ftp://ftp.gnu.org/gnu/tar/tar-%version.tar.bz2.sig
Source1: tar.1
Patch0: tar-1.23-alt.diff
Patch1: tar-1.23-owl-default-warnings.diff
Patch2: tar-1.23-owl-info.diff
Patch3: tar-1.23-owl-rsh-command.diff
Patch4: tar-1.23-up-20100320.diff
Patch5: tar-1.23-owl-tests.diff
Requires(post,preun): /sbin/install-info, grep
BuildRequires: gettext, texinfo
BuildRequires: rpm-build >= 0:4, sed >= 4.0.9
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

%{expand:%%define optflags %optflags -Wall}

%build
rm doc/tar.info*
export tar_cv_path_RSH=no
%configure --bindir=/bin --with-rmt=/sbin/rmt --disable-silent-rules
sed -i '/HAVE_CLOCK_GETTIME/d' config.h
%__make LIB_CLOCK_GETTIME=
bzip2 -9fk NEWS

%check
%__make check LIB_CLOCK_GETTIME=

%install
rm -rf %buildroot

%makeinstall bindir=%buildroot/bin LIB_CLOCK_GETTIME=
ln -sf tar %buildroot/bin/gtar

mkdir -p %buildroot%_mandir/man1
install -m 644 %_sourcedir/tar.1 %buildroot%_mandir/man1/

# Remove unpackaged files
rm %buildroot%_infodir/dir

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
%doc AUTHORS COPYING NEWS.bz2 README THANKS

%changelog
* Mon Jun 30 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.23-owl5
- Replaced the deprecated PreReq tag with Requires(post,preun).

* Sat Dec 04 2010 Solar Designer <solar-at-owl.openwall.com> 1.23-owl4
- Adjusted tests/truncate.at for its inherent yet undesirable race condition to
be less likely triggered, and to use less disk space (2 MB instead of 500 MB).

* Sun Mar 21 2010 Solar Designer <solar-at-owl.openwall.com> 1.23-owl3
- Fixed a couple of bugs in tests/extrac07.at.
- Updated the documentation on --rsh-command to reflect the lack of default.

* Sat Mar 20 2010 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.23-owl2
- Updated to release_1_23-7-g340dbf5 snapshot to fix regressions
introduced in 1.23 release.
- Changed --rsh-command to have no default as proposed by Solar Designer.
If this option is not given, then the "remote functionality" is now
disabled.  If a filename looks like it is "remote" and neither the
--rsh-command nor the --force-local option is given, then tar will fail
with an error.

* Thu Mar 11 2010 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.23-owl1
- Updated to 1.23.

* Tue Dec 08 2009 Solar Designer <solar-at-owl.openwall.com> 1.22.90-owl3
- Corrected highly non-optimal memory allocation by
canonicalize_filename_mode(), which got exposed with an unrelated change
made shortly before the 1.22.90 alpha release.

* Tue Aug 25 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.22.90-owl2
- Fixed tests/xform-h.at.

* Mon Aug 17 2009 Solar Designer <solar-at-owl.openwall.com> 1.22.90-owl1
- Updated to 1.22.90.
- Extracted Dmitry V. Levin's latest changes from ALT Linux's repository at
http://git.altlinux.org/gears/t/tar.git and forward-ported them from upstream
code slightly newer than 1.22 to the 1.22.90 alpha release.
- Since most of our error handling fixes have been replaced by more elaborate
changes by Sergey Poznyakoff in the upstream code, the new error handling
patch has been reduced to forward-ports of two fixes that seem to have been
missed upstream, as well as a new fix that became relevant with 1.22.90.
- Dropped the --ignore-device-id option (in favor of its official name of
--no-check-device).

* Tue Dec 23 2008 Solar Designer <solar-at-owl.openwall.com> 1.20-owl4
- A further change to the error handling patch: when creating incremental
archives, validate the filenames passed as input to tar in
collect_and_sort_names(), but have the first call to dump_file() assume that
we're not at the top level, as explained in a newly added lengthy comment.

* Sun Nov 23 2008 Solar Designer <solar-at-owl.openwall.com> 1.20-owl3
- Further improvements to the error handling patch:
When creating incremental archives, don't wrongly tell the dump_file()
function that we are at the top level.
When a file shrinks while being archived, only set the exit status to
TAREXIT_DIFFERS if no other non-zero exit status was previously specified.

* Fri Nov 14 2008 Solar Designer <solar-at-owl.openwall.com> 1.20-owl2
- When creating archives, consistently don't treat disappearing directory
entries as a fatal error.

* Sat Nov 01 2008 Andrey V. Stolyarov <croco-at-owl.openwall.com> 1.20-owl1
- Took the fresh GNU tar 1.20, applied patches made by ALT Linux team,
added the --ignore-device-id option as an alias to --no-check-device.
- Fixed two warnings
- Updated the manual page

* Mon Jan 14 2008 Grigoriy Strokin <grg-at-owl.openwall.com> 1.18-owl2
- Added a new option: --ignore-device-id.

* Fri Aug 17 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.18-owl1
- Updated to 1.18.
- Fixed crash bug in list and extract modes.
- Use fchown/fchmod instead of chown/chmod to set permissions of just
created regular files.

* Tue Nov 28 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.15.1-owl7
- Disabled GNUTYPE_NAMES handling by default and added
--allow-name-mangling option to re-enable it.
(CVE-2006-6097, patch from Kees Cook).

* Mon Jun 26 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.15.1-owl6
- Fixed build with gcc-4.x.

* Mon Feb 20 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.15.1-owl5
- Backported upstream fix for potential heap buffer overrun in handling
extended headers (CVE-2006-0300).

* Fri Dec 23 2005 Solar Designer <solar-at-owl.openwall.com> 1.15.1-owl4
- Disabled tests/listed02.at because of a known race condition bug (reported
upstream by ldv@).

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

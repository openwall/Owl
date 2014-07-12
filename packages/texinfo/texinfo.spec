# $Owl: Owl/packages/texinfo/texinfo.spec,v 1.32 2014/07/12 14:19:30 galaxy Exp $

Summary: Tools needed to create Texinfo format documentation files.
Name: texinfo
Version: 4.8
Release: owl6
License: GPL
Group: Applications/Publishing
Source0: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%version.tar.bz2
Source1: info-dir
Patch0: texinfo-4.8-owl-texindex-tmp.diff
Patch1: texinfo-4.8-owl-alt-texi2dvi-tmp.diff
Patch2: texinfo-4.8-mdk-alt-bz2-support.diff
Patch3: texinfo-4.2-rh-owl-data_size-fix.diff
Patch4: texinfo-4.8-deb-fixes.diff
Patch5: texinfo-4.8-owl-info.diff
Patch6: texinfo-4.8-rh-bound.diff
Requires(post,preun): /sbin/install-info, gzip
Prefix: %_prefix
Requires: mktemp >= 1:1.3.1
BuildRoot: /override/%name-%version

%description
Texinfo is a documentation system that can produce both online
information and printed output from a single source file.  The GNU
Project uses the Texinfo file format for most of its documentation.

%package -n info
Summary: A stand-alone TTY-based reader for GNU Texinfo documentation.
Group: System Environment/Base
Requires(post,preun): gzip

%description -n info
The GNU Project uses the Texinfo file format for much of its
documentation.  The info package provides a standalone TTY-based
browser program for viewing Info files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%{expand: %%define optflags %optflags -Wall}
%define __spec_install_post %_prefix/lib/rpm/brp-strip \; %_prefix/lib/rpm/brp-strip-comment-note

%build
unset LINGUAS || :
export LC_ALL=C
%configure --mandir=%_mandir --infodir=%_infodir
%__make
bzip2 -9f ChangeLog*

%check
%__make check

%install
rm -rf %buildroot
mkdir -p %buildroot/{etc,sbin}

export LC_ALL=C
%makeinstall

cd %buildroot
mv .%_infodir/dir ./etc/info-dir
ln -s ../../../etc/info-dir .%_infodir/dir
mv .%_bindir/install-info sbin/
gzip -9 .%_infodir/*info*

%post
/sbin/install-info %_infodir/texinfo %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/texinfo %_infodir/dir
fi

%post -n info
/sbin/install-info %_infodir/info-stnd.info %_infodir/dir

%preun -n info
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete \
		%_infodir/info-stnd.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog* INTRODUCTION NEWS README TODO
%doc info/README
%_bindir/makeinfo
%_bindir/texindex
%_bindir/texi2dvi
%_bindir/texi2pdf
%_infodir/texinfo*
%_datadir/locale/*/*/*
%_mandir/man1/makeinfo.1*
%_mandir/man1/texi2dvi.1*
%_mandir/man1/texindex.1*
%_mandir/man5/texinfo.5*
%_datadir/texinfo

%files -n info
%defattr(-,root,root)
%config(noreplace) %verify(not size md5 mtime) /etc/info-dir
%config(noreplace) %_infodir/dir
%_bindir/info
%_infodir/info.info*
%_infodir/info-stnd.info*
/sbin/install-info
%_bindir/infokey
%_mandir/man1/info.1*
%_mandir/man1/infokey.1*
%_mandir/man1/install-info.1*
%_mandir/man5/info.5*

%changelog
* Mon Jun 30 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.8-owl6
- Replaced the deprecated PreReq tag with Requires(post,preun).

* Wed May 27 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.8-owl5
- Compressed all texinfo files.

* Sat Oct 28 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.8-owl4
- Fixed potential heap buffer overflow in texindex (CVE-2006-4810),
patch from Miloslav Trmac.

* Sun Mar 12 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.8-owl3
- Made %_infodir/dir symlink relative.

* Mon Apr 25 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.8-owl2
- Fixed info files installation as suggested by Dmitry V. Levin.
- Reverted back the removal of the __spec_install_post macro since its
absence breaks the package build. We have to fix our rpm package first.

* Wed Mar 30 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.8-owl1
- Updated to 4.8.
- Set LC_ALL=C to use English in the produced files.
- Reviewed unpackaged files and included them.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl4
- Removed verify checks for info-dir since it's heavily modified during
the system lifetime.
- Cleaned up the spec.

* Fri Nov 22 2002 Solar Designer <solar-at-owl.openwall.com> 4.2-owl3
- Corrected the path to bzcat, thanks to (GalaxyMaster).

* Tue Aug 27 2002 Solar Designer <solar-at-owl.openwall.com>
- PreReq: gzip in info subpackage as required for the new texinfo
(install-info now invokes external *zcat instead of using zlib).

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Sat Jul 13 2002 Solar Designer <solar-at-owl.openwall.com>
- Require mktemp >= 1:1.3.1 as needed by the updated patches.
- Package the ChangeLog gzipped as it grew too large.

* Thu Jun 20 2002 Michail Litvak <mci-at-owl.openwall.com>
- 4.2
- reviewed patches, added patches from ALT

* Mon Feb 04 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Jan 03 2001 Solar Designer <solar-at-owl.openwall.com>
- Patch to create temporary files safely.
- Give offline sorting in texindex a chance to work (fixed a bug in there;
did anyone ever test that code, it certainly looks like not).

* Wed Aug 09 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH
- FHS build

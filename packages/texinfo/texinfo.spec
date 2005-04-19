# $Id: Owl/packages/texinfo/texinfo.spec,v 1.20 2005/04/19 03:12:52 galaxy Exp $

%define BUILD_TEST 1

Summary: Tools needed to create Texinfo format documentation files.
Name: texinfo
Version: 4.8
Release: owl1
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
PreReq: /sbin/install-info
Prefix: %_prefix
Requires: mktemp >= 1:1.3.1
BuildRoot: /override/%name-%version

#%%define __spec_install_post %_libdir/rpm/brp-strip \; %_libdir/rpm/brp-strip-comment-note

%description
Texinfo is a documentation system that can produce both online
information and printed output from a single source file.  The GNU
Project uses the Texinfo file format for most of its documentation.

%package -n info
Summary: A stand-alone TTY-based reader for GNU Texinfo documentation.
Group: System Environment/Base
PreReq: gzip

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

%{expand: %%define optflags %optflags -Wall}

%build
unset LINGUAS || :
export LC_ALL=C
%configure --mandir=%_mandir --infodir=%_infodir
%__make
%if %BUILD_TEST
%__make check
%endif
bzip2 -9f ChangeLog*

%install
rm -rf %buildroot
mkdir -p %buildroot/{etc,sbin}

export LC_ALL=C
%makeinstall

cd %buildroot
mv .%_infodir/dir .%_sysconfdir/info-dir
ln -s %_sysconfdir/info-dir %buildroot%_infodir/dir
mv .%_bindir/install-info sbin/

%post
/sbin/install-info %_infodir/texinfo.* %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/texinfo.* %_infodir/dir
fi

%post -n info
/sbin/install-info %_infodir/info-stnd.info.* %_infodir/dir

%preun -n info
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete \
		%_infodir/info-stnd.info.* %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog* INTRODUCTION NEWS README TODO
%doc info/README
%_prefix/bin/makeinfo
%_prefix/bin/texindex
%_prefix/bin/texi2dvi
%_prefix/bin/texi2pdf
%_infodir/texinfo*
%_prefix/share/locale/*/*/*
%_mandir/man1/makeinfo.1*
%_mandir/man1/texi2dvi.1*
%_mandir/man1/texindex.1*
%_mandir/man5/texinfo.5*
%_datadir/texinfo

%files -n info
%defattr(-,root,root)
%config(noreplace) %verify(not size md5 mtime) %_sysconfdir/info-dir
%config(noreplace) %_infodir/dir
%_prefix/bin/info
%_infodir/info.info*
%_infodir/info-stnd.info*
/sbin/install-info
%_bindir/infokey
%_mandir/man1/info.1*
%_mandir/man1/infokey.1*
%_mandir/man1/install-info.1*
%_mandir/man5/info.5*


%changelog
* Wed Mar 30 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 4.8-owl1
- Updated to 4.8.
- Set LC_ALL=C to use English in the produced files.
- Reviewed unpackaged files and included them.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 4.2-owl4
- Removed verify checks for info-dir since it's heavily modified during
the system lifetime.
- Cleaned up the spec.

* Fri Nov 22 2002 Solar Designer <solar@owl.openwall.com> 4.2-owl3
- Corrected the path to bzcat, thanks to (GalaxyMaster).

* Tue Aug 27 2002 Solar Designer <solar@owl.openwall.com>
- PreReq: gzip in info subpackage as required for the new texinfo
(install-info now invokes external *zcat instead of using zlib).

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Sat Jul 13 2002 Solar Designer <solar@owl.openwall.com>
- Require mktemp >= 1:1.3.1 as needed by the updated patches.
- Package the ChangeLog gzipped as it grew too large.

* Thu Jun 20 2002 Michail Litvak <mci@owl.openwall.com>
- 4.2
- reviewed patches, added patches from ALT

* Mon Feb 04 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Jan 03 2001 Solar Designer <solar@owl.openwall.com>
- Patch to create temporary files safely.
- Give offline sorting in texindex a chance to work (fixed a bug in there;
did anyone ever test that code, it certainly looks like not).

* Wed Aug 09 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- FHS build

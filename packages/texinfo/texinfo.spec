# $Id: Owl/packages/texinfo/texinfo.spec,v 1.13 2002/11/22 20:25:48 solar Exp $

Summary: Tools needed to create Texinfo format documentation files.
Name: texinfo
Version: 4.2
Release: owl3
License: GPL
Group: Applications/Publishing
Source0: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.gz
Source1: info-dir
Patch0: texinfo-4.2-owl-texindex-tmp.diff
Patch1: texinfo-4.2-owl-alt-texi2dvi-tmp.diff
Patch2: texinfo-4.2-rh-texi2dvi-fileext.diff
Patch3: texinfo-4.2-mdk-alt-bz2-support.diff
Patch4: texinfo-4.2-rh-owl-data_size-fix.diff
Patch5: texinfo-4.2-deb-fixes.diff
Patch6: texinfo-4.2-owl-info.diff
PreReq: /sbin/install-info
Prefix: %{_prefix}
Requires: mktemp >= 1:1.3.1
BuildRoot: /override/%{name}-%{version}

%define __spec_install_post /usr/lib/rpm/brp-strip \; /usr/lib/rpm/brp-strip-comment-note

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
%patch6 -p1

%build
unset LINGUAS || :
%configure --mandir=%{_mandir} --infodir=%{_infodir}
make
gzip -9nf ChangeLog

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{etc,sbin}

%makeinstall

cd $RPM_BUILD_ROOT
install -m 644 $RPM_SOURCE_DIR/info-dir etc/info-dir
ln -sf /etc/info-dir ${RPM_BUILD_ROOT}%{_infodir}/dir
mv .%{_prefix}/bin/install-info sbin/
gzip -9nf .%{_infodir}/*info*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/texinfo.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/texinfo.gz %{_infodir}/dir
fi

%post -n info
/sbin/install-info %{_infodir}/info-stnd.info.gz %{_infodir}/dir

%preun -n info
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete \
		%{_infodir}/info-stnd.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog* INTRODUCTION NEWS README TODO
%doc info/README
%{_prefix}/bin/makeinfo
%{_prefix}/bin/texindex
%{_prefix}/bin/texi2dvi
%{_infodir}/texinfo*
%{_prefix}/share/locale/*/*/*

%files -n info
%defattr(-,root,root)
%config(noreplace) /etc/info-dir
%config(noreplace) %{_infodir}/dir
%{_prefix}/bin/info
%{_infodir}/info.info*
%{_infodir}/info-stnd.info*
/sbin/install-info

%changelog
* Fri Nov 22 2002 Solar Designer <solar@owl.openwall.com>
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

# $Owl: Owl/packages/libtool/libtool.spec,v 1.29 2014/07/12 13:57:03 galaxy Exp $

Summary: The GNU Libtool, which simplifies the use of shared libraries.
Name: libtool
Version: 2.4.2
Release: owl1
License: GPL/LGPL
Group: Development/Tools
URL: http://www.gnu.org/software/libtool/
Source: ftp://ftp.gnu.org/gnu/%name/%name-%version.tar.xz
Patch0: %name-2.4.2-alt-tmp.diff
Patch1: %name-2.4.2-owl-info.diff
Patch2: %name-2.4.2-owl-buildhost.diff
#Patch3: %name-1.5.18-alt-deb-link_all_deplibs.diff
#Patch4: %name-1.5.18-alt-ltmain-legacy.diff
Patch6: %name-2.4.2-rh-multilib-hack.diff
Requires(post,pre): /sbin/install-info
Requires: autoconf, automake, m4, perl
Requires: libtool-libs = %version-%release, mktemp
Prefix: %_prefix
BuildRequires: automake >= 1.14, autoconf >= 2.69, texinfo
BuildRoot: /override/%name-%version

%description
The libtool package contains the GNU Libtool, a set of shell scripts
that allow package developers to provide generic shared library support.

%package libs
Summary: Runtime libraries for GNU Libtool.
Group: System Environment/Libraries

%description libs
The libtool-libs package contains the runtime libraries from GNU Libtool.
GNU Libtool uses these libraries to provide portable dynamic loading of
shared libraries.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
#patch3 -p1
#patch4 -p1
%patch6 -p1

%build
rm doc/libtool.info
%define __libtoolize echo --
%configure

%__make
bzip2 -9fk ChangeLog

%check
%__make check

%install
rm -rf %buildroot
mkdir -p %buildroot%_prefix

%makeinstall

# Remove unpackaged files
rm %buildroot%_infodir/dir
rm %buildroot%_libdir/*.la

%post
/sbin/install-info %_infodir/libtool.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/libtool.info %_infodir/dir
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING NEWS README THANKS TODO ChangeLog.bz2
%attr(0755,root,root) %_bindir/*
%_infodir/libtool.info*
%_includedir/ltdl.h
%dir %_includedir/libltdl
%_includedir/libltdl/lt_dlloader.h
%_includedir/libltdl/lt_error.h
%_includedir/libltdl/lt_system.h
%_datadir/libtool
%_libdir/libltdl.so
%_libdir/libltdl.a
%_datadir/aclocal/libtool.m4
%_datadir/aclocal/ltdl.m4
%_datadir/aclocal/argz.m4
%_datadir/aclocal/ltoptions.m4
%_datadir/aclocal/ltsugar.m4
%_datadir/aclocal/ltversion.m4
%_datadir/aclocal/lt~obsolete.m4
%_mandir/man1/libtool.1*
%_mandir/man1/libtoolize.1*

%files libs
%defattr(0644,root,root,0755)
%_libdir/libltdl.so.*

%changelog
* Sun Jun 15 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.4.2-owl1
- Updated to 2.4.2.
- Replaced the deprecated PreReq tag with Requires(post,preun).

* Tue Oct 11 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.5.22-owl5
- Patched tagdemo test to be compliant with g++ 4.6.1.

* Mon Nov 30 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.5.22-owl4
- Applied upstream's backport of libltdl changes from the 2.26b release
to fix CVE-2009-3736.

* Sun Aug 30 2009 Solar Designer <solar-at-owl.openwall.com> 1.5.22-owl3
- Run the tests during package build by default.

* Sat May 09 2009 Solar Designer <solar-at-owl.openwall.com> 1.5.22-owl2
- Once again prevent build host name leaks into the generated libtool script
(this was broken with a previous update).

* Tue Jun 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.5.22-owl1
- Updated to 1.5.22.

* Sun Sep 25 2005 Michail Litvak <mci-at-owl.openwall.com> 1.5.18-owl2
- Don't package .la files.

* Thu May 26 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.5.18-owl1
- Updated to 1.5.18, reviewed and updated patches.
- Applied a change from Debian and ALT: do not add the contents of
dependency_libs to the link line when linking programs.
- Corrected info files installation.
- Added URL.

* Sat Mar 20 2004 Michail Litvak <mci-at-owl.openwall.com> 1.5.2-owl1.1
- Don't install demo in docs, we can do make check if we need this.

* Tue Feb 24 2004 Michail Litvak <mci-at-owl.openwall.com> 1.5.2-owl1
- 1.5.2
- Regenerate patches, some spec changes.
- Add -alt-ltmain-legacy.diff

* Wed Oct 22 2003 Solar Designer <solar-at-owl.openwall.com> 1.3.5-owl11
- Prevent build host name leaks into the generated libtool script.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 1.3.5-owl10
- Deal with info dir entries such that the menu looks pretty.

* Tue Feb 05 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Sun May 06 2001 Solar Designer <solar-at-owl.openwall.com>
- Ensure proper permissions on demo (installed as documentation).

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH

# $Owl: Owl/packages/libtool/libtool.spec,v 1.22 2009/05/09 06:03:53 solar Exp $

%define BUILD_TEST 0

Summary: The GNU Libtool, which simplifies the use of shared libraries.
Name: libtool
Version: 1.5.22
Release: owl2
License: GPL/LGPL
Group: Development/Tools
URL: http://www.gnu.org/software/libtool/
Source: ftp://ftp.gnu.org/gnu/libtool/libtool-%version.tar.gz
Patch0: libtool-1.5.22-alt-tmp.diff
Patch1: libtool-1.5.18-owl-info.diff
Patch2: libtool-1.5.22-owl-buildhost.diff
Patch3: libtool-1.5.18-alt-deb-link_all_deplibs.diff
Patch4: libtool-1.5.18-alt-ltmain-legacy.diff
Patch5: libtool-1.5.18-alt-ld.so.conf.diff
Patch6: libtool-1.5.18-rh-multilib-hack.diff
PreReq: /sbin/install-info, autoconf, automake, m4, perl
Requires: libtool-libs = %version-%release, mktemp
Prefix: %_prefix
BuildRequires: automake >= 1.9, autoconf, texinfo
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
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
rm doc/libtool.info
%define __libtoolize echo --
%configure

make -C doc
make
%if %BUILD_TEST
%__make check
%endif
bzip2 -9fk ChangeLog

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

%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README THANKS TODO ChangeLog.bz2
%_bindir/*
%_infodir/libtool.info*
%_includedir/ltdl.h
%_datadir/libtool
%_libdir/libltdl.so
%_libdir/libltdl.a
%_datadir/aclocal/libtool.m4
%_datadir/aclocal/ltdl.m4

%files libs
%defattr(-,root,root)
%_libdir/libltdl.so.*

%changelog
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

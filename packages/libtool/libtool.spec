# $Id: Owl/packages/libtool/libtool.spec,v 1.10 2004/11/23 22:40:46 mci Exp $

Summary: The GNU Libtool, which simplifies the use of shared libraries.
Name: libtool
Version: 1.5.2
Release: owl1.1
License: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/libtool/libtool-%version.tar.gz
Patch0: libtool-1.5.2-rh-mktemp.diff
Patch1: libtool-1.5.2-rh-nonneg.diff
Patch2: libtool-1.5.2-owl-info.diff
Patch3: libtool-1.5.2-owl-buildhost.diff
Patch4: libtool-1.5.2-alt-ltmain-legacy.diff
PreReq: /sbin/install-info, autoconf, automake, m4, perl
Requires: libtool-libs = %version-%release, mktemp
Prefix: %_prefix
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

%build
rm doc/libtool.info
%define __libtoolize echo --
%configure

make -C doc
make

# XXX: make this ifdef'ed ?
# make check

%install
rm -rf %buildroot
mkdir -p %buildroot%_prefix

%makeinstall

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/libtool.info.gz %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/libtool.info.gz %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS README
%doc THANKS TODO ChangeLog
%_bindir/*
%_infodir/libtool.info*
%_includedir/ltdl.h
%_datadir/libtool
%_libdir/libltdl.so
%_libdir/libltdl.*a
%_datadir/aclocal/libtool.m4
%_datadir/aclocal/ltdl.m4

%files libs
%defattr(-,root,root)
%_libdir/libltdl.so.*

%changelog
* Sat Mar 20 2004 Michail Litvak <mci@owl.openwall.com> 1.5.2-owl1.1
- Don't install demo in docs, we can do make check if we need this.

* Tue Feb 24 2004 Michail Litvak <mci@owl.openwall.com> 1.5.2-owl1
- 1.5.2
- Regenerate patches, some spec changes.
- Add -alt-ltmain-legacy.diff

* Wed Oct 22 2003 Solar Designer <solar@owl.openwall.com> 1.3.5-owl11
- Prevent build host name leaks into the generated libtool script.

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com> 1.3.5-owl10
- Deal with info dir entries such that the menu looks pretty.

* Tue Feb 05 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Sun May 06 2001 Solar Designer <solar@owl.openwall.com>
- Ensure proper permissions on demo (installed as documentation).

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

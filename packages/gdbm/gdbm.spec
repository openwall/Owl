# $Owl: Owl/packages/gdbm/gdbm.spec,v 1.17 2014/07/12 13:51:10 galaxy Exp $

%define def_with() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _with_%1 --with-%1%{?2:=%2}}}}
%define def_without() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _without_%1 --without-%1}}}
%define def_enable() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _with_%1 --enable-%1%{?2:=%2}}}}
%define def_disable() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _without_%1 --disable-%1}}}

%def_enable	nls
%def_enable	static
%def_enable	compat

Summary: A GNU set of database routines which use extensible hashing.
Name: gdbm
Version: 1.11
Release: owl1
License: GPL
Group: System Environment/Libraries
Source: ftp://ftp.gnu.org/gnu/gdbm/gdbm-%version.tar.gz
Patch0: %name-1.10-fc-zeroheaders.diff
Prefix: %_prefix
BuildRequires: sed >= 4.0.9
BuildRequires: gettext >= 0.19.1, libtool, automake, autoconf
BuildRequires: /sbin/ldconfig
BuildRoot: /override/%name-%version

%description
gdbm is a GNU database indexing library, including routines which use
extensible hashing.  gdbm works in a similar way to standard Unix dbm
routines.  gdbm is useful for developers who write C applications and
need access to a simple and efficient database or who are building C
applications which will use such a database.

%package utils
Summary: Command line utilities for the gdbm library.
Group: Development/Libraries
Requires: gdbm >= %version

%description utils
This package provides command line utilities to help administer the
GDBM databases.

%package devel
Summary: Development libraries and header files for the gdbm library.
Group: Development/Libraries
Requires(post,preun): /sbin/install-info
Requires: gdbm = %version

%description devel
gdbm-devel contains the development libraries and header files for
gdbm, the GNU database system.  These libraries and header files are
necessary if you plan to do development using the gdbm database.

%prep
%setup -q
%patch0 -p 1

gettextize -f -q --symlink
rm src/gettext.h
ln -s '%_datadir/gettext/gettext.h' src/
aclocal --force -I m4
autoreconf -fis

%{expand:%%define optflags %optflags -Wall}
%{expand:%%global _oldincludedir %_includedir}
%{expand:%%global _includedir %_includedir/gdbm}

%build
%configure \
	--disable-rpath \
%if 0%{?_with_compat:1}
	--enable-libgdbm-compat \
%else
	--disable-libgdbm-compat \
%endif
	%{?_with_static}%{?_without_static} \
#

%__make

%install
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'

%makeinstall

%if %{?_with_compat:1}
/sbin/ldconfig -v -n '%buildroot%_libdir'
%endif

pushd '%buildroot'
ln -sf gdbm/gdbm.h .%_oldincludedir/gdbm.h
popd

%find_lang %name || :
touch '%name.lang'

# remove unpackaged files
find '%buildroot' -type f -name '*.la' -delete
rm -- '%buildroot%_infodir/dir'

%check
%__make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info '%_infodir/gdbm.info' '%_infodir/dir' \
	--entry="* gdbm: (gdbm).					The GNU Database."

%preun devel
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete '%_infodir/gdbm.info' '%_infodir/dir' \
		--entry="* gdbm: (gdbm).					The GNU Database."
fi

%files -f %name.lang
%defattr(0644,root,root,0755)
%doc COPYING NEWS README
%_libdir/libgdbm.so.*
%if 0%{?_with_compat:1}
%_libdir/libgdbm_compat.so.*
%endif

%files utils
%defattr(0644,root,root,0755)
%attr(0755,root,root) %_bindir/gdbm_dump
%attr(0755,root,root) %_bindir/gdbm_load
%attr(0755,root,root) %_bindir/gdbmtool
%_mandir/man1/gdbm_dump.1*
%_mandir/man1/gdbm_load.1*
%_mandir/man1/gdbmtool.1*

%files devel
%defattr(0644,root,root,0755)
%_oldincludedir/gdbm.h
%_includedir
%_infodir/*.info*
%_mandir/man3/*
%_libdir/libgdbm.so
%if 0%{?_with_static:1}
%_libdir/libgdbm.a
%endif
%if 0%{?_with_compat:1}
%_libdir/libgdbm_compat.so
%if 0%{?_with_static:1}
%_libdir/libgdbm_compat.a
%endif
%endif

%changelog
* Thu Jun 19 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.11-owl1
- Updated to 1.11.
- Introduced the utils sub-package.
- Replaced the deprecated PreReq tag with Requires(post,preun).

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.8.0-owl11
- Corrected info files installation.

* Fri Sep 23 2005 Michail Litvak <mci-at-owl.openwall.com> 1.8.0-owl10
- Don't package .la files.

* Wed Jul 21 2004 Michail Litvak <mci-at-owl.openwall.com> 1.8.0-owl9
- Use sed -i.

* Thu Jul 01 2004 Solar Designer <solar-at-owl.openwall.com> 1.8.0-owl8
- Fixed whacky libdir statement in libgdbm.la (patch from Andreas Ericsson
with minor changes).

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 1.8.0-owl7
- Deal with info dir entries such that the menu looks pretty.

* Fri Feb 01 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions
- include text docs in binary package
- handle CFLAGS and fhs stuff in Makefile

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH
- fix URL

# $Id: Owl/packages/gdbm/gdbm.spec,v 1.11 2004/11/23 22:40:45 mci Exp $

Summary: A GNU set of database routines which use extensible hashing.
Name: gdbm
Version: 1.8.0
Release: owl9
License: GPL
Group: System Environment/Libraries
Source: ftp://ftp.gnu.org/gnu/gdbm/gdbm-%version.tar.gz
Patch0: gdbm-1.8.0-rh-header.diff
Patch1: gdbm-1.8.0-rh-owl-Makefile.diff
PreReq: /sbin/ldconfig
Prefix: %_prefix
BuildRequires: sed >= 4.0.9
BuildRoot: /override/%name-%version

%description
gdbm is a GNU database indexing library, including routines which use
extensible hashing.  gdbm works in a similar way to standard Unix dbm
routines.  gdbm is useful for developers who write C applications and
need access to a simple and efficient database or who are building C
applications which will use such a database.

%package devel
Summary: Development libraries and header files for the gdbm library.
Group: Development/Libraries
PreReq: /sbin/install-info
Requires: gdbm

%description devel
gdbm-devel contains the development libraries and header files for
gdbm, the GNU database system.  These libraries and header files are
necessary if you plan to do development using the gdbm database.

%prep
%setup -q
%patch0 -p 1
%patch1 -p 1

%{expand:%%define optflags %optflags -Wall}
%{expand:%%global _includedir %_includedir/gdbm}

%build
libtoolize --force --copy
aclocal
autoreconf
%configure
make

%install
rm -rf %buildroot

%makeinstall install-compat

cd %buildroot

# Fix devel package whackyness
sed -i "s,^\(libdir=\).*$,\1'%_libdir'," .%_libdir/libgdbm.la

ln -sf gdbm/gdbm.h .%_oldincludedir/gdbm.h
ln -sf libgdbm.so.2.0.0 .%_libdir/libgdbm.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %_infodir/gdbm.info.gz %_infodir/dir \
	--entry="* gdbm: (gdbm).                                 The GNU Database."

%preun devel
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gdbm.info.gz %_infodir/dir \
		--entry="* gdbm: (gdbm).                                 The GNU Database."
fi

%files
%defattr(-,root,root)
%doc COPYING NEWS README
%_libdir/libgdbm.so.*

%files devel
%defattr(-,root,root)
%_libdir/libgdbm.so
%_libdir/libgdbm.la
%_libdir/libgdbm.a
%_oldincludedir/gdbm.h
%_includedir
%_infodir/*.info*
%_mandir/man3/*

%changelog
* Wed Jul 21 2004 Michail Litvak <mci@owl.openwall.com> 1.8.0-owl9
- Use sed -i.

* Thu Jul 01 2004 Solar Designer <solar@owl.openwall.com> 1.8.0-owl8
- Fixed whacky libdir statement in libgdbm.la (patch from Andreas Ericsson
with minor changes).

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com> 1.8.0-owl7
- Deal with info dir entries such that the menu looks pretty.

* Fri Feb 01 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions
- include text docs in binary package
- handle CFLAGS and fhs stuff in Makefile

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- fix URL

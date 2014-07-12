# $Owl: Owl/packages/sqlite/sqlite.spec,v 1.1 2014/07/12 13:59:12 galaxy Exp $

%define def_enable() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _with_%1 --enable-%1}}}
%define def_disable() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _without_%1 --disable-%1}}}

%def_enable  dynamic_extensions
%def_enable  readline
%def_disable tcl
%def_enable  tests
%def_enable  threadsafe

Summary: A serverless, zero-configuration, transactional SQL database engine.
Name: sqlite
Version: 3.8.5
Release: owl1
License: Public Domain
URL: http://sqlite.org/
Group: Applications/Databases

# Source: http://www.sqlite.org/2013/sqlite-autoconf-3080200.tar.gz
Source: %name-%version.tar.xz

BuildRoot: /override/%name-%version
Requires: lib%name >= %version
BuildRequires: autoconf >= 2.61
BuildRequires: libtool
%if 0%{?_with_readline:1}
BuildRequires: readline-devel, ncurses-devel
%endif
%if 0%{?_with_tcl:1}
BuildRequires: tcl
%endif

%description
SQLite is a software library that implements a self-contained,
serverless, zero-configuration, transactional SQL database engine.
SQLite is likely the most widely deployed SQL database engine in the
world.

%package -n lib%name
Summary: Library that implements an embeddable SQL database engine.
Group: System/Libraries

%description -n lib%name
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexibility of an SQL database without the administrative hassles of
supporting a separate database server.

%package -n lib%name-devel
Summary: Development tools for the SQLite embeddable SQL database engine
Group: Development/Libraries
Requires: lib%name = %version-%release
# RHEL/CentOS compatibility
Provides: sqlite-devel

%description -n lib%name-devel
This package contains the header files and development documentation 
for lib%name. If you like to develop programs using lib%name, you will
need to install this package.

%package -n lib%name-devel-static
Summary: Static library that implements an embeddable SQL database engine.
Group: Development/Libraries
Requires: lib%name-devel = %version-%release

%description -n lib%name-devel-static
This package constains the static library for lib%name.  If you want to
link your applications statically with lib%name you will need to install
this package.

%prep
%setup -q

autoreconf -fis

%build
CFLAGS='%optflags -DNDEBUG -DSQLITE_TEMP_STORE=2 -DSQLITE_ENABLE_FTS4 -DSQLITE_ENABLE_RTREE -DSQLITE_SECURE_DELETE -DSQLITE_ENABLE_UNLOCK_NOTIFY -DSQLITE_ENABLE_FTS3_PARENTHESIS -DSQLITE_ENABLE_MEMORY_MANAGEMENT -DSQLITE_SOUNDEX -DSQLITE_ENABLE_COLUMN_METADATA'
%if 0%{?_with_readline:1}
# For some reason the configure script fails to find our readline (I
# suspect it's due to the way we link our library that it requires an
# explicit link agains libtinfo). So, let's provide the needed
# information -- it's better this way anyway :) -- (GM)
ac_cv_search_readline="-lreadline -ltinfo"
export ac_cv_search_readline
%endif
export CFLAGS
%configure \
	--enable-shared \
	--enable-static \
	%{?_with_readline} %{?_without_readline} \
	%{?_with_threadsafe} %{?_without_threadsafe} \
%if 0%{?_with_dynamic_extensions:1}
	--enable-dynamic-extensions \
%else
	--disable-dynamic-extensions \
%endif
#

%__make

%if 0%{?_with_tcl:1}
echo 'WARNING: the TCL build is totally untested!'
pushd tea
%configure \
	--enable-shared \
	--enable-threads \
	--disable-rpath \
#

%__make
popd
%endif

%install
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'

%__make install 'DESTDIR=%buildroot'

%if 0%{?_with_tcl:1}
%__make -C tea install 'DESTDIR=%buildroot'
%endif

# clean up
find '%buildroot' -xdev -name '*.la' -delete
rm -rf -- '%buildroot%_libdir/pkgconfig'

%check
# requires tcl to be present
#%__make test
echo 'WARNING: tests were skipped since they require Tcl' >&2

%post -n lib%name -p /sbin/ldconfig
%postun -n lib%name -p /sbin/ldconfig

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %_bindir/*
%_mandir/man1/*.1*

%files -n lib%name
%defattr(0644,root,root,0755)
%_libdir/*.so.*

%files -n lib%{name}-devel
%defattr(0644,root,root,0755)
%_includedir/*
%_libdir/*.so*

%files -n lib%name-devel-static
%defattr(0644,root,root,0755)
%_libdir/*.a

%changelog
* Mon Jun 09 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.8.5-owl1
- Introduced to Owl.
- updated to 3.8.5.

* Mon May 12 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.8.4.3-owlx0
- updated to 3.8.4.3.

* Tue Feb 18 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.8.3.1-owlx0
- updated to 3.8.3.1

* Sat Jan 25 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.8.2-owlx0
- updated to 3.8.2.

* Tue Dec 14 2010 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.6.23.1-owlx0
- Cleaned the spec up and updated it in accordance with the latest
OwlX conventions.

* Wed Jun 16 2010 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.6.23.1-gm1
- wrapped the creation of ld.so's config files into a conditional since
this is needed only on non-system builds.
- packaged the current symlink.

* Sun Apr 11 2010 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.6.23.1-gm0
- updated to 3.6.23.1.
- revised the spec file to use common macros from rpm-build-owlx.
- splitted the package into subpackages.

* Thu Apr 16 2009 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.6.13-gm0
- Updated to 3.6.13 and started to use the amalgamation source.

* Fri Mar 20 2009 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.6.7-gm2
- Added /etc/ld.so.conf.d/libsqlite.conf

* Sun Aug 31 2008 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.6.7-gm1
- Initial Owl release.


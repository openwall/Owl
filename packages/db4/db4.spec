# $Owl: Owl/packages/db4/db4.spec,v 1.27 2017/06/15 14:18:27 solar Exp $

%define __soversion	4.3
%define _libdb_a	libdb-%__soversion.a
%define _libcxx_a	libdb_cxx-%__soversion.a
%define _libdb_so	libdb-%__soversion.so
%define docdir		%_docdir/%name-%version

Summary: The Berkeley DB database library (version 4) for C.
Name: db4
Version: 4.3.29
Release: owl6
License: Sleepycat
Group: System Environment/Libraries
URL: http://www.sleepycat.com
# ftp://ftp.sleepycat.com/releases/db-%version.tar.gz
Source0: db-%version.tar.bz2
Source1: ftp://ftp.sleepycat.com/releases/db.1.85.tar.gz
Patch0: db-1.85-up-fixes.diff
Patch1: db-1.85-rh-errno.diff
# http://www.oracle.com/technology/products/berkeley-db/db/update/4.3.29/patch.4.3.29.1
Patch2: db-4.3.29.1.diff
Patch3: db-4.3.29-cvs-20051006-db185.diff
Patch4: db-4.3.29-up-configure-mutex.diff
Patch5: db-4.3.29-alt-configure.diff
Patch6: db-4.3.29-owl-DB_CONFIG.diff
Obsoletes: db1, db1-devel
BuildRequires: perl, libtool, ed, gcc-c++, glibc-utils
BuildRoot: /override/%name-%version

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications.  The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery.  The Berkeley DB supports C, C++, Java, and Perl APIs.

%package utils
Summary: Command line tools for managing Berkeley DB (version 4) databases.
Group: Applications/Databases
Requires: db4 = %version-%release
Obsoletes: db2-utils, db3-utils

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications.  The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery.  The Berkeley DB supports C, C++, Java, and Perl APIs.

%package devel
Summary: Development files for the Berkeley DB (version 4) library.
Group: Development/Libraries
Requires: db4 = %version-%release
Obsoletes: db2-devel, db3-devel

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications.  This package contains the header files
and libraries for building programs which use the Berkeley DB.

%package doc
Summary: Development documentation for the Berkeley DB (version 4) library.
Group: Documentation

%description doc
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications.  This package contains the documentation
for building programs which use the Berkeley DB.

%ifnarch x86_64
%package compat-fake
Summary: Fake package to help upgrade db4 from 4.0 and 4.2 to 4.3+.
Group: System Environment/Libraries
Provides: libdb-4.0.so, libdb_cxx-4.0.so, libdb-4.2.so, libdb_cxx-4.2.so

%description compat-fake
This package solves the problem with upgrading db4 4.0 and 4.2 -based Owl
to db4 4.3+ version by reporting necessary Provides to RPM.  All packages
in db4 4.3+ -based Owl don't rely on older sonames.  If you have a package
which uses these older libraries, you have to recompile that package
against the db4 package supplied with Owl or create a compatibility
package with necessary binaries of old libdb libraries.
%endif

%prep
%setup -q -n db-%version -a 1
pushd db.1.85
%patch0 -p1
%patch1 -p1
popd
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# Package missing docs.
cp -p docs/gsg/JAVA/returns.html docs/gsg/C/

%{expand:%%define optflags_lib %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%build
mkdir dist/build

# Static link with old db-185 libraries.
%__make -C db.1.85/PORT/%_os CC="%__cc" OORG="%optflags_lib"
sh libtool --mode=compile %__cc %optflags \
	-Idb.1.85/PORT/%_os/include -D_REENTRANT \
	-c db_dump185/db_dump185.c -o dist/build/db_dump185.lo
sh libtool --mode=link %__cc -o dist/build/db_dump185 \
	dist/build/db_dump185.lo db.1.85/PORT/%_os/libdb.a

pushd dist/build
ln -s ../configure .
CC="%__cc"
CXX="%__cxx"
export CC CXX
%configure \
	--enable-compat185 --enable-dump185 \
	--enable-shared --enable-static \
	--enable-rpc \
	--enable-cxx \
	--disable-java \
	--disable-posixmutexes
%__make
popd #dist/build

%install
rm -rf %buildroot
mkdir -p %buildroot{/%_lib,%_libdir,%_includedir/db4}

%makeinstall -C dist/build docdir=%buildroot%docdir

pushd %buildroot

# Compress Postscript documentation.
gzip -9 .%docdir/ref/refs/*.ps
sed -i 's/usenix\.ps/&.gz/g' .%docdir/ref/refs/refs.html

# Allow owner to modify to make our brp-scripts happy
chmod -R u+w .{%_bindir,%_libdir}

# Relocate main shared library from %_libdir/ to /%_lib/.
mv .%_libdir/%_libdb_so ./%_lib/
for f in .%_libdir/libdb{,-{*,%__soversion}}.so; do
	ln -sf ../../%_lib/%_libdb_so "$f"
done

# Remove non-versioned archives.
rm .%_libdir/libdb{,_cxx}.a

# Relocate header files.
pushd .%_includedir
mv *.h db4/
for i in db4/*.h; do
	ln -s $i .
done
popd #.%_includedir

popd #%buildroot

install -pm644 README LICENSE %buildroot%docdir/
cp -a examples_c* %buildroot%docdir/

# Remove unpackaged files
rm %buildroot%_libdir/*.la

# caught by the newer RPM
LIB_MAJ='%__soversion'
LIB_MAJ="${LIB_MAJ%%.*}"
rm -- "%buildroot%_libdir/libdb-$LIB_MAJ.so"
rm -- "%buildroot%_libdir/libdb_cxx-$LIB_MAJ.so"

# Remove unneeded documentation.
rm %buildroot%docdir/examples_*/tags
rm -r %buildroot%docdir/java

chmod -R u+w %buildroot

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %docdir
%docdir/[A-Z]*
/%_lib/libdb-%__soversion.so
%_libdir/libdb-%__soversion.so
%_libdir/libdb_cxx-%__soversion.so

%files utils
%defattr(-,root,root)
%dir %docdir
%docdir/utility
%_bindir/berkeley_db*_svc
%_bindir/db*_archive
%_bindir/db*_checkpoint
%_bindir/db*_deadlock
%_bindir/db*_dump*
%_bindir/db*_load
%_bindir/db*_printlog
%_bindir/db*_recover
%_bindir/db*_stat
%_bindir/db*_upgrade
%_bindir/db*_verify

%files devel
%defattr(-,root,root)
%_libdir/libdb.so
%_libdir/libdb_cxx.so
%_libdir/%_libdb_a
%_libdir/%_libcxx_a
%_includedir/%name
%_includedir/*.h

%files doc
%defattr(-,root,root)
%dir %docdir
%docdir/[a-tv-z]*

%ifnarch x86_64
%files compat-fake
%endif

%changelog
* Thu Jun 15 2017 Solar Designer <solar-at-owl.openwall.com> 4.3.29-owl6
- Don't open the DB_CONFIG file in the current directory.

* Sun Aug 16 2009 Solar Designer <solar-at-owl.openwall.com> 4.3.29-owl5
- Don't require the main package in -doc.

* Sat May 09 2009 Solar Designer <solar-at-owl.openwall.com> 4.3.29-owl4
- Moved the documentation from db4-devel to db4-doc (a new subpackage).

* Tue Oct 09 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.3.29-owl3
- Applied official update 4.3.29.1.
- Backported fix for configure mutexes support from db-4.4.20.

* Thu May 04 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.3.29-owl2
- Added glibc-utils to BuildRequires due to rpcgen.

* Thu Apr 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.3.29-owl1
- Updated to 4.3.29.
- Backported db185 fixes from db-4.4.20.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2.52-owl2
- Compressed Postscript documentation.

* Wed Dec 21 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2.52-owl1
- Updated to 4.2.52.
- Linked libdb_cxx shared library dynamically with libgcc_s and libstdc++.
- Added compat-fake subpackage to help upgrade procedure.

* Fri Sep 23 2005 Michail Litvak <mci-at-owl.openwall.com> 4.0.14-owl3
- Don't package .la files.

* Sun Jan 16 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.0.14-owl2
- Add write permission to files under %_bindir and %_libdir to allow brp-
scripts to do their work.
- Add "-Xcompiler -static-libgcc" to LIBXSO_LIBS to link libgcc statically.
- Used %%__cc and %%__make macros.
- Cleaned up the spec.

* Tue Mar 02 2004 Michail Litvak <mci-at-owl.openwall.com> 4.0.14-owl1
- Imported spec from RH.

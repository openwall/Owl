# $Owl: Owl/packages/db4/db4.spec,v 1.16 2006/04/04 00:28:34 ldv Exp $

%define __soversion	4.2
%define _libdb_a	libdb-%__soversion.a
%define _libcxx_a	libdb_cxx-%__soversion.a
%define _libdb_so	libdb-%__soversion.so
%define docdir		%_docdir/%name-%version

Summary: The Berkeley DB database library (version 4) for C.
Name: db4
Version: 4.2.52
Release: owl2
License: Sleepycat
Group: System Environment/Libraries
URL: http://www.sleepycat.com
Source0: http://www.sleepycat.com/update/snapshot/db-%version.tar.gz
Source1: http://www.sleepycat.com/update/snapshot/db.1.85.tar.gz
Patch0: db-1.85-up-fixes.diff
Patch1: db-1.85-rh-errno.diff
Patch2: db-4.2.52-up-fixes.diff
Patch3: db-4.2.52-alt-configure.diff
Patch4: db-4.2.52-rh-java.diff
Patch5: db-4.2.52-rh-gcj.diff
Patch6: db-4.2.52-rh-fastjar.diff
Obsoletes: db1, db1-devel
BuildRequires: perl, libtool, ed, gcc-c++
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
Group: System Environment/Libraries
Requires: db4 = %version-%release
Obsoletes: db2-devel, db3-devel

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications.  This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%package compat-fake
Summary: Fake package to help upgrade db4 from 4.0 to 4.2+.
Group: System Environment/Libraries
Provides: libdb-4.0.so, libdb_cxx-4.0.so

%description compat-fake
This package solves the problem with upgrading db4 4.0 -based Owl to
db4 4.2+ version by reporting necessary Provides to RPM.  All packages
in db4 4.2+ -based Owl don't rely on libdb-4.0.so and libdb_cxx-4.0.so.  If
you have a package which uses these older libraries, you have to recompile
that package against the db4 package supplied with Owl or create a
compatibility package with necessary binaries of old libdb libraries.

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
mv .%_libdir/%_libdb_so ./lib/
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

# Remove unneeded documentation.
rm %buildroot%docdir/examples_*/tags
rm -r %buildroot%docdir/java

rm %buildroot%_libdir/*.la

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
%dir %docdir
%docdir/[aeirs]*
%_libdir/libdb.so
%_libdir/libdb_cxx.so
%_libdir/%_libdb_a
%_libdir/%_libcxx_a
%_includedir/%name
%_includedir/*.h

%files compat-fake

%changelog
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

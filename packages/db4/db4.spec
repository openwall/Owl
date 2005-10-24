# $Id: Owl/packages/db4/db4.spec,v 1.11 2005/10/24 02:22:11 solar Exp $

%define __soversion	4.0
%define _libdb_a	libdb-%__soversion.a
%define _libcxx_a	libdb_cxx-%__soversion.a
%define _libdb_so	libdb-%__soversion.so

Summary: The Berkeley DB database library (version 4) for C.
Name: db4
Version: 4.0.14
Release: owl3
License: GPL
Group: System Environment/Libraries
URL: http://www.sleepycat.com
Source0: http://www.sleepycat.com/update/snapshot/db-%version.tar.gz
Source1: http://www.sleepycat.com/update/snapshot/db.1.85.tar.gz
Patch0: db-1.85-up-fixes.diff
Patch1: db-1.85-rh-errno.diff
Patch2: db-4.0.14-rh-ham-dirty-meta.diff
Patch3: db-4.0.14-rh-recover.diff
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

%prep
%setup -q -n db-%version -a 1
pushd db.1.85
%patch0 -p1
%patch1 -p1
popd
%patch2 -p1
%patch3 -p1

%{expand:%%define optflags_lib %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%build

# Static link with old db-185 libraries.
%__make -C db.1.85/PORT/%_os CC="%__cc" OORG="%optflags_lib"
/bin/sh libtool --mode=compile %__cc %optflags \
	-Idb.1.85/PORT/%_os/include -D_REENTRANT \
	-c db_dump185/db_dump185.c -o dist/db_dump185.lo
/bin/sh libtool --mode=link %__cc -o dist/db_dump185 \
	dist/db_dump185.lo db.1.85/PORT/%_os/libdb.a

pushd dist

CC="%__cc"
CXX="%__cc"
# XXX: (GM): This is a workaround to link libgcc statically
LIBXSO_LIBS="-Xcompiler -static-libgcc"
export CC CXX LIBXSO_LIBS
%configure \
	--enable-compat185 --enable-dump185 \
	--enable-shared --enable-static --enable-rpc \
	--enable-cxx \
	--disable-java \
	--disable-posixmutexes
%__make libdb=%_libdb_a libcxx=%_libcxx_a LIBSO_LIBS='$(LIBS)'
popd

%install
rm -rf %buildroot

mkdir -p %buildroot{/lib,%_libdir,%_includedir/db4}

%makeinstall -C dist libdb=%_libdb_a libcxx=%_libcxx_a

chmod +x %buildroot%_libdir/*.so*

# Allow owner to modify to make our brp-scripts happy
chmod -R u+w %buildroot{%_bindir,%_libdir}

pushd %buildroot
# Relocate main shared library from %_libdir/ to /lib/.
mv .%_libdir/%_libdb_so ./lib/
for f in .%_libdir/libdb{,-{*,%__soversion}}.so; do
	ln -s -nf ../../lib/%_libdb_so "$f"
done

mv .%_includedir/*.h .%_includedir/db4/

for i in db.h db_cxx.h db_185.h cxx_common.h cxx_except.h; do
	ln -s db4/$i .%_includedir
done
popd

rm -f %buildroot%_libdir/*.la

# Eliminate installed docs.
rm -rf %buildroot%_prefix/docs

%clean
rm -rf %buildroot

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc LICENSE README docs/images
/%_lib/libdb-%__soversion.so
%_libdir/libdb-%__soversion.so
%_libdir/libdb_cxx-%__soversion.so

%files utils
%defattr(-,root,root)
%doc docs/utility
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
%doc docs/api_c docs/api_cxx docs/api_tcl docs/index.html
%doc docs/ref docs/sleepycat
%doc examples_c examples_cxx
%_libdir/libdb.so
%_libdir/libdb_cxx.so
%_libdir/%_libdb_a
%_libdir/%_libcxx_a
%_includedir/%name
%_includedir/*.h

%changelog
* Fri Sep 23 2005 Michail Litvak <mci@owl.openwall.com> 4.0.14-owl3
- Don't package .la files.

* Sun Jan 16 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 4.0.14-owl2
- Add write permission to files under %_bindir and %_libdir to allow brp-
scripts to do their work.
- Add "-Xcompiler -static-libgcc" to LIBXSO_LIBS to link libgcc statically.
- Used %%__cc and %%__make macros.
- Cleaned up the spec.

* Tue Mar 02 2004 Michail Litvak <mci@owl.openwall.com> 4.0.14-owl1
- Imported spec from RH.

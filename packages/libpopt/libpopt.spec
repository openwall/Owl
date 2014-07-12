# $Owl: Owl/packages/libpopt/libpopt.spec,v 1.1 2014/07/12 13:56:30 galaxy Exp $

%define def_with() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _with_%1 --with-%1%{?2:=%2}}}}
%define def_without() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _without_%1 --without-%1}}}
%define def_enable() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _with_%1 --enable-%1%{?2:=%2}}}}
%define def_disable() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _without_%1 --disable-%1}}}

%def_enable	nls
%def_enable	static

Summary: C library for parsing command line parameters
Name: libpopt
Version: 1.16
Release: owl1
License: MIT
Group: System Environment/Libraries
URL: http://www.rpm5.org/
Source: http://www.rpm5.org/files/popt/popt-%version.tar.gz
Patch0: %name-1.16-fc-execfail.diff
Patch1: %name-1.16-fc-man-page.diff
Patch2: %name-1.16-fc-help.diff
Patch3: %name-1.16-owl-autotools.diff
Patch4: %name-1.16-owl-libversion.diff
BuildRequires: gettext, libtool, autoconf >= 2.69, automake >= 1.14
Obsoletes: popt <= 1.8-owl29
# RHEL/FC compatibility
Provides: popt = %version-%release
BuildRoot: /override/%name-%version

%description
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but
it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%package devel
Summary: Development files for the popt library
Group: Development/Libraries
Requires: %name = %version-%release
# RHEL/FC compatibility
Provides: popt-devel = %version-%release

%description devel
The popt-devel package includes header files and libraries necessary
for developing programs which use the popt C library. It contains the
API documentation of the popt library, too.

%if 0%{?_with_static:1}
%package devel-static
Summary: Static library for parsing command line parameters
Group: Development/Libraries
Requires: %name-devel = %version-%release
# RHEL/FC compatibility
Provides: popt-static = %version-%release

%description devel-static
The popt-static package includes static libraries of the popt library.
Install it if you need to link statically with libpopt.
%endif

%prep
%setup -q -n popt-%version

%patch0 -p1 -b .execfail
%patch1 -p1 -b .man-page
%patch2 -p1 -b .help
%patch3 -p1 -b .autotools
%patch4 -p1 -b .libversion

gettextize -f -q --symlink
autoreconf -fis

%build
%configure \
	--disable-rpath \
	%{?_with_static}%{?_without_static} \
	%{?_with_nls}%{?_without_nls} \
# end of configure

%__make

%install
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'

%makeinstall

pushd '%buildroot'
mkdir -p './%_lib'
mv -v '.%_libdir/%name'.so.* './%_lib/'
rm -- '.%_libdir/%name.so'
ln -s "../../%_lib/$(cd '%_lib' && ls libpopt.so.*.*.*)" \
	'.%_libdir/libpopt.so'

# Multiple popt configurations are possible
mkdir -p './%_sysconfdir/popt.d'
popd

%find_lang popt || :
touch popt.lang

# remove unpackaged file
find '%buildroot' -name '*.la' -ls -delete
# XXX: is it hardcoded to /usr/lib?
rm -r -- '%buildroot%_prefix/lib/pkgconfig'

%check
./testit.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f popt.lang
%defattr(0644,root,root,0755)
%license COPYING
%doc CHANGES
%_sysconfdir/popt.d
/%_lib/libpopt.so.*

%files devel
%defattr(0644,root,root,0755)
%doc README
%_libdir/libpopt.so
%_includedir/popt.h
%_mandir/man3/popt.3*

%if 0%{?_with_static:1}
%files devel-static
%defattr(0644,root,root,0755)
%_libdir/libpopt.a
%endif

%changelog
* Thu Jun 26 2014 (GalaxyMaster) <galaxy-at-openwall.com> 1.16-owl1
- Initial spec for Owl.

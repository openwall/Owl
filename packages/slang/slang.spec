# $Id: Owl/packages/slang/Attic/slang.spec,v 1.11 2004/11/02 04:03:23 solar Exp $

Summary: The shared library for the S-Lang extension language.
Name: slang
Version: 1.4.6
Release: owl4
License: GPL
Group: System Environment/Libraries
URL: http://www.s-lang.org
Source: ftp://ftp.jedsoft.org/pub/davis/slang/v1.4/slang-%version.tar.bz2
Patch0: slang-1.4.6-owl-fixes.diff
Patch1: slang-1.4.6-owl-tmp.diff
PreReq: /sbin/ldconfig
BuildRequires: sed >= 4.0.9
BuildRoot: /override/%name-%version

%description
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package devel
Summary: The static library and header files for development using S-Lang.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
This package contains the S-Lang extension language static libraries
and header files which you'll need if you want to develop S-Lang based
applications.  Documentation which may help you write S-Lang based
applications is also included.

%prep
%setup -q -n slang-%version
%patch0 -p1
%patch1 -p1

%build
sed -i 's,\(ELF_CFLAGS=".*\)-O2\(.*\),\1'"$RPM_OPT_FLAGS"'\2,' configure
export ac_cv_func_snprintf=yes ac_cv_func_vsnprintf=yes \
%configure \
	--includedir=%_includedir/slang \
	--enable-warnings
make elf all

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/include/slang

%makeinstall \
	install_lib_dir=$RPM_BUILD_ROOT%_libdir \
	install_include_dir=$RPM_BUILD_ROOT%_includedir/slang install-elf

# XXX: (GM): Remove unpackaged files (check later).
# Some of these are installed with doc/ in the build directory, but a
# conscious decision needs to be made.
rm %buildroot/usr/doc/slang/COPYING
rm %buildroot/usr/doc/slang/COPYING.ART
rm %buildroot/usr/doc/slang/COPYING.GPL
rm %buildroot/usr/doc/slang/COPYRIGHT
rm %buildroot/usr/doc/slang/changes.txt
rm %buildroot/usr/doc/slang/cref.txt
rm %buildroot/usr/doc/slang/cslang.txt
rm %buildroot/usr/doc/slang/slang.txt
rm %buildroot/usr/doc/slang/slangdoc.html
rm %buildroot/usr/doc/slang/slangfun.txt

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%_libdir/libslang.so.*

%files devel
%defattr(-,root,root)
%doc doc/*
%_libdir/libslang.a
%_libdir/libslang.so
%_includedir/slang

%changelog
* Tue Nov 02 2004 Solar Designer <solar@owl.openwall.com> 1.4.6-owl4
- Set Release to -owl4 to permit for making this public.

* Thu Sep 09 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 1.4.6-owl3.1
- Fixed -fixes.patch to compile under glibc 2.3+

* Tue Jul 20 2004 Michail Litvak <mci@owl.openwall.com> 1.4.6-owl3
- Use sed -i instead of perl.

* Sat Oct 12 2002 Solar Designer <solar@owl.openwall.com> 1.4.6-owl2
- Updated to 1.4.6.
- Reviewed all of the library code for environment variable uses and
restricted those which would be unsafe in SUID/SGID programs.
- Corrected the examples to not use temporary files unsafely.
- Enable snprintf() and vsnprintf() explicitly.
- Set ELF_CFLAGS (used for the shared library) to include RPM_OPT_FLAGS.

* Wed Sep 25 2002 Ilya Andreiv <ilya@if5641.spb.edu>
- Upgrade to 1.4.5

* Tue Feb 05 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Dec 14 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

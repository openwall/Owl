# $Id: Owl/packages/slang/Attic/slang.spec,v 1.3 2002/02/05 16:33:22 solar Exp $

Summary: The shared library for the S-Lang extension language.
Name: slang
Version: 1.4.2
Release: owl2
License: GPL
Group: System Environment/Libraries
URL: http://www.s-lang.org/
Source: ftp://space.mit.edu/pub/davis/slang/v1.4/slang-%{version}.tar.bz2
BuildRoot: /override/%{name}-%{version}

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
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the S-Lang extension language static libraries
and header files which you'll need if you want to develop S-Lang based
applications.  Documentation which may help you write S-Lang based
applications is also included.

%prep
%setup -n slang-%{version} -q

%build
mv autoconf/configure.in .
%configure --includedir=/usr/include/slang
make elf all

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/include/slang

%makeinstall \
	install_lib_dir=$RPM_BUILD_ROOT/usr/lib \
	install_include_dir=$RPM_BUILD_ROOT/usr/include/slang install-elf

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/lib/libslang.so.*

%files devel
%defattr(-,root,root)
%doc doc
/usr/lib/libslang.a
/usr/lib/libslang.so
/usr/include/slang

%changelog
* Tue Feb 05 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Dec 14 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

# $Id: Owl/packages/newt/Attic/newt.spec,v 1.8 2002/02/06 18:52:46 solar Exp $

Summary: A development library for text mode user interfaces.
Name: newt
Version: 0.50.18
Release: owl3
License: LGPL
Group: System Environment/Libraries
Source: ftp://ftp.redhat.com/pub/redhat/code/newt/newt-%{version}.tar.gz
Patch0: newt-0.50.18-castle-owl-Gpm_Open.diff
Patch1: newt-0.50.18-owl-notcl.diff
Patch2: newt-0.50.18-owl-nopython.diff
Requires: slang
BuildRequires: slang
BuildRoot: /override/%{name}-%{version}

%package devel
Summary: Newt windowing toolkit development files.
Requires: slang-devel, %{name} = %{version}-%{release}
Group: Development/Libraries

%description
newt is a programming library for color text mode, widget based user
interfaces.  newt can be used to add stacked windows, entry widgets,
checkboxes, radio buttons, labels, plain text fields, scrollbars,
etc., to text mode user interfaces.  This package also contains the
shared library needed by programs built with newt, as well as a
/usr/bin/dialog replacement called whiptail.  newt is based on the
slang library.

%description devel
The newt-devel package contains the header files and libraries
necessary for developing applications which use newt.  newt is a
development library for text mode user interfaces.  newt is based on
the slang library.

%prep
%setup
%patch0 -p1
%patch1 -p1

%build
autoconf
./configure
make
make shared

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make instroot=$RPM_BUILD_ROOT install
make instroot=$RPM_BUILD_ROOT install-sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr (-,root,root)
%doc CHANGES COPYING
/usr/lib/libnewt.so.*
/usr/bin/whiptail

%files devel
%defattr (-,root,root)
%doc tutorial.sgml
/usr/include/newt.h
/usr/lib/libnewt.a
/usr/lib/libnewt.so

%changelog
* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Fri May 18 2001 Solar Designer <solar@owl.openwall.com>
- Imported Gpm_Open() cleanups from Castle with minor changes, thanks to
Dmitry V. Levin <ldv@alt-linux.org>.

* Thu Dec 14 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- spec cleanup

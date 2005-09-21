# $Id: Owl/packages/cdk/cdk.spec,v 1.3 2005/09/21 22:18:51 solar Exp $

Summary: Curses Development Kit.
Name: cdk
Version: 5.0
%define snapshot 20050424
Release: owl1
License: BSD
Group: System Environment/Libraries
URL: http://invisible-island.net/cdk/
Source: ftp://invisible-island.net/cdk/cdk-%version-%snapshot.tgz
PreReq: /sbin/ldconfig
BuildRequires: ncurses-devel
BuildRoot: /override/%name-%version

%description
CDK is a widget set developed on top of the basic curses library.  It
contains 21 ready to use widgets.  Some of which are text entry field,
scrolling list, selection list, alphalist, pull-down menu, radio
list, viewer widget, dialog box, and many more.

%package devel
Summary: Static library, header files and development documentation for CDK library.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
Header files and development documentation for CDK library.

%prep
%setup -q -n %name-%version-%snapshot

%{expand:%%define optflags %optflags -Wall}

%build
%configure
%__make cdklib cdkshlib

%install
rm -rf %buildroot
%__make install installCDKSHLibrary \
	DESTDIR=%buildroot \
	DOCUMENT_DIR=%buildroot%_docdir/%name-%version

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc CHANGES EXPANDING NOTES README TODO COPYING
%attr(755,root,root) %_libdir/lib*.so.*.*

%files devel
%defattr(-,root,root)
%doc examples demos
%attr(755,root,root) %_libdir/lib*.so
%_libdir/lib*.a
%_includedir/*
%_mandir/man3/*

%changelog
* Mon Sep 19 2005 Michail Litvak <mci@owl.openwall.com> 5.0-owl1
- Initial packaging for Owl.

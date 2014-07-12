# $Owl: Owl/packages/cdk/cdk.spec,v 1.10 2014/07/12 14:08:25 galaxy Exp $

Summary: Curses Development Kit.
Name: cdk
Version: 5.0
%define snapshot 20050424
Release: owl4
License: BSD
Group: System Environment/Libraries
URL: http://invisible-island.net/cdk/
Source: ftp://invisible-island.net/cdk/cdk-%version-%snapshot.tgz
Patch0: cdk-5.0-20050424-owl-tmp.diff
BuildRequires: ncurses-devel, /sbin/ldconfig
BuildRoot: /override/%name-%version

%description
CDK is a widget set developed on top of the basic curses library.  It
contains 21 ready to use widgets, some of which are text entry field,
scrolling list, selection list, alphalist, pull-down menu, radio list,
viewer widget, dialog box, and many more.

%package devel
Summary: Static library, header files, and development documentation for CDK.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
Static library, header files, and development documentation for CDK.

%prep
%setup -q -n %name-%version-%snapshot
%patch0 -p1

%build
%configure --with-warnings
%__make cdklib cdkshlib

%install
rm -rf %buildroot
%__make install installCDKSHLibrary \
	DESTDIR=%buildroot \
	DOCUMENT_DIR=%buildroot%_docdir/%name-%version
/sbin/ldconfig -n %buildroot%_libdir

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc CHANGES EXPANDING NOTES README TODO COPYING
%attr(755,root,root) %_libdir/lib*.so.*

%files devel
%defattr(-,root,root)
%doc examples demos
%attr(755,root,root) %_libdir/lib*.so
%_libdir/lib*.a
%_includedir/*
%_mandir/man3/*

%changelog
* Mon Jun 30 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 5.0-owl4
- Dropped the deprecated PreReq tag for /sbin/ldconfig.
- Added /sbin/ldconfig to the build requirements.

* Thu Mar 30 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 5.0-owl3
- Added a call to ldconfig(8) in the %%install section to create all necessary
symbolic links for libraries.
- Removed a redundant ".*" wildcard at %%files section.

* Thu Sep 22 2005 Solar Designer <solar-at-owl.openwall.com> 5.0-owl2
- Patched temporary file handling issues in headers.sh and demos/rolodex.c;
many more remain under cli/ but we are not packaging that.
- configure --with-warnings instead of adding -Wall to %optflags.
- Miscellaneous spec file updates.

* Mon Sep 19 2005 Michail Litvak <mci-at-owl.openwall.com> 5.0-owl1
- Initial packaging for Owl.

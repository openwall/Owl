# $Id: Owl/packages/gpm/gpm.spec,v 1.16 2004/09/10 07:23:53 galaxy Exp $

# This defines the library version that this package builds.
%define LIBVER 1.18.0
%define BUILD_GPM_ROOT 0

Summary: A mouse server for the Linux console.
Name: gpm
Version: 1.19.6
Release: owl3
License: GPL
Group: System Environment/Daemons
Source0: ftp://arcana.linux.it/pub/gpm/%name-%version.tar.bz2
Source1: gpm.init
Patch0: gpm-1.19.6-rh-no-ps.diff
Patch1: gpm-1.19.6-rh-owl-socket-mode.diff
Patch2: gpm-1.19.6-rh-gpm-root.diff
Patch3: gpm-1.19.6-owl-gpm-root.diff
Patch4: gpm-1.19.6-owl-liblow.diff
Patch5: gpm-1.19.6-owl-tmp.diff
Patch6: gpm-1.19.6-owl-warnings.diff
Patch7: gpm-1.19.6-owl-doc-mkinstalldirs.diff
Patch8: gpm-1.19.6-owl-info.diff
PreReq: /sbin/chkconfig, /sbin/ldconfig, /sbin/install-info
BuildRequires: bison
BuildRoot: /override/%name-%version

%description
gpm provides mouse support to text-based Linux applications as well as
console cut-and-paste operations using the mouse.

%package devel
Summary: Libraries and header files for developing mouse driven programs.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
The gpm-devel package contains the libraries and header files needed
for the development of mouse driven programs for the console.

%if %BUILD_GPM_ROOT
%package root
Summary: A mouse server add-on which draws pop-up menus on the console.
Group: System Environment/Daemons
Requires: %name = %version-%release

%description root
The gpm-root program allows pop-up menus to appear on a text console
at the click of a mouse button.
%endif

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
%configure
make CFLAGS="" CPPFLAGS=""

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%_sysconfdir

%makeinstall

install -m 644 doc/gpm-root.1 $RPM_BUILD_ROOT%_mandir/man1/
install -m 644 conf/gpm-root.conf $RPM_BUILD_ROOT%_sysconfdir/

cd $RPM_BUILD_ROOT

chmod +x .%_libdir/libgpm.so.%LIBVER
ln -sf libgpm.so.%LIBVER .%_libdir/libgpm.so

mkdir -p .%_sysconfdir/rc.d/init.d
install -m 755 $RPM_SOURCE_DIR/gpm.init .%_sysconfdir/rc.d/init.d/gpm

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot/etc/gpm-root.conf
rm %buildroot%_bindir/disable-paste
rm %buildroot%_sbindir/gpm-root
rm %buildroot%_mandir/man1/gpm-root.1*
rm %buildroot%_mandir/man1/mouse-test.1*
rm %buildroot%_mandir/man7/gpm-types.7*

%pre
rm -f /var/run/gpm.restart
if [ $1 -ge 2 ]; then
	/etc/rc.d/init.d/gpm status && touch /var/run/gpm.restart || :
	/etc/rc.d/init.d/gpm stop || :
fi

%post
if [ $1 -eq 1 ]; then
	/sbin/chkconfig --add gpm
fi
if [ -f /var/run/gpm.restart ]; then
	/etc/rc.d/init.d/gpm start
fi
rm -f /var/run/gpm.restart
/sbin/ldconfig
/sbin/install-info %_infodir/gpm.info.gz %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gpm.info.gz %_infodir/dir
	/etc/rc.d/init.d/gpm stop || :
	/sbin/chkconfig --del gpm
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%_sbindir/gpm
%_bindir/mev
%_infodir/gpm.info*
%_mandir/man1/mev.1*
%_mandir/man8/gpm.8*
%_libdir/libgpm.so.%LIBVER
%config %_sysconfdir/rc.d/init.d/gpm

%files devel
%defattr(-,root,root)
%_includedir/*
%_libdir/libgpm.a
%_libdir/libgpm.so

%if %BUILD_GPM_ROOT
%files root
%defattr(-,root,root)
%config %_sysconfdir/gpm-root.conf
%_sbindir/gpm-root
%_mandir/man1/gpm-root.1*
%endif

%changelog
* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com> 1.19.6-owl3
- Deal with info dir entries such that the menu looks pretty.

* Sun Feb 03 2002 Michail Litvak <mci@owl.openwall.com>
- Fix source URL
- Enforce our new spec file conventions

* Mon Nov 05 2001 Solar Designer <solar@owl.openwall.com>
- /etc/init.d -> /etc/rc.d/init.d for consistency.

* Sat Oct 06 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 1.19.6.
- Dropped hltest, t-mouse.el* (gpm itself is broken enough).

* Wed Jun 27 2001 Solar Designer <solar@owl.openwall.com>
- Disabled packaging gpm-root by default.

* Tue Jun 26 2001 Solar Designer <solar@owl.openwall.com>
- Moved gpm-root to a separate subpackage.
- Disabled support for ~/.gpm-root because of too many security issues
with this feature, updated the documentation accordingly.
- Fixed many gpm-root reliability bugs including the format string bug
reported by Colin Phipps to Debian (http://bugs.debian.org/102031) and
several other bugs which were about as bad.

* Sun May 27 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- hack to avoid double use of $RPM_OPT_FLAGS

* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- Updated the patches for fail-closeness in many cases.
- Re-generate gpm-root.c at build time, to avoid maintaining two patches.
- /tmp fixes in the documentation (don't suggest bad practices).
- More startup script cleanups.
- Restart after package upgrades in an owl-startup compatible way.

* Fri Jan 05 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import mktemp patch from Immunix, fix strncpy

* Sun Dec 24 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

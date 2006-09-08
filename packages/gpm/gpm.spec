# $Owl: Owl/packages/gpm/gpm.spec,v 1.30 2006/09/08 12:48:14 galaxy Exp $

%define BUILD_GPM_ROOT 0

Summary: A mouse server for the Linux console.
Name: gpm
Version: 1.20.1
Release: owl2
License: GPL
Group: System Environment/Daemons
Source0: http://ftp.schottelius.org/pub/linux/gpm/%name-%version.tar.bz2
Source1: gpm.init
Patch0: gpm-1.20.1-rh-owl-socket-mode.diff
Patch1: gpm-1.20.1-owl-gpm-root.diff
Patch2: gpm-1.20.1-owl-liblow.diff
Patch3: gpm-1.20.1-owl-tmp.diff
Patch4: gpm-1.20.1-owl-warnings.diff
Patch5: gpm-1.19.6-owl-info.diff
Patch6: gpm-1.20.1-owl-autoconf.diff
Patch7: gpm-1.20.1-owl-broken-headers.diff
PreReq: /sbin/chkconfig, /sbin/ldconfig, /sbin/install-info
BuildRequires: sed, gawk, texinfo, bison, ncurses-devel, automake, autoconf
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

%build
rm acconfig.h
autoreconf -fis
%configure
%__make CFLAGS="" CXXFLAGS=""

%install
rm -rf %buildroot
mkdir -p %buildroot%_sysconfdir

%makeinstall

install -m 644 doc/gpm-root.1 %buildroot%_mandir/man1/
install -m 644 conf/gpm-root.conf %buildroot%_sysconfdir

cd %buildroot

chmod +x .%_libdir/libgpm.so.*
ldconfig -n .%_libdir

mkdir -p .%_sysconfdir/rc.d/init.d
install -m 755 %_sourcedir/gpm.init .%_sysconfdir/rc.d/init.d/gpm

# create ghost files
touch %buildroot%_sysconfdir/gpm-{syn,twiddler}.conf
chmod 0644 %buildroot%_sysconfdir/gpm-{syn,twiddler}.conf

# Remove unpackaged files
rm %buildroot%_bindir/disable-paste
rm %buildroot%_bindir/hltest
rm %buildroot%_bindir/mouse-test
rm %buildroot%_mandir/man1/mouse-test.1*
rm %buildroot%_mandir/man7/gpm-types.7*
%if !%BUILD_GPM_ROOT
rm %buildroot/etc/gpm-root.conf
rm %buildroot%_sbindir/gpm-root
rm %buildroot%_mandir/man1/gpm-root.1*
%endif

%pre
rm -f /var/run/gpm.restart
if [ $1 -ge 2 ]; then
	%_sysconfdir/rc.d/init.d/gpm status && touch /var/run/gpm.restart || :
	%_sysconfdir/rc.d/init.d/gpm stop || :
fi

%post
if [ $1 -eq 1 ]; then
	/sbin/chkconfig --add gpm
fi
if [ -f /var/run/gpm.restart ]; then
	%_sysconfdir/rc.d/init.d/gpm start
fi
rm -f /var/run/gpm.restart
/sbin/ldconfig
/sbin/install-info %_infodir/gpm.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gpm.info %_infodir/dir
	%_sysconfdir/rc.d/init.d/gpm stop || :
	/sbin/chkconfig --del gpm
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,0755)
%doc doc/FAQ doc/README.* conf/gpm-syn.conf conf/gpm-twiddler.conf
%_sbindir/gpm
%_bindir/mev
%_infodir/gpm.info*
%_mandir/man1/mev.1*
%_mandir/man8/gpm.8*
%_libdir/libgpm.so.*
%config %_sysconfdir/rc.d/init.d/gpm
%config %ghost %_sysconfdir/gpm-syn.conf
%config %ghost %_sysconfdir/gpm-twiddler.conf

%files devel
%defattr(-,root,root)
%_includedir/*
%_libdir/libgpm.a
%_libdir/libgpm.so

%if %BUILD_GPM_ROOT
%files root
%defattr(-,root,root,0755)
%config %_sysconfdir/gpm-root.conf
%_sbindir/gpm-root
%_mandir/man1/gpm-root.1*
%endif

%changelog
* Fri Sep 08 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.20.1-owl2
- Reverted back the change to %%__make since Makefile uses CFLAGS and
CXXFLAGS from the environment and RPM's %%configure exports these variables.

* Sun Sep 03 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.20.1-owl1
- Updated to 1.20.1.
- Re-generated patches.
- Added sample config files for Synaptics and Twiddler (although Syn/PS2
seems to be broken).
- Used %%_sysconfdir instead /etc in the spec file since GPM honors
the --sysconfdir configure option.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.19.6-owl6
- Corrected info files installation.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.19.6-owl5
- Added libgpm.so.1 to the list of packaged files since it's created
by ldconfig anyway, but now we have a track where this file comes from.
- Added a patch to deal with "label at end of compound statement" issue.

* Tue Nov 02 2004 Solar Designer <solar-at-owl.openwall.com> 1.19.6-owl4
- Remove unpackaged files.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 1.19.6-owl3
- Deal with info dir entries such that the menu looks pretty.

* Sun Feb 03 2002 Michail Litvak <mci-at-owl.openwall.com>
- Fix source URL
- Enforce our new spec file conventions

* Mon Nov 05 2001 Solar Designer <solar-at-owl.openwall.com>
- /etc/init.d -> /etc/rc.d/init.d for consistency.

* Sat Oct 06 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 1.19.6.
- Dropped hltest, t-mouse.el* (gpm itself is broken enough).

* Wed Jun 27 2001 Solar Designer <solar-at-owl.openwall.com>
- Disabled packaging gpm-root by default.

* Tue Jun 26 2001 Solar Designer <solar-at-owl.openwall.com>
- Moved gpm-root to a separate subpackage.
- Disabled support for ~/.gpm-root because of too many security issues
with this feature, updated the documentation accordingly.
- Fixed many gpm-root reliability bugs including the format string bug
reported by Colin Phipps to Debian (http://bugs.debian.org/102031) and
several other bugs which were about as bad.

* Sun May 27 2001 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- hack to avoid double use of $RPM_OPT_FLAGS

* Sat Jan 06 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated the patches for fail-closeness in many cases.
- Re-generate gpm-root.c at build time, to avoid maintaining two patches.
- /tmp fixes in the documentation (don't suggest bad practices).
- More startup script cleanups.
- Restart after package upgrades in an owl-startup compatible way.

* Fri Jan 05 2001 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import mktemp patch from Immunix, fix strncpy

* Sun Dec 24 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH

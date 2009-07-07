# $Owl: Owl/packages/chkconfig/chkconfig.spec,v 1.21 2009/07/07 21:31:55 mci Exp $

%define BUILD_NTSYSV 0
%define INSTALL_ALTERNATIVES 1

Summary: A system tool for maintaining the /etc/rc.d/rc*.d hierarchy.
Name: chkconfig
Version: 1.3.38
Release: owl1
License: GPL
Group: System Environment/Base
Source: %name-%version.tar.bz2
Patch0: chkconfig-1.3.38-owl-fixes.diff
Patch1: chkconfig-1.3.38-owl-no-ntsysv.diff
BuildRequires: gettext, glibc >= 0:2.2
BuildRoot: /override/%name-%version

%description
chkconfig is a basic system utility.  It updates and queries runlevel
information for system services.  chkconfig manipulates the numerous
symbolic links in /etc/rc.d/rc*.d to relieve system administrators of
some of the drudgery of manually editing the symbolic links.

%if %BUILD_NTSYSV
%package -n ntsysv
Summary: A tool to set the stop/start of system services in a runlevel.
Group: System Environment/Base

%description -n ntsysv
ntsysv provides a simple interface for setting which system services
are started or stopped in various runlevels (instead of directly
manipulating the numerous symbolic links in /etc/rc.d/rc*.d).  Unless
you specify a runlevel or runlevels on the command line (see the man
page), ntsysv configures the current runlevel.
%endif

%prep
%setup -q
%patch0 -p1
%if !%BUILD_NTSYSV
%patch1 -p1
%endif

%build
%if %BUILD_NTSYSV
%ifarch sparc sparcv9
LIBMHACK=-lm
%endif
%endif

%__make \
	CC="%__cc" \
	CFLAGS="%optflags -Wall -D_GNU_SOURCE" \
	LIBMHACK="$LIBMHACK"

%install
rm -rf %buildroot
%__make install \
	DESTDIR="%buildroot" \
	BINDIR="/sbin" \
	USRSBINDIR="%_sbindir" \
	MANDIR="%_mandir" \
	ALTDIR="%_var/lib/alternatives" \
	ALTDATADIR="/etc/alternatives"

mkdir -p %buildroot/etc/rc.d/init.d
ln -s rc.d/init.d %buildroot/etc/init.d
for n in 0 1 2 3 4 5 6; do
	mkdir -p %buildroot/etc/rc.d/rc${n}.d
	ln -s rc.d/rc${n}.d %buildroot/etc/rc${n}.d
done

# Remove unpackaged files
%if !%INSTALL_ALTERNATIVES
rm %buildroot%_sbindir/alternatives
rm %buildroot%_mandir/man?/*alternatives.*
%endif
%if !%BUILD_NTSYSV
rm %buildroot%_mandir/man?/ntsysv.*
%endif

%find_lang %name

%files -f %name.lang
%defattr(-,root,root)
/sbin/chkconfig
/etc/init.d
/etc/rc.d/init.d
/etc/rc[0-6].d
/etc/rc.d/rc[0-6].d
%_mandir/*/chkconfig*

%if %INSTALL_ALTERNATIVES
%dir /etc/alternatives
%dir %_var/lib/alternatives
%_sbindir/update-alternatives
%_sbindir/alternatives
%_mandir/man?/*alternatives.*
%endif

%if %BUILD_NTSYSV
%files -n ntsysv
%defattr(-,root,root)
%_sbindir/ntsysv
%_mandir/man?/ntsysv.*
%endif

%changelog
* Tue Jul 07 2009 Michail Litvak <mci-at-owl.openwall.com> 1.3.38-owl1
- Updated to 1.3.38.

* Tue Jun 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.3.29-owl1
- Updated to 1.3.29.

* Tue Apr 04 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.3.25-owl2
- Package update-alternatives manpage.

* Fri Dec 23 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.3.25-owl1
- Updated to 1.3.25.
- Cleaned up chkconfig code a bit.
- Enabled packaging of alternatives by default.

* Fri Jan 07 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.3.9-owl2
- Used %%__cc macro and configured build more correctly.
- Clean up the spec.

* Fri Feb 06 2004 Michail Litvak <mci-at-owl.openwall.com> 1.3.9-owl1
- 1.3.9

* Thu Jan 24 2002 Solar Designer <solar-at-owl.openwall.com> 1.2.16-owl1
- Enforce our new spec file conventions.

* Sat Sep 23 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import spec from RH
- disable ntsysv by default

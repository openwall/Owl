# $Id: Owl/packages/chkconfig/chkconfig.spec,v 1.10 2005/01/12 15:44:43 galaxy Exp $

%define BUILD_NTSYSV 0
%define INSTALL_ALTERNATIVES 0

Summary: A system tool for maintaining the /etc/rc.d/rc*.d hierarchy.
Name: chkconfig
Version: 1.3.9
Release: owl2
License: GPL
Group: System Environment/Base
Source: ftp://ftp.redhat.com/pub/redhat/code/chkconfig/%name-%version.tar.gz
Patch0: chkconfig-1.3.9-owl-xinetd.d-check.diff
Patch1: chkconfig-1.3.9-owl-no-ntsysv.diff
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
    CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" \
    LIBMHACK="$LIBMHACK" \

%install
rm -rf %buildroot
%__make install \
    instroot="%buildroot" \
    BINDIR="/sbin" \
    USRSBINDIR="%_sbindir" \
    MANDIR="%_mandir" \
    ALTDIR="%_var/%_lib/alternatives" \
    ALTDATADIR="%_sysconfdir/alternatives"

mkdir -p %buildroot%_sysconfdir/rc.d/init.d
ln -s rc.d/init.d %buildroot%_sysconfdir/init.d
for n in 0 1 2 3 4 5 6; do
	mkdir -p %buildroot%_sysconfdir/rc.d/rc${n}.d
	ln -s rc.d/rc${n}.d %buildroot%_sysconfdir/rc${n}.d
done

# Remove unpackaged files
%if !%INSTALL_ALTERNATIVES
rm %buildroot%_sbindir/alternatives
rm %buildroot%_mandir/man8/alternatives.8*
%endif
%if !%BUILD_NTSYSV
rm %buildroot%_mandir/man8/ntsysv.8*
%endif

%find_lang %name

%files -f %name.lang
%defattr(-,root,root)
/sbin/chkconfig
%_sysconfdir/init.d
%_sysconfdir/rc.d/init.d
%_sysconfdir/rc[0-6].d
%_sysconfdir/rc.d/rc[0-6].d
%_mandir/*/chkconfig*

%if %INSTALL_ALTERNATIVES
%dir %_sysconfdir/alternatives
%dir %_var/%_lib/alternatives
%_sbindir/update-alternatives
%_sbindir/alternatives
%_mandir/*/alternatives*
%endif

%if %BUILD_NTSYSV
%files -n ntsysv
%defattr(-,root,root)
%_sbindir/ntsysv
%_mandir/*/ntsysv.8*
%endif

%changelog
* Fri Jan 07 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 1.3.9-owl2
- Used %__cc macro and configured build more correctly.
- Clean up the spec.

* Fri Feb 06 2004 Michail Litvak <mci@owl.openwall.com> 1.3.9-owl1
- 1.3.9

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com> 1.2.16-owl1
- Enforce our new spec file conventions.

* Sat Sep 23 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
- disable ntsysv by default

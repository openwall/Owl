# $Id: Owl/packages/chkconfig/chkconfig.spec,v 1.4 2003/10/29 18:40:33 solar Exp $

%define BUILD_NTSYSV 0

Summary: A system tool for maintaining the /etc/rc.d/rc*.d hierarchy.
Name: chkconfig
Version: 1.2.16
Release: owl1
License: GPL
Group: System Environment/Base
Source: ftp://ftp.redhat.com/pub/redhat/code/chkconfig/%name-%version.tar.gz
Patch0: chkconfig-1.2.16-owl-xinetd.d-check.diff
Patch1: chkconfig-1.2.16-owl-no-ntsysv.diff
BuildRoot: /override/%name-%version

%description
Chkconfig is a basic system utility.  It updates and queries runlevel
information for system services.  Chkconfig manipulates the numerous
symbolic links in /etc/rc.d/rc*.d to relieve system administrators of
some of the drudgery of manually editing the symbolic links.

%if %BUILD_NTSYSV
%package -n ntsysv
Summary: A tool to set the stop/start of system services in a runlevel.
Group: System Environment/Base

%description -n ntsysv
Ntsysv provides a simple interface for setting which system services
are started or stopped in various runlevels (instead of directly
manipulating the numerous symbolic links in /etc/rc.d/rc*.d). Unless
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

make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" LIBMHACK=$LIBMHACK

%install
rm -rf $RPM_BUILD_ROOT
make instroot=$RPM_BUILD_ROOT MANDIR=%_mandir install

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
ln -s rc.d/init.d $RPM_BUILD_ROOT/etc/init.d
for n in 0 1 2 3 4 5 6; do
	mkdir -p $RPM_BUILD_ROOT/etc/rc.d/rc${n}.d
	ln -s rc.d/rc${n}.d $RPM_BUILD_ROOT/etc/rc${n}.d
done

%files
%defattr(-,root,root)
/sbin/chkconfig
/etc/init.d
/etc/rc.d/init.d
/etc/rc[0-6].d
/etc/rc.d/rc[0-6].d
%_mandir/*/chkconfig*
/usr/share/locale/*/LC_MESSAGES/chkconfig.mo

%if %BUILD_NTSYSV
%files -n ntsysv
%defattr(-,root,root)
/usr/sbin/ntsysv
%_mandir/*/ntsysv.8*
%endif

%changelog
* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com> 1.2.16-owl1
- Enforce our new spec file conventions.

* Sat Sep 23 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
- disable ntsysv by default

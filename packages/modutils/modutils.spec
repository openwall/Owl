# $Id: Owl/packages/modutils/modutils.spec,v 1.9 2002/02/06 18:45:35 solar Exp $

Summary: Kernel module utilities.
Name: modutils
Version: 2.3.21
Release: owl1
License: GPL
Group: System Environment/Kernel
Source: ftp://ftp.kernel.org/pub/linux/utils/kernel/modutils/v2.3/modutils-%{version}.tar.gz
Patch0: modutils-2.3.17-owl-alias.diff
Patch1: modutils-2.3.17-rh-systemmap.diff
PreReq: /sbin/chkconfig
Obsoletes: modules
BuildRoot: /override/%{name}-%{version}

%description
The modutils package includes the various programs needed for automatic
loading and unloading of modules under 2.2 and later kernels as well as
other module management programs.  Examples of loaded and unloaded
modules are device drivers and filesystems, as well as some other things.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%ifarch sparcv9
%define _target_platform sparc-%{_vendor}-%{_target_os}
%endif
%configure --disable-compat-2-0 --disable-kerneld --enable-insmod-static \
	--exec_prefix=/
make dep all

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
%makeinstall sbindir=$RPM_BUILD_ROOT%{_sbindir}

rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/{kdstat,kerneld}.8

# security hole, works poorly anyway
rm -f $RPM_BUILD_ROOT/sbin/request-route
find $RPM_BUILD_ROOT/sbin/ -type l -a -name '*.static' -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x /etc/rc.d/init.d/kerneld ]; then
	/sbin/chkconfig --del kerneld
fi
if [ -f /etc/conf.modules -a ! -f /etc/modules.conf ]; then
	mv -f /etc/conf.modules /etc/modules.conf
fi

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/*/*

%changelog
* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Wed Nov 22 2000 Solar Designer <solar@owl.openwall.com>
- v2.3.21

* Tue Nov 21 2000 Solar Designer <solar@owl.openwall.com>
- Added a patch by Andreas Hasenack of Conectiva to fix a typo in the
recent security fix to modprobe.c.

* Fri Nov 17 2000 Solar Designer <solar@owl.openwall.com>
- v2.3.20
- Pass plain sparc- target to configure when building for sparcv9, to
allow for the use of sparcv9 optflags while not confusing configure.

* Wed Oct 25 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- v2.3.19

* Wed Oct 18 2000 Solar Designer <solar@owl.openwall.com>
- Removed /etc/cron.d/kmod

* Sun Oct 01 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
- fix aliases
- v2.3.17

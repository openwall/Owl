# $Id: Owl/packages/modutils/modutils.spec,v 1.19 2004/11/23 22:40:47 mci Exp $

Summary: Kernel module utilities.
Name: modutils
Version: 2.4.27
Release: owl1
License: GPL
Group: System Environment/Kernel
Source: ftp://ftp.kernel.org/pub/linux/utils/kernel/modutils/v2.4/modutils-%version.tar.bz2
Patch0: modutils-2.4.16-alt-GPL.diff
Patch1: modutils-2.4.16-alt-modprobe-bL.diff
Patch2: modutils-2.4.27-alt-owl-aliases.diff
Patch3: modutils-2.4.16-rh-owl-syms.diff
Patch4: modutils-2.4.27-owl-warnings.diff
PreReq: /sbin/chkconfig
Obsoletes: modules
BuildRoot: /override/%name-%version

%description
The modutils package includes the various programs needed for automatic
loading and unloading of modules under 2.2 and later kernels as well as
other module management programs.  Examples of loaded and unloaded
modules are device drivers and filesystems, as well as some other things.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%{expand:%%define optflags %optflags -Wall}

%build
%ifarch sparcv9
%define _target_platform sparc-%_vendor-%_target_os
%endif
# Build a statically-linked version of insmod (and symlinks to it) to
# satisfy Red Hat's mkinitrd.
%configure \
	--exec_prefix=/ \
	--disable-compat-2-0 --disable-kerneld --enable-insmod-static
make dep all

%install
rm -rf %buildroot
mkdir -p %buildroot/sbin
%makeinstall sbindir=%buildroot/sbin

%post
if [ -x /etc/rc.d/init.d/kerneld ]; then
	/sbin/chkconfig --del kerneld
fi
if [ -f /etc/conf.modules -a ! -f /etc/modules.conf ]; then
	mv -f /etc/conf.modules /etc/modules.conf
fi

%files
%defattr(-,root,root)
%doc README CREDITS TODO ChangeLog example/kallsyms.c include/kallsyms.h
/sbin/*
%_mandir/*/*

%changelog
* Fri Nov 05 2004 Solar Designer <solar@owl.openwall.com> 2.4.27-owl1
- Fixed two new compiler warnings.

* Thu Oct 14 2004 Maxim Timofeyev <tma@tma.spb.ru> 2.4.27-owl0
- v2.4.27
- Remove modutils-2.4.16-owl-warnings.diff
- Update alt-owl-aliases.diff

* Mon Jun 10 2002 Michail Litvak <mci@owl.openwall.com> 2.4.16-owl1
- v2.4.16
- reviewed patches, added patches from ALT
- build with -Wall

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

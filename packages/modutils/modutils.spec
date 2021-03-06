# $Owl: Owl/packages/modutils/modutils.spec,v 1.30 2014/07/12 14:09:37 galaxy Exp $

Summary: Kernel module utilities.
Name: modutils
Version: 2.4.27
Release: owl7
License: GPL
Group: System Environment/Kernel
Source0: ftp://ftp.kernel.org/pub/linux/utils/kernel/modutils/v2.4/modutils-%version.tar.bz2
%define mitver 3.1
Source1: http://www.kernel.org/pub/linux/utils/kernel/module-init-tools/module-init-tools-%mitver.tar.bz2
Patch0: modutils-2.4.27-rh-owl-syms.diff
Patch1: modutils-2.4.27-rh-versions.diff
Patch2: modutils-2.4.27-rh-showconfig.diff
Patch3: modutils-2.4.27-alt-owl-aliases.diff
Patch4: modutils-2.4.27-alt-insmod-GPL.diff
Patch5: modutils-2.4.27-alt-modprobe-bL.diff
Patch6: modutils-2.4.27-alt-depmod-prtdepend-cut_prefix.diff
Patch7: modutils-2.4.27-alt-allowable-licenses.diff
Patch8: modutils-2.4.27-alt-insmod-force_load.diff
Patch9: modutils-2.4.27-deb-alt-fixes.diff
Patch10: modutils-2.4.27-alt-warning-stderr.diff
Patch11: modutils-2.4.27-owl-warnings.diff
Patch12: module-init-tools-3.1-alt-release-memory.diff
Patch13: module-init-tools-3.1-alt-depmod-check-aliases.diff
Patch14: module-init-tools-3.1-alt-modinfo-legacy.diff
Patch15: modutils-2.4.27-alt-mit-combined.diff
Patch16: modutils-2.4.27-alt-owl-doc.diff
Requires(post,preun): chkconfig
Provides: module-init-tools = %mitver
Obsoletes: modules
BuildRequires: flex
BuildRoot: /override/%name-%version

%description
The modutils package includes the various programs needed for automatic
loading and unloading of modules under 2.2 and later kernels as well as
other module management programs.  Examples of loaded and unloaded
modules are device drivers and filesystems, as well as some other things.

%prep
%setup -q -a1
mv module-init-tools-%mitver module-init-tools
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
pushd module-init-tools
%patch12 -p1
%patch13 -p1
%patch14 -p1
popd # module-init-tools
%patch15 -p1
%patch16 -p1
bzip2 -9k ChangeLog

%{expand:%%define optflags %optflags -Wall}

%build
%ifarch sparcv9
%define _target_platform sparc-%_vendor-%_target_os
%endif

pushd module-init-tools
%configure CPPFLAGS="-D_COMBINED_MODUTILS_=1"
%__make combined 
popd # module-init-tools

# Build a statically-linked version of insmod (and symlinks to it) to
# satisfy Red Hat's mkinitrd.
%configure \
	--exec_prefix=/ \
	--disable-compat-2-0 --disable-kerneld --enable-insmod-static
%__make dep all

%install
rm -rf %buildroot
mkdir -p %buildroot/{sbin,etc}
%makeinstall sbindir=%buildroot/sbin
touch %buildroot/etc/modules.conf

%post
if [ -x /etc/rc.d/init.d/kerneld ]; then
	/sbin/chkconfig --del kerneld
fi
if [ -f /etc/conf.modules -a ! -s /etc/modules.conf ]; then
	mv -f /etc/conf.modules /etc/modules.conf
fi

%files
%defattr(-,root,root)
%doc CREDITS ChangeLog.bz2 README TODO example/kallsyms.c include/kallsyms.h
/sbin/*
%_mandir/*/*
%config(noreplace) /etc/modules.conf

%changelog
* Sun Jun 29 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.4.27-owl7
- Replaced the deprecated PreReq tag with Requires(post,preun).
- Regenerated the fixes and mit-combined patches since they were fuzzy.

* Tue Jun 05 2012 Solar Designer <solar-at-owl.openwall.com> 2.4.27-owl6
- Marked /etc/modules.conf %%config(noreplace).

* Mon Jul 26 2010 Solar Designer <solar-at-owl.openwall.com> 2.4.27-owl5
- Install an empty /etc/modules.conf to make "depmod -A" work right (otherwise
it'd always assume that the dependencies are out of date), as well as to have
the file owned by this package.

* Mon Oct 30 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.4.27-owl4
- Fixed check for verbose flag in insmod, patch from Alexander Kanevskiy.
- Imported Debian patch that fixes build with recent versions of flex and gcc.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.4.27-owl3
- Compressed ChangeLog file.

* Wed Oct 26 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.4.27-owl2
- Imported a bunch of patches from ALT's modutils-2.4.27-alt4 package,
including integrated module-init-tools for kernel 2.6.x support.

* Fri Nov 05 2004 Solar Designer <solar-at-owl.openwall.com> 2.4.27-owl1
- Fixed two new compiler warnings.

* Thu Oct 14 2004 Maxim Timofeyev <tma-at-tma.spb.ru> 2.4.27-owl0
- v2.4.27
- Remove modutils-2.4.16-owl-warnings.diff
- Update alt-owl-aliases.diff

* Mon Jun 10 2002 Michail Litvak <mci-at-owl.openwall.com> 2.4.16-owl1
- v2.4.16
- reviewed patches, added patches from ALT
- build with -Wall

* Wed Feb 06 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Wed Nov 22 2000 Solar Designer <solar-at-owl.openwall.com>
- v2.3.21

* Tue Nov 21 2000 Solar Designer <solar-at-owl.openwall.com>
- Added a patch by Andreas Hasenack of Conectiva to fix a typo in the
recent security fix to modprobe.c.

* Fri Nov 17 2000 Solar Designer <solar-at-owl.openwall.com>
- v2.3.20
- Pass plain sparc- target to configure when building for sparcv9, to
allow for the use of sparcv9 optflags while not confusing configure.

* Wed Oct 25 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- v2.3.19

* Wed Oct 18 2000 Solar Designer <solar-at-owl.openwall.com>
- Removed /etc/cron.d/kmod

* Sun Oct 01 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import spec from RH
- fix aliases
- v2.3.17

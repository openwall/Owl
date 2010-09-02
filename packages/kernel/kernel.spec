# $Owl: Owl/packages/kernel/kernel.spec,v 1.32 2010/09/02 23:18:28 solar Exp $

%{?!BUILD_MODULES: %define BUILD_MODULES 1}

Summary: The Linux kernel.
Name: kernel
Version: 2.6.18
%define ovzversion 194.11.3.el5.028stab071.3
Release: %ovzversion.owl1
License: GPLv2
Group: System Environment/Kernel
URL: http://wiki.openvz.org/Download/kernel/rhel5-testing/028stab071.3
Source0: http://www.kernel.org/pub/linux/kernel/v2.6/linux-2.6.18.tar.bz2
# Signature: http://www.kernel.org/pub/linux/kernel/v2.6/linux-2.6.18.tar.bz2.sign
Source1: dot-config-i686
Source2: dot-config-x86_64
Patch0: patch-%ovzversion-combined.bz2
# http://download.openvz.org/kernel/branches/rhel5-2.6.18-testing/028stab071.3/patches/patch-194.11.3.el5.028stab071.3-combined.gz
# Signature: http://download.openvz.org/kernel/branches/rhel5-2.6.18-testing/028stab071.3/patches/patch-194.11.3.el5.028stab071.3-combined.gz.asc
Patch1: linux-%version-%ovzversion-owl.diff
PreReq: basesystem
Provides: kernel-drm = 4.3.0
ExclusiveArch: i686 x86_64
BuildRoot: /override/%name-%version

%description
The Linux kernel with OpenVZ container-based virtualization, from OpenVZ
project's "rhel5" branch.

%package headers
Summary: The Linux kernel header files.
Group: Development/System
Obsoletes: glibc-kernheaders
Provides: glibc-kernheaders = 3.0-46

%description headers
The Linux kernel header files.

%package fake
Summary: A fake Linux kernel package for use in OpenVZ containers and the like.
Group: System Environment/Base
Provides: kernel = %version-%release, kernel-drm = 4.3.0

%description fake
A fake Linux kernel package for use in OpenVZ containers and the like to
satisfy possible dependencies of other packages.

%prep
%setup -q -n linux-%version
%patch0 -p1
%patch1 -p1
cp %_sourcedir/dot-config-%_target_cpu .config

%build
#yes '' | %__make oldconfig
%__make nonint_oldconfig
%__make bzImage
%if %BUILD_MODULES
%__make modules
%endif

%install
rm -rf %buildroot
mkdir -p %buildroot{/boot,%_includedir}

install -m 644 arch/%_arch/boot/bzImage \
	%buildroot/boot/vmlinuz-%version-%release
install -m 644 System.map \
	%buildroot/boot/System.map-%version-%release
install -m 644 .config \
	%buildroot/boot/config-%version-%release

cp -a include/{linux,asm,asm-generic,asm-%_arch} \
	%buildroot%_includedir/

%if %BUILD_MODULES
INSTALL_MOD_PATH=%buildroot %__make modules_install
%endif

# Remove possible symlinks that we're replacing with directories (or we'd
# follow the symlinks and replace files at their destination).
# Note that "asm" will remain a symlink, so we don't remove it here.
%pre headers
for f in %_includedir/{linux,asm-generic,asm-%_arch}; do
	test -L $f && rm -v $f || :
done

%files
%defattr(-,root,root)
/boot/*-%version-%release
%if %BUILD_MODULES
/lib/modules/%version-%release
# These would be symlinks to our build tree
%exclude /lib/modules/%version-%release/build
%exclude /lib/modules/%version-%release/source
%endif

%files headers
%defattr(644,root,root,755)
%_includedir/*

%files fake

%changelog
* Thu Sep 02 2010 Solar Designer <solar-at-owl.openwall.com> 2.6.18-194.11.3.el5.028stab071.3-owl1
- Updated to 2.6.18-194.11.3.el5.028stab071.3.

* Mon Aug 30 2010 Solar Designer <solar-at-owl.openwall.com> 2.6.18-194.8.1.el5.028stab070.4-owl1
- Updated to 2.6.18-194.8.1.el5.028stab070.4.
- Added most post-194.8.1 patches from Red Hat's -194.11.1.
- Fixed an Owl-specific bug in init/do_mounts.c: do_mount_root() with
root=/dev/cdrom failing to access CD drives on IDE slaves.
- Applied a variation of Kees Cook's partial fix to fs/exec.c's argv expansion:
http://www.openwall.com/lists/oss-security/2010/08/27/1
http://www.openwall.com/lists/oss-security/2010/08/30/3
- Applied upstream's fix to integer overflow flaws in ext4_ext_in_cache() and
ext4_ext_get_blocks():
http://www.openwall.com/lists/oss-security/2010/08/16/1
- Enabled CONFIG_FUSION_* and CONFIG_PCNET32 as modules.

* Wed Jul 21 2010 Solar Designer <solar-at-owl.openwall.com> 2.6.18-194.8.1.el5.028stab070.2.owl3
- Backported the AHCI vs. Marvell PATA driver co-existence fixes from 2.6.34.1,
made the corresponding messages more verbose.
- Implemented support of root=/dev/cdrom - a magic root device that corresponds
to the first CD drive with a valid filesystem (maybe of a specified type).

* Tue Jul 20 2010 Solar Designer <solar-at-owl.openwall.com> 2.6.18-194.8.1.el5.028stab070.2.owl2
- Fixed a bug in drivers/dca/Kconfig that prevented CONFIG_DCA from being set
to "y" when module support is enabled.
- Made assorted changes to the kernel configs.

* Sat Jul 17 2010 Solar Designer <solar-at-owl.openwall.com> 2.6.18-194.8.1.el5.028stab070.2.owl1
- RPM'ed the kernel in a way allowing for easy non-RPM'ed builds as well.

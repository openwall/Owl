# $Owl: Owl/packages/kernel/kernel.spec,v 1.129 2020/05/19 18:18:41 solar Exp $

%{?!BUILD_MODULES: %define BUILD_MODULES 1}

Summary: The Linux kernel.
Name: kernel
Version: 2.6.18
%define ovzversion 431.el5.028stab123.1
Release: %ovzversion.owl3
License: GPLv2
Group: System Environment/Kernel
URL: https://openvz.org/Download/kernel/rhel5/028stab122.4
Source0: linux-2.6.18.tar.xz
# Source0: http://www.kernel.org/pub/linux/kernel/v2.6/linux-2.6.18.tar.bz2
# Signature: http://www.kernel.org/pub/linux/kernel/v2.6/linux-2.6.18.tar.bz2.sign
Source1: dot-config-i686
Source2: dot-config-x86_64
Patch0: patch-%ovzversion-combined.xz
# http://download.openvz.org/kernel/branches/rhel5-2.6.18/028stab122.4/patches/patch-419.el5.028stab122.4-combined.gz
# Signature: http://download.openvz.org/kernel/branches/rhel5-2.6.18/028stab122.4/patches/patch-419.el5.028stab122.4-combined.gz.asc
Patch1: linux-%version-%ovzversion-owl.diff
Requires: basesystem
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

cp -a include/{linux,asm,asm-generic,asm-%_arch,ub} \
	%buildroot%_includedir/

%if %BUILD_MODULES
INSTALL_MOD_PATH=%buildroot %__make modules_install
%endif

# Remove possible symlinks that we're replacing with directories (or we'd
# follow the symlinks and replace files at their destination).
# Note that "asm" will remain a symlink and "ub" was never a symlink, so we
# don't remove these two here.
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
* Tue May 19 2020 Solar Designer <solar-at-owl.openwall.com> 2.6.18-431.el5.028stab123.1.owl3
- Merged the most relevant fixes from Red Hat's -436:
  - [alsa] seq: Fix use-after-free at creating a port (Denys Vlasenko) [1503379] {CVE-2017-15265}
  - [ipc] mqueue: fix a use-after-free in sys_mq_notify() (Radomir Vrbovsky) [1476123] {CVE-2017-11176}
  - [x86] fix kexec load warnings with PTI enabled (Rafael Aquini) [1576191]
  - [net] tcp: fix 0 divide in __tcp_select_window (Davide Caratti) [1488343] {CVE-2017-14106}
  - [net] tcp: initialize rcv_mss to TCP_MIN_MSS instead of 0 (Davide Caratti) [1488343] {CVE-2017-14106}
  - [x86] adjust / fix LDT handling for PTI (Rafael Aquini) [1584622]

* Thu Jun 28 2018 Solar Designer <solar-at-owl.openwall.com> 2.6.18-431.el5.028stab123.1.owl2
- Fixed a regression introduced with the previous update (to -431) where some
32-bit syscalls would fail with EFAULT on a 64-bit kernel because of improper
alignment of the newly introduced KAISER/KPTI trampoline stack.  This fix is
due to investigation and patch by Pavel Kankovsky and bug report by Chris Bopp.

* Sun May 20 2018 Solar Designer <solar-at-owl.openwall.com> 2.6.18-431.el5.028stab123.1.owl1
- Updated to 2.6.18-431.el5.028stab123.1.

* Wed Oct 18 2017 Solar Designer <solar-at-owl.openwall.com> 2.6.18-419.el5.028stab122.4.owl1
- Updated to 2.6.18-419.el5.028stab122.4.

* Mon Jun 19 2017 Solar Designer <solar-at-owl.openwall.com> 2.6.18-408.el5.028stab120.1.owl11
- On SUID/SGID exec, limit the size of argv+envp to 512 KiB and the stack size
to 10 MiB, similarly to what grsecurity did in 2012.

* Mon Jun 19 2017 Solar Designer <solar-at-owl.openwall.com> 2.6.18-408.el5.028stab120.1.owl10
- For ping sockets, use inet_sockraw_ops instead of inet_dgram_ops, with the
only difference being that the latter used udp_poll(), which upon a combination
of flags would unnecessarily compute UDP checksum.  The same bug had worse
consequences in newer upstream kernels, where it was discovered and reported by
Sasha Levin and investigated and fixed by Eric Dumazet:
http://lists.openwall.net/netdev/2017/06/03/13
http://lists.openwall.net/netdev/2017/06/03/26

* Wed Jun 07 2017 Solar Designer <solar-at-owl.openwall.com> 2.6.18-408.el5.028stab120.1.owl9
- Backported upstream reimplementation of restricted hard links, controllable
via the fs.protected_hardlinks sysctl and enabled by default, similar to what
we had as part of CONFIG_HARDEN_LINK in -ow patches and what grsecurity had as
part of CONFIG_GRKERNSEC_LINK.

* Sun Apr 02 2017 Solar Designer <solar-at-owl.openwall.com> 2.6.18-408.el5.028stab120.1.owl8
- Merged upstream fix to locking in net/ipv4/ping.c: ping_unhash().

* Wed Jan 25 2017 Solar Designer <solar-at-owl.openwall.com> 2.6.18-408.el5.028stab120.1.owl7
- Merged in a fix of use after free in the recvmmsg() exit path (CVE-2016-7117)
from Red Hat's -417.

* Sat Dec 10 2016 Solar Designer <solar-at-owl.openwall.com> 2.6.18-408.el5.028stab120.1.owl6
- Reduced CONFIG_NR_CPUS from 255 to 96 in order to mitigate the kernel package
installed size increase of the previous change (was 15 MB).  Most of the size
increase came from the .gnu.linkonce.this_module sections, which are instances
of "struct module", which in turn contains an array of size NR_CPUS of cache
line aligned reference counts (thus, NR_CPUS times 64 bytes per module).  With
our current module count, this change saves almost 9 MB.

* Sat Dec 10 2016 Solar Designer <solar-at-owl.openwall.com> 2.6.18-408.el5.028stab120.1.owl5
- Merged in Red Hat's CVE-2016-5195 "Dirty COW" fix from -416 (slightly
different from the fix included in OpenVZ's 120.3 released earlier) while also
keeping the mitigation introduced in owl4.
- In the x86_64 config, enabled CONFIG_MICROCODE=m, CONFIG_NUMA=y and many
related options, CONFIG_HUGETLB_PAGE=y, CONFIG_HUGETLBFS=y, CONFIG_I2C=m and
many sensors (similar to RHEL's), bumped up CONFIG_NR_CPUS from 32 to 255.
Tested many of these on a Dell PowerEdge R720xd with 2x E5-2660 v2 (NUMA, huge
pages, some I2C sensors, 40 logical CPUs).

* Sun Oct 23 2016 Solar Designer <solar-at-owl.openwall.com> 2.6.18-408.el5.028stab120.1.owl4
- Merged in Red Hat's fixes from -412.
- To mitigate CVE-2016-5195 "Dirty COW", take mmap_sem for writing on
MADV_DONTNEED, PTRACE_POKEDATA, PTRACE_POKETEXT, and as it happens also on
PTRACE_PEEKDATA, PTRACE_PEEKTEXT.

* Tue Aug 23 2016 Solar Designer <solar-at-owl.openwall.com> 2.6.18-408.el5.028stab120.1.owl1
- Updated to 2.6.18-408.el5.028stab120.1.
- Applied Dmitry V. Levin's patch to fix a kernel panic triggerable via the
move_pages() syscall.

* Thu Jun 11 2015 Solar Designer <solar-at-owl.openwall.com> 2.6.18-406.el5.028stab119.1.owl2
- CVE-2015-2925 fix for OpenVZ containers.

* Tue Jun 09 2015 Solar Designer <solar-at-owl.openwall.com> 2.6.18-406.el5.028stab119.1.owl1
- Updated to 2.6.18-406.el5.028stab119.1.

* Sun Dec 28 2014 Solar Designer <solar-at-owl.openwall.com> 2.6.18-400.el5.028stab117.2.owl1
- Updated to 2.6.18-400.el5.028stab117.2.

* Thu Jul 10 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.6.18-371.9.1.el5.028stab114.2.owl3
- Replaced the deprecated PreReq tag with the Plain Require tag.

* Thu Jul 10 2014 Solar Designer <solar-at-owl.openwall.com> 2.6.18-371.9.1.el5.028stab114.2.owl2
- Fixed a ping sockets bug introduced in 2.6.18-371.8.1.el5.028stab113.1.owl1,
which resulted in the ping command printing incorrect responding IP addresses.

* Mon Jul 07 2014 Solar Designer <solar-at-owl.openwall.com> 2.6.18-371.9.1.el5.028stab114.2.owl1
- Updated to 2.6.18-371.9.1.el5.028stab114.2.
- Added a hardening measure against the ptrace SYSRET vulnerability
(CVE-2014-4699), even though RHEL5 kernels are understood to be unaffected.

* Sun Jun 08 2014 Solar Designer <solar-at-owl.openwall.com> 2.6.18-371.8.1.el5.028stab113.1.owl1
- Updated to 2.6.18-371.8.1.el5.028stab113.1.
- Disabled the new option CONFIG_ARCH_RANDOM in our patch, as this option would
otherwise be forcibly enabled.  The RDRAND support code backported to RHEL 5.10
and enabled with this option suffers from the security risks discussed after
that code had been introduced into mainline (in particular, get_random_bytes()
may be less random under VMs than it was otherwise), so let's keep it disabled.
- Enabled CONFIG_CPU_FREQ* and related options like in RHEL, except that
CONFIG_X86_LONGRUN (for Transmeta CPUs) is not enabled.
- Patched many RHEL kernel bugs due to our gcc warnings (newer than what RHEL5
is normally built with).

* Sun Apr 07 2013 Solar Designer <solar-at-owl.openwall.com> 2.6.18-348.3.1.el5.028stab106.2.owl1
- Updated to 2.6.18-348.3.1.el5.028stab106.2.

* Tue Mar 19 2013 Solar Designer <solar-at-owl.openwall.com> 2.6.18-348.3.1.el5.028stab106.1.owl1
- Updated to 2.6.18-348.3.1.el5.028stab106.1.

* Fri Feb 22 2013 Solar Designer <solar-at-owl.openwall.com> 2.6.18-308.20.1.el5.028stab104.3.owl1
- Updated to 2.6.18-308.20.1.el5.028stab104.3.
- CONFIG_EFI_PARTITION=y
- CONFIG_SOUND=m with the same set of sound drivers as in RHEL5, except that
we don't enable CONFIG_SND_FM801_TEA575X_BOOL as that would bring in a video
capture subsystem, we don't enable CONFIG_SND_DYNAMIC_MINORS as it'd require
udev or similar, but we do enable CONFIG_SND_SUPPORT_OLD_API=y.

* Sat Aug 18 2012 Solar Designer <solar-at-owl.openwall.com> 2.6.18-308.11.1.el5.028stab102.1.owl1
- Updated to 2.6.18-308.11.1.el5.028stab102.1.
- Made "make menuconfig" work with new binutils (added -ltinfo).
- Support builds with CONFIG_IP_PING=n.

* Sun May 06 2012 Solar Designer <solar-at-owl.openwall.com> 2.6.18-308.4.1.el5.028stab100.2.owl1
- Updated to 2.6.18-308.4.1.el5.028stab100.2.
- Reverted the dmesg_restrict sysctl tri-state feature in favor of the approach
taken by OpenVZ as discussed at http://bugzilla.openvz.org/show_bug.cgi?id=2197
- In drivers/net/bnx2x/bnx2x_main.c, wrapped the hacks needed for building with
gcc 3.4.5 (Owl 3.0-stable) in #if __GNUC__ < 4 ... #endif.
- In fs/proc/task_mmu.c: show_map_internal(), corrected the struct mm_struct
leak on i686 that was introduced in 2.6.18-274.18.1.el5.028stab098.1.owl1.

* Sat Feb 25 2012 Solar Designer <solar-at-owl.openwall.com> 2.6.18-274.18.1.el5.028stab098.1.owl1
- Updated to 2.6.18-274.18.1.el5.028stab098.1.
- Introduced the previously missed RLIMIT_NPROC check into fs/compat.c:
compat_do_execve() (used by 32-bit program binaries on 64-bit kernel).
- Introduced protection against unintended self-read by a SUID/SGID program of
/proc/<pid>/mem and /proc/<pid>/*maps files, based on approaches taken in
recent grsecurity patches.
- Made the dmesg_restrict sysctl tri-state and container-aware.
- CONFIG_NFSD=m, CONFIG_CIFS=m, CONFIG_NET_SCHED=y, CONFIG_NET_RADIO=y and lots
of WiFi drivers as modules, CONFIG_PCCARD=m and relevant WiFi drivers.

* Wed Jan 25 2012 Solar Designer <solar-at-owl.openwall.com> 2.6.18-274.17.1.el5.028stab097.1.owl1
- Updated to 2.6.18-274.17.1.el5.028stab097.1.

* Tue Dec 27 2011 Solar Designer <solar-at-owl.openwall.com> 2.6.18-274.12.1.el5.028stab096.1.owl1
- Updated to 2.6.18-274.12.1.el5.028stab096.1.
- CONFIG_VIA_RHINE=m, CONFIG_VIA_RHINE_MMIO=y, CONFIG_VIA_RHINE_NAPI=y

* Sun Nov 27 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.18-274.7.1.el5.028stab095.1.owl1
- Updated to -274.7.1.el5.028stab095.1.  Security and bugfix update.
- Set CONFIG_PCNET32=y again as VMware emulates NIC of this type by default.

* Wed Oct 26 2011 Solar Designer <solar-at-owl.openwall.com> 2.6.18-274.3.1.el5.028stab094.3.owl3
- Discard section .eh_frame in arch/i386/kernel/vmlinux.lds.S just like it was
already being done for x86_64.

* Sun Oct 16 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.18-274.3.1.el5.028stab094.3.owl2
- Fixed compilation failures under gcc 4.6.1.

* Sun Oct 09 2011 Solar Designer <solar-at-owl.openwall.com> 2.6.18-274.3.1.el5.028stab094.3.owl1
- Updated to 2.6.18-274.3.1.el5.028stab094.3.
- Restricted permissions on /proc/slabinfo.
- Moved some OpenVZ features to modules like it is done in OpenVZ's official
kernel builds.
- Changed CONFIG_UDF_FS=y to =m.
- Changed CONFIG_BLK_DEV_CRYPTOLOOP and most CONFIG_CRYPTO_* from =y to =m.
- On x86_64, changed CONFIG_PCNET32 and CONFIG_FORCEDETH (these are some of the
100 Mbps NIC drivers) from =y to =m.  Of the 100 Mbps NIC drivers, we're
leaving only those for Intel, Realtek, and NE2000-compatible NICs built into
the kernel on x86_64 now.
- CONFIG_SCSI_AIC94XX=y, CONFIG_BLK_CPQ_CISS_DA=y (the latter was already =y on
i686, now it is =y on x86_64 as well).

* Wed Jul 27 2011 Solar Designer <solar-at-owl.openwall.com> 2.6.18-238.19.1.el5.028stab092.2.owl1
- Updated to 2.6.18-238.19.1.el5.028stab092.2.
- In kernel/sched.c, wrapped the use of sched_goidle in
#ifdef CONFIG_SCHEDSTATS ... #endif (otherwise the new revision of the code
wouldn't compile with our config).
- In drivers/net/bonding/bond_main.c, moved the body of a function to be
inlined up in the code to make this compilable by gcc 3.4.5;
set CONFIG_BONDING=m in dot-config-*.
- CONFIG_BLK_CPQ_CISS_DA=m and CONFIG_CISS_SCSI_TAPE=y in dot-config-x86_64.
- Applied a patch adding limited support for LSISAS8208ELP (PCI device id
0x0059), which provides access to individual hard drives:
http://bugs.gentoo.org/show_bug.cgi?id=325805
http://bugs.gentoo.org/attachment.cgi?id=236721
http://forums.gentoo.org/viewtopic-t-731366.html
- Moved the RLIMIT_NPROC check from set_user() to execve():
http://www.openwall.com/lists/kernel-hardening/2011/07/12/1
- In set_user(), SIGKILL the process rather than return -EAGAIN on alloc_uid()
failure (which "can't happen").

* Tue May 03 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.18-238.9.1.el5.028stab089.1-owl1
- Updated to 2.6.18-238.9.1.el5.028stab089.1.  This fixes obscure security
issues: kernel panic by unprivileged user via NFSv4 (CVE-2011-1090) and a NULL
pointer dereference in GRO code (CVE-2011-1478).  It fixes non-security issues
with page tables accounting, AMD Bulldozer boot process, OOM killer and CPU
stats bugs.  It also introduces numerous features.  More detailed description
see at:
http://wiki.openvz.org/Download/kernel/rhel5/028stab089.1
http://wiki.openvz.org/Download/kernel/rhel5/028stab085.5

* Sat Apr 02 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.18-238.5.1.el5.028stab085.3.owl1
- Updated to 2.6.18-238.5.1.el5.028stab085.3.  This fixes a kernel oops caused
by nfsd.
- Fixed a SIGSEGV of top running in Fedora 13 x86_64 container (gcc 3.4.5
inlining issue):
http://bugzilla.openvz.org/show_bug.cgi?id=1815

* Mon Mar 21 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.18-238.5.1.el5.028stab085.2.owl3
- Backported fixes for netfilter infoleaks: arp_tables (CVE-2011-1170),
ip_tables (CVE-2011-1171), ip6_tables (CVE-2011-1172), and ipt_CLUSTERIP:
http://www.openwall.com/lists/oss-security/2011/03/18/15
One must have CAP_NET_ADMIN to exploit these issues.  The default Owl
installation is vulnerable to the infoleak in ip_tables only as we neither ship
other netfilter modules nor have IPv6 enabled.

* Sat Mar 12 2011 Solar Designer <solar-at-owl.openwall.com> 2.6.18-238.5.1.el5.028stab085.2.owl2
- Disabled the eepro100 driver in favor of e100:
http://www.openwall.com/lists/owl-users/2011/03/05/3

* Fri Mar 11 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.18-238.5.1.el5.028stab085.2.owl1
- Updated to 238.5.1.el5.028stab085.2.  This fixes a bug in CFQ.

* Thu Mar 10 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.18-238.5.1.el5.028stab085.1.owl1
- Updated to 238.5.1.el5.028stab085.1.  This fixes a rare kernel panic with
sysfs virtualization, a potential livelock in dirty pages balancing,
garbage collector for AF_UNIX sockets error (CVE-2010-4249):
https://bugzilla.redhat.com/show_bug.cgi?id=657303,
exceeding the receiver's buffer limit of socket queues (CVE-2010-4251):
https://bugzilla.redhat.com/show_bug.cgi?id=656756
- Fixed build failure with CONFIG_IPV6=n (default in Owl).
- Fixed build failure with gcc 3.4.5 (issue with inline functions).
- Fixed bug with fragmented ICMP sockets (Owl-specific issue).  Reported
by Piotr Meyer.

* Thu Feb 10 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.18-238.1.1.el5.028stab084.3.owl1
- Updated to 2.6.18-238.1.1.el5.028stab084.3.  It contains
"fix for optimized kmem accounting."

* Wed Feb 09 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.18-238.1.1.el5.028stab084.2.owl1
- Updated to 2.6.18-238.1.1.el5.028stab084.2.  The fix for VDSO bug in
028stab084.1 was incomplete, now fixed, hopefully:
http://bugzilla.openvz.org/show_bug.cgi?id=1762
- Dropped page accounting fix from -owl patch (fixed in OpenVZ's kernel).
- CONFIG_BRIDGE=m (it also needs CONFIG_BRIDGE_NETFILTER=y,
CONFIG_NETFILTER_XT_MATCH_PHYSDEV=m, CONFIG_BRIDGE_NF_EBTABLES=n).
- CONFIG_PPP_MPPE=m, this is needed by PPTP access server.
- CONFIG_IP_NF_TARGET_ULOG=y.

* Sat Feb 05 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.18-238.1.1.el5.028stab084.1.owl2
- Updated to upstream's "fixed fix for paging accounting".  The incomplete
fix introduced with our 2011/02/04 update could have caused trouble with
32-bit x86 kernels:
http://bugzilla.openvz.org/show_bug.cgi?id=1760

* Fri Feb 04 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.18-238.1.1.el5.028stab084.1.owl1
- Updated to 2.6.18-238.1.1.el5.028stab084.1.
- Enabled VDSO on x86_64 (the actual bug is fixed in 028stab084.1).
- Combined -owl and -owl-pingsockets into -owl.
- Applied a patch fixing flooding "Uncharging too much" for non-4levels page
tables acct:
http://bugzilla.openvz.org/show_bug.cgi?id=1760

* Thu Feb 03 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.18-238.1.1.el5.028stab083.1.owl4
- Initialize ping_group_range to {1, 0} to disable the feature for
daemons that don't drop GID 0.  Suggested by Solar.

* Mon Jan 31 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.6.18-238.1.1.el5.028stab083.1.owl3
- Added ICMP socket kind.

* Sat Jan 29 2011 Solar Designer <solar-at-owl.openwall.com> 2.6.18-238.1.1.el5.028stab083.1.owl2
- Applied a patch fixing APIC driver selection on x86_64 systems with more than
8 logical CPUs (thanks to Pavel Emelyanov of OpenVZ for providing this patch).
- Disabled VDSO on x86_64 as a temporary workaround for a bug introduced in
2.6.18-238.1.1.el5.028stab083.1.

* Fri Jan 28 2011 Solar Designer <solar-at-owl.openwall.com> 2.6.18-238.1.1.el5.028stab083.1.owl1
- Updated to 2.6.18-238.1.1.el5.028stab083.1.
- Fixed an infoleak in net/core/ethtool.c: ethtool_get_regs().
This was the portion of CVE-2010-4655 affecting RHEL5 kernels.
http://www.openwall.com/lists/oss-security/2011/01/28/1
- CONFIG_PCIE_ECRC=y to match Red Hat's kernels; presumably they had enabled
this option for a reason (broken BIOSes?)
- CONFIG_PCI_IOV=y, which is indirectly required for the bnx2x driver (via what
looks like a somewhat bogus dependency in the current PCI code).
- CONFIG_SCSI_3W_SAS=y (new driver backport in RHEL 5.6).
- CONFIG_FUSION_SAS=y, also requiring CONFIG_SCSI_SAS_ATTRS=y.  On i686, also
CONFIG_FUSION_FC=y and CONFIG_SCSI_FC_ATTRS=y.  Previously, these were built
as modules.
- CONFIG_SATA_SIS=y, CONFIG_PATA_SIS=y, and CONFIG_SIS900=y (on i686) or
CONFIG_SIS900=m (on x86_64).  These were needed for at least a certain Atom CPU
based mini-server.  These chips are presumably unlikely to be seen on a 64-bit
capable system, yet this is possible.  The SATA/PATA drivers are tiny.  The NIC
driver is larger, so it's excluded from the x86_64 kernel image.
- CONFIG_BNX2X=m (also sets CONFIG_MDIO=m, CONFIG_CRYPTO_CRC32C=m, and
CONFIG_LIBCRC32C=m).
- Enabled building of old 3Com NIC drivers as modules.
- Moved the EDAC drivers to modules to avoid console flood on certain buggy
machines, as well as to reduce kernel size.
- Moved the DMA engine stuff to modules because it resulted in a boot-time
failure on at least one server type (Supermicro X8DTU/X8DTU-F motherboard)
when compiled into the kernel.

* Thu Dec 09 2010 Solar Designer <solar-at-owl.openwall.com> 2.6.18-194.26.1.el5.028stab079.1-owl2
- In the CVE-2010-4258 fix, moved the in_interrupt() check to be done before
the newly added set_fs() call.  Rationale:
http://www.openwall.com/lists/oss-security/2010/12/09/4
- Added mmap_min_addr checks into install_special_mapping() and
__bprm_mm_init().  The problem was discovered and a similar patch proposed by
Tavis Ormandy of Google Security Team:
http://www.openwall.com/lists/oss-security/2010/12/09/12
- Set the default mmap_min_addr to 98304, just like we do in our sysctl.conf.
- Merged linux-2.6-net-limit-sendto-recvfrom-iovec-total-length-to-int_max.patch
from 2.6.18-236.el5.

* Wed Dec 08 2010 Solar Designer <solar-at-owl.openwall.com> 2.6.18-194.26.1.el5.028stab079.1-owl1
- Updated to 2.6.18-194.26.1.el5.028stab079.1.
- Fixed "Dangerous interaction between clear_child_tid, set_fs(), and kernel
oopses" (CVE-2010-4258).  Problem discovered and fix proposed by Nelson Elhage
of Ksplice:
http://www.openwall.com/lists/oss-security/2010/12/02/3
http://www.openwall.com/lists/oss-security/2010/12/02/7
http://www.openwall.com/lists/oss-security/2010/12/08/4
- Merged many security-relevant patches from 2.6.18-236.el5 (mostly for
infoleaks discovered by Dan Rosenberg, as well as his patch introducing
the dmesg_restrict sysctl and CONFIG_SECURITY_DMESG_RESTRICT).
- Set CONFIG_SECURITY_DMESG_RESTRICT=y in our default configs.
- Package include/ub/, which is needed for external kernel module builds
against OpenVZ kernel headers (ub/ files are included from the "regular" linux/
header files, so even a non-OpenVZ-specific module ends up needing them).

* Fri Sep 24 2010 Solar Designer <solar-at-owl.openwall.com> 2.6.18-194.11.3.el5.028stab071.5-owl1
- Updated to 2.6.18-194.11.3.el5.028stab071.5.
- Added a fix for CVE-2010-3081 from 028stab070.5 (the same as Red Hat's
linux-2.6-misc-make-compat_alloc_user_space-incorporate-the-access_ok.patch
from their -194.11.4 kernel, but adjusted to apply on top of OpenVZ).
- Restricted permissions on /proc/kallsyms (0444 to 0400).
- Enabled building of DRBD as a module (also enabled connector and HMAC).
- Set CONFIG_FUSION_SPI=y and CONFIG_PCNET32=y (these were at =m before) to run
under VMware out of the box, but switched CONFIG_IXGBE and CONFIG_IXGB (large
10G Ethernet drivers) from =y to =m (have to fit on a 2.88 MB "floppy").
- Switched to using xz-compressed source tarball and OpenVZ patch.

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

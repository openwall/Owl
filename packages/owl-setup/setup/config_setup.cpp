#include "config.hpp"




ScriptVariable OwlInstallConfig::FdiskPath() const
{ return "/sbin/fdisk"; }

ScriptVariable OwlInstallConfig::CpPath() const
{ return "/bin/cp"; }

ScriptVariable OwlInstallConfig::PasswdPath() const
{ return "/usr/bin/passwd"; }

ScriptVariable OwlInstallConfig::WorldDir() const
{ return "/usr/src/world"; }

ScriptVariable OwlInstallConfig::MakePath() const
{ return "/usr/bin/make"; }

ScriptVariable OwlInstallConfig::MkdirPath() const
{ return "/bin/mkdir"; }

ScriptVariable OwlInstallConfig::MountPath() const
{ return "/bin/mount"; }

ScriptVariable OwlInstallConfig::UmountPath() const
{ return "/bin/umount"; }

ScriptVariable OwlInstallConfig::MkswapPath() const
{ return "/sbin/mkswap"; }

ScriptVariable OwlInstallConfig::SwaponPath() const
{ return "/sbin/swapon"; }

ScriptVariable OwlInstallConfig::SwapoffPath() const
{ return "/sbin/swapoff"; }

ScriptVariable OwlInstallConfig::EditorPath() const
{ return "/bin/vi"; }

ScriptVariable OwlInstallConfig::InstallWorldTarget() const
{ return "installworld"; }

ScriptVariable OwlInstallConfig::ProcMounts() const
{ return "/proc/mounts"; }

ScriptVariable OwlInstallConfig::ProcSwaps() const
{ return "/proc/swaps"; }

ScriptVariable OwlInstallConfig::OwlRoot() const
{ return "/"; }




void OwlInstallConfig::PkgInstalledCheckFiles(ScriptVector &vec) const
{
    vec.Clear();
    vec.AddItem("/etc/passwd");
    vec.AddItem("/bin/sh");
    vec.AddItem("/dev/tty1");
}

ScriptVariable OwlInstallConfig::RootShadowFile() const
{ return "/etc/tcb/root/shadow"; }



ScriptVariable OwlInstallConfig::MkfsPath(const ScriptVariable& fst) const
{
    return ScriptVariable("/sbin/mkfs.")+fst;
}


ScriptVariable OwlInstallConfig::KeymapFileSuffix() const
{ return "map.gz"; }

ScriptVariable OwlInstallConfig::KeymapDbPath() const
{ return "/lib/kbd/keymaps/i386"; }

ScriptVariable OwlInstallConfig::KeymapSysconf() const
{ return "/etc/sysconfig/keyboard"; }

ScriptVariable OwlInstallConfig::LoadkeysPath() const
{ return "/bin/loadkeys"; }



ScriptVariable OwlInstallConfig::ZoneinfoDbPath() const
{ return "/usr/share/zoneinfo"; }

ScriptVariable OwlInstallConfig::ZoneinfoFile() const
{ return "/etc/localtime"; }

ScriptVariable OwlInstallConfig::ZoneinfoSysconf() const
{ return "/etc/sysconfig/clock"; }





ScriptVariable OwlInstallConfig::ResolvFile() const
{ return "/etc/resolv.conf"; }

ScriptVariable OwlInstallConfig::HostsFile() const
{ return "/etc/hosts"; }

ScriptVariable OwlInstallConfig::NetworkScriptsDir() const
{ return "/etc/sysconfig/network-scripts"; }

ScriptVariable OwlInstallConfig::NetworkSysconf() const
{ return "/etc/sysconfig/network"; }



ScriptVariable OwlInstallConfig::DefaultKernel() const
{ return "/boot/bzImage"; }

ScriptVariable OwlInstallConfig::DefaultKernelMap() const
{ return "/boot/System.map"; }

ScriptVariable OwlInstallConfig::TargetKernel() const
{ return "/boot/bzImage"; }

ScriptVariable OwlInstallConfig::TargetKernelMap() const
{ return "/boot/System.map"; }

ScriptVariable OwlInstallConfig::LiloconfFile() const
{ return "/etc/lilo.conf"; }

ScriptVariable OwlInstallConfig::LiloPath() const
{ return "/sbin/lilo"; }

ScriptVariable OwlInstallConfig::LiloMap() const
{ return "/bool/map"; }




ScriptVariable OwlInstallConfig::FstabFile() const
{ return "/etc/fstab"; }

ScriptVariable OwlInstallConfig::DefaultFstabContent() const
{
    return
#if 0
        "proc\t/proc\tproc\tgid=110\t0 0\n"
        "devpts\t/dev/pts\tdevpts\tgid=5,mode=620\t0 0\n"
        "/dev/cdrom\t/mnt/cdrom\tiso9660\tnoauto,nosuid,owner,ro\t0 0\n"
        "/dev/floppy\t/mnt/floppy\text2\tnoauto,nosuid,owner\t0 0\n";
#endif
        "";
}


OwlInstallConfig *the_config = 0;

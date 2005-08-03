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
{ return "/owl"; }




void OwlInstallConfig::PkgInstalledCheckFiles(ScriptVector &vec) const
{
    vec.Clear();
    vec.AddItem("/owl/etc/passwd");
    vec.AddItem("/owl/bin/sh");
    vec.AddItem("/owl/dev/tty1");
}

ScriptVariable OwlInstallConfig::RootShadowFile() const
{ return "/owl/etc/tcb/root/shadow"; }



ScriptVariable OwlInstallConfig::MkfsPath(const ScriptVariable& fst) const
{
    return ScriptVariable("/sbin/mkfs.")+fst;
}


ScriptVariable OwlInstallConfig::KeymapFileSuffix() const
{ return "map.gz"; }

ScriptVariable OwlInstallConfig::KeymapDbPath() const
{ return "/lib/kbd/keymaps/i386"; }

ScriptVariable OwlInstallConfig::KeymapSysconf() const
{ return "/owl/etc/sysconfig/keyboard"; }

ScriptVariable OwlInstallConfig::LoadkeysPath() const
{ return "/bin/loadkeys"; }



ScriptVariable OwlInstallConfig::ZoneinfoDbPath() const
{ return "/usr/share/zoneinfo"; }

ScriptVariable OwlInstallConfig::ZoneinfoSysconf() const
{ return "/owl/etc/localtime"; }





ScriptVariable OwlInstallConfig::ResolvFile() const
{ return "/owl/etc/resolv.conf"; }

ScriptVariable OwlInstallConfig::HostsFile() const
{ return "/owl/etc/hosts"; }

ScriptVariable OwlInstallConfig::NetworkScriptsDir() const
{ return "/owl/etc/sysconfig/network-scripts"; }

ScriptVariable OwlInstallConfig::NetworkSysconf() const
{ return "/owl/etc/sysconfig/network"; }



ScriptVariable OwlInstallConfig::DefaultKernel() const
{ return "/boot/bzImage"; }

ScriptVariable OwlInstallConfig::DefaultKernelMap() const
{ return "/boot/System.map"; }

ScriptVariable OwlInstallConfig::TargetKernel() const
{ return "/owl/boot/bzImage"; }

ScriptVariable OwlInstallConfig::TargetKernelMap() const
{ return "/owl/boot/System.map"; }

ScriptVariable OwlInstallConfig::LiloconfFile() const
{ return "/owl/etc/lilo.conf"; }

ScriptVariable OwlInstallConfig::LiloPath() const
{ return "/sbin/lilo"; }

ScriptVariable OwlInstallConfig::LiloMap() const
{ return "/owl/boot/map"; }




ScriptVariable OwlInstallConfig::FstabFile() const
{ return "/owl/etc/fstab"; }

ScriptVariable OwlInstallConfig::DefaultFstabContent() const
{
    return
        "proc\t/proc\tproc\tgid=110\t0 0\n"
        "devpts\t/dev/pts\tdevpts\tgid=5,mode=620\t0 0\n"
        "/dev/cdrom\t/mnt/cdrom\tiso9660\tnoauto,nosuid,owner,ro\t0 0\n"
        "/dev/floppy\t/mnt/floppy\text2\tnoauto,nosuid,owner\t0 0\n";
}


OwlInstallConfig *the_config = 0;

#include "config.hpp"




ScriptVariable OwlInstallConfig::FdiskPath() const
{ return "/sbin/fdisk"; }

ScriptVariable OwlInstallConfig::CpPath() const
{ return "/bin/cp"; }

ScriptVariable OwlInstallConfig::SuPath() const
{ return "/bin/su"; }

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
{ return root == "" ? ScriptVariable("/") : root; }




void OwlInstallConfig::PkgInstalledCheckFiles(ScriptVector &vec) const
{
    vec.Clear();
    vec.AddItem(root+"/etc/passwd");
    vec.AddItem(root+"/bin/sh");
    vec.AddItem(root+"/dev/tty1");
}

ScriptVariable OwlInstallConfig::RootShadowFile() const
{ return root+"/etc/tcb/root/shadow"; }

ScriptVariable OwlInstallConfig::OwlInstallCdLabel() const
{ return "/.Owl-CD-ROM"; }

ScriptVariable OwlInstallConfig::MkfsPath(const ScriptVariable& fst) const
{
    return ScriptVariable("/sbin/mkfs.")+fst;
}


ScriptVariable OwlInstallConfig::KeymapFileSuffix() const
{ return "map.gz"; }

ScriptVariable OwlInstallConfig::KeymapDbPath() const
{ return "/lib/kbd/keymaps/i386"; }

ScriptVariable OwlInstallConfig::KeymapSysconf() const
{ return root+"/etc/sysconfig/keyboard"; }

ScriptVariable OwlInstallConfig::LoadkeysPath() const
{ return "/bin/loadkeys"; }



ScriptVariable OwlInstallConfig::ZoneinfoDbPath() const
{ return "/usr/share/zoneinfo"; }

ScriptVariable OwlInstallConfig::ZoneinfoFile() const
{ return root+"/etc/localtime"; }

ScriptVariable OwlInstallConfig::ZoneinfoSysconf() const
{ return root+"/etc/sysconfig/clock"; }

ScriptVariable OwlInstallConfig::UtcTimezoneName() const
{ return "UTC"; }




ScriptVariable OwlInstallConfig::ResolvFile() const
{ return root+"/etc/resolv.conf"; }

ScriptVariable OwlInstallConfig::HostsFile() const
{ return root+"/etc/hosts"; }

ScriptVariable OwlInstallConfig::NetworkScriptsDir() const
{ return root+"/etc/sysconfig/network-scripts"; }

ScriptVariable OwlInstallConfig::NetworkSysconf() const
{ return root+"/etc/sysconfig/network"; }



ScriptVariable OwlInstallConfig::DefaultKernel() const
{ return "/boot/bzImage"; }

ScriptVariable OwlInstallConfig::DefaultKernelMap() const
{ return "/boot/System.map"; }

ScriptVariable OwlInstallConfig::TargetKernel() const
{ return root+"/boot/bzImage"; }

ScriptVariable OwlInstallConfig::TargetKernelMap() const
{ return root+"/boot/System.map"; }

ScriptVariable OwlInstallConfig::LiloconfFile() const
{ return root+"/etc/lilo.conf"; }

ScriptVariable OwlInstallConfig::LiloPath() const
{ return "/sbin/lilo"; }

ScriptVariable OwlInstallConfig::LiloMap() const
{ return root+"/boot/map"; }


ScriptVariable OwlInstallConfig::KernelHeadersSource() const
{ return "/usr/src/linux"; /* NO TRAILING SLASH HERE!!! */ }

ScriptVariable OwlInstallConfig::KernelHeadersTarget() const
{ return root+"/usr/src/"; }

ScriptVariable OwlInstallConfig::KernelHeadersDirName() const
{ return "linux"; }



ScriptVariable OwlInstallConfig::FstabFile() const
{ return root+"/etc/fstab"; }

OwlInstallConfig *the_config = 0;

#include "config.hpp"




ScriptVariable OwlInstallConfig::FdiskPath() const
{ return "/sbin/fdisk"; }

ScriptVariable OwlInstallConfig::CfdiskPath() const
{ return "/sbin/cfdisk"; }

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

#if 0
ScriptVariable OwlInstallConfig::EditorPath() const
{ return "/bin/vi"; }
#endif

void OwlInstallConfig::EditorCmdline(ScriptVector &cmdl) const
{
    cmdl.Clear();
    cmdl.AddItem("/bin/vi");
    cmdl.AddItem("-c");
    cmdl.AddItem("set helpheight=8");
    cmdl.AddItem("-c");
    cmdl.AddItem("help");
    cmdl.AddItem("-c");
    cmdl.AddItem("resize 8");
}

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
{ return ".map.gz"; }

ScriptVariable OwlInstallConfig::KeymapDbPath() const
#ifdef __sparc__
{ return "/lib/kbd/keymaps/sun"; }
#else
{ return "/lib/kbd/keymaps/i386"; }
#endif

ScriptVariable OwlInstallConfig::KeymapSysconf() const
{ return root+"/etc/sysconfig/keyboard"; }

ScriptVariable OwlInstallConfig::LoadkeysPath() const
{ return "/bin/loadkeys"; }

ScriptVariable OwlInstallConfig::ConsolefontsDbPath() const
{ return "/lib/kbd/consolefonts"; }

ScriptVariable OwlInstallConfig::ConsolefontsSuffix() const
{ return ".gz"; }

ScriptVariable OwlInstallConfig::UnimapsDbPath() const
{ return "/lib/kbd/consoletrans"; }

ScriptVariable OwlInstallConfig::UnimapsSuffix() const
{ return ".trans"; }

ScriptVariable OwlInstallConfig::CharmapsDbPath() const
{ return "/lib/kbd/consoletrans"; }

ScriptVariable OwlInstallConfig::CharmapsSuffix() const
{ return ""; }

#if 0
ScriptVariable OwlInstallConfig::SetfontPath() const
{ return "/bin/setfont"; }
#endif

ScriptVariable OwlInstallConfig::SetsysfontPath() const
{ return "/sbin/setsysfont"; }

ScriptVariable OwlInstallConfig::LocalePath() const
{ return "/usr/bin/locale"; }

ScriptVariable OwlInstallConfig::I18nSysconf() const
{ return root+"/etc/sysconfig/i18n"; }

const OwlInstallConfig::PresetFontItem*
OwlInstallConfig::PresetSetfontCombinations() const
{
    /*
        The following table contains the combinations of setfont(8)
        parameters which are known to work for us the Openwall
        team members. If you've got a combination to share, PLEASE
        PLEASE PLEASE report it to us!
     */
    static PresetFontItem the_table[] = {
            // from http://linuxgazette.net/issue91/loozzr.html
        { "lat1-16", 0, "cp437", "Default (cp437, looks like latin1)" },

#if 0
            // from AltLinux
            //    disabled: our version of kbd doesn't contain the font
        { "UniCyr_8x16",  0, "koi8-r", "Cyrillic koi8-r, using UniCyr" },
#endif

            // recommended by Gremlin
        { "koi8r-8x16", "koi8-r_to_uni.trans",  0,   "Cyrillic koi8-r" },

            // the one from Owl CD /README file
        { "koi8r-8x16", "/lib/kbd/unimaps/iso01",  0,
                                         "Cyrillic koi8-r Owl default" },

            // legacy is from older Linux distros
        { "alt-8x16", 0, "koi2alt", "Cyrillic koi8-r legacy (with koi2alt)" },
        { "alt-8x14", 0, "koi2alt", "Cyrillic koi8-r legacy, 28 lines" },
        { "alt-8x8",  0, "koi2alt", "Cyrillic koi8-r legacy, 50 lines" },

        { 0, 0, 0, 0 }
    };

    return the_table;
}


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

ScriptVariable OwlInstallConfig::PamServiceName() const
{ return "passwd"; }

OwlInstallConfig *the_config = 0;

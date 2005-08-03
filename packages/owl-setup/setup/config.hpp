#ifndef CONFIG_HPP_SENTRY
#define CONFIG_HPP_SENTRY

#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

class OwlInstallConfig {
public:


    ScriptVariable FdiskPath() const;
    ScriptVariable CpPath() const;
    ScriptVariable MkdirPath() const;
    ScriptVariable PasswdPath() const;
    ScriptVariable MakePath() const;
    ScriptVariable MountPath() const;
    ScriptVariable UmountPath() const;
    ScriptVariable MkswapPath() const;
    ScriptVariable SwaponPath() const;
    ScriptVariable SwapoffPath() const;
    ScriptVariable EditorPath() const;

    ScriptVariable WorldDir() const;
    ScriptVariable InstallWorldTarget() const;

    ScriptVariable OwlRoot() const;

        // /proc
    ScriptVariable ProcMounts() const;
    ScriptVariable ProcSwaps() const;

        // Checks
    void PkgInstalledCheckFiles(ScriptVector &vec) const;
    ScriptVariable RootShadowFile() const;


        // partitioning
    ScriptVariable MkfsPath(const ScriptVariable& fst) const;

        // key maps
    ScriptVariable KeymapDbPath() const;
    ScriptVariable KeymapFileSuffix() const;
    ScriptVariable KeymapSysconf() const;
    ScriptVariable LoadkeysPath() const;

        // time zone
    ScriptVariable ZoneinfoDbPath() const;
    ScriptVariable ZoneinfoSysconf() const;

        // network config
    ScriptVariable ResolvFile() const;
    ScriptVariable HostsFile() const;
    ScriptVariable NetworkScriptsDir() const;
    ScriptVariable NetworkSysconf() const;

        // kernel
    ScriptVariable DefaultKernel() const;
    ScriptVariable DefaultKernelMap() const;
    ScriptVariable TargetKernel() const;
    ScriptVariable TargetKernelMap() const;
    ScriptVariable LiloconfFile() const;
    ScriptVariable LiloPath() const;
    ScriptVariable LiloMap() const;


    ScriptVariable FstabFile() const;
    ScriptVariable DefaultFstabContent() const;
};

extern OwlInstallConfig *the_config;

#endif

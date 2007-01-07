#ifndef CONFIG_HPP_SENTRY
#define CONFIG_HPP_SENTRY

#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

class OwlInstallConfig {
    ScriptVariable root;
public:
    OwlInstallConfig(const char *rt = "") : root(rt) {}

    void SetRoot(const char *rt) { root = rt; }

    ScriptVariable FdiskPath() const;
    ScriptVariable CfdiskPath() const;
    ScriptVariable CpPath() const;
    ScriptVariable SuPath() const;
    ScriptVariable MkdirPath() const;
    ScriptVariable PasswdPath() const;
    ScriptVariable MakePath() const;
    ScriptVariable MountPath() const;
    ScriptVariable UmountPath() const;
    ScriptVariable MkswapPath() const;
    ScriptVariable SwaponPath() const;
    ScriptVariable SwapoffPath() const;
#if 0
    ScriptVariable EditorPath() const;
#endif
    void EditorCmdline(ScriptVector &cmdl) const;

    ScriptVariable WorldDir() const;
    ScriptVariable InstallWorldTarget() const;

    ScriptVariable OwlRoot() const;

        // /proc
    ScriptVariable ProcMounts() const;
    ScriptVariable ProcSwaps() const;

        // Checks
    void PkgInstalledCheckFiles(ScriptVector &vec) const;
    ScriptVariable RootShadowFile() const;
    ScriptVariable OwlInstallCdLabel() const;


        // partitioning
    ScriptVariable MkfsPath(const ScriptVariable& fst) const;

        // key maps
    ScriptVariable KeymapDbPath() const;
    ScriptVariable KeymapFileSuffix() const;
    ScriptVariable KeymapSysconf() const;
    ScriptVariable LoadkeysPath() const;
        // screen font
    ScriptVariable ConsolefontsDbPath() const;
    ScriptVariable ConsolefontsSuffix() const;
    ScriptVariable UnimapsDbPath() const;
    ScriptVariable UnimapsSuffix() const;
    ScriptVariable CharmapsDbPath() const;
    ScriptVariable CharmapsSuffix() const;
#if 0
    ScriptVariable SetfontPath() const;
#endif
    ScriptVariable SetsysfontPath() const;
        // locale
    ScriptVariable LocalePath() const;
    ScriptVariable I18nSysconf() const;

        // preset setfont combinations
    struct PresetFontItem {
        const char *sysfont;
        const char *unimap;
        const char *sysfontacm;
        const char *comment;
    };

    const PresetFontItem* PresetSetfontCombinations() const;

        // time zone
    ScriptVariable ZoneinfoDbPath() const;
    ScriptVariable ZoneinfoFile() const;
    ScriptVariable ZoneinfoSysconf() const;
    ScriptVariable UtcTimezoneName() const;

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

        // kernel headers
    ScriptVariable KernelHeadersSource() const;
    ScriptVariable KernelHeadersTarget() const;
    ScriptVariable KernelHeadersDirName() const;

    ScriptVariable FstabFile() const;

    ScriptVariable PamServiceName() const;
};

extern OwlInstallConfig *the_config;

#endif

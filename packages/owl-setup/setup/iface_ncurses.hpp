#ifndef IFACE_NCURSES_HPP_SENTRY
#define IFACE_NCURSES_HPP_SENTRY

#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

#include "iface.hpp"

class NcursesIfaceSingleChoice : public IfaceSingleChoice {
    friend class NcursesOwlInstallInterface;
    NcursesIfaceSingleChoice();
public:
    ScriptVariable Run();
};

class NcursesIfaceHierChoice : public IfaceHierChoice {
    friend class NcursesOwlInstallInterface;
    void *the_cdkscreen;
    NcursesIfaceHierChoice(void *a_screen);
public:
    bool Run(ScriptVector &result);
};

class NcursesOwlInstallInterface : public OwlInstallInterface {
    void *cdkscreen;
    void *noticewin;
public:
    NcursesOwlInstallInterface(bool allow_colors);
    ~NcursesOwlInstallInterface();

    IfaceSingleChoice *CreateSingleChoice() const;
    IfaceHierChoice *CreateHierChoice() const;

    void Message(const ScriptVariable& msg);
    void Notice(const ScriptVariable& msg);
    void ClearNotices();
    bool YesNoMessage(const ScriptVariable& msg, bool dfl = false);
    YesNoCancelResult YesNoCancelMessage(const ScriptVariable& msg,
                                         int dfl = ync_cancel);

    ScriptVariable QueryString(const ScriptVariable &prompt,
                               const ScriptVariable &defval);

    void ExecWindow(const ScriptVariable& msg);
    void CloseExecWindow();
};




#endif

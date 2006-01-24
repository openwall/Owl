#ifndef IFACE_DUMB_HPP_SENTRY
#define IFACE_DUMB_HPP_SENTRY

#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

#include "iface.hpp"

class DumbIfaceSingleChoice : public IfaceSingleChoice {
    friend class DumbOwlInstallInterface;
    DumbIfaceSingleChoice();
public:
    ScriptVariable Run();
};

class DumbIfaceHierChoice : public IfaceHierChoice {
    friend class DumbOwlInstallInterface;
    DumbIfaceHierChoice();
public:
    bool Run(ScriptVector &result);
};

class DumbOwlInstallInterface : public OwlInstallInterface {
public:
    DumbOwlInstallInterface() : OwlInstallInterface() {}

    IfaceSingleChoice *CreateSingleChoice() const;
    IfaceHierChoice *CreateHierChoice() const;

    void Message(const ScriptVariable& msg);
    void Notice(const ScriptVariable& msg);
    void ClearNotices() {}
    bool YesNoMessage(const ScriptVariable& msg, bool dfl = false);
    YesNoCancelResult YesNoCancelMessage(const ScriptVariable& msg, 
                                         int dfl = ync_cancel);

    ScriptVariable QueryString(const ScriptVariable &prompt,
                               const ScriptVariable &defval);

    void ExecWindow(const ScriptVariable& msg);
    void CloseExecWindow();
};




#endif

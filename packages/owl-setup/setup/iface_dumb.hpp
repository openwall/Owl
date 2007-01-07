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
    bool numbers;
public:
    bool Run(ScriptVector &result, const void **uptr);
};

class DumbIfaceProgressBar : public IfaceProgressBar {
    ScriptVariable title;
    ScriptVariable message;
public:
    DumbIfaceProgressBar(const ScriptVariable &a_title,
                         const ScriptVariable &a_message,
                         int total = 100,
                         const char *units = "%",
                         int order = 0)
        : IfaceProgressBar(total, units, order),
          title(a_title), message(a_message) {}
    virtual ~DumbIfaceProgressBar() {}

    virtual void Draw();
    virtual void SetCurrent(int c);
    virtual void Erase();
};

class DumbIfaceProgressCanceller : public IfaceProgressCanceller {
    int pid;
    class SymbolicInterruption *si;
public:
    DumbIfaceProgressCanceller();
    ~DumbIfaceProgressCanceller();

    virtual void Run(int signo);
    virtual void Remove();
    virtual const char* Message() const;
};



class DumbOwlInstallInterface : public OwlInstallInterface {
public:
    DumbOwlInstallInterface() : OwlInstallInterface() {}

    IfaceSingleChoice *CreateSingleChoice() const;
    IfaceHierChoice *CreateHierChoice() const;
    IfaceProgressBar *CreateProgressBar(const ScriptVariable &title,
                                        const ScriptVariable &msg,
                                        int total,
                                        const ScriptVariable &units,
                                        int order) const;
    IfaceProgressCanceller *CreateProgressCanceller() const;

    void Message(const ScriptVariable& msg);
    void Notice(const ScriptVariable& msg);
    void ClearNotices() {}
    bool YesNoMessage(const ScriptVariable& msg, bool dfl = false);
    YesNoCancelResult YesNoCancelMessage(const ScriptVariable& msg,
                                         int dfl = ync_cancel);

    ScriptVariable QueryString(const ScriptVariable &prompt,
                               const ScriptVariable &defval,
                               bool blind = false);

    void ExecWindow(const ScriptVariable& msg);
    void CloseExecWindow(bool keywait = false);
};




#endif

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

class NcursesIfaceProgressBar : public IfaceProgressBar {
    ScriptVariable title;
    ScriptVariable message;
    void *the_slider;
    void *the_screen;
public:
    NcursesIfaceProgressBar(void *a_screen,
                         const ScriptVariable &a_title,
                         const ScriptVariable &a_message,
                         int total = 100,
                         const char *units = "%",
                         int order = 0)
        : IfaceProgressBar(total, units, order),
          title(a_title), message(a_message),
          the_slider(0), the_screen(a_screen) {}
    virtual ~NcursesIfaceProgressBar() {}

    virtual void Draw();
    virtual void SetCurrent(int c);
    virtual void Erase();
};

class NcursesIfaceProgressCanceller : public IfaceProgressCanceller {
    int pid;
    class SymbolicInterruption *si;
public:
    NcursesIfaceProgressCanceller();
    ~NcursesIfaceProgressCanceller();

    virtual void Run(int signo);
    virtual void Remove();
    virtual const char* Message() const;
};


class NcursesOwlInstallInterface : public OwlInstallInterface {
    void *cdkscreen;
    void *noticewin;
public:
    NcursesOwlInstallInterface(bool allow_colors);
    ~NcursesOwlInstallInterface();

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
    void ClearNotices();
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

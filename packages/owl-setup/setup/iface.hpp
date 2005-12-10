#ifndef IFACE_HPP_SENTRY
#define IFACE_HPP_SENTRY

#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"


class IfaceSingleChoice {
protected:
    IfaceSingleChoice();

    struct Item {
        ScriptVariable label;
        ScriptVariable comment;
        bool enabled;
        Item *next;
    };

    Item* first;
    Item* last;

    ScriptVariable caption;
    ScriptVariable defvalue;

public:

    virtual ~IfaceSingleChoice();

    void AddItem(const ScriptVariable& label,
                 const ScriptVariable& comment,
                 bool enabled = true);

    void SetCaption(const ScriptVariable& a) { caption = a; }
    void SetDefault(const ScriptVariable& a) { defvalue = a; }

    virtual ScriptVariable Run() = 0;
};

class IfaceHierChoice {
protected:
    struct Item {
        ScriptVariable name;
        Item *parent;
        Item *children;
        Item *next;
        Item(const ScriptVariable &a, Item* a_parent)
            : name(a), parent(a_parent)
            { children = next = 0; }
    };

    Item* first;
    Item** last;
    Item* parent;

    ScriptVariable caption;
    bool ignore_case;

public:
    IfaceHierChoice();
    virtual ~IfaceHierChoice();

    void SetCaption(const ScriptVariable& a) { caption = a; }

    void AddItem(const ScriptVariable& name);
    void AddDir(const ScriptVariable& name);
    void EndDir();

    virtual bool Run(ScriptVector &result) = 0;

    void SetCaseSensitivity(bool sensitive) { ignore_case = !sensitive; }
private:
    void RmTree(Item *t);
};

enum YesNoCancelResult { ync_yes = 1, ync_no = 0, ync_cancel = -1 };

class OwlInstallInterface {
public:
    OwlInstallInterface();
    virtual ~OwlInstallInterface() {}

    virtual IfaceSingleChoice *CreateSingleChoice() const = 0;
    virtual IfaceHierChoice *CreateHierChoice() const = 0;

    virtual void Message(const ScriptVariable& msg) = 0;
    virtual void Notice(const ScriptVariable& msg) = 0;
    virtual void ClearNotices() = 0;
    virtual bool YesNoMessage(const ScriptVariable& msg, bool dfl=false)=0;
    virtual YesNoCancelResult YesNoCancelMessage(const ScriptVariable& msg)=0;


    ScriptVariable QueryString(const ScriptVariable &prompt);

    virtual ScriptVariable QueryString(const ScriptVariable &prompt,
                                       const ScriptVariable &defval) = 0;

    static const char *qs_cancel;
    static const char *qs_escape;
    static const char *qs_eof;

    static const char *qs_redraw; // never actually returned by publics
                            // not made private because is used by other
                            // classes of the module

    virtual void ExecWindow(const ScriptVariable& msg) = 0;
    virtual void CloseExecWindow() = 0;
};




#endif

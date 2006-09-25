#ifndef PARMFILE_HPP_SENTRY
#define PARMFILE_HPP_SENTRY

#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"


class ParametersFile {
public:
    class Iterator;
    class Parameter {
        friend class ParametersFile;
        friend class ParametersFile::Iterator;
        ScriptVector comment;
        ScriptVariable name;
        ScriptVariable value;
        Parameter *next;
        Parameter() { next = 0; }
        ~Parameter() {}
    public:
        ScriptVariable& Value() { return value; }
        ScriptVariable GetName() { return name; }
        
    };
private:
    Parameter *first;
    ScriptVariable filename;
    mutable ScriptVariable error;
public:
    ParametersFile() { first = 0; }
    ~ParametersFile();

    Parameter& operator[](const ScriptVariable &name) const;
    bool IsDefined(const ScriptVariable &name) const;
    bool Undefine(const ScriptVariable &name);

    bool Load(const ScriptVariable &filename);
    bool Save() const;
    bool SaveAs(const ScriptVariable &filename) const;

    ScriptVariable LastError() const { return error; }

    friend class Iterator;
    class Iterator {
        Parameter *current;
    public:
        Iterator(const ParametersFile &master) : current(master.first) {}
        Parameter *GetNext() {
            Parameter *ret = current;
            if(ret) current = current->next;
            return ret;
        }
    };
};



#endif

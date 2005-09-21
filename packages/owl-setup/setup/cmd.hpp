#ifndef CMD_HPP_SENTRY
#define CMD_HPP_SENTRY

class ScriptVariable;
class ScriptVector;

class ReadStream {
    void *f;
public:
    ReadStream() : f(0) {}

    bool FOpen(const char *fname);
    bool FDOpen(int fd);
    void FClose();

    bool IsOpen() const { return f != 0; }

    bool ReadLine(ScriptVariable &buf);
    bool ReadLine(ScriptVector &buf, int words = 0,
                 const char *delimiters = " \n\r\t",
                 const char *trimspaces = 0);
};

class ReadText : public ReadStream {
public:
    ReadText(const char *filename) {
        FOpen(filename);
    }
    ~ReadText() { if(IsOpen()) FClose(); }
};

class ExecProgram {
protected:
    int pid;
    int status;
    int save_pgrp;
public:
    ExecProgram();
    ~ExecProgram();

    bool CheckChild();
    void WaitChild();

    bool Success() const;

    class ForkFailed {};
    class PipeFailed {};
};



class ExecResultParse : public ReadStream, public ExecProgram {
public:
    ExecResultParse(const char *path, ...);
    ~ExecResultParse();
};

class ExecAndWait : public ExecProgram {
public:
    ExecAndWait(const char *path, ...);
    ~ExecAndWait();
};

class ChrootExecWait : public ExecProgram {
public:
    ChrootExecWait(const char *root, const char *path, ...);
    ~ChrootExecWait();
};


class FileStat {
    void *stat_info;
public:
    FileStat(const char *filename);
    ~FileStat();

    bool Exists() const;
    bool IsDir() const;
    bool IsRegularFile() const;
    bool IsEmpty() const;
};


class ReadDir {
    void *dir;
public:
    ReadDir(const char *path);
    ~ReadDir();
    const char* Next();
};


class PreserveTerminalMode {
    void *p;
public:
    PreserveTerminalMode();
    ~PreserveTerminalMode();
};


#endif

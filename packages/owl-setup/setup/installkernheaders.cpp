#ifdef __i386__

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <limits.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <setjmp.h>

#include "scriptpp/scrvar.hpp"

#include "cmd.hpp"
#include "iface.hpp"
#include "config.hpp"



static const int approx_kh_files = 2600;

static sigjmp_buf escape_process;
static void (*ep_savesig)(int);
static void sigusr1h(int a) {
    signal(SIGUSR1, ep_savesig);
    siglongjmp(escape_process, 1);
}

void install_kernel_headers(OwlInstallInterface *the_iface)
{
    ScriptVariable from_path;
    ScriptVariable dir_name;

    FileStat source_dir_stat(the_config->KernelHeadersSource().c_str(), false);
    if(!source_dir_stat.Exists()) {
        the_iface->Message("Source directory not found");
        return;
    }
    if(source_dir_stat.IsSymlink()) {
        char buf[PATH_MAX];
        int rc = readlink(the_config->KernelHeadersSource().c_str(),
                          buf, sizeof(buf)-1);
        if(rc<0) {
            the_iface->Message("readlink failed");
            return;
        }
        buf[rc] = 0;
        while(--rc>0 && buf[rc] == '/') /* remove trailing slashes */
            buf[rc] = 0;
        if(buf[0] == '/') {
            from_path = buf;
            char * last_slash = strrchr(buf, '/');
            dir_name = last_slash+1;
        } else {
            ScriptVariable srcpath = the_config->KernelHeadersSource();
            ScriptVariable::Substring s = srcpath.Strrchr('/');
            s.Move(1);
            s.ExtendToEnd();
            s.Erase();
            srcpath += buf;
            ScriptVariable::Substring s2 = srcpath.Strrchr('/');
            s2.Move(1);
            s2.ExtendToEnd();
            dir_name = s2.Get();
            from_path = srcpath;
        }
    } else {
        from_path = the_config->KernelHeadersSource();
        dir_name = the_config->KernelHeadersDirName();
    }

#if 0
    the_iface->ExecWindow("Copying files...");
    ScriptVariable commd = the_config->CpPath() + " -a -v " +
                   from_path + " " +
                   the_config->KernelHeadersTarget();
    unsetenv("BASH_ENV");
    ExecAndWait cp(the_config->SuPath().c_str(), "-c",
                   commd.c_str(), "sources", 0);
    the_iface->CloseExecWindow(true);
#else  ////////////////////////////////
    IfaceProgressCanceller *canceller = 
        the_iface->CreateProgressCanceller();
    IfaceProgressBar *bar = 
        the_iface->CreateProgressBar("Copying kernel header files",
                                     canceller->Message(),
                                     approx_kh_files, "files", 0);

    ScriptVariable commd = the_config->CpPath() + " -a -v " +
                   from_path + " " +
                   the_config->KernelHeadersTarget();
    unsetenv("BASH_ENV");
    //ExecResultParse cp(the_config->SuPath().c_str(), "-c",
    //                   commd.c_str(), "sources", 0);
    int fd[2];
    pipe(fd);
    int cp_pid = fork();
    if(cp_pid == -1) {
        the_iface->Message("Couldn't fork, try again");
        return;
    }
    if(cp_pid == 0) { /* child */
        dup2(fd[1], 1);
        dup2(fd[1], 2);
        close(fd[0]);
        close(fd[1]);
        const char *cmd = the_config->SuPath().c_str();
        execlp(cmd, cmd, "-c", commd.c_str(), "sources", 0);
        exit(1);
    }
    close(fd[1]);
    ReadStream cp_stream;
    cp_stream.FDOpen(fd[0]);

    ScriptVariable v;
    bool cancelled = false;
    ep_savesig = signal(SIGUSR1, sigusr1h);
    if(0 == sigsetjmp(escape_process, 1)) {
        canceller->Run(SIGUSR1);
        bar->Draw();

        int progress = 0;
        while(cp_stream.ReadLine(v)) {
            progress++;
            if(progress%10 == 0 && progress <= approx_kh_files) {
                bar->SetCurrent(progress);
            }
        }
    } else {
        // cancelled!
        cancelled = true;
    }
    kill(cp_pid, 9); /* in case of cancel, this is useful; 
                        in case of normal flow, this might be useful too, 
                        to avoid deadlocks in case of cp internal problems
                      */
    signal(SIGUSR1, ep_savesig);
    close(fd[0]);
    canceller->Remove();
    bar->Erase();
    delete canceller;
    delete bar;

    int status = 0;
    waitpid(cp_pid, &status, 0);
    if(cancelled) {
        the_iface->Message(ScriptVariable(
                           "Copying cancelled. Some files might\n"
                           "have been copied though, so you'll\n"
                           "need to remove them manually from\n") +
                           the_config->KernelHeadersTarget());
        return;
    }
    if(!WIFEXITED(status) || WEXITSTATUS(status)!=0) {
        the_iface->Message("Copying failed");
        return;
    }
#endif


    if(dir_name != the_config->KernelHeadersDirName()) {
        if(-1 == symlink(dir_name.c_str(),
                         (the_config->KernelHeadersTarget()+"/"+
                          the_config->KernelHeadersDirName()).c_str()))
        {
            the_iface->Message("Symlink failed");
        }
    }
}

#endif // __i386__

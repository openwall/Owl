#ifdef __i386__

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <limits.h>

#include "scriptpp/scrvar.hpp"

#include "cmd.hpp"
#include "iface.hpp"
#include "config.hpp"

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

    the_iface->ExecWindow("Copying files...");
    ScriptVariable commd = the_config->CpPath() + " -a -v " +
                   from_path + " " +
                   the_config->KernelHeadersTarget();
    unsetenv("BASH_ENV");
    ExecAndWait cp(the_config->SuPath().c_str(), "-c",
                   commd.c_str(), "sources", 0);
    the_iface->CloseExecWindow(true);
    if(!cp.Success()) {
        the_iface->Message("Copying failed");
        return;
    }
    if(dir_name != the_config->KernelHeadersDirName()) {
        if(-1 == symlink(dir_name.c_str(),
                         (the_config->KernelHeadersTarget()+"/"+
                          the_config->KernelHeadersDirName()).c_str()))
        {
            the_iface->Message("Symlink failed");
        }
    }
}

#endif

#ifndef COMMAND_LINE_HPP_SENTRY
#define COMMAND_LINE_HPP_SENTRY

#include <unistd.h>

struct OwlSetupCommandline {
    bool ncurses_interface;
    bool allow_ncurses_color;

    OwlSetupCommandline()
    {
#ifdef NCURSES_DEFAULT
        ncurses_interface = true;
#else
        ncurses_interface = false;
#endif
        allow_ncurses_color = true;
    }

    virtual ~OwlSetupCommandline() {}

    virtual bool SpecificProcess(int c)
    {
        return false;
    }

    virtual const char* OptChars() const { return "dmbh"; }

    void DisplayUsage(bool by_option)
    {
        if(!by_option) {
            printf("Invalid command line\n");
        }
        printf("Usage: settle -d      use dumb terminal interface\n"
               "       settle -m      use ncurses interface\n"
               "       settle -b      force bw mode for ncurses\n");
        exit(by_option ? 0 : 1);
    }

    void Process(int argc, char **argv)
    {
	int c;
        while(-1 != (c = getopt(argc, argv, OptChars()))) {
            if(SpecificProcess(c)) continue;
            switch(c) {
            case 'd':
               ncurses_interface = false;
               break;
            case 'm':
               ncurses_interface = true;
               break;
            case 'b':
               allow_ncurses_color = false;
               break;
            case 'h':
               DisplayUsage(true);
               break;
            default:
               DisplayUsage(false);
            }
        }
    }
};




#endif

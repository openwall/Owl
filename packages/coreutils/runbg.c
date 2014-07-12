#include <stdio.h>
#include <errno.h>
#include <error.h>
#include <stdlib.h>
#include <unistd.h>

extern const char *__progname;

int
main (int ac, const char *const *av)
{
	pid_t   pid;

	if (ac < 2)
		error (EXIT_FAILURE, 0, "usage: %s program [arguments]",
		       __progname);

	if (access (av[1], X_OK))
		error (EXIT_FAILURE, errno, "%s", av[1]);

	pid = fork ();
	if (pid < 0)
		error (EXIT_FAILURE, errno, "fork");
	else if (pid)
		return EXIT_SUCCESS;
	if (setsid () < 0)
		error (EXIT_FAILURE, errno, "setsid");

	execvp (av[1], (char *const *) av + 1);
	error (EXIT_FAILURE, errno, "%s", av[1]);
	return EXIT_FAILURE;
}

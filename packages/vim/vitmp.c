#include <stdio.h>
#include <unistd.h>

int main(int argc, const char * const *argv)
{
	char *newargv[argc + 4];

	newargv[0] = "/bin/vi";
	/* No swap files, use memory only */
	newargv[1] = "-n";
	/* Don't make a backup before overwriting a file */
	newargv[2] = "-c"; newargv[3] = "set nowritebackup";
	memcpy(&newargv[4], &argv[1], argc * sizeof(char *));

	execv(newargv[0], newargv);
	perror("execv");

	return 1;
}

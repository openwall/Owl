/*
 * This is a wrapper around the VIM editor which may be used to invoke
 * the editor in a way that is guaranteed to be suitable for editing
 * temporary files used with programs such as crontab(1) and edquota(8).
 *
 * Written by Solar Designer <solar@owl.openwall.com> and placed in the
 * public domain.
 *
 * $Owl: Owl/packages/vim/vitmp.c,v 1.3 2005/11/16 13:32:45 solar Exp $
 */
#include <stdio.h>
#include <unistd.h>

int main(int argc, const char * const *argv)
{
	char *newargv[argc + 4]; /* GNU C */

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

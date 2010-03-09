/*
 * This is a wrapper around the VIM editor which may be used to invoke
 * the editor in a way that is guaranteed to be suitable for editing
 * temporary files used with programs such as crontab(1) and edquota(8).
 *
 * Written by Solar Designer <solar at owl.openwall.com> and placed in the
 * public domain.
 *
 * $Owl: Owl/packages/vim/vitmp.c,v 1.6 2010/03/09 02:33:11 ldv Exp $
 */
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main(int argc, const char * const *argv)
{
	char *newargv[argc + 4]; /* GNU C */

	newargv[0] = "vi";
	/* No swap files, use memory only */
	newargv[1] = "-n";
	/* Don't make a backup before overwriting a file */
	newargv[2] = "-c";
	newargv[3] = "set nobackup nowritebackup patchmode=";
	memcpy(&newargv[4], &argv[1], argc * sizeof(char *));

	execv("/bin/vi", newargv);
	perror("execv");

	return 1;
}

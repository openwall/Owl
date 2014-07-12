#include <stdio.h>
#include <unistd.h>
#include <pwd.h>

extern const char *__progname;

int
main (int ac, char *const *av)
{
	struct passwd *pw;

	if (ac != 2)
	{
		fprintf (stderr, "Usage: %s <username>\n", __progname);
		return 1;
	}

	pw = getpwnam (av[1]);
	if (!pw)
		return 1;

	printf ("%u\n", pw->pw_uid);

	return 0;
}

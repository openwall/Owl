#ifndef _GNU_SOURCE
#define _GNU_SOURCE 1
#endif

#include <stdio.h>
#include <errno.h>
#include <error.h>
#include <stdlib.h>
#include <limits.h>
#include <unistd.h>

void
usage(void)
{
	fprintf(stderr, "usage: %s [microseconds]\n",
			program_invocation_short_name);

	exit(EXIT_FAILURE);
}

int
main(int argc, const char **argv)
{
	unsigned long delay = 1;
	char *p = 0;

	if(argc != 2)
		usage();

	delay = strtoul(argv[1], &p, 0);
	if(*p || delay < 0 || delay == ULONG_MAX) {
		error(0, EINVAL, "%s", argv[1]);
		usage();
	}

	usleep(delay);

	return EXIT_SUCCESS;
}

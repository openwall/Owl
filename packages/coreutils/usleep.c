/*
 * Written by Dmitry V. Levin for ALT Linux and placed in the public domain.
 * Further modifications by Solar Designer for Openwall GNU/*/Linux, still
 * public domain.  There's absolutely no warranty.
 */

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdio.h>
#include <errno.h>
#include <error.h>
#include <stdlib.h>
#include <limits.h>
#include <unistd.h>

static void __attribute__ ((__noreturn__)) usage(void)
{
	fprintf(stderr, "usage: %s [microseconds]\n",
		program_invocation_short_name);

	exit(EXIT_FAILURE);
}

int main(int argc, const char **argv)
{
	unsigned long delay = 1;

	if (argc > 2)
		usage();

	if (argc == 2) {
		char *p = 0;

		errno = 0;
		delay = strtoul(argv[1], &p, 10);
		if (!*argv[1] || *p || errno) {
			error(EXIT_SUCCESS, errno ? : EINVAL, "%s", argv[1]);
			usage();
		}
	}

	if (usleep(delay))
		error(EXIT_FAILURE, errno, "%s", argv[1]);

	return EXIT_SUCCESS;
}

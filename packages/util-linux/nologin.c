/*	$Owl: Owl/packages/util-linux/nologin.c,v 1.1 2005/12/24 16:03:38 ldv Exp $	*/
/*	$OpenBSD: nologin.c,v 1.5 2003/07/10 00:00:58 david Exp $	*/

/*
 * Copyright (c) 1997, Jason Downs.  All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR(S) ``AS IS'' AND ANY EXPRESS
 * OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR(S) BE LIABLE FOR ANY DIRECT,
 * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

#ifndef _GNU_SOURCE
# define _GNU_SOURCE 1
#endif
#include <sys/types.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>

/* Distinctly different from _PATH_NOLOGIN. */
#define _PATH_NOLOGIN_TXT	"/etc/nologin.txt"

#define DEFAULT_MESG	"This account is currently not available.\r\n"

static  ssize_t
write_loop(int fd, const char *buffer, size_t count)
{
	ssize_t offset = 0;

	while (count > 0)
	{
		ssize_t block =
			TEMP_FAILURE_RETRY(write(fd, &buffer[offset], count));

		if (block <= 0)
			return offset ? : block;
		offset += block;
		count -= block;
	}
	return offset;
}

int
main(void)
{
	int     nfd;
	ssize_t nrd;
	char    nbuf[BUFSIZ];

	if ((nfd = open(_PATH_NOLOGIN_TXT, O_RDONLY)) < 0)
	{
		write_loop(STDOUT_FILENO, DEFAULT_MESG,
			   sizeof(DEFAULT_MESG) - 1);
		exit(EXIT_FAILURE);
	}

	while ((nrd = TEMP_FAILURE_RETRY(read(nfd, nbuf, sizeof(nbuf)))) > 0)
		if (write_loop(STDOUT_FILENO, nbuf, (size_t) nrd) != nrd)
			break;
	close(nfd);

	exit(EXIT_FAILURE);
}

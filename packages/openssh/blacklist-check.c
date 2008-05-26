/*
 * The blacklist checker for RSA/DSA key blacklisting based on partial
 * fingerprints,
 * developed under Openwall Project for Owl - http://www.openwall.com/Owl/
 *
 * Copyright (c) 2008 Dmitry V. Levin <ldv at cvs.openwall.com>
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 *
 * The blacklist encoding was designed by Solar Designer and Dmitry V. Levin.
 * No intellectual property rights to the encoding scheme are claimed.
 *
 * This effort was supported by CivicActions - http://www.civicactions.com
 *
 * The file size to encode 294,903 of 48-bit fingerprints is just 1.3 MB,
 * which corresponds to less than 4.5 bytes per fingerprint.
 */

#ifndef _GNU_SOURCE
# define _GNU_SOURCE
#endif

#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <errno.h>
#include <error.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

static unsigned
c2u(uint8_t c)
{
	return (c >= 'a') ? (c - 'a' + 10) : (c - '0');
}

static ssize_t
read_retry(int fd, void *buf, size_t records)
{
	return TEMP_FAILURE_RETRY(read(fd, buf, records));
}

static ssize_t
read_loop(int fd, char *buffer, size_t records)
{
	ssize_t offset = 0;

	while (records > 0)
	{
		ssize_t block = read_retry(fd, &buffer[offset], records);

		if (block <= 0)
			return offset ? : block;
		offset += block;
		records -= block;
	}
	return offset;
}

typedef struct
{
	/* format version identifier */
	char version[8];
	/* index size, in bits */
	uint8_t index_size;
	/* offset size, in bits */
	uint8_t offset_size;
	/* record size, in bits */
	uint8_t record_bits;
	/* number of records */
	uint8_t records[3];
	/* offset shift */
	uint8_t shift[2];

} fp_header;

static int
open_blacklist(const char *fname, unsigned *bytes, unsigned *records, unsigned *shift)
{
	int     fd;
	unsigned expected;
	struct stat st;
	fp_header header;

	if ((fd = open(fname, O_RDONLY)) < 0)
	{
		error(0, errno, "open: %s", fname);
		return -1;
	}
	if (fstat(fd, &st))
	{
		error(0, errno, "fstat: %s", fname);
		close(fd);
		return -1;
	}

	if (read_loop(fd, (char *) &header, sizeof header) != sizeof header)
	{
		error(0, errno, "read header: %s", fname);
		close(fd);
		return -1;
	}

	if (header.index_size != 16 || header.offset_size != 16)
	{
		error(0, 0, "%s: unsupported file format", fname);
		close(fd);
		return -1;
	}

	*bytes = (header.record_bits >> 3) - 2;
	*records =
		(((header.records[0] << 8) +
		  header.records[1]) << 8) + header.records[2];
	*shift = (header.shift[0] << 8) + header.shift[1];

	expected = sizeof(header) + 0x20000 + (*records) * (*bytes);
	if (st.st_size != expected)
	{
		error(0, 0, "%s: expected file size %u, found file size %lu",
		      fname, expected, (unsigned long) st.st_size);
		close(fd);
		return -1;
	}

	return fd;
}

static int
expected_offset(uint16_t index, uint16_t shift, unsigned records)
{
	return ((index * (long long) records) >> 16) - shift;
}

static int
xlseek(const char *fname, int fd, unsigned seek)
{
	if (lseek(fd, seek, SEEK_SET) != seek)
	{
		error(0, errno, "lseek: %s", fname);
		return -1;
	}
	return 0;
}

static int
check(const char *fname, const char *s)
{
	int     fd;
	unsigned bytes, records, shift;
	unsigned i, j;
	int     offset, off_end;
	uint16_t index;
	/* max number of bytes stored in record_bits, minus two bytes used for index */
	uint8_t buf[(0xff >> 3) - 2];

	if (strlen(s) != 32 || strlen(s) != strspn(s, "0123456789abcdef"))
	{
		fprintf(stderr, "invalid fingerprint: %s\n", s);
		return 1;
	}

	fd = open_blacklist(fname, &bytes, &records, &shift);
	if (fd < 0)
		return 1;

	index = (((((c2u(s[0]) << 4) | c2u(s[1])) << 4) |
		c2u(s[2])) << 4) | c2u(s[3]);
	if (xlseek(fname, fd, sizeof(fp_header) + index * 2))
	{
		close(fd);
		return 1;
	}

	if (read_loop(fd, (char *) buf, 4) != 4)
	{
		error(0, errno, "read offsets: %s", fname);
		close(fd);
		return 1;
	}

	offset = (buf[0] << 8) + buf[1] +
		expected_offset(index, shift, records);
	if (offset < 0 || offset > records)
	{
		error(0, 0, "index=%#x, offset overflow: %d",
		      index, offset);
		close(fd);
		return 1;
	}
	if (index < 0xffff)
	{
		off_end = (buf[2] << 8) + buf[3] +
			expected_offset(index + 1, shift, records);
		if (off_end < offset || off_end > records)
		{
			error(0, 0, "index=%#x, offset overflow: %d",
			      index, off_end);
			close(fd);
			return 1;
		}
	} else
		off_end = records;

	if (xlseek(fname, fd, sizeof(fp_header) + 0x20000 + offset * bytes))
	{
		close(fd);
		return 1;
	}

	for (i = 0; i < off_end - offset; ++i)
	{
		if (read_loop(fd, (char *) buf, bytes) != bytes)
		{
			error(0, errno, "read fingerprints: %s", fname);
			close(fd);
			return 1;
		}

		for (j = 0; j < bytes; ++j)
			if (((c2u(s[4 + j * 2]) << 4) | c2u(s[5 + j * 2]))
			    != buf[j])
				break;
		if (j >= bytes)
		{
			fprintf(stderr, "BAD: %s offset=%u, offcnt=%u, i=%u\n",
				s, offset, off_end - offset, i);
			close(fd);
			return 1;
		}
	}

	fprintf(stderr, "OK: %s offset=%u, offcnt=%u\n",
		s, offset, off_end - offset);
	close(fd);
	return 0;
}

int
main(int ac, const char **av)
{
	int i, rc = 0;

	if (ac < 3)
		error(EXIT_FAILURE, 0, "insufficient arguments");
	for (i = 2; i < ac; ++i)
		rc |= check(av[1], av[i]);
	return rc;
}

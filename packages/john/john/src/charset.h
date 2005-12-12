/*
 * This file is part of John the Ripper password cracker,
 * Copyright (c) 1996-2001,2005 by Solar Designer
 */

/*
 * Charset file generation.
 */

#ifndef _JOHN_CHARSET_H
#define _JOHN_CHARSET_H

#include "params.h"
#include "common.h"
#include "loader.h"

/*
 * Charset file control char codes (only CHARSET_ESC is reserved, and can't
 * be used in a charset).
 */
#define CHARSET_ESC			0
#define CHARSET_NEW			1
#define CHARSET_LINE			2

/*
 * Charset file header.
 */
struct charset_header {
/* CHARSET_V* */
	char version[4];

/* A checksum of the file or equivalent */
	unsigned char check[4];

/* CHARSET_MIN, CHARSET_MAX */
	unsigned char min, max;

/* CHARSET_LENGTH */
	unsigned char length;

/* Number of different characters, up to (max - min + 1) */
	unsigned char count;

/* File offsets for each length, 32-bit little endian */
	unsigned char offsets[CHARSET_LENGTH][4];

/*
 * Cracking order.
 *
 * This is a list of current {length, fixed position, character count}.
 * There are CHARSET_LENGTH different lengths, and fixed position is up
 * to the current length, which means we have exactly (CHARSET_LENGTH *
 * (CHARSET_LENGTH + 1) / 2) different {length, fixed position} pairs;
 * for each such pair we need to try all charsets from 1 character and
 * up to CHARSET_SIZE characters large.
 */
	unsigned char order
		[CHARSET_LENGTH * (CHARSET_LENGTH + 1) / 2 * CHARSET_SIZE * 3];
};

/*
 * Reads a charset file header.
 */
extern void charset_read_header(FILE *file, struct charset_header *header);

/*
 * Generates a charset file, based on plaintexts in the database.
 */
extern void do_makechars(struct db_main *db, char *charset);

#endif

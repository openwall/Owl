/*
 * This file is part of John the Ripper password cracker,
 * Copyright (c) 1996-2001 by Solar Designer
 */

/*
 * OpenBSD-style Blowfish-based password hash implementation.
 */

#ifndef _JOHN_BF_STD_H
#define _JOHN_BF_STD_H

#include "arch.h"
#include "common.h"

typedef ARCH_WORD_32 BF_word;

/*
 * Binary salt type, also keeps the number of rounds.
 */
typedef BF_word BF_salt[4 + 1];

/*
 * Binary ciphertext type.
 */
typedef BF_word BF_binary[6];

/*
 * BF_std_crypt() output buffer.
 */
extern BF_binary BF_out;

/*
 * ASCII to binary conversion table, for use in BF_fmt.valid().
 */
extern unsigned char BF_atoi64[0x80];

#define BF_ALGORITHM_NAME		"32/" ARCH_BITS_STR

/*
 * Sets a key for BF_std_crypt().
 */
extern void BF_std_set_key(char *key);

/*
 * Main encryption routine, sets first two words of BF_out.
 */
extern void BF_std_crypt(BF_salt salt);

/*
 * Calculates the rest of BF_out, for exact comparison.
 */
extern void BF_std_crypt_exact(void);

/*
 * Returns the salt for BF_std_crypt().
 */
extern BF_word *BF_std_get_salt(char *ciphertext);

/*
 * Converts an ASCII ciphertext to binary.
 */
extern BF_word *BF_std_get_binary(char *ciphertext);

#endif

/*
 * This file is part of John the Ripper password cracker,
 * Copyright (c) 1996-2001 by Solar Designer
 */

#include <stdlib.h>
#include <string.h>

#include "arch.h"
#include "misc.h"
#include "BF_std.h"
#include "common.h"
#include "formats.h"

#define FORMAT_LABEL			"bf"
#define FORMAT_NAME			"OpenBSD Blowfish"

#define BENCHMARK_COMMENT		" (x32)"
#define BENCHMARK_LENGTH		-1

#define PLAINTEXT_LENGTH		72
#define CIPHERTEXT_LENGTH		60

#define BINARY_SIZE			4
#define SALT_SIZE			20

#define MIN_KEYS_PER_CRYPT		1
#define MAX_KEYS_PER_CRYPT		1

static struct fmt_tests tests[] = {
	{"$2a$05$CCCCCCCCCCCCCCCCCCCCC.E5YPO9kmyuRGyh0XouQYb4YMJKvyOeW",
		"U*U"},
	{"$2a$05$CCCCCCCCCCCCCCCCCCCCC.VGOzA784oUp/Z0DY336zx7pLYAy0lwK",
		"U*U*"},
	{"$2a$05$XXXXXXXXXXXXXXXXXXXXXOAcXxm9kjPGEMsLznoKqmqw7tc8WCx4a",
		"U*U*U"},
	{"$2a$05$CCCCCCCCCCCCCCCCCCCCC.7uG0VCzI2bS7j6ymqJi9CdcdxiRTWNy",
		""},
	{"$2a$05$abcdefghijklmnopqrstuu5s2v8.iXieOjg/.AySBTTZIIVFJeBui",
		"0123456789abcdefghijklmnopqrstuvwxyz"
		"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"},
	{NULL}
};

static char saved_key[PLAINTEXT_LENGTH + 1];
static BF_salt saved_salt;

static int valid(char *ciphertext)
{
	int rounds;
	char *pos;

	if (strncmp(ciphertext, "$2a$", 4)) return 0;

	if (ciphertext[4] < '0' || ciphertext[4] > '9') return 0;
	if (ciphertext[5] < '0' || ciphertext[5] > '9') return 0;
	rounds = atoi(ciphertext + 4);
	if (rounds < 4 || rounds > 31) return 0;

	if (ciphertext[6] != '$') return 0;

	for (pos = &ciphertext[7]; atoi64[ARCH_INDEX(*pos)] != 0x7F; pos++);
	if (*pos || pos - ciphertext != CIPHERTEXT_LENGTH) return 0;

	if (BF_atoi64[ARCH_INDEX(*(pos - 1))] & 3) return 0;
	if (BF_atoi64[ARCH_INDEX(ciphertext[28])] & 0xF) return 0;

	return 1;
}

static int binary_hash_0(void *binary)
{
	return *(BF_word *)binary & 0xF;
}

static int binary_hash_1(void *binary)
{
	return *(BF_word *)binary & 0xFF;
}

static int binary_hash_2(void *binary)
{
	return *(BF_word *)binary & 0xFFF;
}

static int get_hash_0(int index)
{
	return BF_out[0] & 0xF;
}

static int get_hash_1(int index)
{
	return BF_out[0] & 0xFF;
}

static int get_hash_2(int index)
{
	return BF_out[0] & 0xFFF;
}

static int salt_hash(void *salt)
{
	return *(BF_word *)salt & 0x3FF;
}

static void set_salt(void *salt)
{
	memcpy(saved_salt, salt, sizeof(saved_salt));
}

static void set_key(char *key, int index)
{
	BF_std_set_key(key);

	strnfcpy(saved_key, key, PLAINTEXT_LENGTH);
}

static char *get_key(int index)
{
	saved_key[PLAINTEXT_LENGTH] = 0;

	return saved_key;
}

static void crypt_all(int count)
{
	BF_std_crypt(saved_salt);
}

static int cmp_all(void *binary, int index)
{
	return *(BF_word *)binary == BF_out[0];
}

static int cmp_exact(char *source, int index)
{
	BF_std_crypt_exact();

	return !memcmp(BF_std_get_binary(source), BF_out, sizeof(BF_binary));
}

struct fmt_main fmt_BF = {
	{
		FORMAT_LABEL,
		FORMAT_NAME,
		BF_ALGORITHM_NAME,
		BENCHMARK_COMMENT,
		BENCHMARK_LENGTH,
		PLAINTEXT_LENGTH,
		BINARY_SIZE,
		SALT_SIZE,
		MIN_KEYS_PER_CRYPT,
		MAX_KEYS_PER_CRYPT,
		FMT_CASE | FMT_8_BIT,
		tests
	}, {
		fmt_default_init,
		valid,
		fmt_default_split,
		(void *(*)(char *))BF_std_get_binary,
		(void *(*)(char *))BF_std_get_salt,
		{
			binary_hash_0,
			binary_hash_1,
			binary_hash_2
		},
		salt_hash,
		set_salt,
		set_key,
		get_key,
		fmt_default_clear_keys,
		crypt_all,
		{
			get_hash_0,
			get_hash_1,
			get_hash_2
		},
		cmp_all,
		cmp_all,
		cmp_exact
	}
};

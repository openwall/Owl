/*
 * This file is part of John the Ripper password cracker,
 * Copyright (c) 2009,2010 by Solar Designer
 */

#define _XOPEN_SOURCE /* for crypt(3) */
#include <string.h>
#include <unistd.h>

#include "arch.h"
#include "misc.h"
#include "params.h"
#include "common.h"
#include "formats.h"

#define FORMAT_LABEL			"crypt"
#define FORMAT_NAME			"generic crypt(3)"
#define ALGORITHM_NAME			"?/" ARCH_BITS_STR

#define BENCHMARK_COMMENT		""
#define BENCHMARK_LENGTH		0

#define PLAINTEXT_LENGTH		72

#define BINARY_SIZE			128
#define SALT_SIZE			BINARY_SIZE

#define MIN_KEYS_PER_CRYPT		0x40
#define MAX_KEYS_PER_CRYPT		0x40

static struct fmt_tests tests[] = {
	{"CCNf8Sbh3HDfQ", "U*U*U*U*"},
	{"CCX.K.MFy4Ois", "U*U***U"},
	{"CC4rMpbg9AMZ.", "U*U***U*"},
	{"XXxzOu6maQKqQ", "*U*U*U*U"},
	{"SDbsugeBiC58A", ""},
	{NULL}
};

static char saved_key[MAX_KEYS_PER_CRYPT][PLAINTEXT_LENGTH + 1];
static char saved_salt[SALT_SIZE];
static char crypt_out[MAX_KEYS_PER_CRYPT][BINARY_SIZE];

static int valid(char *ciphertext)
{
#if 1
	int length, count_base64;

	length = count_base64 = 0;
	while (ciphertext[length]) {
		if (atoi64[ARCH_INDEX(ciphertext[length])] != 0x7F &&
		    (ciphertext[0] == '_' || length >= 2))
			count_base64++;
		length++;
	}

	if (length >= BINARY_SIZE)
		return 0;

	if (length >= 34 && ciphertext[0] == '$')
		return 1;

	if (length == 13 && count_base64 == 11)
		return 1;

	if (length == 20 && count_base64 == 19 && ciphertext[0] == '_')
		return 1;

	if (length >= 13 &&
	    count_base64 >= length - 2 && /* allow for invalid salt */
	    length % 11 == 0)
		return 1;

	return 0;
#else
/*
 * Poor load time, but more effective at detecting supported and rejecting
 * bad/unsupported hashes.
 */
	char *r = strlen(ciphertext) >= 13 ? crypt("", ciphertext) : "";
	int l = strlen(r);
	return
	    !strncmp(r, ciphertext, 2) &&
	    l == strlen(ciphertext) &&
	    l >= 13 && l < BINARY_SIZE;
#endif
}

static void *binary(char *ciphertext)
{
	static char out[BINARY_SIZE];
	strncpy(out, ciphertext, sizeof(out)); /* NUL padding is required */
	return out;
}

static void *salt(char *ciphertext)
{
	static char out[SALT_SIZE];
	int cut = sizeof(out);

#if 1
/* This piece is optional, but matching salts are not detected without it */
	switch (strlen(ciphertext)) {
	case 13:
	case 24:
		cut = 2;
		break;

	case 35:
	case 46:
	case 57:
		if (ciphertext[0] != '$') cut = 2;
		break;

	case 20:
		if (ciphertext[0] == '_') cut = 9;
		break;

	case 34:
		if (!strncmp(ciphertext, "$1$", 3)) {
			char *p = strchr(ciphertext + 3, '$');
			if (p) cut = p - ciphertext;
		}
		break;

	case 59:
		if (!strncmp(ciphertext, "$2$", 3)) cut = 28;
		break;

	case 60:
		if (!strncmp(ciphertext, "$2a$", 4)) cut = 29;
		break;

	default:
		if ((!strncmp(ciphertext, "$5$", 3) ||
		    !strncmp(ciphertext, "$6$", 3)) &&
		    strlen(ciphertext) >= 55) {
			char *p = strchr(ciphertext + 3, '$');
			if (p && !strncmp(ciphertext + 3, "rounds=", 7))
				p = strchr(p + 1, '$');
			if (p) cut = p - ciphertext;
		}
	}
#endif

	/* NUL padding is required */
	memset(out, 0, sizeof(out));
	memcpy(out, ciphertext, cut);

	return out;
}

#define H(s, i) \
	((int)(unsigned char)(atoi64[ARCH_INDEX((s)[(i)])] ^ (s)[(i) - 1]))

#define H0(s) \
	int i = strlen(s) - 1; \
	return i > 0 ? H((s), i) & 0xF : 0
#define H1(s) \
	int i = strlen(s) - 1; \
	return i > 2 ? (H((s), i) ^ (H((s), i - 2) << 4)) & 0xFF : 0
#define H2(s) \
	int i = strlen(s) - 1; \
	return i > 2 ? (H((s), i) ^ (H((s), i - 2) << 6)) & 0xFFF : 0
#define H3(s) \
	int i = strlen(s) - 1; \
	return i > 4 ? (H((s), i) ^ (H((s), i - 2) << 5) ^ \
	    (H((s), i - 4) << 10)) & 0xFFFF : 0
#define H4(s) \
	int i = strlen(s) - 1; \
	return i > 6 ? (H((s), i) ^ (H((s), i - 2) << 5) ^ \
	    (H((s), i - 4) << 10) ^ (H((s), i - 6) << 15)) & 0xFFFFF : 0

static int binary_hash_0(void *binary)
{
	H0((char *)binary);
}

static int binary_hash_1(void *binary)
{
	H1((char *)binary);
}

static int binary_hash_2(void *binary)
{
	H2((char *)binary);
}

static int binary_hash_3(void *binary)
{
	H3((char *)binary);
}

static int binary_hash_4(void *binary)
{
	H4((char *)binary);
}

static int get_hash_0(int index)
{
	H0(crypt_out[index]);
}

static int get_hash_1(int index)
{
	H1(crypt_out[index]);
}

static int get_hash_2(int index)
{
	H2(crypt_out[index]);
}

static int get_hash_3(int index)
{
	H3(crypt_out[index]);
}

static int get_hash_4(int index)
{
	H4(crypt_out[index]);
}

static int salt_hash(void *salt)
{
	int i, h;

	i = strlen((char *)salt) - 1;

	h = (unsigned char)atoi64[ARCH_INDEX(((char *)salt)[i])];
	h ^= ((unsigned char *)salt)[i - 1];
	h <<= 6;
	h ^= (unsigned char)atoi64[ARCH_INDEX(((char *)salt)[i - 1])];
	h ^= ((unsigned char *)salt)[i];

	return h & 0x3FF;
}

static void set_salt(void *salt)
{
	strcpy(saved_salt, salt);
}

static void set_key(char *key, int index)
{
	strnzcpy(saved_key[index], key, PLAINTEXT_LENGTH + 1);
}

static char *get_key(int index)
{
	return saved_key[index];
}

static void crypt_all(int count)
{
	int index;

	for (index = 0; index < count; index++)
		strnzcpy(crypt_out[index], crypt(saved_key[index], saved_salt),
		    BINARY_SIZE);
}

static int cmp_all(void *binary, int count)
{
	return 1;
}

static int cmp_one(void *binary, int index)
{
	return !strcmp((char *)binary, crypt_out[index]);
}

static int cmp_exact(char *source, int index)
{
	return 1;
}

struct fmt_main fmt_crypt = {
	{
		FORMAT_LABEL,
		FORMAT_NAME,
		ALGORITHM_NAME,
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
		binary,
		salt,
		{
			binary_hash_0,
			binary_hash_1,
			binary_hash_2,
			binary_hash_3,
			binary_hash_4
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
			get_hash_2,
			get_hash_3,
			get_hash_4
		},
		cmp_all,
		cmp_one,
		cmp_exact
	}
};

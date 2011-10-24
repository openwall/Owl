/*
 * This file is part of John the Ripper password cracker,
 * Copyright (c) 1996-2002,2005,2010,2011 by Solar Designer
 */

#include <string.h>

#ifdef _OPENMP
#include <omp.h>
#endif

#include "arch.h"
#include "common.h"
#include "DES_std.h"
#include "DES_bs.h"

#if DES_BS_VECTOR
#define DEPTH				[depth]
#define START				[0]
#define init_depth() \
	int depth; \
	depth = index >> ARCH_BITS_LOG; \
	index &= (ARCH_BITS - 1);
#define for_each_depth() \
	for (depth = 0; depth < DES_BS_VECTOR; depth++)
#else
#define DEPTH
#define START
#define init_depth()
#define for_each_depth()
#endif

#if defined(_OPENMP) && !DES_BS_ASM
int DES_bs_min_kpc, DES_bs_max_kpc;
int DES_bs_nt = 0;
DES_bs_combined *DES_bs_all_p = NULL;
#elif !DES_BS_ASM
DES_bs_combined CC_CACHE_ALIGN DES_bs_all;
#endif

static unsigned char DES_LM_KP[56] = {
	1, 2, 3, 4, 5, 6, 7,
	10, 11, 12, 13, 14, 15, 0,
	19, 20, 21, 22, 23, 8, 9,
	28, 29, 30, 31, 16, 17, 18,
	37, 38, 39, 24, 25, 26, 27,
	46, 47, 32, 33, 34, 35, 36,
	55, 40, 41, 42, 43, 44, 45,
	48, 49, 50, 51, 52, 53, 54
};

static unsigned char DES_LM_reverse[16] = {
	0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15
};

#if DES_BS_ASM
extern void DES_bs_init_asm(void);
#endif

void DES_bs_init(int LM)
{
	ARCH_WORD **k;
	int round, index, bit;
	int p, q, s;
	int c;
#if DES_bs_mt
	int t, n;

/*
 * The array of DES_bs_all's is not exactly tiny, but we use mem_alloc_tiny()
 * for its alignment support and error checking.  We do not need to free() this
 * memory anyway.
 *
 * We allocate one extra entry (will be at "thread number" -1) to hold "ones"
 * and "salt" fields that are shared between threads.
 */
	n = DES_bs_nt;
	if (!n) {
		n = omp_get_max_threads();
		if (n < 1)
			n = 1;
		if (n > DES_bs_mt_max)
			n = DES_bs_mt_max;
		DES_bs_min_kpc = n * DES_BS_DEPTH;
		n *= DES_bs_cpt;
		if (n > DES_bs_mt_max)
			n = DES_bs_mt_max;
		DES_bs_max_kpc = n * DES_BS_DEPTH;
		DES_bs_nt = n;
		DES_bs_all_p = mem_alloc_tiny(
		    ++n * DES_bs_all_size, MEM_ALIGN_PAGE);
	}
#endif

	for_each_t(n) {
#if DES_BS_EXPAND
		if (LM)
			k = DES_bs_all.KS.p;
		else
			k = DES_bs_all.KSp;
#else
		k = DES_bs_all.KS.p;
#endif

		s = 0;
		for (round = 0; round < 16; round++) {
			s += DES_ROT[round];
			for (index = 0; index < 48; index++) {
				p = DES_PC2[index];
				q = p < 28 ? 0 : 28;
				p += s;
				while (p >= 28) p -= 28;
				bit = DES_PC1[p + q];
				bit ^= 070;
				bit -= bit >> 3;
				bit = 55 - bit;
				if (LM) bit = DES_LM_KP[bit];
				*k++ = &DES_bs_all.K[bit] START;
			}
		}

		for (index = 0; index < DES_BS_DEPTH; index++)
			DES_bs_all.pxkeys[index] =
			    &DES_bs_all.xkeys.c[0][index & 7][index >> 3];

		if (LM) {
			for (c = 0; c < 0x100; c++)
			if (c >= 'a' && c <= 'z')
				DES_bs_all.E.u[c] = c & ~0x20;
			else
				DES_bs_all.E.u[c] = c;
		} else {
			for (index = 0; index < 48; index++)
				DES_bs_all.Ens[index] =
				    &DES_bs_all.B[DES_E[index]];
			DES_bs_all.salt = 0xffffff;
#if DES_bs_mt
			DES_bs_set_salt_for_thread(t, 0);
#else
			DES_bs_set_salt(0);
#endif
		}

#if !DES_BS_ASM
		memset(&DES_bs_all.zero, 0, sizeof(DES_bs_all.zero));
		memset(&DES_bs_all.ones, -1, sizeof(DES_bs_all.ones));
		for (bit = 0; bit < 8; bit++)
			memset(&DES_bs_all.masks[bit], 1 << bit,
			    sizeof(DES_bs_all.masks[bit]));
#endif
	}

#if DES_bs_mt
/* Skip the special entry (will be at "thread number" -1) */
	if (n > DES_bs_nt)
		DES_bs_all_p = (DES_bs_combined *)
		    ((char *)DES_bs_all_p + DES_bs_all_size);
#endif

#if DES_BS_ASM
	DES_bs_init_asm();
#endif
}

#if DES_bs_mt
void DES_bs_set_salt(ARCH_WORD salt)
{
	DES_bs_all_by_tnum(-1).salt = salt;
}
#endif

void DES_bs_set_key(char *key, int index)
{
	unsigned char *dst;

	init_t();

	dst = DES_bs_all.pxkeys[index];

	DES_bs_all.keys_changed = 1;

	if (!key[0]) goto fill8;
	*dst = key[0];
	*(dst + sizeof(DES_bs_vector) * 8) = key[1];
	*(dst + sizeof(DES_bs_vector) * 8 * 2) = key[2];
	if (!key[1]) goto fill6;
	if (!key[2]) goto fill5;
	*(dst + sizeof(DES_bs_vector) * 8 * 3) = key[3];
	*(dst + sizeof(DES_bs_vector) * 8 * 4) = key[4];
	if (!key[3]) goto fill4;
	if (!key[4] || !key[5]) goto fill3;
	*(dst + sizeof(DES_bs_vector) * 8 * 5) = key[5];
	if (!key[6]) goto fill2;
	*(dst + sizeof(DES_bs_vector) * 8 * 6) = key[6];
	*(dst + sizeof(DES_bs_vector) * 8 * 7) = key[7];
	return;
fill8:
	dst[0] = 0;
	dst[sizeof(DES_bs_vector) * 8] = 0;
fill6:
	dst[sizeof(DES_bs_vector) * 8 * 2] = 0;
fill5:
	dst[sizeof(DES_bs_vector) * 8 * 3] = 0;
fill4:
	dst[sizeof(DES_bs_vector) * 8 * 4] = 0;
fill3:
	dst[sizeof(DES_bs_vector) * 8 * 5] = 0;
fill2:
	dst[sizeof(DES_bs_vector) * 8 * 6] = 0;
	dst[sizeof(DES_bs_vector) * 8 * 7] = 0;
}

void DES_bs_set_key_LM(char *key, int index)
{
	unsigned char *dst;

	init_t();

	dst = DES_bs_all.pxkeys[index];

/*
 * gcc 4.5.0 on x86_64 would generate redundant movzbl's without explicit
 * use of "long" here.
 */
	unsigned long c = (unsigned char)key[0];
	if (!c) goto fill7;
	*dst = DES_bs_all.E.u[c];
	c = (unsigned char)key[1];
	if (!c) goto fill6;
	*(dst + sizeof(DES_bs_vector) * 8) = DES_bs_all.E.u[c];
	c = (unsigned char)key[2];
	if (!c) goto fill5;
	*(dst + sizeof(DES_bs_vector) * 8 * 2) = DES_bs_all.E.u[c];
	c = (unsigned char)key[3];
	if (!c) goto fill4;
	*(dst + sizeof(DES_bs_vector) * 8 * 3) = DES_bs_all.E.u[c];
	c = (unsigned char)key[4];
	if (!c) goto fill3;
	*(dst + sizeof(DES_bs_vector) * 8 * 4) = DES_bs_all.E.u[c];
	c = (unsigned char)key[5];
	if (!c) goto fill2;
	*(dst + sizeof(DES_bs_vector) * 8 * 5) = DES_bs_all.E.u[c];
	c = (unsigned char)key[6];
	*(dst + sizeof(DES_bs_vector) * 8 * 6) = DES_bs_all.E.u[c];
	return;
fill7:
	dst[0] = 0;
fill6:
	dst[sizeof(DES_bs_vector) * 8] = 0;
fill5:
	dst[sizeof(DES_bs_vector) * 8 * 2] = 0;
fill4:
	dst[sizeof(DES_bs_vector) * 8 * 3] = 0;
fill3:
	dst[sizeof(DES_bs_vector) * 8 * 4] = 0;
fill2:
	dst[sizeof(DES_bs_vector) * 8 * 5] = 0;
	dst[sizeof(DES_bs_vector) * 8 * 6] = 0;
}

static ARCH_WORD *DES_bs_get_binary_raw(ARCH_WORD *raw, int count)
{
	static ARCH_WORD out[2];

/* For odd iteration counts, swap L and R here instead of doing it one
 * more time in DES_bs_crypt(). */
	count &= 1;
	out[count] = raw[0];
	out[count ^ 1] = raw[1];

	return out;
}

ARCH_WORD *DES_bs_get_binary(char *ciphertext)
{
	return DES_bs_get_binary_raw(
		DES_raw_get_binary(ciphertext),
		DES_raw_get_count(ciphertext));
}

ARCH_WORD *DES_bs_get_binary_LM(char *ciphertext)
{
	ARCH_WORD block[2], value;
	int l, h;
	int index;

	block[0] = block[1] = 0;
	for (index = 0; index < 16; index += 2) {
		l = atoi16[ARCH_INDEX(ciphertext[index])];
		h = atoi16[ARCH_INDEX(ciphertext[index + 1])];
		value = DES_LM_reverse[l] | (DES_LM_reverse[h] << 4);
		block[index >> 3] |= value << ((index << 2) & 0x18);
	}

	return DES_bs_get_binary_raw(DES_do_IP(block), 1);
}

int DES_bs_get_hash(int index, int count)
{
	int result;
	DES_bs_vector *b;

	init_t();
	init_depth();
	b = (DES_bs_vector *)&DES_bs_all.B[0] DEPTH;

	result = (b[0] START >> index) & 1;
	result |= ((b[1] START >> index) & 1) << 1;
	result |= ((b[2] START >> index) & 1) << 2;
	result |= ((b[3] START >> index) & 1) << 3;
	if (count == 4) return result;

	result |= ((b[4] START >> index) & 1) << 4;
	result |= ((b[5] START >> index) & 1) << 5;
	result |= ((b[6] START >> index) & 1) << 6;
	result |= ((b[7] START >> index) & 1) << 7;
	if (count == 8) return result;

	result |= ((b[8] START >> index) & 1) << 8;
	result |= ((b[9] START >> index) & 1) << 9;
	result |= ((b[10] START >> index) & 1) << 10;
	result |= ((b[11] START >> index) & 1) << 11;
	if (count == 12) return result;

	result |= ((b[12] START >> index) & 1) << 12;
	result |= ((b[13] START >> index) & 1) << 13;
	result |= ((b[14] START >> index) & 1) << 14;
	result |= ((b[15] START >> index) & 1) << 15;
	if (count == 16) return result;

	result |= ((b[16] START >> index) & 1) << 16;
	result |= ((b[17] START >> index) & 1) << 17;
	result |= ((b[18] START >> index) & 1) << 18;
	result |= ((b[19] START >> index) & 1) << 19;

	return result;
}

/*
 * The trick used here allows to compare one ciphertext against all the
 * DES_bs_crypt*() outputs in just O(log2(ARCH_BITS)) operations, assuming
 * that DES_BS_VECTOR is 0 or 1. This routine isn't vectorized yet.
 */
int DES_bs_cmp_all(ARCH_WORD *binary, int count)
{
	ARCH_WORD value, mask;
	int bit;
	DES_bs_vector *b;
#if DES_BS_VECTOR
	int depth;
#endif
#if DES_bs_mt
	int t, n = (count + (DES_BS_DEPTH - 1)) / DES_BS_DEPTH;
#endif

	for_each_t(n)
	for_each_depth() {
		value = binary[0];
		b = (DES_bs_vector *)&DES_bs_all.B[0] DEPTH;

		mask = b[0] START ^ -(value & 1);
		mask |= b[1] START ^ -((value >> 1) & 1);
		if (mask == ~(ARCH_WORD)0) goto next_depth;
		mask |= b[2] START ^ -((value >> 2) & 1);
		mask |= b[3] START ^ -((value >> 3) & 1);
		if (mask == ~(ARCH_WORD)0) goto next_depth;
		value >>= 4;
		b += 4;
		for (bit = 4; bit < 32; bit += 2) {
			mask |= b[0] START ^
				-(value & 1);
			if (mask == ~(ARCH_WORD)0) goto next_depth;
			mask |= b[1] START ^
				-((value >> 1) & 1);
			if (mask == ~(ARCH_WORD)0) goto next_depth;
			value >>= 2;
			b += 2;
		}

		return 1;
next_depth:
		;
	}

	return 0;
}

int DES_bs_cmp_one(ARCH_WORD *binary, int count, int index)
{
	int bit;
	DES_bs_vector *b;

	init_t();
	init_depth();
	b = (DES_bs_vector *)&DES_bs_all.B[0] DEPTH;

	for (bit = 0; bit < 31; bit++, b++)
		if (((b[0] START >> index) ^ (binary[0] >> bit)) & 1) return 0;

	for (; bit < count; bit++, b++)
		if (((b[0] START >> index) ^
			(binary[bit >> 5] >> (bit & 0x1F))) & 1) return 0;

	return 1;
}

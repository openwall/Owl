/*
 * This file is part of John the Ripper password cracker,
 * Copyright (c) 1996-99,2003,2005,2008,2010-2013 by Solar Designer
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>

#include "arch.h"
#include "misc.h"
#include "params.h"
#include "path.h"
#include "memory.h"
#include "list.h"
#include "crc32.h"
#include "signals.h"
#include "loader.h"
#include "external.h"
#include "charset.h"

typedef unsigned int (*char_counters)
	[CHARSET_SIZE + 1][CHARSET_SIZE + 1][CHARSET_SIZE];

typedef unsigned int (*crack_counters)
	[CHARSET_LENGTH][CHARSET_LENGTH][CHARSET_SIZE];

static CRC32_t checksum;

static unsigned long charset_filter_plaintexts(struct db_main *db,
    struct list_main **lists)
{
	int length, old_length;
	unsigned long count;
	struct list_entry *current, *next;
	char *ptr, key[PLAINTEXT_BUFFER_SIZE];

	for (length = 0; length <= CHARSET_LENGTH; length++)
		list_init(&lists[length]);

	count = 0;

	if ((current = db->plaintexts->head))
	do {
		next = current->next;

		if (!current->data[0])
			continue;

		old_length = 0;
		ptr = current->data;
		if (f_filter) {
			old_length = strlen(current->data);
/*
 * The current->data string might happen to end near page boundary and the next
 * page might not be mapped, whereas ext_filter_body() may pre-read a few chars
 * beyond NUL for greater speed in uses during cracking.  Also, the external
 * filter() may make the string longer.  Finally, ext_filter_body() assumes
 * that the string passed to it fits in PLAINTEXT_BUFFER_SIZE.  Hence, we copy
 * the string here.
 */
			if (old_length < sizeof(key)) {
				memcpy(key, current->data, old_length + 1);
			} else {
				memcpy(key, current->data, sizeof(key) - 1);
				key[sizeof(key) - 1] = 0;
			}
			if (!ext_filter_body(key, key))
				continue;
			ptr = key;
		}

		length = 0;
		while (*ptr) {
			int c = *(unsigned char *)ptr;
			if (c < CHARSET_MIN || c > CHARSET_MAX)
				break;
			length++;
			ptr++;
		}

		if (!*ptr) {
			struct list_main *list;
/*
 * lists[CHARSET_LENGTH] is a catch-all for excessive length strings that
 * nevertheless consist exclusively of characters in the CHARSET_MIN to
 * CHARSET_MAX range (including in their portion beyond CHARSET_LENGTH).
 */
			if (length > CHARSET_LENGTH)
				list = lists[CHARSET_LENGTH];
			else
				list = lists[length - 1];
			if (old_length) {
				if (length > old_length) {
					list_add(list, key);
				} else {
					memcpy(current->data, key, length + 1);
					list_add_link(list, current);
				}
			} else {
/*
 * Truncate very long strings at PLAINTEXT_BUFFER_SIZE for consistency with
 * what would happen if we applied a dummy filter(), as we as for easy testing
 * against older revisions of this code.
 */
				if (length >= PLAINTEXT_BUFFER_SIZE)
					current->data
					    [PLAINTEXT_BUFFER_SIZE - 1] = 0;
				list_add_link(list, current);
			}
			count++;
		}
	} while ((current = next));

	return count;
}

static int cfputc(int c, FILE *stream)
{
	unsigned char ch;

	ch = c;
	CRC32_Update(&checksum, &ch, 1);

	return fputc(c, stream);
}

static void charset_checksum_header(struct charset_header *header)
{
	CRC32_Update(&checksum, header->version, sizeof(header->version));
	CRC32_Update(&checksum, &header->min, 1);
	CRC32_Update(&checksum, &header->max, 1);
	CRC32_Update(&checksum, &header->length, 1);
	CRC32_Update(&checksum, &header->count, 1);
	CRC32_Update(&checksum, header->offsets, sizeof(header->offsets));
	CRC32_Update(&checksum, header->order, sizeof(header->order));
	CRC32_Final(header->check, checksum);
}

static void charset_write_header(FILE *file, struct charset_header *header)
{
	fwrite(header->version, sizeof(header->version), 1, file);
	fwrite(header->check, sizeof(header->check), 1, file);
	fputc(header->min, file);
	fputc(header->max, file);
	fputc(header->length, file);
	fputc(header->count, file);
	fwrite(header->offsets, sizeof(header->offsets), 1, file);
	fwrite(header->order, sizeof(header->order), 1, file);
}

int charset_read_header(FILE *file, struct charset_header *header)
{
	if (fread(header->version, sizeof(header->version), 1, file) != 1 ||
	    fread(header->check, sizeof(header->check), 1, file) != 1)
		return -1;
	{
		unsigned char values[4];
		if (fread(values, sizeof(values), 1, file) != 1)
			return -1;
		header->min = values[0];
		header->max = values[1];
		header->length = values[2];
		header->count = values[3];
	}
	return
	    fread(header->offsets, sizeof(header->offsets), 1, file) != 1 ||
	    fread(header->order, sizeof(header->order), 1, file) != 1;
}

static int charset_new_length(int length,
	struct charset_header *header, FILE *file)
{
	int result;
	long offset;

	if ((result = length < CHARSET_LENGTH)) {
		printf("%d ", length + 1);
		fflush(stdout);

		if ((offset = ftell(file)) < 0) pexit("ftell");
		header->offsets[length][0] = offset;
		header->offsets[length][1] = offset >> 8;
		header->offsets[length][2] = offset >> 16;
		header->offsets[length][3] = offset >> 24;
	}

	return result;
}

typedef struct {
	int pos;
	unsigned int value;
} count_sort_t;

static int cmp_count(const void *p1, const void *p2)
{
	const count_sort_t *c1 = (const count_sort_t *)p1;
	const count_sort_t *c2 = (const count_sort_t *)p2;
	int diff = (int)c2->value - (int)c1->value;
	if (diff)
		return diff;
	return c1->pos - c2->pos;
}

static void charset_generate_chars(struct list_main **lists,
	FILE *file, struct charset_header *header,
	char_counters chars, crack_counters cracks)
{
	struct list_entry *current;
	unsigned char buffer[CHARSET_SIZE];
	count_sort_t pv[CHARSET_SIZE];
	int length, pos, count;
	int i, j, k;

/* Zeroize the same portion of "chars" as is used by the loop below */
	memset((*chars)[0][0], 0, sizeof((*chars)[0][0]));

	for (length = 0; length <= CHARSET_LENGTH; length++) {
		if ((current = lists[length]->head))
		do {
			char *ptr;
			for (ptr = current->data; *ptr; ptr++) {
				int c = *(unsigned char *)ptr;
				(*chars)[0][0][ARCH_INDEX(c - CHARSET_MIN)]++;
			}
		} while ((current = current->next));
	}

	count = 0;
	for (k = 0; k < CHARSET_SIZE; k++) {
		unsigned int value = (*chars)[0][0][k];
		if (value) {
			pv[count].pos = k;
			pv[count++].value = value;
		}
	}

	if (count > 1)
		qsort(pv, count, sizeof(pv[0]), cmp_count);

	for (k = 0; k < count; k++)
		buffer[k] = CHARSET_MIN + pv[k].pos;

	header->count = count;
	fwrite(buffer, 1, count, file);
	CRC32_Update(&checksum, buffer, count);

	for (length = 0; charset_new_length(length, header, file); length++)
	for (pos = 0; pos <= length; pos++) {
		if (event_abort) return;

		cfputc(CHARSET_ESC, file); cfputc(CHARSET_NEW, file);
		cfputc(length, file); cfputc(pos, file);

		if ((current = lists[length]->head))
		switch (pos) {
		case 0:
			memset((*chars)[CHARSET_SIZE][CHARSET_SIZE], 0,
			    sizeof((*chars)[CHARSET_SIZE][CHARSET_SIZE]));
			do {
				unsigned char *ptr =
				    (unsigned char *)current->data;
				int c = ARCH_INDEX(ptr[0] - CHARSET_MIN);
				(*chars)[CHARSET_SIZE][CHARSET_SIZE][c]++;
			} while ((current = current->next));
			break;
		case 1:
			memset((*chars)[CHARSET_SIZE], 0,
			    sizeof((*chars)[CHARSET_SIZE]));
			do {
				unsigned char *ptr =
				    (unsigned char *)current->data;
				int b = ARCH_INDEX(ptr[0] - CHARSET_MIN);
				int c = ARCH_INDEX(ptr[1] - CHARSET_MIN);
				(*chars)[CHARSET_SIZE][b][c]++;
				(*chars)[CHARSET_SIZE][CHARSET_SIZE][c]++;
			} while ((current = current->next));
			break;
		default:
			memset(chars, 0, sizeof(*chars));
			do {
				unsigned char *ptr =
				    (unsigned char *)current->data;
				int a = ARCH_INDEX(ptr[pos - 2] - CHARSET_MIN);
				int b = ARCH_INDEX(ptr[pos - 1] - CHARSET_MIN);
				int c = ARCH_INDEX(ptr[pos] - CHARSET_MIN);
				(*chars)[a][b][c]++;
				(*chars)[CHARSET_SIZE][b][c]++;
				(*chars)[CHARSET_SIZE][CHARSET_SIZE][c]++;
			} while ((current = current->next));
		}

		for (i = (pos > 1 ? 0 : CHARSET_SIZE); i <= CHARSET_SIZE; i++)
		for (j = (pos ? 0 : CHARSET_SIZE); j <= CHARSET_SIZE; j++) {
			count = 0;
			for (k = 0; k < CHARSET_SIZE; k++) {
				unsigned int value = (*chars)[i][j][k];
				if (value) {
					pv[count].pos = k;
					pv[count++].value = value;
				}
			}

			if (!count)
				continue;

			if (count > 1)
				qsort(pv, count, sizeof(pv[0]), cmp_count);

			if (i == CHARSET_SIZE && j == CHARSET_SIZE)
				for (k = 0; k < count; k++)
					(*cracks)[length][pos][k] = pv[k].value;

			for (k = 0; k < count; k++)
				buffer[k] = CHARSET_MIN + pv[k].pos;

			cfputc(CHARSET_ESC, file);
			cfputc(CHARSET_LINE, file);
			cfputc(i, file); cfputc(j, file);
			fwrite(buffer, 1, count, file);
			CRC32_Update(&checksum, buffer, count);
		}
	}

	cfputc(CHARSET_ESC, file); cfputc(CHARSET_NEW, file);
	cfputc(CHARSET_LENGTH, file);
}

static double powi(int x, unsigned int y)
{
	double a = 1.0;
	if (y) {
		double b = x;
		do {
			if (y & 1)
				a *= b;
			if (!(y >>= 1))
				break;
			b *= b;
		} while (1);
	}
	return a;
}

typedef struct {
	int length, pos, count;
	double value;
} ratio_sort_t;

static int cmp_ratio(const void *p1, const void *p2)
{
	const ratio_sort_t *r1 = (const ratio_sort_t *)p1;
	const ratio_sort_t *r2 = (const ratio_sort_t *)p2;
	int diff;
	if (r1->value < r2->value)
		return -1;
	if (r1->value > r2->value)
		return 1;
	diff = r1->length - r2->length;
	if (diff)
		return diff;
#if 1
	diff = r1->count - r2->count;
	if (diff)
		return diff;
	return r1->pos - r2->pos;
#else
/*
 * Stabilize the sorting order differently for testing against older revisions
 * of the code.  This kind of stabilization is arguably illogical and it tends
 * to require many more recalculations.
 */
	diff = r1->pos - r2->pos;
	if (diff)
		return diff;
	return r1->count - r2->count;
#endif
}

/*
 * This generates the "cracking order" (please see the comment in charset.h)
 * based on the number of candidate passwords for each {length, fixed index
 * position, character count} combination, and on the number of cracked
 * passwords for that combination.  The idea is to start with combinations for
 * which the ratio between the number of candidates and the number of
 * successful cracks is the smallest.  This way, the expected number of
 * successful cracks per unit of time will be monotonically non-increasing
 * over time.  Of course, this applies to the expectation only (based on
 * available statistics) - actual behavior (on a yet unknown set of passwords
 * to be cracked) may and likely will differ.  Additionally, there are some
 * algorithmic constraints, which may force us to deviate from the perfect
 * monotonically non-decreasing sequence of ratios.
 *
 * The cracks[] array is used as input (containing the number of successful
 * cracks for each combination).
 */
static void charset_generate_order(crack_counters cracks,
	unsigned char *order, int size)
{
	int length, pos, count; /* zero-based */
	int nratios, taken;
	double total;
	unsigned char *ptr, *end;
	ratio_sort_t (*ratios)
	    [CHARSET_LENGTH * (CHARSET_LENGTH + 1) / 2 * CHARSET_SIZE];
	int counts[CHARSET_LENGTH][CHARSET_LENGTH];
	int recalcs;
	unsigned char *prev_order;

	ratios = mem_alloc(sizeof(*ratios));

/* Calculate the ratios */

	nratios = 0;
	for (length = 0; length < CHARSET_LENGTH; length++)
	for (count = 0; count < CHARSET_SIZE; count++) {
/* First, calculate the number of candidate passwords for this combination of
 * length and count (number of different character indices).  We subtract the
 * number of candidates for the previous count (at the same length) because
 * those are to be tried as a part of another combination. */
		total = powi(count + 1, length + 1) - powi(count, length + 1);

/* Calculate the number of candidates for a {length, fixed index position,
 * character count} combination, for the specific values of length and count.
 * Obviously, this value is the same for each position in which the character
 * index is fixed - it only depends on the length and count - which is why we
 * calculate it out of the inner loop. */
		if (count)
			total /= length + 1;

/* Finally, for each fixed index position separately, calculate the candidates
 * to successful cracks ratio.  We treat combinations with no successful cracks
 * (so far) the same as those with exactly one successful crack. */
		for (pos = 0; pos <= length; pos++) {
			double ratio = total;
			unsigned int div = (*cracks)[length][pos][count];
			if (div)
				ratio /= div;
			(*ratios)[nratios].length = length;
			(*ratios)[nratios].pos = pos;
			(*ratios)[nratios].count = count;
			(*ratios)[nratios++].value = ratio;
		}
	}

	prev_order = NULL;
	recalcs = 0;

again:

	assert(nratios == sizeof(*ratios) / sizeof((*ratios)[0]));

/*
 * Fill out the order[] with combinations sorted for (mostly) non-decreasing
 * ratios (except as we may have to deviate from this to meet the
 * "count == counts[length][pos]" constraint).
 */

	qsort(ratios, nratios, sizeof((*ratios)[0]), cmp_ratio);

	memset(counts, 0, sizeof(counts));

	taken = 0;
	ptr = order;
	do {
/* Find the minimum non-taken ratio and its corresponding combination */
		int found = 0, alltaken = 1;
		int i;

		for (i = taken; i < nratios; i++) {
			if ((*ratios)[i].value < 0.0) {
				if (alltaken && taken < i)
					taken = i;
				continue;
			}
			alltaken = 0;
			length = (*ratios)[i].length;
			pos = (*ratios)[i].pos;
			count = (*ratios)[i].count;
			if (count == counts[length][pos]) {
				found = 1;
				break;
			}
		}

		if (!found)
			break;

		counts[length][pos]++;

/* Record the combination and "take" it out of the input array */
		(*ratios)[i].value = -1.0; /* taken */
		assert(ptr <= order + size - 3);
		*ptr++ = length;
		*ptr++ = pos;
		*ptr++ = count;
	} while (!event_abort);

	if (event_abort)
		goto out;

	assert(ptr == order + size);

	end = ptr;

	if (prev_order) {
		int stable = !memcmp(order, prev_order, end - order);
		if (++recalcs >= 1000 || stable) {
			printf("%stable order (%d recalculations)\n",
			    stable ? "S" : "Uns", recalcs);
			goto out;
		}
	} else {
		prev_order = mem_alloc(end - order);
	}
	memcpy(prev_order, order, end - order);

/* Recalculate the ratios */

	memset(counts, 0, sizeof(counts));
	ptr = order;
	nratios = 0;
	do {
		double est;

		length = *ptr++;
		pos = *ptr++;
		count = *ptr++;
		counts[length][pos] = count;

/* First calculate the number of candidate passwords */
		total = 1.0;
		{
			int i;
			for (i = 0; i <= length; i++)
			if (i != pos)
				total *= counts[length][i] + 1;
		}

/* Then calculate the candidates to successful cracks ratio */
		{
			int i, j;
			est = 1.0; /* estimated cracks for this portion */
			for (i = 0; i <= length; i++)
			if (i != pos) {
				unsigned int sum = 0;
				double tmp = 0.0;
				for (j = 0; j <= counts[length][i]; j++)
					tmp += (*cracks)[length][i][j];
				for (j = 0; j < CHARSET_SIZE; j++)
					sum += (*cracks)[length][i][j];
				if (sum)
					tmp /= sum;
				est *= tmp;
			}
			est *= (*cracks)[length][pos][count];
			if (est < 1e-3) /* may adjust this */
				est = 1e-3;
		}
		(*ratios)[nratios].length = length;
		(*ratios)[nratios].pos = pos;
		(*ratios)[nratios].count = count;
		(*ratios)[nratios++].value = total / est;
	} while (ptr < end);

	if (!event_abort)
		goto again;

out:
	MEM_FREE(prev_order);
	MEM_FREE(ratios);
}

static void charset_generate_all(struct list_main **lists, char *charset)
{
	FILE *file;
	int was_error;
	struct charset_header *header;
	char_counters chars;
	crack_counters cracks;

	header = (struct charset_header *)mem_alloc(sizeof(*header));
	memset(header, 0, sizeof(*header));

	chars = (char_counters)mem_alloc(sizeof(*chars));

	cracks = (crack_counters)mem_alloc(sizeof(*cracks));

	if (!(file = fopen(path_expand(charset), "wb")))
		pexit("fopen: %s", path_expand(charset));

	charset_write_header(file, header);

	printf("Generating charsets... ");
	fflush(stdout);

	charset_generate_chars(lists, file, header, chars, cracks);
	if (event_abort) {
		fclose(file);
		unlink(charset);
		putchar('\n'); check_abort(0);
	}

	printf("DONE\nGenerating cracking order... ");
	fflush(stdout);

	charset_generate_order(cracks, header->order, sizeof(header->order));
	if (event_abort) {
		fclose(file);
		unlink(charset);
		putchar('\n'); check_abort(0);
	}

	fflush(file);
	if (!ferror(file) && !fseek(file, 0, SEEK_SET)) {
		strncpy(header->version, CHARSET_V, sizeof(header->version));
		header->min = CHARSET_MIN;
		header->max = CHARSET_MAX;
		header->length = CHARSET_LENGTH;
		charset_checksum_header(header);
		charset_write_header(file, header);
	}

	MEM_FREE(cracks);
	MEM_FREE(chars);

	was_error = ferror(file);
	if (fclose(file) || was_error) {
		unlink(charset);
		fprintf(stderr, "Failed to write charset file: %s\n", charset);
		error();
	}

	printf("Successfully written charset file: %s (%d character%s)\n",
		charset, header->count, header->count != 1 ? "s" : "");

	MEM_FREE(header);
}

void do_makechars(struct db_main *db, char *charset)
{
	struct list_main *lists[CHARSET_LENGTH + 1];
	unsigned long total, remaining;

	total = db->plaintexts->count;

	printf("Loaded %lu plaintext%s%s\n",
		total,
		total != 1 ? "s" : "",
		total ? "" : ", exiting...");

	remaining = charset_filter_plaintexts(db, lists);

	if (remaining < total)
		printf("Remaining %lu plaintext%s%s\n",
			remaining,
			remaining != 1 ? "s" : "",
			remaining ? "" : ", exiting...");

	if (!remaining)
		return;

	CRC32_Init(&checksum);

	charset_generate_all(lists, charset);
}

/*
 * This file is part of John the Ripper password cracker,
 * Copyright (c) 1996-2001,2003,2004,2006,2008,2009 by Solar Designer
 */

#ifdef __ultrix__
#define __POSIX
#define _POSIX_SOURCE
#endif

#ifdef _SCO_C_DIALECT
#include <limits.h>
#endif
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <time.h>
#include <sys/time.h>
#include <sys/times.h>

#include "times.h"

#include "arch.h"
#include "misc.h"
#include "math.h"
#include "params.h"
#include "memory.h"
#include "signals.h"
#include "formats.h"
#include "bench.h"

long clk_tck = 0;

void clk_tck_init(void)
{
	if (clk_tck) return;

#if defined(_SC_CLK_TCK) || !defined(CLK_TCK)
	clk_tck = sysconf(_SC_CLK_TCK);
#else
	clk_tck = CLK_TCK;
#endif
}

unsigned int benchmark_time = BENCHMARK_TIME;

static volatile int bench_running;

static void bench_handle_timer(int signum)
{
	bench_running = 0;
}

static void bench_set_keys(struct fmt_main *format,
	struct fmt_tests *current, int cond)
{
	char *plaintext;
	int index, length;

	format->methods.clear_keys();

	length = format->params.benchmark_length;
	for (index = 0; index < format->params.max_keys_per_crypt; index++) {
		do {
			if (!current->ciphertext)
				current = format->params.tests;
			plaintext = current->plaintext;
			current++;

			if (cond > 0) {
				if ((int)strlen(plaintext) > length) break;
			} else
			if (cond < 0) {
				if ((int)strlen(plaintext) <= length) break;
			} else
				break;
		} while (1);

		format->methods.set_key(plaintext, index);
	}
}

char *benchmark_format(struct fmt_main *format, int salts,
	struct bench_results *results)
{
	static void *binary = NULL;
	static int binary_size = 0;
	static char s_error[64];
	char *where;
	struct fmt_tests *current;
	int cond;
#if OS_TIMER
	struct itimerval it;
#endif
	struct tms buf;
	clock_t start_real, start_virtual, end_real, end_virtual;
	unsigned ARCH_WORD count;
	char *ciphertext;
	void *salt, *two_salts[2];
	int index, max;

	clk_tck_init();

	if (!(current = format->params.tests)) return "FAILED (no data)";
	if ((where = fmt_self_test(format))) {
		sprintf(s_error, "FAILED (%s)", where);
		return s_error;
	}

	if (format->params.binary_size > binary_size) {
		binary_size = format->params.binary_size;
		binary = mem_alloc_tiny(binary_size, MEM_ALIGN_WORD);
		memset(binary, 0x55, binary_size);
	}

	for (index = 0; index < 2; index++) {
		two_salts[index] = mem_alloc(format->params.salt_size);

		if ((ciphertext = format->params.tests[index].ciphertext))
			salt = format->methods.salt(ciphertext);
		else
			salt = two_salts[0];

		memcpy(two_salts[index], salt, format->params.salt_size);
	}

	if (format->params.benchmark_length > 0) {
		cond = (salts == 1) ? 1 : -1;
		salts = 1;
	} else
		cond = 0;

	bench_set_keys(format, current, cond);

#if OS_TIMER
	memset(&it, 0, sizeof(it));
	if (setitimer(ITIMER_REAL, &it, NULL)) pexit("setitimer");
#endif

	bench_running = 1;
	signal(SIGALRM, bench_handle_timer);

/* Cap it at a sane value to hopefully avoid integer overflows below */
	if (benchmark_time > 3600)
		benchmark_time = 3600;

/* In the future, "zero time" may mean self-tests without benchmarks */
	if (!benchmark_time)
		benchmark_time = 1;

#if OS_TIMER
	it.it_value.tv_sec = benchmark_time;
	if (setitimer(ITIMER_REAL, &it, NULL)) pexit("setitimer");
#else
	sig_timer_emu_init(benchmark_time * clk_tck);
#endif

	start_real = times(&buf);
	start_virtual = buf.tms_utime + buf.tms_stime;
	count = 0;

	index = salts;
	max = format->params.max_keys_per_crypt;
	do {
		if (!--index) {
			index = salts;
			if (!(++current)->ciphertext)
				current = format->params.tests;
			bench_set_keys(format, current, cond);
		}

		if (salts > 1) format->methods.set_salt(two_salts[index & 1]);
		format->methods.crypt_all(max);
		format->methods.cmp_all(binary, max);

		count++;
#if !OS_TIMER
		sig_timer_emu_tick();
#endif
	} while (bench_running && !event_abort);

	end_real = times(&buf);
	end_virtual = buf.tms_utime + buf.tms_stime;
	if (end_virtual == start_virtual) end_virtual++;

	results->real = end_real - start_real;
	results->virtual = end_virtual - start_virtual;
	results->count = count * max;

	for (index = 0; index < 2; index++)
		MEM_FREE(two_salts[index]);

	return event_abort ? "" : NULL;
}

void benchmark_cps(unsigned ARCH_WORD count, clock_t time, char *buffer)
{
	unsigned int cps_hi, cps_lo;
	int64 tmp;

	tmp.lo = count; tmp.hi = 0;
	mul64by32(&tmp, clk_tck);
	cps_hi = div64by32lo(&tmp, time);

	if (cps_hi >= 1000000)
		sprintf(buffer, "%uK", cps_hi / 1000);
	else
	if (cps_hi >= 100)
		sprintf(buffer, "%u", cps_hi);
	else {
		mul64by32(&tmp, 10);
		cps_lo = div64by32lo(&tmp, time) % 10;
		sprintf(buffer, "%u.%u", cps_hi, cps_lo);
	}
}

int benchmark_all(void)
{
	struct fmt_main *format;
	char *result, *msg_1, *msg_m;
	struct bench_results results_1, results_m;
	char s_real[64], s_virtual[64];
	unsigned int total, failed;

	total = failed = 0;
	if ((format = fmt_list))
	do {
		printf("Benchmarking: %s%s [%s]... ",
			format->params.format_name,
			format->params.benchmark_comment,
			format->params.algorithm_name);
		fflush(stdout);

		switch (format->params.benchmark_length) {
		case -1:
			msg_m = "Raw";
			msg_1 = NULL;
			break;

		case 0:
			msg_m = "Many salts";
			msg_1 = "Only one salt";
			break;

		default:
			msg_m = "Short";
			msg_1 = "Long";
		}

		total++;

		if ((result = benchmark_format(format,
		    format->params.salt_size ? BENCHMARK_MANY : 1,
		    &results_m))) {
			puts(result);
			failed++;
			continue;
		}

		if (msg_1)
		if ((result = benchmark_format(format, 1, &results_1))) {
			puts(result);
			failed++;
			continue;
		}

		puts("DONE");

		benchmark_cps(results_m.count, results_m.real, s_real);
		benchmark_cps(results_m.count, results_m.virtual, s_virtual);
#if !defined(__DJGPP__) && !defined(__CYGWIN32__) && !defined(__BEOS__)
		printf("%s:\t%s c/s real, %s c/s virtual\n",
			msg_m, s_real, s_virtual);
#else
		printf("%s:\t%s c/s\n",
			msg_m, s_real);
#endif

		if (!msg_1) {
			putchar('\n');
			continue;
		}

		benchmark_cps(results_1.count, results_1.real, s_real);
		benchmark_cps(results_1.count, results_1.virtual, s_virtual);
#if !defined(__DJGPP__) && !defined(__CYGWIN32__) && !defined(__BEOS__)
		printf("%s:\t%s c/s real, %s c/s virtual\n\n",
			msg_1, s_real, s_virtual);
#else
		printf("%s:\t%s c/s\n\n",
			msg_1, s_real);
#endif
	} while ((format = format->next) && !event_abort);

	if (failed && total > 1 && !event_abort)
		printf("%u out of %u tests have FAILED\n", failed, total);

	return failed || event_abort;
}

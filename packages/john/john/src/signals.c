/*
 * This file is part of John the Ripper password cracker,
 * Copyright (c) 1996-2001 by Solar Designer
 */

#ifdef __ultrix__
#define __POSIX
#define _POSIX_SOURCE
#endif

#ifdef _SCO_C_DIALECT
#include <limits.h>
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/time.h>
#include <errno.h>

#ifdef __DJGPP__
#include <dos.h>
#endif

#ifdef __CYGWIN32__
#include <windows.h>
#endif

#include "arch.h"
#include "misc.h"
#include "params.h"
#include "tty.h"
#include "config.h"

volatile int event_pending = 0;
volatile int event_abort = 0, event_save = 0, event_status = 0;

static int timer_save_interval, timer_save_value;

#if !OS_TIMER

#include <time.h>
#include <sys/times.h>

static clock_t timer_emu_interval = 0;
static unsigned int timer_emu_count = 0, timer_emu_max = 0;

void sig_timer_emu_init(clock_t interval)
{
	timer_emu_interval = interval;
	timer_emu_count = 0; timer_emu_max = 0;
}

void sig_timer_emu_tick(void)
{
	static clock_t last = 0;
	clock_t current;
	struct tms buf;

	if (++timer_emu_count < timer_emu_max) return;

	current = times(&buf);

	if (!last) {
		last = current;
		return;
	}

	if (current - last < timer_emu_interval && current >= last) {
		timer_emu_max += timer_emu_max + 1;
		return;
	}

	last = current;
	timer_emu_count = 0;
	timer_emu_max >>= 1;

	raise(SIGALRM);
}

#endif

static void sig_install_update(void);

static void sig_handle_update(int signum)
{
	event_save = event_pending = 1;

#ifndef SA_RESTART
	sig_install_update();
#endif
}

static void sig_install_update(void)
{
#ifdef SA_RESTART
	struct sigaction sa;

	memset(&sa, 0, sizeof(sa));
	sa.sa_handler = sig_handle_update;
	sa.sa_flags = SA_RESTART;
	sigaction(SIGHUP, &sa, NULL);
#else
	signal(SIGHUP, sig_handle_update);
#endif
}

static void sig_remove_update(void)
{
	signal(SIGHUP, SIG_IGN);
}

void check_abort(void)
{
	if (event_abort) {
		fprintf(stderr, "Session aborted\n");
		error();
	}
}

static void sig_install_abort(void);

#ifdef __CYGWIN32__
static BOOL sig_handle_abort(DWORD ctrltype)
#else
static void sig_handle_abort(int signum)
#endif
{
	int saved_errno = errno;

	check_abort();

	event_abort = event_pending = 1;

	fprintf(stderr, "Wait...\r");

#ifdef __CYGWIN32__
	errno = saved_errno;
	return TRUE;
#else
	sig_install_abort();
	errno = saved_errno;
#endif
}

static void sig_install_abort(void)
{
#ifdef __DJGPP__
	setcbrk(1);
#endif

#ifdef __CYGWIN32__
#ifdef __CYGWIN__
	SetConsoleCtrlHandler((PHANDLER_ROUTINE)sig_handle_abort, TRUE);
#else
	SetConsoleCtrlHandler((HANDLER_ROUTINE *)sig_handle_abort, TRUE);
#endif
#else
	signal(SIGINT, sig_handle_abort);
	signal(SIGTERM, sig_handle_abort);
#ifdef SIGXCPU
	signal(SIGXCPU, sig_handle_abort);
#endif
#endif
}

static void sig_remove_abort(void)
{
	signal(SIGINT, SIG_DFL);
	signal(SIGTERM, SIG_DFL);
}

#ifdef __CYGWIN32__

static int sig_getchar(void)
{
	int c;

	if ((c = tty_getchar()) == 3) {
		sig_handle_abort(CTRL_C_EVENT);
		return -1;
	}

	return c;
}

#else

#define sig_getchar tty_getchar

#endif

static void sig_install_timer(void);

static void sig_handle_timer(int signum)
{
	int saved_errno = errno;

	if (!--timer_save_value) {
		timer_save_value = timer_save_interval;

		event_save = event_pending = 1;
	}

	if (sig_getchar() >= 0) {
		while (sig_getchar() >= 0);

		event_status = event_pending = 1;
	}

#if !OS_TIMER
	signal(SIGALRM, sig_handle_timer);
#elif !defined(SA_RESTART) && !defined(__DJGPP__)
	sig_install_timer();
#endif

	errno = saved_errno;
}

static void sig_install_timer(void)
{
#if !OS_TIMER
	signal(SIGALRM, sig_handle_timer);
	sig_timer_emu_init(TIMER_INTERVAL * CLK_TCK);
#else
	struct sigaction sa;
	struct itimerval it;

	memset(&sa, 0, sizeof(sa));
	sa.sa_handler = sig_handle_timer;
#ifdef SA_RESTART
	sa.sa_flags = SA_RESTART;
#endif
	sigaction(SIGALRM, &sa, NULL);
#if !defined(SA_RESTART) && !defined(__DJGPP__)
	siginterrupt(SIGALRM, 0);
#endif

	it.it_value.tv_sec = TIMER_INTERVAL;
	it.it_value.tv_usec = 0;
#if defined(SA_RESTART) || defined(__DJGPP__)
	it.it_interval = it.it_value;
#else
	memset(&it.it_interval, 0, sizeof(it.it_interval));
#endif
	if (setitimer(ITIMER_REAL, &it, NULL)) pexit("setitimer");
#endif
}

static void sig_remove_timer(void)
{
#if OS_TIMER
	struct itimerval it;

	memset(&it, 0, sizeof(it));
	if (setitimer(ITIMER_REAL, &it, NULL)) pexit("setitimer");
#endif

	signal(SIGALRM, SIG_DFL);
}

static void sig_done(void);

void sig_init(void)
{
	timer_save_interval = cfg_get_int(SECTION_OPTIONS, NULL, "Save");
	if (timer_save_interval < 0)
		timer_save_interval = TIMER_SAVE_DELAY;
	else
	if ((timer_save_interval /= TIMER_INTERVAL) <= 0)
		timer_save_interval = 1;
	timer_save_value = timer_save_interval;

	atexit(sig_done);

	sig_install_update();
	sig_install_abort();
	sig_install_timer();
}

static void sig_done(void)
{
	sig_remove_update();
	sig_remove_abort();
	sig_remove_timer();
}

/*
 * This file is part of John the Ripper password cracker,
 * Copyright (c) 1996-2004,2006,2009-2011 by Solar Designer
 */

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>

#include "arch.h"
#include "misc.h"
#include "params.h"
#include "path.h"
#include "memory.h"
#include "list.h"
#include "tty.h"
#include "signals.h"
#include "common.h"
#include "idle.h"
#include "formats.h"
#include "loader.h"
#include "logger.h"
#include "status.h"
#include "options.h"
#include "config.h"
#include "bench.h"
#include "charset.h"
#include "single.h"
#include "wordlist.h"
#include "inc.h"
#include "external.h"
#include "batch.h"

#if CPU_DETECT
extern int CPU_detect(void);
#endif

extern struct fmt_main fmt_DES, fmt_BSDI, fmt_MD5, fmt_BF;
extern struct fmt_main fmt_AFS, fmt_LM;
#ifdef HAVE_CRYPT
extern struct fmt_main fmt_crypt;
#endif
extern struct fmt_main fmt_trip;
extern struct fmt_main fmt_dummy;

extern int unshadow(int argc, char **argv);
extern int unafs(int argc, char **argv);
extern int unique(int argc, char **argv);

static struct db_main database;
static struct fmt_main dummy_format;

static int exit_status = 0;

static void john_register_one(struct fmt_main *format)
{
	if (options.format)
	if (strcmp(options.format, format->params.label)) return;

	fmt_register(format);
}

static void john_register_all(void)
{
	if (options.format) strlwr(options.format);

	john_register_one(&fmt_DES);
	john_register_one(&fmt_BSDI);
	john_register_one(&fmt_MD5);
	john_register_one(&fmt_BF);
	john_register_one(&fmt_AFS);
	john_register_one(&fmt_LM);
#ifdef HAVE_CRYPT
	john_register_one(&fmt_crypt);
#endif
	john_register_one(&fmt_trip);
	john_register_one(&fmt_dummy);

	if (!fmt_list) {
		fprintf(stderr, "Unknown ciphertext format name requested\n");
		error();
	}
}

static void john_log_format(void)
{
	int min_chunk, chunk;

	log_event("- Hash type: %.100s (lengths up to %d%s)",
		database.format->params.format_name,
		database.format->params.plaintext_length,
		database.format->methods.split != fmt_default_split ?
		", longer passwords split" : "");

	log_event("- Algorithm: %.100s",
		database.format->params.algorithm_name);

	chunk = min_chunk = database.format->params.max_keys_per_crypt;
	if (options.flags & (FLG_SINGLE_CHK | FLG_BATCH_CHK) &&
	    chunk < SINGLE_HASH_MIN)
			chunk = SINGLE_HASH_MIN;
	if (chunk > 1)
		log_event("- Candidate passwords %s be buffered and "
			"tried in chunks of %d",
			min_chunk > 1 ? "will" : "may",
			chunk);
}

static char *john_loaded_counts(void)
{
	static char s_loaded_counts[80];

	if (database.password_count == 1)
		return "1 password hash";

	sprintf(s_loaded_counts,
		database.salt_count > 1 ?
		"%d password hashes with %d different salts" :
		"%d password hashes with no different salts",
		database.password_count,
		database.salt_count);

	return s_loaded_counts;
}

static void john_load(void)
{
	struct list_entry *current;

	umask(077);

	if (options.flags & FLG_EXTERNAL_CHK)
		ext_init(options.external);

	if (options.flags & FLG_MAKECHR_CHK) {
		options.loader.flags |= DB_CRACKED;
		ldr_init_database(&database, &options.loader);

		if (options.flags & FLG_PASSWD) {
			ldr_show_pot_file(&database, POT_NAME);

			database.options->flags |= DB_PLAINTEXTS;
			if ((current = options.passwd->head))
			do {
				ldr_show_pw_file(&database, current->data);
			} while ((current = current->next));
		} else {
			database.options->flags |= DB_PLAINTEXTS;
			ldr_show_pot_file(&database, POT_NAME);
		}

		return;
	}

	if (options.flags & FLG_STDOUT) {
		ldr_init_database(&database, &options.loader);
		database.format = &dummy_format;
		memset(&dummy_format, 0, sizeof(dummy_format));
		dummy_format.params.plaintext_length = options.length;
		dummy_format.params.flags = FMT_CASE | FMT_8_BIT;
	}

	if (options.flags & FLG_PASSWD) {
		int total;

		if (options.flags & FLG_SHOW_CHK) {
			options.loader.flags |= DB_CRACKED;
			ldr_init_database(&database, &options.loader);

			ldr_show_pot_file(&database, POT_NAME);

			if ((current = options.passwd->head))
			do {
				ldr_show_pw_file(&database, current->data);
			} while ((current = current->next));

			printf("%s%d password hash%s cracked, %d left\n",
				database.guess_count ? "\n" : "",
				database.guess_count,
				database.guess_count != 1 ? "es" : "",
				database.password_count -
				database.guess_count);

			return;
		}

		if (options.flags & (FLG_SINGLE_CHK | FLG_BATCH_CHK) &&
		    status.pass <= 1)
			options.loader.flags |= DB_WORDS;
		else
		if (mem_saving_level)
			options.loader.flags &= ~DB_LOGIN;
		ldr_init_database(&database, &options.loader);

		if ((current = options.passwd->head))
		do {
			ldr_load_pw_file(&database, current->data);
		} while ((current = current->next));

		if ((options.flags & FLG_CRACKING_CHK) &&
		    database.password_count) {
			log_init(LOG_NAME, NULL, options.session);
			if (status_restored_time)
				log_event("Continuing an interrupted session");
			else
				log_event("Starting a new session");
			log_event("Loaded a total of %s", john_loaded_counts());
			printf("Loaded %s (%s [%s])\n",
				john_loaded_counts(),
				database.format->params.format_name,
				database.format->params.algorithm_name);
		}

		total = database.password_count;
		ldr_load_pot_file(&database, POT_NAME);
		ldr_fix_database(&database);

		if (!database.password_count) {
			log_discard();
			printf("No password hashes %s (see FAQ)\n",
			    total ? "left to crack" : "loaded");
		} else
		if (database.password_count < total) {
			log_event("Remaining %s", john_loaded_counts());
			printf("Remaining %s\n", john_loaded_counts());
		}

		if ((options.flags & FLG_PWD_REQ) && !database.salts) exit(0);
	}
}

static void john_init(char *name, int argc, char **argv)
{
	int make_check = (argc == 2 && !strcmp(argv[1], "--make_check"));
	if (make_check)
		argv[1] = "--test=0";

#if CPU_DETECT
	if (!CPU_detect()) {
#if CPU_REQ
#if CPU_FALLBACK
#if defined(__DJGPP__) || defined(__CYGWIN32__)
#error CPU_FALLBACK is incompatible with the current DOS and Win32 code
#endif
		if (!make_check) {
#define CPU_FALLBACK_PATHNAME JOHN_SYSTEMWIDE_EXEC "/" CPU_FALLBACK_BINARY
			execv(CPU_FALLBACK_PATHNAME, argv);
			perror("execv: " CPU_FALLBACK_PATHNAME);
		}
#endif
		fprintf(stderr, "Sorry, %s is required\n", CPU_NAME);
		if (make_check)
			exit(0);
		error();
#endif
	}
#endif

	if (!make_check) {
		path_init(argv);

#if JOHN_SYSTEMWIDE
		cfg_init(CFG_PRIVATE_FULL_NAME, 1);
		cfg_init(CFG_PRIVATE_ALT_NAME, 1);
#endif
		cfg_init(CFG_FULL_NAME, 1);
		cfg_init(CFG_ALT_NAME, 0);
	}

	status_init(NULL, 1);
	if (argc < 2)
		john_register_all(); /* for printing by opt_init() */
	opt_init(name, argc, argv);
	john_register_all(); /* maybe restricted to one format by options */
	common_init();
	sig_init();

	john_load();
}

static void john_run(void)
{
	if (options.flags & FLG_TEST_CHK)
		exit_status = benchmark_all() ? 1 : 0;
	else
	if (options.flags & FLG_MAKECHR_CHK)
		do_makechars(&database, options.charset);
	else
	if (options.flags & FLG_CRACKING_CHK) {
		int remaining = database.password_count;

		if (!(options.flags & FLG_STDOUT)) {
			status_init(NULL, 1);
			log_init(LOG_NAME, POT_NAME, options.session);
			john_log_format();
			if (idle_requested(database.format))
				log_event("- Configured to use otherwise idle "
					"processor cycles only");
		}
		tty_init(options.flags & FLG_STDIN_CHK);

		if (options.flags & FLG_SINGLE_CHK)
			do_single_crack(&database);
		else
		if (options.flags & FLG_WORDLIST_CHK)
			do_wordlist_crack(&database, options.wordlist,
				(options.flags & FLG_RULES) != 0);
		else
		if (options.flags & FLG_INC_CHK)
			do_incremental_crack(&database, options.charset);
		else
		if (options.flags & FLG_EXTERNAL_CHK)
			do_external_crack(&database);
		else
		if (options.flags & FLG_BATCH_CHK)
			do_batch_crack(&database);

		status_print();
		tty_done();

		if (database.password_count < remaining) {
			char *might = "Warning: passwords printed above might";
			char *partial = " be partial";
			char *not_all = " not be all those cracked";
			switch (database.options->flags &
			    (DB_SPLIT | DB_NODUP)) {
			case DB_SPLIT:
				fprintf(stderr, "%s%s\n", might, partial);
				break;
			case DB_NODUP:
				fprintf(stderr, "%s%s\n", might, not_all);
				break;
			case (DB_SPLIT | DB_NODUP):
				fprintf(stderr, "%s%s and%s\n",
				    might, partial, not_all);
			}
			fputs("Use the \"--show\" option to display all of "
			    "the cracked passwords reliably\n", stderr);
		}
	}
}

static void john_done(void)
{
	path_done();

	if ((options.flags & FLG_CRACKING_CHK) &&
	    !(options.flags & FLG_STDOUT)) {
		if (event_abort)
			log_event("Session aborted");
		else
			log_event("Session completed");
	}
	log_done();
	check_abort(0);
}

int main(int argc, char **argv)
{
	char *name;

#ifdef __DJGPP__
	if (--argc <= 0) return 1;
	if ((name = strrchr(argv[0], '/')))
		strcpy(name + 1, argv[1]);
	name = argv[1];
	argv[1] = argv[0];
	argv++;
#else
	if (!argv[0])
		name = "john";
	else
	if ((name = strrchr(argv[0], '/')))
		name++;
	else
		name = argv[0];
#endif

#ifdef __CYGWIN32__
	strlwr(name);
	if (strlen(name) > 4 && !strcmp(name + strlen(name) - 4, ".exe"))
		name[strlen(name) - 4] = 0;
#endif

	if (!strcmp(name, "unshadow"))
		return unshadow(argc, argv);

	if (!strcmp(name, "unafs"))
		return unafs(argc, argv);

	if (!strcmp(name, "unique"))
		return unique(argc, argv);

	john_init(name, argc, argv);
	john_run();
	john_done();

	return exit_status;
}

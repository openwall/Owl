/* Copyright (C) 2001 Red Hat, Inc.

   Written by Jakub Jelinek <jakub@redhat.com>.
   
   This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation; either version 2 of the
   License, or (at your option) any later version.
               
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.
                           
   You should have received a copy of the GNU General Public
   License along with this program; see the file COPYING.  If not,
   write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
   Boston, MA 02111-1307, USA.  */
  
/*  Changes by Rémy Card to use constants and add option -n.  */
/*  Changes by Jindrich Novy to add option -h, replace mmap(2) */

#define _GNU_SOURCE
#include <sys/types.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <string.h>
#include <dirent.h>
#include <fcntl.h>

#define NHASH	(1<<17)	/* Must be a power of 2! */
#define NIOBUF	(1<<12)
#define NAMELEN	4096
#define NBUF	64

struct _f;
typedef struct _h {
  struct _h *next;
  struct _f *chain;
  off_t size;
  time_t mtime;
} h;

typedef struct _d {
  struct _d *next;
  char name[0];
} d;

d *dirs;

h *hps[NHASH];

int no_link = 0;
int verbose = 0;
int content_only = 0;

typedef struct _f {
  struct _f *next;
  ino_t ino;
  dev_t dev;
  unsigned int cksum;
  char name[0];
} f;

inline unsigned int hash(off_t size, time_t mtime)
{
  return (size ^ mtime) & (NHASH - 1);
}

inline int stcmp(struct stat *st1, struct stat *st2, int content_only)
{
  if (content_only)
    return st1->st_size != st2->st_size;
  return st1->st_mode != st2->st_mode || st1->st_uid != st2->st_uid ||
         st1->st_gid != st2->st_gid || st1->st_size != st2->st_size ||
         st1->st_mtime != st2->st_mtime;
}

long long ndirs, nobjects, nregfiles, ncomp, nlinks, nsaved;

void doexit(int i)
{
  if (verbose) {  
    fprintf(stderr, "\n\n");
    fprintf(stderr, "Directories %lld\n", ndirs);
    fprintf(stderr, "Objects %lld\n", nobjects);
    fprintf(stderr, "IFREG %lld\n", nregfiles);
    fprintf(stderr, "Comparisons %lld\n", ncomp);
    fprintf(stderr, "%s %lld\n", (no_link ? "Would link" : "Linked"), nlinks);
    fprintf(stderr, "%s %lld\n", (no_link ? "Would save" : "saved"), nsaved);
  }
  exit(i);
}

void usage(char *prog)
{
  fprintf (stderr, "Usage: %s [-cnvh] directories...\n", prog);
  fprintf (stderr, "  -c    When finding candidates for linking, compare only file contents.\n");
  fprintf (stderr, "  -n    Don't actually link anything, just report what would be done.\n");
  fprintf (stderr, "  -v    Print summary after hardlinking.\n");
  fprintf (stderr, "  -vv   Print every hardlinked file and bytes saved + summary.\n");
  fprintf (stderr, "  -h    Show help.\n");
  exit(255);
}

unsigned int buf[NBUF];
char iobuf1[NIOBUF], iobuf2[NIOBUF];

typedef struct {
  char *buf;
  size_t alloc;
} dynstr;

void initstr(dynstr *str)
{
  str->buf = NULL;
  str->alloc = 0;
}

void growstr(dynstr *str, size_t newlen)
{
  if (newlen < str->alloc)
    return;
  str->buf = realloc(str->buf, str->alloc = newlen + 1);
  if (!str->buf || str->alloc < newlen) {
    fprintf(stderr, "\nOut of memory 4\n");
    doexit(4);
  }
}

void rf (char *name)
{
  struct stat st, st2, st3;
  nobjects++;
  if (lstat (name, &st))
    return;
  if (S_ISDIR (st.st_mode)) {
    d * dp = malloc(sizeof(d) + 1 + strlen (name));
    if (!dp) {
      fprintf(stderr, "\nOut of memory 3\n");
      doexit(3);
    }
    strcpy (dp->name, name);
    dp->next = dirs;
    dirs = dp;
  } else if (S_ISREG (st.st_mode)) {
    int fd, i;
    f * fp, * fp2;
    h * hp;
    char *n1, *n2;
    int cksumsize = sizeof(buf);
    unsigned int cksum;
    time_t mtime = content_only ? 0 : st.st_mtime;
    unsigned int hsh = hash (st.st_size, mtime);
    off_t fsize;
    nregfiles++;
    if (verbose > 1)
      fprintf(stderr, "  %s", name);
    fd = open (name, O_RDONLY);
    if (fd < 0) return;
    if (st.st_size < sizeof(buf)) {
      cksumsize = st.st_size;
      memset (((char *)buf) + cksumsize, 0, (sizeof(buf) - cksumsize) % sizeof(buf[0]));
    }
    if (read (fd, buf, cksumsize) != cksumsize) {
      close(fd);
      if (verbose > 1)
        fprintf(stderr, "\r%*s\r", (int)strlen(name)+2, "");
      return;
    }
    cksumsize = (cksumsize + sizeof(buf[0]) - 1) / sizeof(buf[0]);
    for (i = 0, cksum = 0; i < cksumsize; i++) {
      if (cksum + buf[i] < cksum)
        cksum += buf[i] + 1;
      else
        cksum += buf[i];
    }
    for (hp = hps[hsh]; hp; hp = hp->next)
      if (hp->size == st.st_size && hp->mtime == mtime)
        break;
    if (!hp) {
      hp = malloc(sizeof(h));
      if (!hp) {
        fprintf(stderr, "\nOut of memory 1\n");
        doexit(1);
      }
      hp->size = st.st_size;
      hp->mtime = mtime;
      hp->chain = NULL;
      hp->next = hps[hsh];
      hps[hsh] = hp;
    }
    for (fp = hp->chain; fp; fp = fp->next)
      if (fp->cksum == cksum)
        break;
    for (fp2 = fp; fp2 && fp2->cksum == cksum; fp2 = fp2->next)
      if (fp2->ino == st.st_ino && fp2->dev == st.st_dev) {
        close(fd);
        if (verbose > 1)
          fprintf(stderr, "\r%*s\r", (int)strlen(name)+2, "");
        return;
      }
    for (fp2 = fp; fp2 && fp2->cksum == cksum; fp2 = fp2->next)
      if (!lstat (fp2->name, &st2) && S_ISREG (st2.st_mode) &&
          !stcmp (&st, &st2, content_only) &&
          st2.st_ino != st.st_ino &&
          st2.st_dev == st.st_dev) {
        int fd2 = open (fp2->name, O_RDONLY);
        if (fd2 < 0) continue;
        if (fstat (fd2, &st2) || !S_ISREG (st2.st_mode) || st2.st_size == 0) {
          close (fd2);
          continue;
        }
        ncomp++;
	lseek(fd, 0, SEEK_SET);
	for (fsize = st.st_size; fsize > 0; fsize -= NIOBUF) {
	  off_t rsize = fsize >= NIOBUF ? NIOBUF : fsize;
	  if (read (fd, iobuf1, rsize) != rsize || read (fd2, iobuf2, rsize) != rsize) {
	    close(fd);
	    close(fd2);
	    fprintf(stderr, "\nReading error\n");
	    return;
	  }
	  if (memcmp (iobuf1, iobuf2, rsize)) break;
	}
	close(fd2);
	if (fsize > 0) continue;
        if (lstat (name, &st3)) {
          fprintf(stderr, "\nCould not stat %s again\n", name);
          close(fd);
          return;
        }
        st3.st_atime = st.st_atime;
        if (stcmp (&st, &st3, 0)) {
          fprintf(stderr, "\nFile %s changed underneath us\n", name);
          close(fd);
          return;
        }
        n1 = fp2->name;
        n2 = name;
        if (!no_link) {
          const char *suffix = ".$$$___cleanit___$$$";
          const size_t suffixlen = strlen(suffix);
          size_t n2len = strlen(n2);
          dynstr nam2;
          initstr(&nam2);
          growstr(&nam2, n2len + suffixlen);
          memcpy(nam2.buf, n2, n2len);
          memcpy(&nam2.buf[n2len], suffix, suffixlen + 1);
          if (rename (n2, nam2.buf)) {
            fprintf(stderr, "\nFailed to rename %s to %s\n", n2, nam2.buf);
            free(nam2.buf);
            continue;
          }
          if (link (n1, n2)) {
            fprintf(stderr, "\nFailed to hardlink %s to %s\n", n1, n2);
            if (rename (nam2.buf, n2)) {
              fprintf(stderr, "\nBad bad - failed to rename back %s to %s\n", nam2.buf, n2);
            }
            close(fd);
            free(nam2.buf);
            return;
          }
          unlink (nam2.buf);
          free(nam2.buf);
        }
        nlinks++;
        if (st3.st_nlink > 1) {
	  /* We actually did not save anything this time, since the link second argument
	     had some other links as well.  */
          if (verbose > 1)
            fprintf(stderr, "\r%*s\r%s %s to %s\n", (int)strlen(name)+2, "", (no_link ? "Would link" : "Linked"), n1, n2);
        } else {
          nsaved+=((st.st_size+4095)/4096)*4096;
          if (verbose > 1)
            fprintf(stderr, "\r%*s\r%s %s to %s, %s %ld\n", (int)strlen(name)+2, "", (no_link ? "Would link" : "Linked"), n1, n2, (no_link ? "would save" : "saved"), st.st_size);
	}
        close(fd);
        return;
      }
    fp2 = malloc(sizeof(f) + 1 + strlen (name));
    if (!fp2) {
      fprintf(stderr, "\nOut of memory 2\n");
      doexit(2);
    }
    close(fd);
    fp2->ino = st.st_ino;
    fp2->dev = st.st_dev;
    fp2->cksum = cksum;
    strcpy(fp2->name, name);
    if (fp) {
      fp2->next = fp->next;
      fp->next = fp2;
    } else {
      fp2->next = hp->chain;
      hp->chain = fp2;
    }
    if (verbose > 1)
      fprintf(stderr, "\r%*s\r", (int)strlen(name)+2, "");
    return;
  }
}

int main(int argc, char **argv)
{
  int ch;
  int i;
  dynstr nam1;
  size_t nam1baselen;
  d * dp;
  DIR *dh;
  struct dirent *di;
  while ((ch = getopt (argc, argv, "cnvh")) != -1) {
    switch (ch) {
    case 'n':
      no_link++;
      break;
    case 'v':
      verbose++;
      break;
    case 'c':
      content_only++;
      break;
    case 'h':
    default:
      usage(argv[0]);
    }
  }
  if (optind >= argc)
    usage(argv[0]);
  for (i = optind; i < argc; i++)
    rf(argv[i]);
  initstr(&nam1);
  while (dirs) {
    dp = dirs;
    dirs = dp->next;
    growstr(&nam1, (nam1baselen = strlen(dp->name)) + 1);
    memcpy(nam1.buf, dp->name, nam1baselen);
    free (dp);
    nam1.buf[nam1baselen++] = '/';
    nam1.buf[nam1baselen] = 0;
    dh = opendir (nam1.buf);
    if (dh == NULL)
      continue;
    ndirs++;
    while ((di = readdir (dh)) != NULL) {
      if (!di->d_name[0])
        continue;
      if (di->d_name[0] == '.') {
        char *q;
        if (!di->d_name[1] || !strcmp (di->d_name, "..") || !strncmp (di->d_name, ".in.", 4))
          continue;
        q = strrchr (di->d_name, '.');
        if (q && strlen (q) == 7 && q != di->d_name) {
          nam1.buf[nam1baselen] = 0;
          if (verbose)
            fprintf(stderr, "Skipping %s%s\n", nam1.buf, di->d_name);
          continue;
        }
      }
      {
        size_t subdirlen;
        growstr(&nam1, nam1baselen + (subdirlen = strlen(di->d_name)));
        memcpy(&nam1.buf[nam1baselen], di->d_name, subdirlen + 1);
      }
      rf(nam1.buf);
    }
    closedir(dh);
  }
  doexit(0);
  return 0;
}

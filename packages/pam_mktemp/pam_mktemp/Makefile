#
# Copyright (c) 2000,2003 by Solar Designer. See LICENSE.
#

CC = gcc
LD = $(CC)
RM = rm -f
MKDIR = mkdir -p
INSTALL = install -c
CFLAGS = -Wall -O2 -fPIC
LDFLAGS = -s -lpam --shared

TITLE = pam_mktemp
LIBSHARED = $(TITLE).so
SHLIBMODE = 700
SECUREDIR = /lib/security
DESTDIR =

OBJS = pam_mktemp.o

all: $(LIBSHARED)

pam_mktemp.so: $(OBJS)
	$(LD) $(LDFLAGS) $(OBJS) -o pam_mktemp.so

.c.o:
	$(CC) $(CFLAGS) -c $*.c

install:
	$(MKDIR) $(DESTDIR)$(SECUREDIR)
	$(INSTALL) -m $(SHLIBMODE) $(LIBSHARED) $(DESTDIR)$(SECUREDIR)

remove:
	$(RM) $(DESTDIR)$(SECUREDIR)/$(TITLE).so

clean:
	$(RM) $(LIBSHARED) *.o

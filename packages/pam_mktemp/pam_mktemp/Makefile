#
# Copyright (c) 2000 by Solar Designer. See LICENSE.
#

CC = gcc
LD = ld
RM = rm -f
MKDIR = mkdir -p
INSTALL = install
CFLAGS = -c -Wall -O2 -fPIC
LDFLAGS = -s -lpam --shared

TITLE = pam_mktemp
LIBSHARED = $(TITLE).so
SHLIBMODE = 700
SECUREDIR = /lib/security
FAKEROOT =

OBJS = pam_mktemp.o

all: $(LIBSHARED)

pam_mktemp.so: $(OBJS)
	$(LD) $(LDFLAGS) $(OBJS) -o pam_mktemp.so

.c.o:
	$(CC) $(CFLAGS) $*.c

install:
	$(MKDIR) $(FAKEROOT)$(SECUREDIR)
	$(INSTALL) -m $(SHLIBMODE) $(LIBSHARED) $(FAKEROOT)$(SECUREDIR)

remove:
	$(RM) $(FAKEROOT)$(SECUREDIR)/$(TITLE).so

clean:
	$(RM) $(LIBSHARED) *.o

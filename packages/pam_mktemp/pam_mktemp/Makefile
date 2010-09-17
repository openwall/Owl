#
# Copyright (c) 2000,2003 by Solar Designer
# Copyright (c) 2006,2010 by Dmitry V. Levin
# See LICENSE
#

CC = gcc
LD = $(CC)
RM = rm -f
MKDIR = mkdir -p
INSTALL = install -c
CFLAGS = -Wall -O2 -fPIC
LDFLAGS = -s --shared -Wl,--version-script,$(MAP)
LDLIBS = -lpam

# This requires GNU make
ifeq ($(shell uname -s),SunOS)
# We support Sun's older /usr/ucb/install, but not the newer /usr/sbin/install
	override INSTALL = /usr/ucb/install -c
	override LDFLAGS = -G
endif

TITLE = pam_mktemp
PAM_SO_SUFFIX =
LIBSHARED = $(TITLE).so$(PAM_SO_SUFFIX)
SHLIBMODE = 755
SECUREDIR = /lib/security
DESTDIR =

OBJS = pam_mktemp.o
MAP = pam_mktemp.map

ifeq ($(USE_SELINUX),1)
	override CFLAGS += -DUSE_SELINUX=1
	override LDLIBS += -lselinux
endif

ifeq ($(USE_APPEND_FL),1)
	override CFLAGS += -DUSE_APPEND_FL=1
endif

all: $(LIBSHARED)

pam_mktemp.so: $(OBJS) $(MAP)
	$(LD) $(LDFLAGS) $(OBJS) $(LDLIBS) -o pam_mktemp.so

.c.o:
	$(CC) $(CFLAGS) -c $*.c

install:
	$(MKDIR) $(DESTDIR)$(SECUREDIR)
	$(INSTALL) -m $(SHLIBMODE) $(LIBSHARED) $(DESTDIR)$(SECUREDIR)

remove:
	$(RM) $(DESTDIR)$(SECUREDIR)/$(TITLE).so

clean:
	$(RM) $(LIBSHARED) *.o

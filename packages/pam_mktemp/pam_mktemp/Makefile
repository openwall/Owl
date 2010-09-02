#
# Written in 2000 and 2003 by Solar Designer.  See LICENSE.
#

CC = gcc
LD = $(CC)
RM = rm -f
MKDIR = mkdir -p
INSTALL = install -c
CFLAGS = -Wall -O2 -fPIC
LDFLAGS = -s --shared -Wl,--version-script,$(MAP)
LDLIBS = -lpam

TITLE = pam_mktemp
PAM_SO_SUFFIX =
LIBSHARED = $(TITLE).so$(PAM_SO_SUFFIX)
SHLIBMODE = 755
SECUREDIR = /lib/security
DESTDIR =

OBJS = pam_mktemp.o
MAP = pam_mktemp.map

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

CC = gcc
LD = gcc
LD_SHARED = ld
RM = rm -f
MKDIR = mkdir -p
INSTALL = install
CFLAGS = -c -Wall -O2 -Iinclude
CFLAGS_SHARED = $(CFLAGS) -fPIC
LDFLAGS = -s -lpam -ldl
LDFLAGS_SHARED = -s -lpam --shared

TITLE = pam_userpass
LIBSHARED = $(TITLE).so
SHLIBMODE = 755
SECUREDIR = /lib/security
FAKEROOT =

all: $(LIBSHARED) example_userpass

pam_userpass.so: pam_userpass.o
	$(LD_SHARED) $(LDFLAGS_SHARED) pam_userpass.o -o pam_userpass.so

pam_userpass.o: pam_userpass.c include/security/_pam_userpass.h
	$(CC) $(CFLAGS_SHARED) pam_userpass.c -o pam_userpass.o

example_userpass: example_userpass.o appl_userpass.o \
	include/security/_pam_userpass.h include/security/pam_userpass.h
	$(LD) $(LDFLAGS) example_userpass.o appl_userpass.o -o example_userpass

.c.o:
	$(CC) $(CFLAGS) $*.c

install:
	$(MKDIR) $(FAKEROOT)$(SECUREDIR)
	$(INSTALL) -m $(SHLIBMODE) $(LIBSHARED) $(FAKEROOT)$(SECUREDIR)

check: install
	$(INSTALL) -m 644 conf/example_userpass $(FAKEROOT)/etc/pam.d/
	./example_userpass "`head -1`" "`head -1`"

remove:
	$(RM) $(FAKEROOT)$(SECUREDIR) \
		$(FAKEROOT)/etc/pam.d/example_userpass

clean:
	$(RM) $(LIBSHARED) example_userpass *.o

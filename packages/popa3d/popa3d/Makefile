CC = gcc
LD = gcc
RM = rm -f
MKDIR = mkdir -p
INSTALL = install
CFLAGS = -c -Wall -O2 -fomit-frame-pointer
# You may use OpenSSL's MD5 routines instead of the ones supplied here
#CFLAGS += -DHAVE_OPENSSL
LDFLAGS = -s
LIBS =
# Linux with glibc, FreeBSD, NetBSD
#LIBS += -lcrypt
# HP-UX trusted system
#LIBS += -lsec
# Solaris (POP_STANDALONE, POP_VIRTUAL)
#LIBS += -lsocket -lnsl
# PAM
#LIBS += -lpam
# TCP wrappers
#LIBS += -lwrap
# libwrap may also want this
#LIBS += -lnsl
# OpenSSL (-DHAVE_OPENSSL)
#LIBS += -lcrypto

DESTDIR =
PREFIX = /usr/local
SBINDIR = $(PREFIX)/sbin
MANDIR = $(PREFIX)/man

PROJ = popa3d
OBJS = \
	startup.o \
	standalone.o \
	virtual.o \
	auth_passwd.o auth_shadow.o auth_pam.o \
	pop_root.o pop_auth.o pop_trans.o \
	protocol.o database.o mailbox.o \
	misc.o \
	md5/md5.o

all: $(PROJ)

popa3d: $(OBJS)
	$(LD) $(LDFLAGS) $(OBJS) $(LIBS) -o popa3d

md5/md5.o: md5/md5.c md5/md5.h
	$(CC) $(CFLAGS) md5/md5.c -o md5/md5.o

.c.o:
	$(CC) $(CFLAGS) $*.c

install: $(PROJ)
	$(MKDIR) -m 755 $(DESTDIR)$(SBINDIR) $(DESTDIR)$(MANDIR)/man8
	$(INSTALL) -m 700 popa3d $(DESTDIR)$(SBINDIR)/
	$(INSTALL) -m 644 popa3d.8 $(DESTDIR)$(MANDIR)/man8/

remove:
	$(RM) $(DESTDIR)$(SBINDIR)/popa3d $(DESTDIR)$(MANDIR)/man8/popa3d.8

clean:
	$(RM) $(PROJ) $(OBJS)

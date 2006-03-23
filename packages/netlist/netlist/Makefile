CC = gcc
LD = gcc
RM = rm -f
MKDIR = mkdir -p
INSTALL = install
CFLAGS = -Wall -O2 -fomit-frame-pointer
LDFLAGS = -s

DESTDIR =
PREFIX = /usr/local
BINDIR = $(PREFIX)/bin
MANDIR = $(PREFIX)/man

PROJ = netlist
OBJS = netlist.o

all: $(PROJ)

netlist: $(OBJS)
	$(LD) $(LDFLAGS) $(OBJS) -o netlist

.c.o:
	$(CC) $(CFLAGS) -c $*.c

install: $(PROJ)
	$(MKDIR) -m 755 $(DESTDIR)$(BINDIR) $(DESTDIR)$(MANDIR)/man1
	$(INSTALL) -m 755 netlist $(DESTDIR)$(BINDIR)/
	$(INSTALL) -m 644 netlist.1 $(DESTDIR)$(MANDIR)/man1/
	echo "You may need to make netlist SGID to grant it access to /proc"

remove:
	$(RM) $(DESTDIR)$(BINDIR)/netlist $(DESTDIR)$(MANDIR)/man1/netlist.1

clean:
	$(RM) $(PROJ) $(OBJS)

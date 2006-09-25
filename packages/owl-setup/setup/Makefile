CXX = g++
RM = rm -f
MKDIR = mkdir -p
INSTALL = install

WITH_NCURSES = yes

ifeq ($(WITH_NCURSES), yes)
CURSES_LIBS = -lcdk -lmenu -lncurses
CURSES_OBJ = iface_ncurses.o curs_detect.o
#CURSES_FLAGS = -DNCURSES_ENABLE
CURSES_FLAGS = -DNCURSES_ENABLE -DNCURSES_DEFAULT
else
CURSES_LIBS =
CURSES_OBJ =
CURSES_FLAGS =
endif


ifeq ($(DEBUG_INFO), yes)
ifndef CXXFLAGS
CXXFLAGS = -Wall -g -O0 -fomit-frame-pointer
endif
CXXFLAGS += $(CURSES_FLAGS)
LDFLAGS =
else
ifndef CXXFLAGS
CXXFLAGS = -Wall -O2 -fomit-frame-pointer
endif
CXXFLAGS += $(CURSES_FLAGS)
LDFLAGS = -s
endif

LIBDEPS = scriptpp/libscriptpp.a ip4areas/libip4areas.a
LIBS = -L scriptpp -lscriptpp -L ip4areas -lip4areas $(CURSES_LIBS) -lpam

DESTDIR =
PREFIX = /usr
SBINDIR = $(PREFIX)/sbin

PROJ = settle setup

SETTLE_OBJS = settle.o iface.o iface_dumb.o $(CURSES_OBJ) \
	cmd.o parmfile.o\
	state.o repartition.o \
	select_partitions.o \
	swap.o installworld.o root_passwd_settle.o pam_root_passwd.o \
	installkernel.o installkernheaders.o \
	mkfstab.o shellout.o network.o \
	timezone.o i18n.o config.o reboot.o

SETUP_OBJS = setup.o iface.o iface_dumb.o $(CURSES_OBJ) \
	cmd.o parmfile.o\
	root_passwd_setup.o pam_root_passwd.o shellout.o \
	network.o timezone.o i18n.o config.o

SRCS = $(wildcard [^_]*.cpp)

all: $(PROJ)

scriptpp/libscriptpp.a: FORCE
	$(MAKE) -C scriptpp CXXFLAGS="$(CXXFLAGS)"

ip4areas/libip4areas.a: FORCE
	$(MAKE) -C ip4areas CXXFLAGS="$(CXXFLAGS)"

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

settle: $(LIBDEPS) $(SETTLE_OBJS)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $(SETTLE_OBJS) $(LIBS) -o $@

setup: $(LIBDEPS) $(SETUP_OBJS)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $(SETUP_OBJS) $(LIBS) -o $@

install: $(PROJ)
	$(MKDIR) -m 755 $(DESTDIR)$(SBINDIR) $(DESTDIR)$(MANDIR)/man8
	$(INSTALL) -m 700 $(PROJ) $(DESTDIR)$(SBINDIR)/
	$(INSTALL) -m 644 setup.8 settle.8 $(DESTDIR)$(MANDIR)/man8/

clean:
	$(RM) $(PROJ) $(SETTLE_OBJS) $(SETUP_OBJS) deps.mk
	$(MAKE) -C scriptpp clean
	$(MAKE) -C ip4areas clean

FORCE:

deps.mk: $(SRCS) Makefile
	$(CXX) -MM $(SRCS) > $@

ifneq (clean, $(MAKECMDGOALS))
-include deps.mk
endif

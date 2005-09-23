CXX = g++
RM = rm -f
MKDIR = mkdir -p
INSTALL = install

WITH_NCURSES = yes

ifeq ($(WITH_NCURSES), yes)
CURSES_LIBS = -lcdk -lmenu -lncurses
CURSES_OBJ = iface_ncurses.o
CURSES_FLAGS = -DNCURSES_ENABLE
#CURSES_FLAGS = -DNCURSES_ENABLE -DNCURSES_DEFAULT
else
CURSES_LIBS =
CURSES_OBJ =
CURSES_FLAGS =
endif

CXXFLAGS = -Wall -O2 -fomit-frame-pointer $(CURSES_FLAGS)
LDFLAGS = -s

LIBDEPS = scriptpp/libscriptpp.a ip4areas/libip4areas.a
LIBS = -L scriptpp -lscriptpp -L ip4areas -lip4areas $(CURSES_LIBS)

DESTDIR =
PREFIX = /usr
SBINDIR = $(PREFIX)/sbin

PROJ = settle setup

SETTLE_OBJS = settle.o iface.o iface_dumb.o $(CURSES_OBJ) \
	cmd.o \
	state.o repartition.o \
	select_partitions.o \
	swap.o installworld.o root_passwd_settle.o \
	installkernel.o \
	mkfstab.o shellout.o network.o \
	timezone.o keyboard.o config.o reboot.o

SETUP_OBJS = setup.o iface.o iface_dumb.o $(CURSES_OBJ) \
	cmd.o \
	root_passwd_setup.o shellout.o \
	network.o timezone.o keyboard.o config.o

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
	$(MKDIR) -m 755 $(DESTDIR)$(SBINDIR)
	$(INSTALL) -m 700 $(PROJ) $(DESTDIR)$(SBINDIR)/

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

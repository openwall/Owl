CC = gcc
RM = rm -f
MKDIR = mkdir -p
INSTALL = install
LN_S = ln -sf
CFLAGS = -c -O2 -Wall -fPIC -Iinclude
LDFLAGS = -s
LIBS = -lpam
LINK = $(CC) $(LDFLAGS)
LINK_SHARED = $(LINK) -shared
AR = ar
ARFLAGS = rv

TITLE = pam_userpass
LIBPAMSHARED = $(TITLE).so
SONAME = lib$(TITLE).so.1
LIBAPPLSHARED = lib$(TITLE).so.0.9
LIBAPPLSHARED_LINK = lib$(TITLE).so
LIBAPPLSTATIC = lib$(TITLE).a
SHLIBMODE = 755
STLIBMODE = 644
INCLUDEMODE = 644
SECUREDIR = /lib/security
LIBDIR = /usr/lib
INCLUDEDIR = /usr/include/security
PAMDIR = /etc/pam.d
DESTDIR =

.SUFFIXES: .c .o

.c.o:
	$(CC) $(CFLAGS) $*.c

all: $(LIBPAMSHARED) $(LIBAPPLSTATIC) example_userpass

$(LIBPAMSHARED): pam_userpass.o
	$(LINK_SHARED) $< $(LIBS) -o $@

$(LIBAPPLSHARED): appl_userpass.o
	$(LINK_SHARED) -Wl,-soname,$(SONAME) $< $(LIBS) -o $@

$(LIBAPPLSTATIC): appl_userpass.o
	$(AR) $(ARFLAGS) $@ $<

$(SONAME): $(LIBAPPLSHARED)
	$(LN_S) $(LIBAPPLSHARED) $(SONAME)

$(LIBAPPLSHARED_LINK): $(LIBAPPLSHARED)
	$(LN_S) $(LIBAPPLSHARED) $(LIBAPPLSHARED_LINK)

pam_userpass.o: pam_userpass.c include/security/_pam_userpass.h

appl_userpass.o: appl_userpass.c include/security/_pam_userpass.h \
	include/security/pam_userpass.h

example_userpass: example_userpass.o $(LIBAPPLSHARED_LINK)
	$(LINK) $< -L. -l$(TITLE) -o $@

install: all
	$(MKDIR) $(DESTDIR)$(SECUREDIR)
	$(INSTALL) -m $(SHLIBMODE) $(LIBPAMSHARED) $(DESTDIR)$(SECUREDIR)/
	$(MKDIR) $(DESTDIR)$(LIBDIR)
	$(INSTALL) -m $(SHLIBMODE) $(LIBAPPLSHARED) $(DESTDIR)$(LIBDIR)/
	$(INSTALL) -m $(STLIBMODE) $(LIBAPPLSTATIC) $(DESTDIR)$(LIBDIR)/
	$(LN_S) $(LIBAPPLSHARED) $(DESTDIR)$(LIBDIR)/$(SONAME)
	$(LN_S) $(LIBAPPLSHARED) $(DESTDIR)$(LIBDIR)/$(LIBAPPLSHARED_LINK)
	$(MKDIR) $(DESTDIR)$(INCLUDEDIR)
	$(INSTALL) -m $(INCLUDEMODE) include/security/pam_userpass.h \
		$(DESTDIR)$(INCLUDEDIR)/

check: install
	$(MKDIR) $(DESTDIR)$(PAMDIR)
	$(INSTALL) -m 644 conf/example_userpass $(DESTDIR)$(PAMDIR)/
	LD_LIBRARY_PATH=$(DESTDIR)$(LIBDIR) ./example_userpass "`head -1`" "`head -1`"

remove:
	$(RM) $(DESTDIR)$(SECUREDIR)/$(LIBPAMSHARED) \
		$(DESTDIR)$(LIBDIR)/$(LIBAPPLSHARED) \
		$(DESTDIR)$(LIBDIR)/$(SONAME) \
		$(DESTDIR)$(LIBDIR)/$(LIBAPPLSHARED_LINK) \
		$(DESTDIR)$(LIBDIR)/$(LIBAPPLSTATIC) \
		$(DESTDIR)$(INCLUDEDIR)/pam_userpass.h \
		$(DESTDIR)$(PAMDIR)/example_userpass

clean:
	$(RM) example_userpass *.o *.so* *.a

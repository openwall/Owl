CC = gcc
RM = rm -f
CFLAGS = -Wall -O2
LDFLAGS = -s -lpam

PROJ = passwdlg

passwdlg: passwdlg.c
	$(CC) $(CFLAGS) $(LDFLAGS) passwdlg.c -o passwdlg

clean:
	$(RM) $(PROJ)

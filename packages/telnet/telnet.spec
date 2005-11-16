# $Owl: Owl/packages/telnet/telnet.spec,v 1.12 2005/11/16 13:32:45 solar Exp $

Summary: The client program for the telnet remote login protocol.
Name: telnet
Version: 3.0
Release: owl3
License: BSD
Group: Applications/Internet
Source0: telnet-%version-20011117.tar.bz2
Source1: telnetd.xinetd
Patch0: telnet-3.0-owl-linux.diff
Patch1: telnet-3.0-owl-no-mini_inetd.diff
Patch2: telnet-3.0-owl-ipv4-only.diff
Patch10: telnet-3.0-owl-env-export.diff
Patch11: telnet-3.0-owl-env-DISPLAY.diff
Patch12: telnet-3.0-owl-bound.diff
Patch20: telnet-3.0-owl-drop-root.diff
BuildRequires: ncurses-devel
BuildRoot: /override/%name-%version

%description
Telnet is a popular protocol for logging into remote systems over the
Internet.  The telnet package provides a command line telnet client.

%package server
Summary: The server program for the telnet remote login protocol.
Group: System Environment/Daemons
PreReq: grep, shadow-utils
Requires: /var/empty, xinetd

%description server
Telnet is a popular protocol for logging into remote systems over the
Internet.  The telnet-server package provides a telnet daemon, which
will support remote logins into the host machine.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch20 -p1

%{expand:%%define optflags %optflags -Wall}

%build
CFLAGS="-c %optflags" make

%install
rm -rf %buildroot
mkdir -p %buildroot%_bindir
mkdir -p %buildroot/usr/libexec
mkdir -p %buildroot%_mandir/man{1,8}

install -m 755 usr.bin/telnet/telnet %buildroot%_bindir/
install -m 644 usr.bin/telnet/telnet.1 %buildroot%_mandir/man1/
install -m 700 libexec/telnetd/telnetd %buildroot/usr/libexec/
install -m 644 libexec/telnetd/telnetd.8 %buildroot%_mandir/man8/

mkdir -p %buildroot/etc/xinetd.d
install -m 600 %_sourcedir/telnetd.xinetd \
	%buildroot/etc/xinetd.d/telnetd

%pre server
grep -q ^telnetd: /etc/group || groupadd -g 186 telnetd
grep -q ^telnetd: /etc/passwd ||
	useradd -g telnetd -u 186 -d / -s /bin/false -M telnetd

%files
%defattr(-,root,root)
%_bindir/telnet
%_mandir/man1/telnet.1*

%files server
%defattr(-,root,root)
%config(noreplace) /etc/xinetd.d/telnetd
/usr/libexec/telnetd
%_mandir/man8/telnetd.8*

%changelog
* Tue Jun 28 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.0-owl3
- Build with -Wall; fixed compilation warnings.

* Thu Mar 17 2005 Solar Designer <solar-at-owl.openwall.com> 3.0-owl2
- Introduced the appropriate bounds checking into slc_add_reply() and
env_opt_add() (both are in the telnet client only).
- Improved the environment variable export restrictions such that the
exportability of DISPLAY and TERM variables may be controlled too,
updated the man page; this replaced the Red Hat Linux derived patch.
- Resolved a possible truncation of DISPLAY when it is sent in response
to TELOPT_XDISPLOC.

* Mon Feb 04 2002 Solar Designer <solar-at-owl.openwall.com> 3.0-owl1
- Enforce our new spec file conventions.

* Sun Nov 25 2001 Solar Designer <solar-at-owl.openwall.com>
- Do telnet protocol handling as a dedicated pseudo-user and in a chroot
jail.  This uses the approach introduced by Chris Evans in his NetKit
telnetd patches, but the code is different.
- Send fatal*() messages to syslog (and in some cases only to syslog, not
to the remote end).
- Restricted the telnet client to IPv4 only for now due to a problem with
the glibc getaddrinfo(3) for which no trivial fix exists.  The problem is
that with AF_UNSPEC getaddrinfo(3) would perform DNS lookups for possible
IPv6 addresses even if an IPv4 entry exists in the local /etc/hosts.  See
the thread at:
http://sources.redhat.com/ml/libc-alpha/2001-11/threads.html#00125

* Wed Nov 21 2001 Solar Designer <solar-at-owl.openwall.com>
- Eliminated even more dead code in telnetd, made it use logwtmp(3)
rather than writing to the files directly (it does that to remove the
records which is redundant with our login; will be disabled once telnetd
is made to run as non-root).
- Deal with long lines in /etc/issue.net correctly.
- Don't fallback to /etc/issue.
- Pass -h to telnetd by default (disables the printing of host-specific
information).
- Added a Red Hat Linux derived patch to the telnet client such that it
permits queries for exported variables only.

* Tue Nov 20 2001 Solar Designer <solar-at-owl.openwall.com>
- Don't use AI_CANONNAME with getaddrinfo(3) in the telnet client (there's
no longer a reference to ai_canonname in the OpenBSD version of the code).

* Sat Nov 17 2001 Solar Designer <solar-at-owl.openwall.com>
- Ported the telnet client and server from OpenBSD-current (post-3.0),
reviewing changes made in NetBSD-current, FreeBSD-current, and Linux
NetKit 0.17.
- Filter environment variables in telnetd with a white list (took the
list itself from NetKit), but also use a black list for logging likely
attacks.
- Dropped the "mini inetd" from telnetd.
- Dropped Kerberos-related pieces from the man pages (the telnet stuff
is already bad enough, let's better not add to that).
- Wrote telnetd.xinetd.
- Wrote this spec file, based (sub)package descriptions on Red Hat's.

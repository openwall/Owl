# $Id: Owl/packages/nc/nc.spec,v 1.9 2005/10/24 03:06:27 solar Exp $

Summary: Reads and writes data across network connections using TCP or UDP.
Name: nc
Version: 3.2
Release: owl3
License: BSD
Group: Applications/Internet
Source: nc-%version-20021213.tar.bz2
Patch0: nc-3.2-owl-linux.diff
Patch1: nc-3.2-owl-ipv4-default.diff
Patch2: nc-3.2-owl-fixes.diff
BuildRoot: /override/%name-%version

%description
The nc package contains netcat (the program is actually nc), a simple
utility for reading and writing data across network connections, using
the TCP or UDP protocols.  netcat is intended to be a reliable back-end
tool which can be used directly or easily driven by other programs and
scripts.  netcat is also a feature-rich network debugging and exploration
tool, since it can create many different connections and has many
built-in capabilities.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
CFLAGS="-c %optflags" make

%install
rm -rf %buildroot
mkdir -p %buildroot%_bindir
mkdir -p %buildroot%_mandir/man1

install -m 755 usr.bin/nc/nc %buildroot%_bindir/
install -m 644 usr.bin/nc/nc.1 %buildroot%_mandir/man1/

%files
%defattr(-,root,root)
%_bindir/nc
%_mandir/man1/nc.1*

%changelog
* Wed Jul 21 2004 Michail Litvak <mci-at-owl.openwall.com> 3.2-owl3
- Updated -owl-fixes. Fixed bug with handling POLLERR event in
poll()'s loop.

* Fri Jan 24 2003 Michail Litvak <mci-at-owl.openwall.com> 3.2-owl2
- Updated -owl-fixes. Initialize len argument before accept(),
  handle accept()'s errors.

* Fri Dec 27 2002 Michail Litvak <mci-at-owl.openwall.com>
- Ported the nc utility from OpenBSD-current (post-3.2).
- Patch to set AF_INET by default to fix problem with getaddrinfo(3).
- Fix error handling and other.
- Wrote this spec file, based on telnet/telnetd's spec.

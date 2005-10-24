# $Id: Owl/packages/mailx/mailx.spec,v 1.8 2005/10/24 03:06:27 solar Exp $

Summary: The /bin/mail program for sending e-mail messages.
Name: mailx
Version: 8.1.1.2.7
Release: owl2
License: BSD
Group: Applications/Internet
Source: mailx-%version.tar.gz
Patch0: mailx-8.1.1.2.7-owl-linux.diff
BuildRequires: groff
BuildRoot: /override/%name-%version

%description
/bin/mail provides the traditional interface to reading and sending
e-mail messages.  It is often used in shell scripts.

%prep
%setup -q
%patch0 -p1

%build
cd usr.bin/mail
make CFLAGS="%optflags -c -Wall -Dlint"
make -C USD.doc

%install
rm -rf %buildroot
mkdir -p %buildroot{/bin,/etc,/usr/share/misc,%_mandir/man1}
make -C usr.bin/mail install DESTDIR=%buildroot MANDIR=%_mandir

%files
%defattr(-,root,root)
/bin/mail
%config(noreplace) /etc/mail.rc
/usr/share/misc/*
%_mandir/man1/mail.1.*
%doc usr.bin/mail/USD.doc/USD.ps

%changelog
* Thu Feb 12 2004 Michail Litvak <mci-at-owl.openwall.com> 8.1.1.2.7-owl2
- Use RPM macros instead of explicit paths.

* Wed Feb 06 2002 Michail Litvak <mci-at-owl.openwall.com> 8.1.1.2.7-owl1
- Enforce our new spec file conventions

* Tue Nov 14 2000 Solar Designer <solar-at-owl.openwall.com>
- Ported /bin/mail from OpenBSD 2.7 to Linux.
- Did various fixes, mostly to the way locking is done (uses fcntl locks
now, plus can do dotlocks via lockspool helper binary if enabled).
- Reviewed the Debian and Red Hat patches as found in RH 7.0.
- Wrote this spec file.

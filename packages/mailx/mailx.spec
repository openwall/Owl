# $Id: Owl/packages/mailx/mailx.spec,v 1.3 2003/10/30 21:15:46 solar Exp $

Summary: The /bin/mail program for sending e-mail messages.
Name: mailx
Version: 8.1.1.2.7
Release: owl1
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
make CFLAGS="$RPM_OPT_FLAGS -c -Wall -Dlint"
make -C USD.doc

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{bin,etc,usr/man/man1,usr/share/misc}
make -C usr.bin/mail install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/bin/mail
%config(noreplace) /etc/mail.rc
/usr/share/misc/*
/usr/man/man1/mail.1.*
%doc usr.bin/mail/USD.doc/USD.ps

%changelog
* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com> 8.1.1.2.7-owl1
- Enforce our new spec file conventions

* Tue Nov 14 2000 Solar Designer <solar@owl.openwall.com>
- Ported /bin/mail from OpenBSD 2.7 to Linux.
- Did various fixes, mostly to the way locking is done (uses fcntl locks
now, plus can do dotlocks via lockspool helper binary if enabled).
- Reviewed the Debian and Red Hat patches as found in RH 7.0.
- Wrote this spec file.

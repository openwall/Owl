# $Id: Owl/packages/mailx/mailx.spec,v 1.1 2000/11/14 14:03:27 solar Exp $

%define USE_LOCKSPOOL	'no'

Summary: The /bin/mail program for sending e-mail messages.
Name: mailx
Version: 8.1.1.2.7
Release: 1owl
Copyright: BSD
Group: Applications/Internet
Source0: mailx-%{version}.tar.gz
Patch0: mailx-8.1.1.2.7-owl-linux.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
BuildPreReq: groff
%if "%{USE_LOCKSPOOL}"=="'yes'"
Requires: lockspool
%endif

%description
/bin/mail provides the traditional interface to reading and sending
e-mail messages.  It is often used in shell scripts.

%prep
%setup -q
%patch0 -p1

%build
cd usr.bin/mail
%if "%{USE_LOCKSPOOL}"=="'yes'"
make CFLAGS="$RPM_OPT_FLAGS -c -Wall -Dlint -DUSE_LOCKSPOOL"
%else
make CFLAGS="$RPM_OPT_FLAGS -c -Wall -Dlint"
%endif
make -C USD.doc

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{bin,etc,usr/man/man1,usr/share/misc}
make -C usr.bin/mail install DESTDIR=$RPM_BUILD_ROOT
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/bin/mail
%config(noreplace) /etc/mail.rc
/usr/share/misc/*
/usr/man/man1/mail.1.*
%doc usr.bin/mail/USD.doc/USD.ps

%changelog
* Tue Nov 14 2000 Solar Designer <solar@owl.openwall.com>
- Ported /bin/mail from OpenBSD 2.7 to Linux.
- Did various fixes, mostly to the way locking is done (uses fcntl locks
now, plus can do dotlocks via lockspool helper binary if enabled).
- Reviewed the Debian and Red Hat patches as found in RH 7.0.
- Wrote this spec file.

# $Id: Owl/packages/lftp/lftp.spec,v 1.23 2004/11/23 22:40:46 mci Exp $

Summary: Sophisticated command line file transfer program.
Name: lftp
Version: 2.6.10
Release: owl3
License: GPL
Group: Applications/Internet
URL: http://lftp.yar.ru
Source0: ftp://ftp.yars.free.net/pub/software/unix/net/ftp/client/lftp/%name-%version.tar.bz2
Source1: lftpget.1
Patch0: lftp-2.6.9-owl-n-option.diff
Patch1: lftp-2.6.10-rh-handle-malformed-http.diff
Prefix: %_prefix
BuildRequires: openssl-devel, readline-devel >= 4.3
BuildRoot: /override/%name-%version

%description
lftp is a file retrieving tool that supports FTP and HTTP protocols under
both IPv4 and IPv6.  lftp has an amazing set of features, while preserving
its interface as simple and easy as possible.

The main two advantages over other ftp clients are reliability and ability
to perform tasks in background.  It will reconnect and reget the file being
transferred if the connection broke.  You can start a transfer in background
and continue browsing the ftp site.  It does this all in one process.  When
you have started background jobs and feel you are done, you can just exit
lftp and it automatically moves to nohup mode and completes the transfers.
It also has such nice features as reput and mirror.  And it can download a
file faster using multiple connections.

lftp can also be scriptable, it can be used to mirror sites, it lets you
copy files among remote servers (even between FTP and HTTP).  It has an
extensive online help.  It supports bookmarks, and connecting to several
ftp/http sites at the same time.

This package also includes lftpget - a simple non-interactive tool for
downloading files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# Make sure that all message catalogs are built
unset LINGUAS || :

%define __libtoolize echo --
%configure --with-modules --with-ssl
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %buildroot
make install-strip DESTDIR=%buildroot

find %buildroot%_libdir/%name/ -type f -name \*.la -print -delete

install -m 644 $RPM_SOURCE_DIR/lftpget.1 %buildroot%_mandir/man1/

%post
if [ ! -e /usr/bin/ftp -a ! -e %_mandir/man1/ftp.1.gz ]; then
	ln -s lftp /usr/bin/ftp
	ln -s lftp.1.gz %_mandir/man1/ftp.1.gz
fi

%preun
if [ $1 -eq 0 -a -L /usr/bin/ftp -a -L %_mandir/man1/ftp.1.gz ]; then
	if cmp -s /usr/bin/ftp /usr/bin/lftp; then
		rm /usr/bin/ftp
		rm %_mandir/man1/ftp.1.gz
	fi
fi

%files
%defattr(-,root,root)
%doc BUGS COPYING FAQ FEATURES NEWS README* THANKS TODO lftp.lsm
%config /etc/lftp.conf
%attr(755,root,root) %_bindir/*
%_libdir/*
%_mandir/man*/*
%attr(-,root,root) %_datadir/lftp
%_datadir/locale/*/*/*

%changelog
* Fri Feb 20 2004 Michail Litvak <mci@owl.openwall.com> 2.6.10-owl3
- Build with system readline.

* Tue Dec 16 2003 Solar Designer <solar@owl.openwall.com> 2.6.10-owl2
- Added a patch by Nalin Dahyabhai of Red Hat to handle malformed HTTP
server responses gracefully.

* Sat Dec 13 2003 Michail Litvak <mci@owl.openwall.com> 2.6.10-owl1
- 2.6.10 (security fixes in html parsing code)

* Mon Dec 08 2003 Michail Litvak <mci@owl.openwall.com> 2.6.9-owl1
- 2.6.9
- Dropped patch to fix tmp-files handling in configure script,
  this fixed in upstream.
- Do not package .la files.

* Tue Jun 03 2003 Michail Litvak <mci@owl.openwall.com> 2.6.6-owl2
- Fixed tmp-files handling in configure script of included readline.

* Mon Jun 02 2003 Michail Litvak <mci@owl.openwall.com> 2.6.6-owl1
- 2.6.6
- Removed outdated patches.
- Built with included readline.
- Patch to provide -n option for compatibility with old ftp.

* Mon Feb 04 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Thu Apr 26 2001 Solar Designer <solar@owl.openwall.com>
- New release number for upgrades after building against OpenSSL 0.9.6a.

* Fri Mar 23 2001 Solar Designer <solar@owl.openwall.com>
- Corrected the package description.
- Point /usr/bin/ftp to lftp if it doesn't exist when lftp is installed.

* Wed Mar 21 2001 Michail Litvak <mci@owl.openwall.com>
- change source from tar.gz to tar.bz2

* Mon Mar 19 2001 Michail Litvak <mci@owl.openwall.com>
- reworked spec from author's package
- imported patches from Debian
- add patch to check length of address returned from DNS

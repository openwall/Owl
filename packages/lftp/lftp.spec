# $Id: Owl/packages/lftp/lftp.spec,v 1.14 2003/06/01 22:39:26 mci Exp $

Summary: Sophisticated command line file transfer program.
Name: lftp
Version: 2.6.6
Release: owl1
License: GPL
Group: Applications/Internet
Source0: ftp://ftp.yars.free.net/pub/software/unix/net/ftp/client/lftp/%{name}-%{version}.tar.bz2
Source1: lftpget.1
Patch0: lftp-2.6.6-owl-n-option.diff
Prefix: %{_prefix}
BuildRequires: openssl-devel
BuildRoot: /override/%{name}-%{version}

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

lftp can also be scriptable, it can be used to mirror sites, it let you
copy files among remote servers (even between FTP and HTTP).  It has an
extensive online help.  It supports bookmarks, and connecting to several
ftp/http sites at the same time.

This package also includes ftpget and lftpget - simple non-interactive
tools for downloading files.

%prep
%setup -q
%patch0 -p1

%build
# Make sure that all message catalogs are built
unset LINGUAS || :

%define __libtoolize echo --
%configure --with-modules --with-ssl --with-included-readline
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make install-strip DESTDIR=$RPM_BUILD_ROOT
install -m 644 $RPM_SOURCE_DIR/lftpget.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -e /usr/bin/ftp -a ! -e %{_mandir}/man1/ftp.1.gz ]; then
	ln -s lftp /usr/bin/ftp
	ln -s lftp.1.gz %{_mandir}/man1/ftp.1.gz
fi

%preun
if [ $1 -eq 0 -a -L /usr/bin/ftp -a -L %{_mandir}/man1/ftp.1.gz ]; then
	if cmp -s /usr/bin/ftp /usr/bin/lftp; then
		rm /usr/bin/ftp
		rm %{_mandir}/man1/ftp.1.gz
	fi
fi

%files
%defattr(-,root,root)
%doc BUGS COPYING FAQ FEATURES NEWS README* THANKS TODO lftp.lsm
%config /etc/lftp.conf
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*
%{_mandir}/man*/*
%attr(-,root,root) %{_datadir}/lftp
%{_datadir}/locale/*/*/*

%changelog
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

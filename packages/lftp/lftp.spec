# $Id: Owl/packages/lftp/lftp.spec,v 1.1 2001/03/19 22:57:05 mci Exp $

Summary: sophisticated command line file transfer program
Name: lftp
Version: 2.3.8
Release: 1owl
Copyright: GPL
Source0: ftp://ftp.yars.free.net/pub/software/unix/net/ftp/client/lftp/%{name}-%{version}.tar.gz
Source1: lftpget.1
Patch0: lftp-2.3.8-deb-conf.diff
Patch1: lftp-2.3.8-deb-doc.diff
Patch2: lftp-2.3.8-deb-makefile.diff
Patch3: lftp-2.3.8-deb-po.diff
Patch4: lftp-2.3.8-owl-addr.diff
Group: Applications/Internet
Prefix: %{_prefix}
BuildRoot: /var/rpm-buildroot/%{name}-buildroot
Requires: readline >= 4.1
Requires: openssl >= 0.9.5a-1owl
BuildPreReq: readline-devel
BuildPreReq: openssl-devel

%description
Lftp is a file retrieving tool that supports FTP and HTTP protocols under
both IPv4 and IPv6. Lftp has an amazing set of features, while preserving
its interface as simple and easy as possible.

The main two advantages over other ftp clients are reliability and ability
to perform tasks in background. It will reconnect and reget the file being
transferred if the connection broke. You can start a transfer in background
and continue browsing on the ftp site. It does this all in one process. When
you have started background jobs and feel you are done, you can just exit
lftp and it automatically moves to nohup mode and completes the transfers.
It has also such nice features as reput and mirror. It can also download a
file as soon as possible by using several connections at the same time.

Lftp can also be scripteable, it can be used to mirror sites, it let you
copy files among remote servers (even between FTP and HTTP). It has an
extensive online help. It supports bookmarks, and connecting to several
ftp/http sites at the same time.

This package also includes ftpget and lftpget - simple non-interactive
tools for downloading files.

%prep
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

# Make sure that all message catalogs are built
if [ $LINGUAS ]; then
	unset LINGUAS
fi

%define __libtoolize true
%configure --with-modules --with-ssl --mandir=%{_mandir}
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
make install-strip DESTDIR=%{buildroot}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/usr/man/man1/ 

%clean
rm -rf $RPM_BUILD_ROOT 

%files
%defattr(-,root,root)
%doc ABOUT-NLS BUGS COPYING FAQ FEATURES NEWS README* THANKS TODO lftp.lsm
%config /etc/lftp.conf
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*
%{_mandir}/man*/*
%attr(-,root,root) %{_datadir}/lftp
%{_datadir}/locale/*/*/*

%changelog
* Mon Mar 19 2001 Michail Litvak <mci@owl.openwall.com>
- reworked spec from author's package 
- imported patches from Debian
- patch to work tidy with address from DNS

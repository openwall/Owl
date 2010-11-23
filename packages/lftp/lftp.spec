# $Owl: Owl/packages/lftp/lftp.spec,v 1.42 2010/11/23 21:57:48 solar Exp $

Summary: Sophisticated command line file transfer program.
Name: lftp
Version: 4.1.0
Release: owl1
License: GPLv3+
Group: Applications/Internet
URL: http://lftp.yar.ru
Source: http://ftp.yars.free.net/pub/source/lftp/lftp-%version.tar.xz
Patch0: lftp-4.1.0-owl-sentinel.diff
Patch1: lftp-4.0.10-owl-warnings.diff
Requires: less
BuildRequires: openssl-devel >= 0.9.7g-owl1, readline-devel >= 0:4.3
BuildRequires: ncurses-devel, gettext
BuildRoot: /override/%name-%version

%description
lftp is sophisticated file transfer program with command-line interface.
It supports the FTP, HTTP, HTTPS, SFTP, FISH, and BitTorrent protocols,
advanced and obscure features of the protocols, proxy servers, automatic
retries on non-fatal errors and timeouts, continuation of interrupted file
transfers, mirroring, transfer rate throttling, multiple connections and
background jobs, shell-like command syntax and comprehensive scripting,
command-line editing (via the GNU Readline library), context-sensitive
command completion, command history, and a lot more.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
bzip2 -9k NEWS

%build
# Make sure that all message catalogs are built
unset LINGUAS || :
%configure \
	--with-modules --disable-static \
	--without-gnutls --with-openssl \
	--with-pager='exec less' \
	--without-debug
%__make

%install
rm -rf %buildroot
%makeinstall

# Avoid unwanted perl dependencies.
chmod a-x %buildroot%_datadir/%name/{convert-mozilla-cookies,verify-file}

%post
if [ ! -e %_bindir/ftp -a ! -e %_mandir/man1/ftp.1.gz ]; then
	ln -s lftp %_bindir/ftp
	ln -s lftp.1.gz %_mandir/man1/ftp.1.gz
fi

%preun
if [ $1 -eq 0 -a -L %_bindir/ftp -a -L %_mandir/man1/ftp.1.gz ]; then
	if cmp -s %_bindir/ftp %_bindir/lftp; then
		rm %_bindir/ftp
		rm %_mandir/man1/ftp.1.gz
	fi
fi

%files
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING FAQ FEATURES NEWS.bz2 README README.debug-levels
%doc THANKS TODO lftp.lsm
%config /etc/lftp.conf
%_bindir/*
%_libdir/liblftp*.so*
%exclude %_libdir/*.la
%_libdir/lftp
%_mandir/man?/lftp*
%_datadir/lftp
%_datadir/locale/*/LC_MESSAGES/lftp.mo

%changelog
* Tue Nov 23 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 4.1.0-owl1
- Updated to 4.1.0.

* Mon Sep 06 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 4.0.10-owl1
- Updated to 4.0.10.
- Silenced compiler warnings.

* Thu Jul 29 2010 Solar Designer <solar-at-owl.openwall.com> 4.0.9-owl1
- Updated to 4.0.9.

* Tue May 04 2010 Solar Designer <solar-at-owl.openwall.com> 4.0.7-owl1
- Updated to 4.0.7.
- Rewrote the description.

* Thu Mar 29 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.5.10-owl1
- Updated to 3.5.10.

* Mon Mar 26 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.5.9-owl1
- Updated to 3.5.9.

* Sun Sep 03 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.4.6-owl3
- Relaxed the build dependency on readline-devel.

* Sun May 21 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.4.6-owl2
- Rebuilt with libreadline.so.5.

* Sat Apr 29 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.4.6-owl1
- Updated to 3.4.6.

* Wed Apr 19 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.4.4-owl1
- Updated to 3.4.4.
- Changed default pager from "more" to "less".

* Sat Jun 25 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.6.12-owl2
- Rebuilt with libssl.so.5.

* Tue May 10 2005 Andreas Ericsson <exon-at-owl.openwall.com> 2.6.12-owl1
- 2.6.12, fixes hang on copying zero length file with the mirror command.
- Removed malformed-http patch which is now included upstream.
- Enforced recent CONVENTIONS additions.
- Be specific in %%files section.

* Fri Feb 20 2004 Michail Litvak <mci-at-owl.openwall.com> 2.6.10-owl3
- Build with system readline.

* Tue Dec 16 2003 Solar Designer <solar-at-owl.openwall.com> 2.6.10-owl2
- Added a patch by Nalin Dahyabhai of Red Hat to handle malformed HTTP
server responses gracefully.

* Sat Dec 13 2003 Michail Litvak <mci-at-owl.openwall.com> 2.6.10-owl1
- 2.6.10 (security fixes in html parsing code)

* Mon Dec 08 2003 Michail Litvak <mci-at-owl.openwall.com> 2.6.9-owl1
- 2.6.9
- Dropped patch to fix tmp-files handling in configure script,
  this fixed in upstream.
- Do not package .la files.

* Tue Jun 03 2003 Michail Litvak <mci-at-owl.openwall.com> 2.6.6-owl2
- Fixed tmp-files handling in configure script of included readline.

* Mon Jun 02 2003 Michail Litvak <mci-at-owl.openwall.com> 2.6.6-owl1
- 2.6.6
- Removed outdated patches.
- Built with included readline.
- Patch to provide -n option for compatibility with old ftp.

* Mon Feb 04 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Thu Apr 26 2001 Solar Designer <solar-at-owl.openwall.com>
- New release number for upgrades after building against OpenSSL 0.9.6a.

* Fri Mar 23 2001 Solar Designer <solar-at-owl.openwall.com>
- Corrected the package description.
- Point /usr/bin/ftp to lftp if it doesn't exist when lftp is installed.

* Wed Mar 21 2001 Michail Litvak <mci-at-owl.openwall.com>
- change source from tar.gz to tar.bz2

* Mon Mar 19 2001 Michail Litvak <mci-at-owl.openwall.com>
- reworked spec from author's package
- imported patches from Debian
- add patch to check length of address returned from DNS

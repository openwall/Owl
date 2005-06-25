# $Id: Owl/packages/elinks/elinks.spec,v 1.17 2005/06/25 22:34:41 ldv Exp $

Summary: Lynx-like text WWW browser with many features.
Name: elinks
Version: 0.9.1
Release: owl5
License: GPL
Group: Applications/Internet
URL: http://elinks.or.cz
Source: http://elinks.or.cz/download/%name-%version.tar.bz2
Patch0: elinks-0.9.1-owl-config.diff
Patch1: elinks-0.9.1-owl-config-handling.diff
Patch2: elinks-0.9.1-owl-tmp.diff
Patch3: elinks-0.9.1-owl-vitmp.diff
Patch4: elinks-0.9.1-owl-no-xterm-title.diff
Patch5: elinks-0.9.1-owl-no-uname-leak.diff
Patch6: elinks-0.9.1-owl-external-programs.diff
Patch10: elinks-0.9.1-owl-man.diff
Requires: gpm, zlib, bzip2, openssl
Provides: links
Obsoletes: links
BuildRequires: gpm-devel, zlib-devel, bzip2-devel, openssl-devel >= 0.9.7g-owl1
BuildRoot: /override/%name-%version

%description
ELinks is a text mode WWW browser, supporting colors, table rendering,
background downloading, menu driven configuration interface, tabbed
browsing and slim code.

Frames are supported.  You can have different file formats associated
with external viewers.  mailto: and telnet: are supported via external
clients.

ELinks was forked from the original Links browser written by Mikulas Patocka.
It is in no way associated with Twibright Labs and their Links version.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch10 -p1

%build
export ac_cv_header_expat_h=no \
%configure \
	--with-gpm --with-zlib --with-bzlib --with-openssl \
	--without-guile --without-lua --without-gnutls --without-x \
	--enable-ipv6
make

%install
rm -rf %buildroot
make install DESTDIR=%buildroot

pushd %buildroot
ln -sf elinks .%_bindir/links
ln -s elinks.1 .%_mandir/man1/links.1
popd

# Remove unpackaged files
rm %buildroot%_datadir/locale/locale.alias

%find_lang %name

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS BUGS NEWS README SITES THANKS TODO
%doc doc/bookmarks.txt doc/feedback.txt doc/mailcap.html doc/mime.html
%_bindir/%name
%_bindir/links
%_mandir/man?/*

%changelog
* Sat Jun 25 2005 Dmitry V. Levin <ldv@owl.openwall.com> 0.9.1-owl5
- Rebuilt with libssl.so.5.

* Fri Feb 06 2004 Michail Litvak <mci@owl.openwall.com> 0.9.1-owl4
- Fix yet another bug in -owl-tmp patch (Thanks to Maxim Timofeyev).

* Sun Feb 01 2004 Solar Designer <solar@owl.openwall.com> 0.9.1-owl3
- Don't leak kernel version information (uname -srm) via User-Agent by
default.

* Sun Feb 01 2004 Michail Litvak <mci@owl.openwall.com> 0.9.1-owl2
- Fix bug in -owl-tmp patch (Thanks to Alexey Tourbin for report).

* Wed Jan 28 2004 Michail Litvak <mci@owl.openwall.com> 0.9.1-owl1
- 0.9.1
- Regenerated patches.
- Provide symlinks links -> elinks, links.1 -> elinks.1

* Sun Jan 25 2004 Solar Designer <solar@owl.openwall.com> 0.9.0-owl2
- Use vitmp in textarea_edit().
- Minor corrections to the temporary file handling patch.
- Do not set xterm window title (it wasn't getting reset when Elinks is
exited, the URL wasn't sanitized before being used as a part of a terminal
escape sequence, and some xterm's and window managers are known to have
vulnerabilities exploitable via the window title string).
- Don't define external programs for tn3270, gopher, news, and irc URLs by
default.
- When invoking external programs, treat '-' as an unsafe character unless
it is preceded by a safe non-whitespace one.
- man page corrections and updates of the "see also" lists for Owl.
- Enable/disable the use of external libraries explicitly, do not depend
on what libraries might happen to be installed on the build system.
- Obsoletes: links

* Wed Jan 21 2004 Michail Litvak <mci@owl.openwall.com> 0.9.0-owl1
- Switch from Links to ELinks.

* Tue Feb 05 2002 Michail Litvak <mci@owl.openwall.com> 0.96-owl2
- Enforce our new spec file conventions

* Fri Jul 27 2001 Michail Litvak <mci@owl.openwall.com>
- updated to 0.96
- remove configure patch, because it was included in source

* Sat Jun 07 2001 Michail Litvak <mci@owl.openwall.com>
- patch configure.in to force error if OpenSSL not found

* Sat Jun 04 2001 Michail Litvak <mci@owl.openwall.com>
- TMPDIR support
- compile with SSL
- include man page into %files
- mkstemp patch renamed to *-tmp.diff
- some spec and patch cleanups

* Sat Jun 02 2001 Michail Litvak <mci@owl.openwall.com>
- spec file imported from ASP linux
- patch to replace tempnam with mkstemp

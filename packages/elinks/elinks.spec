# $Id: Owl/packages/elinks/elinks.spec,v 1.4 2004/01/25 12:44:23 solar Exp $

Summary: Lynx-like text WWW browser with many features.
Name: elinks
Version: 0.9.0
Release: owl2
License: GPL
Group: Applications/Internet
URL: http://elinks.or.cz
Source: http://elinks.or.cz/download/%name-%version.tar.bz2
Patch0: elinks-0.9.0-owl-tmp.diff
Patch1: elinks-0.9.0-owl-vitmp.diff
Patch2: elinks-0.9.0-owl-no-xterm-title.diff
Requires: gpm, zlib, bzip2, openssl
Obsoletes: links
BuildRequires: gpm-devel, zlib-devel, bzip2-devel, openssl-devel
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

%build
%configure \
	--with-gpm --with-zlib --with-bzlib --with-openssl \
	--without-xbel --without-guile --without-lua --without-gnutls \
	--without-x \
	--enable-ipv6 --enable-leds \
	--disable-smb
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %name

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS BUGS NEWS README SITES THANKS TODO
%doc doc/bookmarks.txt doc/feedback.txt doc/mailcap.html doc/mime.html
%_bindir/%name
%_mandir/man?/*

%changelog
* Sun Jan 25 2004 Solar Designer <solar@owl.openwall.com> 0.9.0-owl2
- Use vitmp in textarea_edit().
- Minor corrections to the temporary file handling patch.
- Do not set xterm window title (it wasn't getting reset when Elinks is
exited, the URL wasn't sanitized before being used as a part of a terminal
escape sequence, and some xterm's and window managers are known to have
vulnerabilities exploitable via the window title string).
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

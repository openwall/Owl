# $Id: Owl/packages/elinks/elinks.spec,v 1.1 2004/01/21 00:51:58 mci Exp $

Summary: Lynx-like text WWW browser with many features.
Name: elinks
Version: 0.9.0
Release: owl1
License: GPL
Group: Applications/Internet
URL: http://elinks.or.cz/
Source: http://elinks.or.cz/download/%{name}-%{version}.tar.bz2
Patch0: elinks-0.9.0-owl-tmp.diff
Requires: openssl
BuildRequires: openssl-devel
BuildRoot: /override/%name-%version

%description
ELinks is a text mode WWW browser, supporting colors, table rendering,
background downloading, menu driven configuration interface, tabbed
browsing and slim code.

Frames are supported.  You can have different file formats associated
with external viewers. mailto: and telnet: are supported via external
clients.

ELinks was forked from the original Links browser written by Mikulas Patocka.
It is in no way associated with Twibright Labs and their Links version.

%prep
%setup -q
%patch0 -p1

%build
%configure --with-ssl --enable-leds
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
* Wed Jan 21 2004 Michail Litvak <mci@owl.openwall.com> 0.9.0-owl1
- Switch to ELinks.

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

# $Id: Owl/packages/links/Attic/links.spec,v 1.12 2003/10/30 09:00:26 solar Exp $

Summary: Lynx-like text WWW browser with support for frames.
Name: links
Version: 0.96
Release: owl2
License: GPL
Group: Applications/Internet
Source: http://artax.karlin.mff.cuni.cz/~mikulas/links/download/%name-%version.tar.gz
Patch0: links-0.96-asp-koi.diff
Patch1: links-0.96-owl-tmp.diff
Requires: openssl
BuildRequires: openssl-devel
BuildRoot: /override/%name-%version

%description
links is a character mode World Wide Web browser.  It supports colors,
correct table and frames rendering, international codepages and user
interfaces, background downloads, multiple connected instances and it
is small and fast.

links has preliminary support for password authentication, cookies
(in-memory only), and simple bookmarks.

It supports SSL, but that's still in the testing phase.  Be warned
that no site certificate checks are currently implemented.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure --with-ssl
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README SITES TODO
%_bindir/links
%_mandir/man1/*

%changelog
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

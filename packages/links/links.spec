# $Id: Owl/packages/links/Attic/links.spec,v 1.5 2001/06/07 13:00:09 mci Exp $

Name: links
Summary: Lynx-like text WWW browser with support for frames
Version: 0.95
Release: 5owl
Copyright: GPL
Source: http://artax.karlin.mff.cuni.cz/~mikulas/links/download/%{name}-%{version}.tar.gz
Group: Applications/Internet
BuildRoot: /var/rpm-buildroot/%{name}-%{version}
Patch0: links-0.95-asp-koi.diff
Patch1: links-0.95-owl-tmp.diff
Patch2: links-0.95-owl-confssl.diff
Requires: openssl
BuildPreReq: openssl-devel

%description
Links is a character mode world wide web browser.  It supports colors,
correct table and frames rendering, international codepages and user
interfaces, background downloads, multiple connected instances and it
is small and fast.

Links has preliminary support for password authentication, cookies
(in-memory only), and simple bookmarks.

It supports SSL, but it's still in the testing phase - if it breaks,
don't use it. :-)

%prep
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
autoconf
%configure --with-ssl

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README SITES TODO
%{_bindir}/links
%{_mandir}/man1/*

%changelog
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

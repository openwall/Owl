# $Id: Owl/packages/gnupg/gnupg.spec,v 1.8 2002/02/07 21:04:23 solar Exp $

Summary: A GNU utility for secure communication and data storage.
Name: gnupg
Version: 1.0.6
Release: owl1
License: GPL
Group: Applications/Cryptography
URL: http://www.gnupg.org/
Source: ftp://ftp.gnupg.org/pub/gcrypt/gnupg/%{name}-%{version}.tar.gz
Patch0: gnupg-1.0.2-rh-locale.diff
Patch1: gnupg-1.0.4-cvs-secret-key-checks.diff
Provides: gpg, openpgp
BuildRoot: /override/%{name}-%{version}

%description
GnuPG (GNU Privacy Guard) is a GNU utility for encrypting data and
creating digital signatures.  GnuPG has advanced key management
capabilities and is compliant with the proposed OpenPGP Internet
standard described in RFC2440.  Since GnuPG doesn't use any patented
algorithm, it is not compatible with any version of PGP2 (PGP2.x uses
only IDEA for symmetric-key encryption, which is patented worldwide).

%prep
%setup -q
%patch0 -p1
%patch1 -p0

%build
unset LINGUAS || :
%configure --enable-shared
make

%install
%makeinstall
sed 's^\.\./g[0-9\.]*/^^g' tools/lspgpot > lspgpot
install -m 755 lspgpot $RPM_BUILD_ROOT%{_bindir}/lspgpot

# Strip files otherwise not touched
strip $RPM_BUILD_ROOT/usr/lib/gnupg/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS PROJECTS README THANKS TODO
%doc doc/DETAILS doc/FAQ doc/HACKING doc/OpenPGP doc/faq.html
%doc g*/OPTIONS g*/pubring.asc

%{_bindir}/gpg
%{_bindir}/gpgv
%{_bindir}/lspgpot
%{_datadir}/gnupg
%{_datadir}/locale/*/*/*
%{_libdir}/gnupg
%{_mandir}/man1/gpg.*
%{_mandir}/man1/gpgv.*

%changelog
* Sun Feb 03 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Wed May 30 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 1.0.6.

* Sun May 27 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- upgraded to 1.0.5

* Mon Mar 26 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- additional checks to secret key
- add the --allow-secret-key-import patch from CVS

* Thu Dec 14 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- detached signatures security fix

* Wed Oct 25 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

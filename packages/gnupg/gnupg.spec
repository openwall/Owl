# $Id: Owl/packages/gnupg/gnupg.spec,v 1.3 2000/12/14 20:43:02 kad Exp $

Summary: 	A GNU utility for secure communication and data storage.
Name: 		gnupg
Version:	1.0.4
Release: 	5owl
Copyright:	GPL
Group: 		Applications/Cryptography
Source0: 	ftp://ftp.gnupg.org/pub/gcrypt/gnupg/%{name}-%{version}.tar.gz
Patch0: 	gnupg-1.0.2-rh-locale.diff
Patch1: 	gnupg-1.0.3-rh-spell.diff
Patch2: 	gnupg-1.0.4-rh-rijndael.diff
Patch3: 	gnupg-1.0.4-rh-strlen-bug.diff
Patch4:		gnupg-1.0.4-owl-security.diff
URL: 		http://www.gnupg.org/
Provides: 	gpg openpgp
BuildRoot: 	/var/rpm-buildroot/%{name}-root

%description
GnuPG (GNU Privacy Guard) is a GNU utility for encrypting data and
creating digital signatures. GnuPG has advanced key management
capabilities and is compliant with the proposed OpenPGP Internet
standard described in RFC2440. Since GnuPG doesn't use any patented
algorithm, it is not compatible with any version of PGP2 (PGP2.x uses
only IDEA for symmetric-key encryption, which is patented worldwide).

%prep
%setup -q
%patch1 -p1 -b .typos
%patch2 -p1 -b .rijndael
%patch3 -p1 -b .strlen

%build
unset LINGUAS || :
%configure --enable-shared
make

%clean
rm -rf $RPM_BUILD_ROOT

%install
%{makeinstall}
sed 's^\.\./g[0-9\.]*/^^g' tools/lspgpot > lspgpot
install -m755 lspgpot $RPM_BUILD_ROOT%{_bindir}/lspgpot

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
* Thu Dec 14 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- detached signatures security fix

* Wed Oct 25 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

* Thu Oct 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix a bug preventing creation of .gnupg directories

* Wed Oct 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- add patch to recognize AES signatures properly (#19312)
- add gpgv to the package

* Tue Oct 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.0.4 to get security fix

* Tue Oct 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix man page typos (#18797)

* Thu Sep 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.0.3
- switch to bundled copy of the man page

* Wed Aug 30 2000 Matt Wilson <msw@redhat.com>
- rebuild to cope with glibc locale binary incompatibility, again

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- revert locale patch (#16222)

* Tue Aug 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- set all locale data instead of LC_MESSAGES and LC_TIME (#16222)

* Sun Jul 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.0.2

* Wed Jul 19 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild to cope with glibc locale binary incompatibility

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jul 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- include lspgpot (#13772)

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new build environment

* Fri Feb 18 2000 Bill Nottingham <notting@redhat.com>
- build of 1.0.1

* Fri Sep 10 1999 Cristian Gafton <gafton@redhat.com>
- version 1.0.0 build for 6.1us

# $Id: Owl/packages/gnupg/gnupg.spec,v 1.14 2002/05/19 03:46:15 solar Exp $

Summary: A GNU utility for secure communication and data storage.
Name: gnupg
Version: 1.0.7
Release: owl1
License: GPL
Group: Applications/Cryptography
URL: http://www.gnupg.org
Source: ftp://ftp.gnupg.org/pub/gcrypt/gnupg/%{name}-%{version}.tar.gz
Patch0: gnupg-1.0.7-fw-secret-key-checks.diff
PreReq: /sbin/install-info
Provides: gpg, openpgp
BuildRequires: zlib-devel, bison, texinfo
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
rm zlib/*
cat > zlib/Makefile.in << EOF
all:
install:
EOF
%patch0 -p1

%build
unset LINGUAS || :
%configure
make INFO_DEPS='gpg.info gpgv.info'

%install
%makeinstall transform= INFO_DEPS='gpg.info gpgv.info'
sed 's^\.\./g[0-9\.]*/^^g' tools/lspgpot > lspgpot
install -m 755 lspgpot $RPM_BUILD_ROOT%{_bindir}/lspgpot

# Strip files otherwise not touched
strip $RPM_BUILD_ROOT/usr/lib/gnupg/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/gpg.info.gz %{_infodir}/dir \
	--entry "* GnuPG: (gpg).                                Encryption and signing tool."
/sbin/install-info %{_infodir}/gpgv.info.gz %{_infodir}/dir \
	--entry "* gpgv: (gpgv).                                GnuPG signature verification tool."

%preun
if [ $1 -eq 0 ]; then
        /sbin/install-info --delete %{_infodir}/gpg.info.gz %{_infodir}/dir \
		--entry "* GnuPG: (gpg).                                Encryption and signing tool."
        /sbin/install-info --delete %{_infodir}/gpgv.info.gz %{_infodir}/dir \
		--entry "* gpgv: (gpgv).                                GnuPG signature verification tool."
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS PROJECTS README THANKS TODO
%doc doc/{DETAILS,FAQ,HACKING,OpenPGP,*.html}

%{_bindir}/gpg
%{_bindir}/gpgv
%{_bindir}/lspgpot
%{_datadir}/gnupg
%{_datadir}/locale/*/*/*
%{_libdir}/gnupg
%{_mandir}/man1/gpg.*
%{_mandir}/man1/gpgv.*
%{_infodir}/gpg.*
%{_infodir}/gpgv.*

%changelog
* Fri May 17 2002 Michail Litvak <mci@owl.openwall.com>
- 1.0.7
- updated -fw-secret-key-checks patch (by Florian Weimer,
  http://cert.uni-stuttgart.de/files/fw/gnupg-klima-rosa.diff)
- add info files into package

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

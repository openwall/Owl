# $Id: Owl/packages/gnupg/gnupg.spec,v 1.24 2004/09/10 07:23:50 galaxy Exp $

Summary: A GNU utility for secure communication and data storage.
Name: gnupg
Version: 1.2.2
Release: owl3
License: GPL
Group: Applications/Cryptography
URL: http://www.gnupg.org
Source: ftp://ftp.gnupg.org/GnuPG/gnupg/%name-%version.tar.bz2
Patch0: gnupg-1.2.2-fw-secret-key-checks.diff
Patch1: gnupg-1.2.2-ds-no-elgamal.diff
PreReq: /sbin/install-info
Provides: gpg, openpgp
BuildRequires: zlib-devel, bison, texinfo
BuildRoot: /override/%name-%version

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
%patch1 -p1

%build
unset LINGUAS || :
%configure \
	--with-included-gettext \
	--with-static-rnd=linux \
	--with-mailprog=/usr/sbin/sendmail
make

%install
mkdir -p $RPM_BUILD_ROOT%_libdir/%name
%makeinstall transform=
sed 's,\.\./g[0-9\.]*/,,g' tools/lspgpot > lspgpot
install -m 755 lspgpot $RPM_BUILD_ROOT%_bindir/lspgpot

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot%_bindir/gpgsplit
rm %buildroot%_datadir/gnupg/FAQ
rm %buildroot%_datadir/gnupg/faq.html
rm %buildroot%_infodir/dir
rm %buildroot%_datadir/locale/locale.alias

%post
/sbin/install-info %_infodir/gpg.info.gz %_infodir/dir \
	--entry "* GnuPG: (gpg).                                 Encryption and signing tool."
/sbin/install-info %_infodir/gpgv.info.gz %_infodir/dir \
	--entry "* gpgv: (gpgv).                                 GnuPG signature verification tool."

%preun
if [ $1 -eq 0 ]; then
        /sbin/install-info --delete %_infodir/gpg.info.gz %_infodir/dir \
		--entry "* GnuPG: (gpg).                                 Encryption and signing tool."
        /sbin/install-info --delete %_infodir/gpgv.info.gz %_infodir/dir \
		--entry "* gpgv: (gpgv).                                 GnuPG signature verification tool."
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS PROJECTS README THANKS TODO
%doc doc/{DETAILS,FAQ,HACKING,OpenPGP,*.html}
%doc tools/convert-from-106

%_bindir/gpg
%_bindir/gpgv
%_bindir/lspgpot
%_datadir/locale/*/*/*
%_libdir/%name
%_mandir/man1/gpg.*
%_mandir/man1/gpgv.*
%_mandir/man7/gnupg.*
%_infodir/gpg.*
%_infodir/gpgv.*
%_libexecdir/*
%dir %_datadir/gnupg
%config(noreplace) %_datadir/gnupg/options.skel

%changelog
* Sat Nov 29 2003 Michail Litvak <mci@owl.openwall.com> 1.2.2-owl3
- Added patch by David Shaw to disable the ability to create signatures
using the ElGamal sign+encrypt (type 20) keys as well as to remove
the option to create such keys.

* Fri May 16 2003 Michail Litvak <mci@owl.openwall.com> 1.2.2-owl2
- %dir %_datadir/gnupg

* Sun May 11 2003 Michail Litvak <mci@owl.openwall.com> 1.2.2-owl1
- 1.2.2 (Fixed key validity bug)
- built with --included-gettext
- spec file cleanups

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

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

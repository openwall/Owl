# $Id: Owl/packages/gnupg/gnupg.spec,v 1.28 2005/10/24 03:06:24 solar Exp $

Summary: A GNU utility for secure communication and data storage.
Name: gnupg
Version: 1.2.6
Release: owl1
License: GPL
Group: Applications/Cryptography
URL: http://www.gnupg.org
Source: ftp://ftp.gnupg.org/GnuPG/gnupg/%name-%version.tar.bz2
Patch0: gnupg-1.2.2-fw-secret-key-checks.diff
PreReq: /sbin/install-info
Provides: gpg, openpgp
BuildRequires: zlib-devel, bison, texinfo
BuildRequires: rpm-build >= 0:4
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

%build
unset LINGUAS || :
%configure \
	--with-static-rnd=linux \
	--with-mailprog=/usr/sbin/sendmail
make

%install
mkdir -p %buildroot%_libdir/%name
%makeinstall transform=
sed 's,\.\./g[0-9\.]*/,,g' tools/lspgpot > lspgpot
install -m 755 lspgpot %buildroot%_bindir/lspgpot

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
%_bindir/gpgsplit
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
%exclude %_datadir/gnupg/FAQ
%exclude %_datadir/gnupg/faq.html
%exclude %_infodir/dir

%changelog
* Fri Dec 03 2004 Michail Litvak <mci-at-owl.openwall.com> 1.2.6-owl1
- 1.2.6
- Dropped patch which was included into upstream.
- Package gpgsplit tool.

* Sat Nov 29 2003 Michail Litvak <mci-at-owl.openwall.com> 1.2.2-owl3
- Added patch by David Shaw to disable the ability to create signatures
using the ElGamal sign+encrypt (type 20) keys as well as to remove
the option to create such keys.

* Fri May 16 2003 Michail Litvak <mci-at-owl.openwall.com> 1.2.2-owl2
- %dir %_datadir/gnupg

* Sun May 11 2003 Michail Litvak <mci-at-owl.openwall.com> 1.2.2-owl1
- 1.2.2 (Fixed key validity bug)
- built with --included-gettext
- spec file cleanups

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Fri May 17 2002 Michail Litvak <mci-at-owl.openwall.com>
- 1.0.7
- updated -fw-secret-key-checks patch (by Florian Weimer,
  http://cert.uni-stuttgart.de/files/fw/gnupg-klima-rosa.diff)
- add info files into package

* Sun Feb 03 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Wed May 30 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 1.0.6.

* Sun May 27 2001 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- upgraded to 1.0.5

* Mon Mar 26 2001 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- additional checks to secret key
- add the --allow-secret-key-import patch from CVS

* Thu Dec 14 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- detached signatures security fix

* Wed Oct 25 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH

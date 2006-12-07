# $Owl: Owl/packages/gnupg/gnupg.spec,v 1.31.2.5 2006/12/07 22:15:19 ldv Exp $

Summary: A GNU utility for secure communication and data storage.
Name: gnupg
Version: 1.4.6
Release: owl0.2.0.1
License: GPL
Group: Applications/Cryptography
URL: http://www.gnupg.org
Source0: ftp://ftp.gnupg.org/gcrypt/gnupg/%name-%version.tar.bz2
Source1: gpgsplit.1
Source2: lspgpot.1
Patch0: gnupg-1.4.3-alt-ru.po.diff
Patch1: gnupg-1.4.3-alt-always-trust.diff
Patch2: gnupg-1.4.2-alt-cp1251.diff
Patch3: gnupg-1.4.2-fw-secret-key-checks.diff
Patch4: gnupg-1.4.6-alt-owl-info.diff
PreReq: /sbin/install-info
Provides: gpg, openpgp
BuildRequires: zlib-devel, bzip2-devel, texinfo, readline-devel
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
bzip2 -9k NEWS doc/{DETAILS,FAQ}

%build
%configure \
	--with-static-rnd=linux \
	--with-mailprog=/usr/sbin/sendmail \
	--enable-noexecstack
%__make

%install
mkdir -p %buildroot%_libdir/%name
%makeinstall transform=
sed 's,\.\./g[0-9\.]*/,,g' tools/lspgpot > lspgpot
install -m755 lspgpot %buildroot%_bindir/lspgpot

install -pm644 %_sourcedir/{gpgsplit,lspgpot}.1 %buildroot%_mandir/man1/

# Move localized manpages to FHS compliant locations
mkdir -p %buildroot%_mandir/ru/man1
mv %buildroot%_mandir/man1/gpg.ru.1 %buildroot%_mandir/ru/man1/gpg.1

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/gnupg1.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
        /sbin/install-info --delete %_infodir/gnupg1.info %_infodir/dir
fi

%triggerpostun -- %name < 1.4.6
/sbin/install-info --delete %_infodir/gpg.info %_infodir/dir
/sbin/install-info --delete %_infodir/gpgv.info %_infodir/dir

%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS.bz2 PROJECTS README THANKS TODO
%doc doc/{DETAILS.bz2,FAQ.bz2,HACKING,OpenPGP,*.html}
%doc tools/convert-from-106

%_bindir/gpg
%_bindir/gpg-zip
%_bindir/gpgsplit
%_bindir/gpgv
%_bindir/lspgpot
%_datadir/locale/*/*/*
%_libdir/%name
%_mandir/man1/*
%_mandir/ru/man1/gpg.*
%_mandir/man7/gnupg.*
%_infodir/gnupg1.*
%_libexecdir/*
%dir %_datadir/gnupg
%config(noreplace) %_datadir/gnupg/options.skel
%exclude %_datadir/gnupg/FAQ
%exclude %_datadir/gnupg/faq.html

%changelog
* Thu Dec 07 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.6-owl0.2.0.1
- Updated to 1.4.6.  This includes a fix for a remotely controllable
function pointer vulnerability (CVE-2006-6235): using malformed OpenPGP
packets an attacker was able to modify and dereference a function pointer
in gpg.

* Wed Nov 29 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.5-owl0.2.0.2
- Applied upstream fix for heap buffer overflow bug in interactive
gpg, see
http://lists.gnupg.org/pipermail/gnupg-announce/2006q4/000241.html
for details.

* Fri Aug 04 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.5-owl0.2.0.1
- Updated to 1.4.5.  This includes fixes for two more possible memory
allocation bugs (CVE-2006-3746), similar to the problem fixed in 1.4.4.

* Wed Jun 28 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.4-owl0.2.0.1
- Updated to 1.4.4.  This release includes fix for integer overflow
vulnerability in packet processing that could allow a remote attacker
to cause gpg to crash and possibly overwrite memory via a message packet
with a large length (CVE-2006-3082).
- Imported gpgsplit(1) and lspgpot(1) manual pages and gpgv(1) fixes
from Debian gnupg package.
- Imported Russian translation fixes from ALT gnupg package.
- Simplified info files installation.

* Sat Mar 11 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.2.2-owl1
- Updated to 1.4.2.2.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.2-owl2
- Dropped ChangeLog file, compressed NEWS file.

* Sat Nov 19 2005 Michail Litvak <mci-at-owl.openwall.com> 1.4.2-owl1
- 1.4.2
- Imported patches from ALT, Red Hat, Debian.

* Fri Dec 03 2004 Michail Litvak <mci-at-owl.openwall.com> 1.2.6-owl1
- 1.2.6
- Dropped patch which was included into upstream.
- Package gpgsplit tool.

* Sat Nov 29 2003 Michail Litvak <mci-at-owl.openwall.com> 1.2.2-owl3
- Added patch by David Shaw to disable the ability to create signatures
using the ElGamal sign+encrypt (type 20) keys as well as to remove
the option to create such keys.

* Fri May 16 2003 Michail Litvak <mci-at-owl.openwall.com> 1.2.2-owl2
- %%dir %_datadir/gnupg

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

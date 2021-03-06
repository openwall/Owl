# $Owl: Owl/packages/gnupg/gnupg.spec,v 1.55 2018/07/03 13:18:37 solar Exp $

Summary: A GNU utility for secure communication and data storage.
Name: gnupg
Version: 1.4.23
Release: owl1
License: GPL
Group: Applications/Cryptography
URL: http://www.gnupg.org
Source0: %name-%version.tar.xz
# ftp://ftp.gnupg.org/gcrypt/gnupg/%name-%version.tar.bz2
# Signature: ftp://ftp.gnupg.org/gcrypt/gnupg/%name-%version.tar.bz2.sig
Source1: gpgsplit.1
Source2: lspgpot.1
Patch0: gnupg-1.4.23-alt.diff
Patch1: gnupg-1.4.11-alt-owl-info.diff
Patch2: gnupg-1.4.11-owl-setuid.diff
Requires(post,preun): /sbin/install-info
Provides: gpg, openpgp
BuildRequires: zlib-devel, bzip2-devel, texinfo, readline-devel >= 0:4.3
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
bzip2 -9k NEWS doc/{DETAILS,FAQ}

%build
%configure \
	--enable-static-rnd=linux \
	--with-mailprog=/usr/sbin/sendmail \
	--with-libusb=no \
	--enable-noexecstack
%__make

%check
%__make check

%install
mkdir -p %buildroot%_libdir/%name
%makeinstall transform=
sed 's,\.\./g[0-9\.]*/,,g' tools/lspgpot > lspgpot
install -m755 lspgpot %buildroot%_bindir/lspgpot

install -pm644 %_sourcedir/{gpgsplit,lspgpot}.1 %buildroot%_mandir/man1/

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
%doc doc/{DETAILS.bz2,FAQ.bz2,HACKING,OpenPGP}
%doc tools/convert-from-106

%_bindir/gpg
%_bindir/gpg-zip
%_bindir/gpgsplit
%_bindir/gpgv
%_bindir/lspgpot
%_datadir/locale/*/*/*
%_libdir/%name
%_mandir/man?/*
%_infodir/*.info*
%_libexecdir/*
%dir %_datadir/gnupg
%config(noreplace) %_datadir/gnupg/options.skel
%exclude %_datadir/gnupg/FAQ

%changelog
* Tue Jul 03 2018 Solar Designer <solar-at-owl.openwall.com> 1.4.23-owl1
- Updated to 1.4.23 with the ALT patch based on 1.4.22-alt2 with the upstream
backports removed (included in 1.4.23).

* Tue Aug 23 2016 Solar Designer <solar-at-owl.openwall.com> 1.4.21-owl1
- Updated to 1.4.21.

* Thu Jul 10 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.4.18-owl2
- Replaced the deprecated PreReq tag with Requires(post,preun).

* Mon Jul 07 2014 Solar Designer <solar-at-owl.openwall.com> 1.4.18-owl1
- Updated to 1.4.18.
- Switched to using a combined ALT Linux patch.

* Fri Feb 22 2013 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.4.13-owl1
- Updated to 1.4.13.
- Fixed a memory corruption and public keyring database corruption bug on
malformed key importing.  For the details see:
https://bugzilla.redhat.com/show_bug.cgi?id=891142
https://bugs.g10code.com/gnupg/issue1455
- Updated -alt-ru.po and -alt-cp1251 patches.

* Wed Apr 06 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.4.11-owl2
- Removed a dependency on libusb.  Reported by Chris Bopp.

* Fri Oct 29 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.4.11-owl1
- Updated to 1.4.11.
- Introduced setuid() return code check.

* Wed Sep 09 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.10-owl1
- Updated to 1.4.10.

* Wed Mar 26 2008 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.9-owl1
- Updated to 1.4.9.

* Tue Jan 01 2008 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.8-owl1
- Updated to 1.4.8.

* Tue Mar 06 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.7-owl1
- Updated to 1.4.7.

* Wed Dec 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.6-owl1
- Updated to 1.4.6.

* Tue Nov 28 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.5-owl3
- Applied upstream fix for heap buffer overflow bug in interactive
gpg, see
http://lists.gnupg.org/pipermail/gnupg-announce/2006q4/000241.html
for details.

* Sun Sep 03 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.4.5-owl2
- Relaxed the build dependency on readline-devel.

* Fri Aug 04 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.5-owl1
- Updated to 1.4.5.

* Wed Jun 28 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.4-owl1
- Updated to 1.4.4.

* Thu Jun 22 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.3-owl1
- Updated to 1.4.3.
- Applied upstream fix for crash bug in parse-packet.c (CVE-2006-3082).
- Imported gpgsplit(1) and lspgpot(1) manual pages and gpgv(1) fixes
from Debian gnupg package.
- Imported Russian translation fixes from ALT gnupg package.
- Simplified info files installation.

* Sun May 21 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.2.2-owl2
- Rebuilt with libreadline.so.5.

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

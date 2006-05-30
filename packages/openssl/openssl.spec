# $Owl: Owl/packages/openssl/openssl.spec,v 1.59 2006/05/30 23:30:09 ldv Exp $

Summary: Secure Sockets Layer and cryptography libraries and tools.
Name: openssl
Version: 0.9.7g
Release: owl5
License: distributable
Group: System Environment/Libraries
URL: http://www.openssl.org
Source: ftp://ftp.openssl.org/source/%name-%version.tar.gz
Patch0: openssl-0.9.7g-owl-alt-issetugid.diff
Patch1: openssl-0.9.7g-mdk-alt-Makefile.diff
Patch2: openssl-0.9.7g-rh-alt-soversion.diff
Patch3: openssl-0.9.7g-rh-mdk-ia64-asm.diff
Patch4: openssl-0.9.7g-rh-version-engines.diff
Patch5: openssl-0.9.7g-up-rh-fixes.diff
Patch6: openssl-0.9.7g-rh-consttime.diff
Patch7: openssl-0.9.7g-up-SSL_OP_MSIE_SSLV2_RSA_PADDING.diff
Provides: SSL
%ifnarch x86_64
# For backwards compatibility.
Provides: libcrypto.so.4, libssl.so.4
%endif
BuildRequires: perl, diffutils
# Due to sed -i.
BuildRequires: sed >= 4.1.1
BuildRequires: /bin/awk
BuildRoot: /override/%name-%version

%description
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, fully featured, and Open Source toolkit implementing the
Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS v1)
protocols as well as a full-strength general purpose cryptography library.
The project is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL toolkit and its
related documentation.

OpenSSL is based on the excellent SSLeay library developed from Eric A.
Young and Tim J. Hudson.  The OpenSSL toolkit is licensed under an
Apache-style licence, which basically means that you are free to get and
use it for commercial and non-commercial purposes.

This package contains the base OpenSSL cryptography and SSL/TLS
libraries and tools.

%package devel
Summary: Secure Sockets Layer and cryptography static libraries and headers.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, fully featured, and Open Source toolkit implementing the
Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS v1)
protocols as well as a full-strength general purpose cryptography library.
The project is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL toolkit and its
related documentation.

OpenSSL is based on the excellent SSLeay library developed from Eric A.
Young and Tim J. Hudson.  The OpenSSL toolkit is licensed under an
Apache-style licence, which basically means that you are free to get and
use it for commercial and non-commercial purposes.

This package contains the OpenSSL cryptography and SSL/TLS static
libraries and header files required when developing or building
applications from source code.

%package perl
Summary: Miscellaneous OpenSSL scripts written in Perl.
Group: Applications/Internet
Requires: %name = %version-%release

%description perl
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, fully featured, and Open Source toolkit implementing the
Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS v1)
protocols as well as a full-strength general purpose cryptography library.
The project is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL toolkit and its
related documentation.

OpenSSL is based on the excellent SSLeay library developed from Eric A.
Young and Tim J. Hudson.  The OpenSSL toolkit is licensed under an
Apache-style licence, which basically means that you are free to get and
use it for commercial and non-commercial purposes.

This package contains some miscellaneous Perl scripts.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p0

bzip2 -9k CHANGES CHANGES.SSLeay

# Avoid conflict with pow10(3).
sed -i s/pow10/pow10i/ crypto/bio/b_print.c

# Correct compilation options.
perl -pi -e 's/-O.(?: -fomit-frame-pointer)?(?: -m.86)?/%optflags/' \
	Configure

# Correct shared library name.
sed -i 's/\\\$(SHLIB_MAJOR)\.\\\$(SHLIB_MINOR)/\\$(VERSION)/g' Configure
sed -i 's/\${SHLIB_MAJOR}\.\${SHLIB_MINOR}/\${VERSION}/g' Makefile.org

%define openssldir %_datadir/ssl
%define opensslflags shared -DSSL_ALLOW_ADH --prefix=%_prefix

%{expand:%%define optflags %optflags -Wall -Wa,--noexecstack}

%build
%ifarch %ix86
%ifarch i386
./Configure %opensslflags --openssldir=%openssldir 386 linux-elf
%else
./Configure %opensslflags --openssldir=%openssldir linux-elf
%endif
%endif
%ifarch x86_64
./Configure %opensslflags --openssldir=%openssldir linux-x86_64
%endif
%ifarch ppc
./Configure %opensslflags --openssldir=%openssldir linux-ppc
%endif
%ifarch alpha alphaev5
./Configure %opensslflags --openssldir=%openssldir linux-alpha-gcc
%endif
%ifarch alphaev56 alphapca56 alphaev6 alphaev67
./Configure %opensslflags --openssldir=%openssldir linux-alpha+bwx-gcc
%endif
%ifarch sparc
./Configure %opensslflags --openssldir=%openssldir linux-sparcv8
%endif
%ifarch sparcv9
./Configure %opensslflags --openssldir=%openssldir linux-sparcv9
%endif

LD_LIBRARY_PATH=`pwd` make SLIB=%_lib
touch -r libcrypto.so.%version libcrypto-stamp
touch -r libssl.so.%version libssl-stamp
LD_LIBRARY_PATH=`pwd` make rehash
LD_LIBRARY_PATH=`pwd` make test

%install
rm -rf %buildroot
%__make install SLIB=%_lib MANDIR=%_mandir INSTALL_PREFIX="%buildroot"

# Fail if one of shared libraries was rebuit.
if [ libcrypto.so.%version -nt libcrypto-stamp -o \
     libssl.so.%version -nt libssl-stamp ]; then
	echo 'Shared library was rebuilt by "make install".'
	exit 1
fi

# Fail if the openssl binary is statically linked against OpenSSL at this
# stage (which could happen if "make install" caused anything to rebuild).
LD_LIBRARY_PATH=`pwd` ldd %buildroot/usr/bin/openssl | tee openssl.libs
grep -qw libssl openssl.libs
grep -qw libcrypto openssl.libs

# Relocate shared libraries from %_libdir/ to /%_lib/.
mkdir %buildroot/%_lib
for f in %buildroot%_libdir/*.so; do
	t=`objdump -p "$f" |awk '/SONAME/ {print $2}'`
	[ -n "$t" ]
	ln -sf ../../%_lib/"$t" "$f"
done
mv %buildroot%_libdir/*.so.* %buildroot/%_lib/

%ifnarch x86_64
# For backwards compatibility.
ln -s libcrypto.so.5 %buildroot/%_lib/libcrypto.so.4
ln -s libssl.so.5 %buildroot/%_lib/libssl.so.4
%endif

# Remove fips fingerprint script.
rm %buildroot%_bindir/openssl_fips_fingerprint

# Rename man pages.
mv %buildroot%_mandir/man1/{,ssl}passwd.1
mv %buildroot%_mandir/man3/{,ssl}err.3
mv %buildroot%_mandir/man3/{,ssl}rand.3

# Make backwards-compatibility symlink to ssleay.
ln -s openssl %buildroot/usr/bin/ssleay

mv %buildroot%_datadir/ssl/misc/CA{.sh,}

# Do not package .pod documentation files.
mkdir docs
cp -a doc docs/
rm -rf docs/doc/{apps,crypto,ssl}
bzip2 -9 docs/doc/ssleay.txt

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%ifnarch x86_64
%triggerpostun -- %name < 0:0.9.7g-owl1
ln -sf libcrypto.so.5 /%_lib/libcrypto.so.4
ln -sf libssl.so.5 /%_lib/libssl.so.4
%endif

%files
%defattr(0644,root,root,0755)
%doc CHANGES*.bz2 LICENSE NEWS README
%doc docs/doc
%attr(0755,root,root) %_bindir/*
%exclude %_bindir/c_rehash
%attr(-,root,root) /%_lib/*.so.?
%attr(0755,root,root) /%_lib/*.so.?.*
%attr(0755,root,root) %openssldir/misc/CA
%attr(0755,root,root) %openssldir/misc/c_*
%attr(0644,root,root) %_mandir/man[157]/*
%exclude %_mandir/man1/CA.pl.1*
%config %attr(0644,root,root) %openssldir/openssl.cnf
%dir %attr(0755,root,root) %openssldir
%dir %attr(0755,root,root) %openssldir/certs
%dir %attr(0755,root,root) %openssldir/misc
%dir %attr(0700,root,root) %openssldir/private

%files devel
%defattr(0644,root,root,0755)
%attr(-,root,root) %_libdir/*.so
%attr(0644,root,root) %_libdir/*.a
%dir %attr(0755,root,root) /usr/include/openssl
%attr(0644,root,root) /usr/include/openssl/*
# XXX: we don't have a package providing %_libdir/pkgconfig directory
%attr(0644,root,root) %_libdir/pkgconfig/openssl.pc
%attr(0644,root,root) %_mandir/man3/*

%files perl
%defattr(0644,root,root,0755)
%attr(0755,root,root) %_bindir/c_rehash
%attr(0755,root,root) %openssldir/misc/CA.pl
%attr(0644,root,root) %_mandir/man1/CA.pl.1*

%changelog
* Sun Apr 30 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.9.7g-owl5
- Introduced the openssl-perl sub-package and moved Perl scripts there.

* Thu Mar 30 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.9.7g-owl4
- Replaced make with %%__make.
- Added the %%openssldir to the main filelist.
- Added /bin/awk to BuildRequires (perhaps, we need to adjust our gawk to
provide 'awk'?)

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.9.7g-owl3
- Compressed ssleay.txt and CHANGES* files.

* Tue Oct 11 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.9.7g-owl2
- Applied upstream fix for potential SSL 2.0 rollback during SSL
handshake (CAN-2005-2969).

* Fri Jun 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.9.7g-owl1
- Updated to 0.9.7g.
- Imported a bunch of patches from RH's openssl-0.9.7f-7 and ALT's
openssl-0.9.7g-alt1 packages, including new constant time/memory access
mod_exp implementation for private key operations, to mitigate timing
attack (CAN-2005-0109).
- Changed soname to match RH's soname convention.
- Packaged soname symlinks along with shared libraries.
- Removed documentation in .pod format.

* Tue Nov 02 2004 Solar Designer <solar-at-owl.openwall.com> 0.9.7d-owl2
- Do package CA.pl; we were packaging CA.pl.pod and CA.pl.1 anyway, and we
had a dependency on Perl anyway (possibly something to be resolved later).
- Remove "Modes of DES.7" man page name which confuses brp-compress.

* Thu Mar 18 2004 Michail Litvak <mci-at-owl.openwall.com> 0.9.7d-owl1
- 0.9.7d

* Thu Mar 18 2004 Solar Designer <solar-at-owl.openwall.com> 0.9.7c-owl3
- Spec file cleanups for issues introduced with the update to 0.9.7+.

* Tue Mar 04 2004 Michail Litvak <mci-at-owl.openwall.com> 0.9.7c-owl2
- Apply RH's soname convention.
- Move libs to /lib and place symlinks to /usr/lib.

* Tue Mar 02 2004 Michail Litvak <mci-at-owl.openwall.com> 0.9.7c-owl1
- 0.9.7c
- Removed patches included by upstream.
- Patch to fix man-pages generation.
- Add /usr/lib/pkgconfig/openssl.pc to the development section.
- Set openssl dir to datadir not to /var.
- Don't install perl scripts (RH install it into openssl-perl package).

* Fri Jan 16 2004 Michail Litvak <mci-at-owl.openwall.com> 0.9.6l-owl2
- Make /usr/include/openssl directory owned by this package.

* Thu Nov 06 2003 Solar Designer <solar-at-owl.openwall.com> 0.9.6l-owl1
- Updated to 0.9.6l.

* Wed Oct 01 2003 Solar Designer <solar-at-owl.openwall.com> 0.9.6k-owl1
- Updated to 0.9.6k.

* Sat Apr 12 2003 Solar Designer <solar-at-owl.openwall.com> 0.9.6j-owl1
- Updated to 0.9.6j.

* Thu Feb 20 2003 Solar Designer <solar-at-owl.openwall.com> 0.9.6i-owl1
- Updated to 0.9.6i.

* Thu Dec 12 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 0.9.6h.
- Dropped clean-shared for the "all" target (invoked by "tests" and
"install"), it resulted in re-linking of shared libraries at best.

* Fri Nov 15 2002 Solar Designer <solar-at-owl.openwall.com>
- Dropped the patch removing -Wl,-Bsymbolic which is no longer needed with
0.9.6g and/or after dropping the explicit "make build-shared".
- Dropped RSAref stuff.

* Wed Sep 25 2002 Solar Designer <solar-at-owl.openwall.com>
- Don't do an explicit "make build-shared", it's not needed and could only
cause harm (link libssl against libcrypto statically), but luckily didn't;
pointed out by Dmitry V. Levin of ALT Linux.

* Mon Aug 12 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 0.9.6g dropping two patches.

* Sat Aug 03 2002 Solar Designer <solar-at-owl.openwall.com>
- Added two post-0.9.6e changes from the CVS which correct the recent ASN.1
parsing vulnerability fixes.

* Wed Jul 31 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 0.9.6e, dropping the shared-on-SPARC and the official security
patches (both are now included).

* Tue Jul 30 2002 Solar Designer <solar-at-owl.openwall.com>
- Applied the official patch with 4 security fixes to problems discovered
by Ben Laurie and others of A.L. Digital Ltd and The Bunker under DARPA's
CHATS program, by consultants at Neohapsis, and by Adi Stav and James Yonan.
The patch has been prepared by Ben Laurie and Dr. Stephen Henson, with one
of the fixes partly based on a version by Adi Stav.
- Renamed the err.3 man page to avoid conflict with the new man-pages
package which documents the BSD-derived libc function under that name.

* Wed May 29 2002 Solar Designer <solar-at-owl.openwall.com>
- Made shared library builds work on SPARC (again).
- Moved the .so symlinks to devel subpackage.

* Sun May 12 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 0.9.6d.
- Added a patch by Ben Laurie for "openssl dgst" to behave on read errors.
- Dropped the incorrect (or no longer correct?) RH-derived configuration
file path patch to ca(1).
- Properly restrict the instruction set in assembly code when building for
i386 (don't use bswapl).

* Wed Feb 06 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Dec 26 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 0.9.6c.

* Wed Jul 11 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 0.9.6b.

* Fri Jul 06 2001 Solar Designer <solar-at-owl.openwall.com>
- Applied patches provided by the OpenSSL team to correct a PRNG
weakness which under unusual circumstances could allow an attacker to
determine internal state of the PRNG and thus to predict future PRNG
output.  This problem has been discovered and reported to the OpenSSL
team by Markku-Juhani O. Saarinen.  No applications are known to be
affected at this time.

* Sun Apr 22 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 0.9.6a which contains a number of security fixes (but breaks
binary compatibility).
- Updated shared libraries building to match the new Makefile conventions.
- Use glibc's __libc_enable_secure for the new OPENSSL_issetugid().
- Various other changes to the spec file.

* Sat Apr 14 2001 Solar Designer <solar-at-owl.openwall.com>
- Support Alpha targets.
- Use the ix86 macro.

* Mon Nov 13 2000 Solar Designer <solar-at-owl.openwall.com>
- Support SPARC targets (32-bit only at this time).

* Sun Oct 29 2000 Solar Designer <solar-at-owl.openwall.com>
- Don't require bc (disable one of the tests if bc isn't available).

* Mon Oct 02 2000 Solar Designer <solar-at-owl.openwall.com>
- Rename the passwd and rand man pages differently (this is still a hack).

* Sun Jul 09 2000 Solar Designer <solar-at-owl.openwall.com>
- Imported Damien Miller's spec file.
- Added two patches from Trustix and, more importantly, a patch to avoid
exporting crypt() as a symbol (which used to override the weak alias for
crypt(3), while applications generally want the libcrypt version).  crypt
defined here is now a #define, so is only available when the appropriate
OpenSSL header is included.

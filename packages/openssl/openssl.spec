# $Id: Owl/packages/openssl/openssl.spec,v 1.42 2004/11/23 22:40:47 mci Exp $

%define soversion 4

Summary: Secure Sockets Layer and cryptography libraries and tools.
Name: openssl
Version: 0.9.7d
Release: owl2
License: distributable
Group: System Environment/Libraries
URL: http://www.openssl.org
Source: ftp://ftp.openssl.org/source/%name-%version.tar.gz
Patch0: openssl-0.9.7c-owl-glibc-enable_secure.diff
Patch1: openssl-0.9.7c-rh-soversion.diff
PreReq: /sbin/ldconfig
Provides: SSL
BuildRequires: perl
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
libraries and header files required when developing applications.

%prep
%setup -q
# XXX: don't rebuild some files at make install time
pushd crypto/objects
touch -r objects.pl *.h
popd
%patch0 -p1
%patch1 -p1

%define openssldir %_datadir/ssl
%define opensslflags shared -DSSL_ALLOW_ADH --prefix=%_prefix

%build
perl -pi -e "s/-O.(?: -fomit-frame-pointer)?(?: -m.86)?/$RPM_OPT_FLAGS/" \
	Configure

%ifarch %ix86
%ifarch i386
./Configure %opensslflags --openssldir=%openssldir 386 linux-elf
%else
./Configure %opensslflags --openssldir=%openssldir linux-elf
%endif
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

LD_LIBRARY_PATH=`pwd` make
LD_LIBRARY_PATH=`pwd` make rehash
LD_LIBRARY_PATH=`pwd` make test

%install
rm -rf %buildroot
make install MANDIR=%_mandir INSTALL_PREFIX="%buildroot"

# Fail if the openssl binary is statically linked against OpenSSL at this
# stage (which could happen if "make install" caused anything to rebuild).
LD_LIBRARY_PATH=`pwd` ldd %buildroot/usr/bin/openssl | tee openssl.libs
grep -qw libssl openssl.libs
grep -qw libcrypto openssl.libs

%define solibbase %(echo %version | sed 's/[[:alpha:]]//g')

mkdir -p %buildroot/%_lib
mv %buildroot/usr/lib/lib*.so.%solibbase %buildroot/%_lib/
rename so.%solibbase so.%version %buildroot/%_lib/*.so.%solibbase
for lib in %buildroot/%_lib/*.so.%version; do
	chmod 755 $lib
	ln -sf ../../%_lib/`basename $lib` %buildroot%_libdir/`basename ${lib} .%version`
	ln -sf ../../%_lib/`basename $lib` %buildroot%_libdir/`basename ${lib} .%version`.%soversion
done

# Rename man pages
mv %buildroot%_mandir/man1/{,ssl}passwd.1
mv %buildroot%_mandir/man3/{,ssl}err.3
mv %buildroot%_mandir/man3/{,ssl}rand.3
# This one already exists as des_modes.7
rm %buildroot%_mandir/man7/"Modes of DES.7"

# Make backwards-compatibility symlink to ssleay
ln -s openssl %buildroot/usr/bin/ssleay

mv %buildroot%_datadir/ssl/misc/CA{.sh,}

# This script is obsolete and insecure.
rm %buildroot%_datadir/ssl/misc/der_chop

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(0644,root,root,0755)
%doc CHANGES CHANGES.SSLeay LICENSE NEWS README
%doc doc
%attr(0755,root,root) %_bindir/*
%attr(0755,root,root) /%_lib/*.so.%version
%attr(0755,root,root) %openssldir/misc/CA
%attr(0755,root,root) %openssldir/misc/CA.pl
%attr(0755,root,root) %openssldir/misc/c_*
%attr(0644,root,root) %_mandir/man[157]/*
%config %attr(0644,root,root) %openssldir/openssl.cnf
%dir %attr(0755,root,root) %openssldir/certs
%dir %attr(0755,root,root) %openssldir/lib
%dir %attr(0755,root,root) %openssldir/misc
%dir %attr(0700,root,root) %openssldir/private

%files devel
%defattr(0644,root,root,0755)
%attr(0644,root,root) /usr/lib/*.a
%attr(0755,root,root) /usr/lib/*.so
%dir %attr(0755,root,root) /usr/include/openssl
%attr(0644,root,root) /usr/include/openssl/*
# XXX: we don't have a package providing /usr/lib/pkgconfig directory
%attr(0644,root,root) /usr/lib/pkgconfig/openssl.pc
%attr(0644,root,root) %_mandir/man3/*

%changelog
* Tue Nov 02 2004 Solar Designer <solar@owl.openwall.com> 0.9.7d-owl2
- Do package CA.pl; we were packaging CA.pl.pod and CA.pl.1 anyway, and we
had a dependency on Perl anyway (possibly something to be resolved later).
- Remove "Modes of DES.7" man page name which confuses brp-compress.

* Thu Mar 18 2004 Michail Litvak <mci@owl.openwall.com> 0.9.7d-owl1
- 0.9.7d

* Thu Mar 18 2004 Solar Designer <solar@owl.openwall.com> 0.9.7c-owl3
- Spec file cleanups for issues introduced with the update to 0.9.7+.

* Tue Mar 04 2004 Michail Litvak <mci@owl.openwall.com> 0.9.7c-owl2
- Apply RH's soname convention.
- Move libs to /lib and place symlinks to /usr/lib.

* Tue Mar 02 2004 Michail Litvak <mci@owl.openwall.com> 0.9.7c-owl1
- 0.9.7c
- Removed patches included by upstream.
- Patch to fix man-pages generation.
- Add /usr/lib/pkgconfig/openssl.pc to the development section.
- Set openssl dir to datadir not to /var.
- Don't install perl scripts (RH install it into openssl-perl package).

* Fri Jan 16 2004 Michail Litvak <mci@owl.openwall.com> 0.9.6l-owl2
- Make /usr/include/openssl directory owned by this package.

* Thu Nov 06 2003 Solar Designer <solar@owl.openwall.com> 0.9.6l-owl1
- Updated to 0.9.6l.

* Wed Oct 01 2003 Solar Designer <solar@owl.openwall.com> 0.9.6k-owl1
- Updated to 0.9.6k.

* Sat Apr 12 2003 Solar Designer <solar@owl.openwall.com> 0.9.6j-owl1
- Updated to 0.9.6j.

* Thu Feb 20 2003 Solar Designer <solar@owl.openwall.com> 0.9.6i-owl1
- Updated to 0.9.6i.

* Thu Dec 12 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 0.9.6h.
- Dropped clean-shared for the "all" target (invoked by "tests" and
"install"), it resulted in re-linking of shared libraries at best.

* Fri Nov 15 2002 Solar Designer <solar@owl.openwall.com>
- Dropped the patch removing -Wl,-Bsymbolic which is no longer needed with
0.9.6g and/or after dropping the explicit "make build-shared".
- Dropped RSAref stuff.

* Wed Sep 25 2002 Solar Designer <solar@owl.openwall.com>
- Don't do an explicit "make build-shared", it's not needed and could only
cause harm (link libssl against libcrypto statically), but luckily didn't;
pointed out by Dmitry V. Levin of ALT Linux.

* Mon Aug 12 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 0.9.6g dropping two patches.

* Sat Aug 03 2002 Solar Designer <solar@owl.openwall.com>
- Added two post-0.9.6e changes from the CVS which correct the recent ASN.1
parsing vulnerability fixes.

* Wed Jul 31 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 0.9.6e, dropping the shared-on-SPARC and the official security
patches (both are now included).

* Tue Jul 30 2002 Solar Designer <solar@owl.openwall.com>
- Applied the official patch with 4 security fixes to problems discovered
by Ben Laurie and others of A.L. Digital Ltd and The Bunker under DARPA's
CHATS program, by consultants at Neohapsis, and by Adi Stav and James Yonan.
The patch has been prepared by Ben Laurie and Dr. Stephen Henson, with one
of the fixes partly based on a version by Adi Stav.
- Renamed the err.3 man page to avoid conflict with the new man-pages
package which documents the BSD-derived libc function under that name.

* Wed May 29 2002 Solar Designer <solar@owl.openwall.com>
- Made shared library builds work on SPARC (again).
- Moved the .so symlinks to devel subpackage.

* Sun May 12 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 0.9.6d.
- Added a patch by Ben Laurie for "openssl dgst" to behave on read errors.
- Dropped the incorrect (or no longer correct?) RH-derived configuration
file path patch to ca(1).
- Properly restrict the instruction set in assembly code when building for
i386 (don't use bswapl).

* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Dec 26 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.9.6c.

* Wed Jul 11 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.9.6b.

* Fri Jul 06 2001 Solar Designer <solar@owl.openwall.com>
- Applied patches provided by the OpenSSL team to correct a PRNG
weakness which under unusual circumstances could allow an attacker to
determine internal state of the PRNG and thus to predict future PRNG
output.  This problem has been discovered and reported to the OpenSSL
team by Markku-Juhani O. Saarinen.  No applications are known to be
affected at this time.

* Sun Apr 22 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.9.6a which contains a number of security fixes (but breaks
binary compatibility).
- Updated shared libraries building to match the new Makefile conventions.
- Use glibc's __libc_enable_secure for the new OPENSSL_issetugid().
- Various other changes to the spec file.

* Sat Apr 14 2001 Solar Designer <solar@owl.openwall.com>
- Support Alpha targets.
- Use the ix86 macro.

* Mon Nov 13 2000 Solar Designer <solar@owl.openwall.com>
- Support SPARC targets (32-bit only at this time).

* Sun Oct 29 2000 Solar Designer <solar@owl.openwall.com>
- Don't require bc (disable one of the tests if bc isn't available).

* Mon Oct 02 2000 Solar Designer <solar@owl.openwall.com>
- Rename the passwd and rand man pages differently (this is still a hack).

* Sun Jul 09 2000 Solar Designer <solar@owl.openwall.com>
- Imported Damien Miller's spec file.
- Added two patches from Trustix and, more importantly, a patch to avoid
exporting crypt() as a symbol (which used to override the weak alias for
crypt(3), while applications generally want the libcrypt version).  crypt
defined here is now a #define, so is only available when the appropriate
OpenSSL header is included.

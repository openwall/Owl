# $Id: Owl/packages/openssl/openssl.spec,v 1.29 2002/12/12 17:33:44 solar Exp $

Summary: Secure Sockets Layer and cryptography libraries and tools.
Name: openssl
Version: 0.9.6h
Release: owl1
License: distributable
Group: System Environment/Libraries
URL: http://www.openssl.org
Source: ftp://ftp.openssl.org/source/%{name}-%{version}.tar.gz
Patch0: openssl-0.9.6e-owl-crypt.diff
Patch1: openssl-0.9.6a-owl-glibc-enable_secure.diff
Patch10: openssl-0.9.6e-up-20020429-read-errors.diff
PreReq: /sbin/ldconfig
Provides: SSL
BuildRequires: perl
BuildRoot: /override/%{name}-%{version}

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
Requires: openssl = %{version}-%{release}

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
pushd crypto/objects/
touch -r objects.pl *.h
popd
%patch0 -p1
%patch1 -p1
%patch10 -p0

%define openssldir /var/ssl
%define opensslflags shared -DSSL_ALLOW_ADH --prefix=/usr

%build
perl -pi -e "s/-O.(?: -fomit-frame-pointer)?(?: -m.86)?/${RPM_OPT_FLAGS}/" \
	Configure

%ifarch %ix86
%ifarch i386
./Configure %{opensslflags} --openssldir=%{openssldir} 386 linux-elf
%else
./Configure %{opensslflags} --openssldir=%{openssldir} linux-elf
%endif
%endif
%ifarch ppc
./Configure %{opensslflags} --openssldir=%{openssldir} linux-ppc
%endif
%ifarch alpha alphaev5
./Configure %{opensslflags} --openssldir=%{openssldir} linux-alpha-gcc
%endif
%ifarch alphaev56 alphapca56 alphaev6 alphaev67
./Configure %{opensslflags} --openssldir=%{openssldir} linux-alpha+bwx-gcc
%endif
%ifarch sparc
./Configure %{opensslflags} --openssldir=%{openssldir} linux-sparcv8
%endif
%ifarch sparcv9
./Configure %{opensslflags} --openssldir=%{openssldir} linux-sparcv9
%endif

# Check these against the DIRS= line and "all" target in top-level Makefile
# when updating to a new version of OpenSSL; with 0.9.6h the Makefile says:
# DIRS= crypto ssl rsaref $(SHLIB_MARK) apps test tools
# all: clean-shared Makefile.ssl sub_all
make Makefile.ssl
make sub_all DIRS="crypto ssl"
LD_LIBRARY_PATH=`pwd` make sub_all DIRS="apps test tools"

if [ ! -x /usr/bin/bc ]; then
	perl -pi -e 's/^test_bn:/test_bn_unused:/' test/Makefile.ssl
	echo 'test_bn:' >> test/Makefile.ssl
fi
LD_LIBRARY_PATH=`pwd` make tests

%install
rm -rf $RPM_BUILD_ROOT
make install MANDIR=%{_mandir} INSTALL_PREFIX="$RPM_BUILD_ROOT"

# Fail if the openssl binary is statically linked against OpenSSL at this
# stage (which could happen if "make install" caused anything to rebuild).
LD_LIBRARY_PATH=`pwd` ldd $RPM_BUILD_ROOT/usr/bin/openssl | tee openssl.libs
grep -qw libssl openssl.libs
grep -qw libcrypto openssl.libs

# Rename man pages
mv $RPM_BUILD_ROOT%{_mandir}/man1/{,ssl}passwd.1
mv $RPM_BUILD_ROOT%{_mandir}/man3/{,ssl}err.3
mv $RPM_BUILD_ROOT%{_mandir}/man3/{,ssl}rand.3

# Make backwards-compatibility symlink to ssleay
ln -s openssl $RPM_BUILD_ROOT/usr/bin/ssleay

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(0644,root,root,0755)
%doc CHANGES CHANGES.SSLeay LICENSE NEWS README
%doc doc

%attr(0755,root,root) /usr/bin/*
%attr(0755,root,root) /usr/lib/*.so.*
%attr(0755,root,root) %{openssldir}/misc/*
%attr(0644,root,root) %{_mandir}/man[157]/*

%config %attr(0644,root,root) %{openssldir}/openssl.cnf
%dir %attr(0755,root,root) %{openssldir}/certs
%dir %attr(0755,root,root) %{openssldir}/lib
%dir %attr(0755,root,root) %{openssldir}/misc
%dir %attr(0700,root,root) %{openssldir}/private

%files devel
%defattr(0644,root,root,0755)
%attr(0644,root,root) /usr/lib/*.a
%attr(0755,root,root) /usr/lib/*.so
%attr(0644,root,root) /usr/include/openssl/*
%attr(0644,root,root) %{_mandir}/man3/*

%changelog
* Thu Dec 12 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 0.9.6h.

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

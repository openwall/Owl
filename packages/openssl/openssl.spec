# $Id: Owl/packages/openssl/openssl.spec,v 1.15 2002/02/06 21:39:00 mci Exp $

%define openssldir /var/ssl

Summary: Secure Sockets Layer and cryptography libraries and tools.
Name: openssl
Version: 0.9.6c
Release: owl1
License: distributable
Group: System Environment/Libraries
URL: http://www.openssl.org
Source: ftp://ftp.openssl.org/source/%{name}-%{version}.tar.gz
Patch0: openssl-0.9.5a-rh-config-path.diff
Patch1: openssl-0.9.5a-owl-crypt.diff
Patch2: openssl-0.9.6a-owl-glibc-enable_secure.diff
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
Summary: Secure Sockets Layer and cryptography static libraries and headers
Group: Development/Libraries
Requires: openssl

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
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%define CONFIG_FLAGS shared -DSSL_ALLOW_ADH --prefix=/usr

perl -pi -e "s/-O.(?: -fomit-frame-pointer)?(?: -m.86)?/${RPM_OPT_FLAGS}/;" \
	Configure

%ifarch %ix86
./Configure %{CONFIG_FLAGS} --openssldir=%{openssldir} linux-elf
%endif
%ifarch ppc
./Configure %{CONFIG_FLAGS} --openssldir=%{openssldir} linux-ppc
%endif
%ifarch alpha alphaev5
./Configure %{CONFIG_FLAGS} --openssldir=%{openssldir} linux-alpha-gcc
%endif
%ifarch alphaev56 alphapca56 alphaev6 alphaev67
./Configure %{CONFIG_FLAGS} --openssldir=%{openssldir} linux-alpha+bwx-gcc
%endif
%ifarch sparc
./Configure %{CONFIG_FLAGS} --openssldir=%{openssldir} linux-sparcv8
%endif
%ifarch sparcv9
./Configure %{CONFIG_FLAGS} --openssldir=%{openssldir} linux-sparcv9
%endif

# Check these against the DIRS= line and "all" target in top-level Makefile
# when updating to a new version of OpenSSL; with 0.9.6c the Makefile says:
# DIRS= crypto ssl rsaref $(SHLIB_MARK) apps test tools
# all: clean-shared Makefile.ssl sub_all
make Makefile.ssl
make sub_all DIRS="crypto ssl rsaref"
make build-shared
LD_LIBRARY_PATH=`pwd` make sub_all DIRS="apps test tools"

if [ ! -x /usr/bin/bc ]; then
	perl -pi -e 's/^test_bn:/test_bn_unused:/' test/Makefile.ssl
	echo 'test_bn:' >> test/Makefile.ssl
fi
LD_LIBRARY_PATH=`pwd` make tests

%install
rm -rf $RPM_BUILD_ROOT
make install MANDIR=/usr/man INSTALL_PREFIX="$RPM_BUILD_ROOT"

# Fail if the openssl binary is statically linked against OpenSSL at this
# stage (which could happen if "make install" caused anything to rebuild).
LD_LIBRARY_PATH=`pwd` ldd $RPM_BUILD_ROOT/usr/bin/openssl | tee openssl.libs
grep -qw libssl openssl.libs
grep -qw libcrypto openssl.libs

# Rename manpages
mv $RPM_BUILD_ROOT%{_mandir}/man1/passwd.1 \
	$RPM_BUILD_ROOT%{_mandir}/man1/sslpasswd.1
mv $RPM_BUILD_ROOT%{_mandir}/man3/rand.3 \
	$RPM_BUILD_ROOT%{_mandir}/man3/sslrand.3

# Install RSAref stuff
install -m 644 rsaref/rsaref.h $RPM_BUILD_ROOT/usr/include/openssl
install -m 644 libRSAglue.a $RPM_BUILD_ROOT/usr/lib

# Make backwards-compatibility symlink to ssleay
ln -s openssl $RPM_BUILD_ROOT/usr/bin/ssleay

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc CHANGES CHANGES.SSLeay LICENSE NEWS README
%doc doc

%attr(0755,root,root) /usr/bin/*
%attr(0755,root,root) /usr/lib/*.so*
%attr(0755,root,root) %{openssldir}/misc/*
%attr(0644,root,root) /usr/man/man[157]/*

%config %attr(0644,root,root) %{openssldir}/openssl.cnf
%dir %attr(0755,root,root) %{openssldir}/certs
%dir %attr(0755,root,root) %{openssldir}/lib
%dir %attr(0755,root,root) %{openssldir}/misc
%dir %attr(0700,root,root) %{openssldir}/private

%files devel
%defattr(0644,root,root,0755)
%attr(0644,root,root) /usr/lib/*.a
%attr(0644,root,root) /usr/include/openssl/*
%attr(0644,root,root) /usr/man/man3/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
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
- Rename the passwd and rand manpages differently (this is still a hack).

* Sun Jul 09 2000 Solar Designer <solar@owl.openwall.com>
- Added two patches from Trustix and, more importantly, a patch to avoid
exporting crypt() as a symbol (which used to override the weak alias for
crypt(3), while applications generally want the libcrypt version).  crypt
defined here is now a #define, so is only available when the appropriate
OpenSSL header is included.

* Sun Feb 27 2000 Damien Miller <djm@mindrot.org>
- Merged patches to spec
- Updated to 0.9.5beta2 (now with manpages)
* Sat Feb  5 2000 Michal Jaegermann <michal@harddata.com>
- added 'linux-alpha' to configuration
- fixed nasty absolute links
* Tue Jan 25 2000 Bennett Todd <bet@rahul.net>
- Added -DSSL_ALLOW_ADH, bumped Release to 4
* Thu Oct 14 1999 Damien Miller <djm@mindrot.org>
- Set default permissions
- Removed documentation from devel sub-package
* Thu Sep 30 1999 Damien Miller <djm@mindrot.org>
- Added "make test" stage
- GPG signed
* Tue Sep 10 1999 Damien Miller <damien@ibs.com.au>
- Updated to version 0.9.4
* Tue May 25 1999 Damien Miller <damien@ibs.com.au>
- Updated to version 0.9.3
- Added attributes for all files
- Paramatised openssl directory
* Sat Mar 20 1999 Carlo M. Arenas Belon <carenas@jmconsultores.com.pe>
- Added "official" bnrec patch and taking other out
- making a link from ssleay to openssl binary
- putting all changelog together on SPEC file
* Fri Mar  5 1999 Henri Gomez <gomez@slib.fr>
- Added bnrec patch
* Tue Dec 29 1998 Jonathan Ruano <kobalt@james.encomix.es>
- minimum spec and patches changes for openssl
- modified for openssl sources
* Sat Aug  8 1998 Khimenko Victor <khim@sch57.msk.ru>
- shared library creating process honours $RPM_OPT_FLAGS
- shared libarry supports threads (as well as static library)
* Wed Jul 22 1998 Khimenko Victor <khim@sch57.msk.ru>
- building of shared library completely reworked
* Tue Jul 21 1998 Khimenko Victor <khim@sch57.msk.ru>
- RPM is BuildRoot'ed
* Tue Feb 10 1998 Khimenko Victor <khim@sch57.msk.ru>
- all stuff is moved out of /usr/local

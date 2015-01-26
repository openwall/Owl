# $Owl: Owl/packages/libnss/libnss.spec,v 1.2 2015/01/26 03:06:36 galaxy Exp $

%define def_with() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _with_%1 --with-%1%{?2:=%2}}}}
%define def_without() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _without_%1 --without-%1}}}

# Beware that the test suite runs for quite a long time (e.g. it takes 30 mins
# on Intel Xeon E3-1230 V2), so by default we skip the tests.
%def_without    test

Summary: Network Security Services (NSS) Library
Name: libnss
Version: 3.17.3
Release: owl1
License: Mozilla
URL: https://developer.mozilla.org/en/docs/NSS
Group: System/Libraries
BuildRoot: /override/%name-%version
BuildRequires: libnspr-devel >= 4.10.7
BuildRequires: zlib-devel
BuildRequires: libsqlite-devel
Provides: nss

Source: ftp://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/NSS_3_17_3_RTM/src/nss-%version.tar.gz
Source1: %name.config.in
Source2: %name.empty-nssdb.tar.xz
Source3: %name.setup
Source4: %name.pkcs11.txt

%description
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

%package sysinit
Summary: System NSS Initilization
Group: System/Libraries
Requires: %name = %version-%release
Provides: nss-sysinit

%description sysinit
Default Operating System module that manages applications loading
NSS globally on the system. This module loads the system defined
PKCS #11 modules for NSS and chains with other NSS modules to load
any system or user configured modules.

%package devel
Summary: Development files for the %name package
Group: Development/Libraries/C and C++
Requires: %name = %version-%release

%description devel
This package provides header files to include, and libraries to link with, for
the Network Security Services (NSS).

%package devel-static
Summary: Development files for the %name package
Group: Development/Libraries/C and C++
Requires: %name = %version-%release

%description devel-static
This package provides static libraries to link with for the Network
Security Services (NSS).

%package -n nss-tools
Summary: Network Security Services (NSS) tools
Group: Development/Other
Requires: %name = %version-%release

%description -n nss-tools
Network Security Services (NSS) tools.

%prep
%setup -q -n nss-%version/nss

rm -r lib/{sqlite,zlib}

%build
export BUILD_OPT=1 
export NS_USE_GCC=1
export NSS_ENABLE_ECC=1
export NSS_USE_SYSTEM_SQLITE=1
export USE_SYSTEM_ZLIB=1
#export PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
#export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1
export NSPR_INCLUDE_DIR=$(nspr-config --includedir)
export NSPR_LIB_DIR=$(nspr-config --libdir)

# Generate symbolic info for debuggers
export 'XCFLAGS=%optflags'

%ifarch x86_64 sparc64
export USE_64=1
%endif

# additional CA certificates
#cat '%_sourcedir/%name.addon-certs >> lib/ckfw/builtins/certdata.txt

# Seems that the parallel build breaks the process
%__make -j1

%install
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'
mkdir -m755 -p '%buildroot%_bindir' '%buildroot%_libdir' '%buildroot%_includedir'

# define some variables
DIST_OBJDIR=$(ls -d ../dist/*.OBJ)
NSPR_VERSION="$(nspr-config --version)"
nss_h="lib/nss/nss.h"
NSS_VMAJOR="$(sed -ne 's,^#define[[:space:]]\+NSS_VMAJOR[[:space:]]\+,,p' "$nss_h")"
NSS_VMINOR="$(sed -ne 's,^#define[[:space:]]\+NSS_VMINOR[[:space:]]\+,,p' "$nss_h")"
NSS_VPATCH="$(sed -ne 's,^#define[[:space:]]\+NSS_VPATCH[[:space:]]\+,,p' "$nss_h")"

cp -aL "$DIST_OBJDIR"/bin/* '%buildroot%_bindir/'
cp -aL "$DIST_OBJDIR"/lib/*.{so,chk} '%buildroot%_libdir/'
cp -aL "$DIST_OBJDIR"/lib/libcrmf.a '%buildroot%_libdir/'
cp -aL ../dist/public/nss '%buildroot%_includedir/'

sed \
	-e "s,@libdir@,%_libdir,g" \
	-e "s,@prefix@,%_prefix,g" \
	-e "s,@exec_prefix@,%_prefix,g" \
	-e "s,@includedir@,%_includedir/nss,g" \
	-e "s,@MOD_MAJOR_VERSION@,$NSS_VMAJOR,g" \
	-e "s,@MOD_MINOR_VERSION@,$NSS_VMINOR,g" \
	-e "s,@MOD_PATCH_VERSION@,$NSS_VPATCH,g" \
	'%_sourcedir/%name.config.in' > '%buildroot%_bindir/nss-config'
chmod 0755 '%buildroot%_bindir/nss-config'

# https://wiki.mozilla.org/NSS_Shared_DB
# https://wiki.mozilla.org/NSS_Shared_DB_Samples
# https://wiki.mozilla.org/NSS_Shared_DB_Howto
# https://wiki.mozilla.org/NSS_Shared_DB_And_LINUX
mkdir -p -- '%buildroot%_sysconfdir/pki/nssdb'
tar xJSf '%_sourcedir/%name.empty-nssdb.tar.xz' \
	-C '%buildroot%_sysconfdir/pki/nssdb'
find '%buildroot%_sysconfdir/pki/nssdb' -name 'blank-*.db' \
		-printf '%%h %%f\n' |
	while read p n; do
		mv -- "$p/$n" "$p/${n#blank-}"
	done

sed -e 's,@@SYSCONFDIR@@,%_sysconfdir,g' '%_sourcedir/%name.setup' \
	> '%buildroot%_bindir/setup-nsssysinit.sh'
install -p -m644 '%_sourcedir/%name.pkcs11.txt' '%buildroot%_sysconfdir/pki/nssdb/pkcs11.txt'

# relocate libnss3.so and libnssutil3.so to /%_lib since their static
# version cannot be built, yet newer RPM requires these two libraries
# and we really want to have a rescue package manager on the root
# filesystem.
mkdir -m755 -p '%buildroot/%_lib'
mv -v -- '%buildroot%_libdir'/libnss{,util}3.so '%buildroot/%_lib/'

%check
# We need a defined entry for localhost.localdomain to run tests
# There is an assumption that 'localhost' can be resolved.
echo 'localhost.localdomain localhost' > .host.aliases
export HOSTALIASES=$(pwd)/.host.aliases

# Run test suite.
export BUILD_OPT=1 
MYRAND=$(($RANDOM % 1000 + 9000))
RANDSERV=selfserv_$MYRAND; echo $RANDSERV ||:
DISTBINDIR=`ls -d ../dist/*.OBJ/bin`; echo $DISTBINDIR ||:
ln -s selfserv "$DISTBINDIR/$RANDSERV"
# man perlrun, man perlrequick
# replace word-occurrences of selfserv with selfserv_$MYRAND
find tests -type f ! -name '*.db' -a ! -name '*.crl' \
	-a ! -name '*.crt' -a ! -name '*CVS*' -print0 | \
  xargs -0 grep -lwZ selfserv |\
  xargs -0 -L 1 perl -pi -e "s/\bselfserv\b/$RANDSERV/g" ||:

killall "$RANDSERV" || :

rm -rf ./tests_results
pushd tests/
# all.sh is the test suite script

#  If you don't need to run all the tests define the following variables
#  (specified before ':') to a set of tests separated by whitespace:
#
#  nss_cycles: standard pkix upgradedb sharedb
#  nss_tests: cipher libpkix cert dbtests tools fips sdr crmf smime ssl ocsp merge pkits chains
#  nss_ssl_tests: crl bypass_normal normal_bypass normal_fips fips_normal iopr
#  nss_ssl_run: cov auth stress
#
# For example, to speed builds up you may want to use somethng like the following:
#
# %%define nss_ssl_tests "normal_fips"
# %%define nss_ssl_run "cov auth"

HOST=localhost DOMSUF=localdomain \
PORT="$MYRAND" \
NSS_CYCLES=%{?nss_cycles} NSS_TESTS=%{?nss_tests} \
NSS_SSL_TESTS=%{?nss_ssl_tests} NSS_SSL_RUN=%{?nss_ssl_run} \
./all.sh

popd
killall "$RANDSERV" || :

TEST_FAILURES=$(grep -c FAILED ../tests_results/security/localhost.1/output.log) || :
if [ ${TEST_FAILURES:-1} -ne 0 ]; then
  echo "error: test suite returned failure(s)"
  exit 1
fi
echo "test suite completed"

%clean
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(0644,root,root,0755)
/%_lib/libnss3.so
/%_lib/libnssutil3.so
%_libdir/libfreebl3.so
%_libdir/libfreebl3.chk
%_libdir/libnssckbi.so
%_libdir/libnssdbm3.so
%_libdir/libnssdbm3.chk
%_libdir/libnsssysinit.so
%_libdir/libsmime3.so
%_libdir/libsoftokn3.so
%_libdir/libsoftokn3.chk
%_libdir/libssl3.so
%dir %_sysconfdir/pki/nssdb
%config(noreplace) %verify(not md5 size mtime) %_sysconfdir/pki/nssdb/cert8.db
%config(noreplace) %verify(not md5 size mtime) %_sysconfdir/pki/nssdb/key3.db
%config(noreplace) %verify(not md5 size mtime) %_sysconfdir/pki/nssdb/secmod.db
#%doc %_mandir/man5/cert8.db.5.gz
#%doc %_mandir/man5/key3.db.5.gz
#%doc %_mandir/man5/secmod.db.5.gz

%files sysinit
%defattr(0644,root,root,0755)
%_libdir/libnsssysinit.so
%config(noreplace) %verify(not md5 size mtime) %_sysconfdir/pki/nssdb/cert9.db
%config(noreplace) %verify(not md5 size mtime) %_sysconfdir/pki/nssdb/key4.db
%config(noreplace) %verify(not md5 size mtime) %_sysconfdir/pki/nssdb/pkcs11.txt
%attr(0755,root,root) %_bindir/setup-nsssysinit.sh

%files devel
%defattr(0644,root,root,0755)
%attr(0755,root,root) %_bindir/nss-config
%_includedir/nss

%files devel-static
%defattr(0644,root,root,0755)
%_libdir/libcrmf.a

%files -n nss-tools
%defattr(0644,root,root,0755)
%attr(0755,root,root) %_bindir/*
%exclude %_bindir/setup-nsssysinit.sh
# Remove tests and samples
%exclude %_bindir/nss-config
%exclude %_bindir/bltest
%exclude %_bindir/dbtest
%exclude %_bindir/mangle
%exclude %_bindir/ocspclnt
%exclude %_bindir/oidcalc
%exclude %_bindir/sdrtest
%exclude %_bindir/shlibsign
%exclude %_bindir/tstclnt
%exclude %_bindir/vfyserv

%changelog
* Mon Jan 26 2015 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.17.3-owl1
- Updated to 3.17.3.
- The test suite is disabled by default since it is a long running one.

* Fri Oct 10 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.17.1-owl1
- Updated to 3.17.1.

* Mon Jun 16 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.16.1-owl1
- Initial release for Owl.
- Introduced the devel-static sub-package.
- Moved libnss{,util}3.so from %%_libdir to /%%_lib since these two
libraries are required for the newer RPM to run.

* Mon Jun 09 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.16.1-owlx0
- Updated to 3.16.1.
- Added libnsprdevel, zlib-devel, and libsqlite-devel to the build
requirements.

* Wed Feb 19 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.15.5-owlx0
- created an initial package for Owl-extra.

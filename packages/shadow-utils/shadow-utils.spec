# $Id: Owl/packages/shadow-utils/shadow-utils.spec,v 1.3 2001/02/09 22:24:22 solar Exp $

%define BUILD_CHSH_CHFN	'yes'
%define BUILD_VIPW_VIGR	'yes'

Summary: Utilities for managing shadow password files and user/group accounts.
Name: shadow-utils
Version: 19990827
Release: 12owl
Serial: 1
Source0: ftp://ftp.ists.pwr.wroc.pl/pub/linux/shadow/shadow-%{version}.tar.gz
Source1: login.defs
Source2: useradd.default
Source3: chsh-chfn.pam
Source4: chsh-chfn.control
Source5: chage.control
Source6: gpasswd.control
Patch0: shadow-19990827-rh-redhat.diff
Patch1: shadow-19990827-owl-man.diff
Patch2: shadow-19990827-owl-restrict-locale.diff
Patch3: shadow-19990827-owl-chage-ro-no-lock.diff
Copyright: BSD
Group: System Environment/Base
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: owl-control < 2.0

%description
The shadow-utils package includes the necessary programs for
converting UNIX password files to the shadow password format, plus
programs for managing user and group accounts.

%prep
%setup -q -n shadow-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
unset LINGUAS || :
libtoolize --copy --force
aclocal
automake
autoheader
autoconf
rm -rf build-$RPM_ARCH
mkdir build-$RPM_ARCH
cd build-$RPM_ARCH
CFLAGS="$RPM_OPT_FLAGS" ../configure --prefix=/usr \
	--disable-desrpc --disable-shared \
	--with-libcrypt --with-libpam --without-libcrack
make

%install
rm -rf $RPM_BUILD_ROOT
cd build-$RPM_ARCH
make install prefix=$RPM_BUILD_ROOT/usr exec_prefix=$RPM_BUILD_ROOT
chmod -R -s $RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT
ln -s useradd usr/sbin/adduser
ln -s vipw usr/sbin/vigr
ln -s useradd.8.gz usr/man/man8/adduser.8.gz
ln -s vipw.8.gz usr/man/man8/vigr.8.gz
ln -s pwconv.8.gz usr/man/man8/pwunconv.8.gz
ln -s pwconv.8.gz usr/man/man8/grpconv.8.gz
ln -s pwconv.8.gz usr/man/man8/grpunconv.8.gz

mkdir -p -m 700 etc/default
install -m 600 ${RPM_SOURCE_DIR}/login.defs etc/login.defs
install -m 600 ${RPM_SOURCE_DIR}/useradd.default etc/default/useradd

%if "%{BUILD_CHSH_CHFN}"=="'yes'"
mkdir -p etc/pam.d
install -m 600 ${RPM_SOURCE_DIR}/chsh-chfn.pam etc/pam.d/chsh
install -m 600 ${RPM_SOURCE_DIR}/chsh-chfn.pam etc/pam.d/chfn
%endif

mkdir -p etc/control.d/facilities
cd etc/control.d/facilities

install -m 700 ${RPM_SOURCE_DIR}/chage.control chage
install -m 700 ${RPM_SOURCE_DIR}/gpasswd.control gpasswd

%if "%{BUILD_CHSH_CHFN}"=="'yes'"
install -m 700 ${RPM_SOURCE_DIR}/chsh-chfn.control chsh
sed 's,/usr/bin/chsh,/usr/bin/chfn,' < chsh > chfn
chmod 700 chfn
%endif

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf build-$RPM_ARCH

%post
grep ^shadow: /etc/group &> /dev/null || groupadd -g 42 shadow
chgrp shadow /etc/shadow && chmod 440 /etc/shadow

%files
%defattr(-,root,root)
%doc doc/ANNOUNCE doc/CHANGES doc/HOWTO
%doc doc/LICENSE doc/README doc/README.linux
%dir /etc/default
%attr(0600,root,root) %config /etc/login.defs
%attr(0600,root,root) %config /etc/default/useradd
/usr/sbin/adduser
/usr/sbin/user*
/usr/sbin/group*
/usr/sbin/grpck
/usr/sbin/pwck
/usr/sbin/*conv
/usr/sbin/chpasswd
/usr/sbin/newusers
%attr(0700,root,root) /usr/bin/chage
%attr(0700,root,root) /usr/bin/gpasswd
/usr/bin/lastlog
/usr/man/man1/chage.1*
/usr/man/man1/gpasswd.1*
/usr/man/man3/shadow.3*
/usr/man/man5/shadow.5*
/usr/man/man8/adduser.8*
/usr/man/man8/group*.8*
/usr/man/man8/user*.8*
/usr/man/man8/pwck.8*
/usr/man/man8/grpck.8*
/usr/man/man8/chpasswd.8*
/usr/man/man8/newusers.8*
/usr/man/man8/*conv.8*
/usr/man/man8/lastlog.8*
/usr/share/locale/*/*/shadow.mo

/etc/control.d/facilities/chage
/etc/control.d/facilities/gpasswd

%if "%{BUILD_VIPW_VIGR}"=="'yes'"
%attr(0700,root,root) /usr/sbin/vi*
/usr/man/man8/vi*.8*
%endif

%if "%{BUILD_CHSH_CHFN}"=="'yes'"
%attr(0700,root,root) /usr/bin/chsh
%attr(0700,root,root) /usr/bin/chfn
/usr/man/man1/chsh.1*
/usr/man/man1/chfn.1*
/etc/pam.d/chsh
/etc/pam.d/chfn
/etc/control.d/facilities/chsh
/etc/control.d/facilities/chfn
%endif

%changelog
* Sat Feb 10 2001 Solar Designer <solar@owl.openwall.com>
- shadow group.
- Don't lock password files with "chage -l" (this is read-only access).

* Sat Aug 26 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file from RH, cleaned it up, and changed heavily.
- Imported many of the Red Hat modifications to useradd, including some
questionable ones.
- Restricted locale support in commands that may be installed SUID/SGID.
- chsh, chfn, vipw, and vigr are now built from this package rather than
from util-linux.  The util-linux versions used incompatible locking, and
vi* lacked the support for shadow files.
- owl-control support for chsh, chfn, chage, and gpasswd.

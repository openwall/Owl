# $Id: Owl/packages/pam_userpass/pam_userpass/pam_userpass.spec,v 1.15 2003/11/02 14:36:45 solar Exp $

Summary: Pluggable authentication module for USER/PASS-style protocols.
Name: pam_userpass
Version: 0.9.1
Release: owl1
License: relaxed BSD and (L)GPL-compatible
Group: System Environment/Base
URL: http://www.openwall.com/pam/
Source: ftp://ftp.openwall.com/pub/projects/pam/modules/%name/%name-%version.tar.gz
BuildRoot: /override/%name-%version

%description
pam_userpass is a PAM authentication module for use specifically by
services implementing non-interactive protocols and wishing to verify
a username/password pair.  This module doesn't do any actual
authentication, -- other modules, such as pam_tcb, should be stacked
after it to provide the authentication.

%package devel
Summary: Libraries and header files for developing pam_userpass-aware applications.
Group: Development/Libraries
Requires: %name = %version-%release, pam-devel

%description devel
This package contains development libraries and header files required
for building pam_userpass-aware applications.

%prep
%setup -q

%build
CFLAGS="-Wall -fPIC $RPM_OPT_FLAGS" make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc LICENSE README
/lib/security/pam_userpass.so
%_libdir/*.so.*

%files devel
%defattr(-,root,root)
%_libdir/*.so
%_libdir/*.a
%_includedir/security/*

%changelog
* Sun Nov 02 2003 Solar Designer <solar@owl.openwall.com> 0.9.1-owl1
- Use "install -c" (makes a difference on some non-Linux systems).
- Moved the "-c" out of CFLAGS.

* Wed Apr 02 2003 Dmitry V. Levin <ldv@owl.openwall.com> 0.9-owl1
- Added libpam_userpass library, in shared and static forms.
- Packaged development libraries and header files in separate
subpackage, pam_userpass-devel.

* Tue Apr 02 2002 Solar Designer <solar@owl.openwall.com>
- 0.5.1: use const within the declaration of pam_userpass_t, use '='
instead of '.set' to declare the alias.

* Thu Feb 07 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Nov 09 2001 Solar Designer <solar@owl.openwall.com>
- 0.5: provide a pam_sm_chauthtok as well, currently only supporting
password changes which don't require the old password to be passed.

* Thu Jun 14 2001 Solar Designer <solar@owl.openwall.com>
- 0.4: deal with null passwords correctly (thanks to Rafal Wojtczuk
<nergal@owl.openwall.com>), support Linux-PAM 0.74+'s new BP macros.

* Tue Dec 19 2000 Solar Designer <solar@owl.openwall.com>
- Added "-Wall -fPIC" to the CFLAGS.

* Fri Aug 18 2000 Solar Designer <solar@owl.openwall.com>
- 0.3, added README.

* Sun Jul 09 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

# $Id: Owl/packages/pam_userpass/pam_userpass/pam_userpass.spec,v 1.10 2002/04/01 20:23:07 solar Exp $

Summary: Pluggable authentication module for USER/PASS-style protocols.
Name: pam_userpass
Version: 0.5.1
Release: owl1
License: relaxed BSD and (L)GPL-compatible
Group: System Environment/Base
Source: pam_userpass-%{version}.tar.gz
BuildRoot: /override/%{name}-%{version}

%description
pam_userpass is a PAM authentication module for use specifically by
services implementing non-interactive protocols and wishing to verify
a username/password pair.  This module doesn't do any actual
authentication, -- other modules, such as pam_tcb, should be stacked
after it to provide the authentication.

%prep
%setup -q

%build
make CFLAGS="-c -Wall -fPIC -Iinclude $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make install FAKEROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE README
/lib/security/pam_userpass.so

%changelog
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

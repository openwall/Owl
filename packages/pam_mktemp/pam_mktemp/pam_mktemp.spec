# $Id: Owl/packages/pam_mktemp/pam_mktemp/pam_mktemp.spec,v 1.2 2001/11/09 03:12:18 solar Exp $

Summary: Pluggable private /tmp space support for interactive (shell) sessions.
Name: pam_mktemp
Version: 0.1
Release: 1owl
License: relaxed BSD and (L)GPL-compatible
Group: System Environment/Base
Source: pam_mktemp-%{version}.tar.gz
BuildRoot: /override/%{name}-%{version}

%description
pam_mktemp is a PAM module which may be used with a PAM-aware login service
to provide per-user private directories under /tmp as a part of PAM session
or account management.

%prep
%setup -q

%build
make CFLAGS="-c -Wall -fPIC -DLINUX_PAM $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make install FAKEROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
mkdir -p -m 711 /tmp/.private

%files
%defattr(-,root,root)
%doc LICENSE README
/lib/security/pam_mktemp.so

%changelog
* Fri Nov 09 2001 Solar Designer <solar@owl.openwall.com>
- Support stacking for account management as well as for session setup.
- No longer set LYNX_TEMP_SPACE.

* Tue Dec 19 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

# $Id: Owl/packages/pam_mktemp/pam_mktemp/pam_mktemp.spec,v 1.1 2000/12/19 11:00:37 solar Exp $

Summary: Pluggable private /tmp space support for interactive (shell) sessions
Name: pam_mktemp
Version: 0.0
Release: 1owl
Copyright: relaxed BSD and (L)GPL-compatible
Group: System Environment/Base
Source: pam_mktemp-%{version}.tar.gz
Buildroot: /var/rpm-buildroot/%{name}-%{version}

%description
pam_mktemp is a PAM module which may be used with a PAM-aware login service
to provide per-user private directories under /tmp as a part of PAM session
management.

%prep
%setup -q

%build
make CFLAGS="-c -Wall -fPIC $RPM_OPT_FLAGS"

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
* Tue Dec 19 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

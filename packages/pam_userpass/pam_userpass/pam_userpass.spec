Summary: Pluggable authentication module for USER/PASS-style protocols
Name: pam_userpass
Version: 0.2
Release: 1owl
Copyright: relaxed BSD and (L)GPL-compatible
Group: System Environment/Base
Source: pam_userpass-0.2.tar.gz
Buildroot: /var/rpm-buildroot/%{name}-%{version}
BuildPreReq: pam >= 0.72-8owl

%description
pam_userpass is a PAM authentication module for use specifically by
services implementing non-interactive protocols and wishing to verify
a username/password pair.  The module doesn't do any actual
authentication, -- other modules, such as pam_pwdb, should be stacked
to provide the authentication.

%prep
%setup -q

%build
make CFLAGS="-c -Iinclude $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make install FAKEROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE
/lib/security/pam_userpass.so

%changelog
* Sun Jul  9 2000 Solar Designer <solar@false.com>
- initial version

# $Id: Owl/packages/owl-etc/owl-etc.spec,v 1.3 2000/07/27 00:12:00 solar Exp $

Summary: Initial set of configuration files
Name: owl-etc
Version: 0.0
Release: 1owl
Copyright: public domain
Group: System Environment/Base
Source0: passwd
Source1: group
Source2: securetty
Source3: shells
Source4: host.conf
Source5: protocols
Source6: services
Source7: profile
Source8: bashrc
Source9: inputrc
Source10: csh.login
Source11: csh.cshrc
Buildroot: /var/rpm-buildroot/%{name}-%{version}
BuildArchitectures: noarch

%description
Initial set of configuration files to be placed into /etc.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
touch $RPM_BUILD_ROOT/etc/motd
# Hack, don't want to list all sources
cp -a $RPM_SOURCE_DIR/* $RPM_BUILD_ROOT/etc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root)
%verify(not md5 size mtime) %config(noreplace) /etc/passwd
%verify(not md5 size mtime) %config(noreplace) /etc/group
%attr(600,root,root) /etc/securetty
%config /etc/shells
%config(noreplace) /etc/host.conf
%config /etc/protocols
%config /etc/services
%config(noreplace) /etc/profile
%config(noreplace) /etc/bashrc
%config /etc/inputrc
%config(noreplace) /etc/csh.login
%config(noreplace) /etc/csh.cshrc
%config /etc/motd
%dir %attr(755,root,root) /etc/profile.d

%changelog
* Thu Jul 27 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

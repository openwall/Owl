# $Id: Owl/packages/owl-etc/owl-etc.spec,v 1.18 2000/12/20 18:49:36 solar Exp $

Summary: Initial set of configuration files
Name: owl-etc
Version: 0.6
Release: 1owl
Copyright: public domain
Group: System Environment/Base
Source0: passwd
Source1: shadow
Source2: group
Source3: fstab
Source10: securetty
Source11: shells
Source12: host.conf
Source20: protocols
Source21: services
Source30: hosts.allow
Source31: hosts.deny
Source40: profile
Source41: bashrc
Source42: inputrc
Source50: csh.login
Source51: csh.cshrc
Buildroot: /var/rpm-buildroot/%{name}-%{version}
BuildArchitectures: noarch
BuildRequires: fileutils >= 4.0.27
Obsoletes: setup

%description
Initial set of configuration files to be placed into /etc.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{etc/profile.d,var/log}
cd $RPM_BUILD_ROOT
touch etc/motd var/log/lastlog
# Hack, don't want to list all sources
cp -rL $RPM_SOURCE_DIR/* etc/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root)
%verify(not md5 size mtime) %config(noreplace) /etc/passwd
%verify(not md5 size mtime) %config(noreplace) %attr(400,root,root) /etc/shadow
%verify(not md5 size mtime) %config(noreplace) /etc/group
%verify(not md5 size mtime) %config(noreplace) %attr(600,root,root) /etc/fstab
%attr(600,root,root) /etc/securetty
%config /etc/shells
%config(noreplace) /etc/host.conf
%config /etc/protocols
%config /etc/services
%config(noreplace) /etc/hosts.allow
%config(noreplace) /etc/hosts.deny
%config(noreplace) /etc/profile
%config(noreplace) /etc/bashrc
%config /etc/inputrc
%config(noreplace) /etc/csh.login
%config(noreplace) /etc/csh.cshrc
%config /etc/motd
%dir %attr(755,root,root) /etc/profile.d
%ghost /var/log/lastlog

%changelog
* Wed Dec 20 2000 Solar Designer <solar@owl.openwall.com>
- Obsoletes: setup (yes, we can upgrade to this from RH).
- Provide default hosts.allow and hosts.deny with useful comments.
- Provide /var/log/lastlog as a ghost just so that it doesn't get removed
when upgrading from Red Hat's "setup" package; the actual file is created
by owl-startup.

* Sat Dec 16 2000 Solar Designer <solar@owl.openwall.com>
- Provide initial fstab here.
- proc group.

* Mon Dec 11 2000 Solar Designer <solar@owl.openwall.com>
- Conflicts: setup

* Wed Dec 06 2000 Solar Designer <solar@owl.openwall.com>
- popa3d user/group.

* Mon Dec 04 2000 Solar Designer <solar@owl.openwall.com>
- utmp group.
- Keep the initial shadow file here rather than use pwconv.

* Tue Nov 21 2000 Solar Designer <solar@owl.openwall.com>
- More pseudo-users/groups: klogd, postfix, postdrop, postman.

* Sun Aug 20 2000 Solar Designer <solar@owl.openwall.com>
- crontab user/group.

* Thu Jul 27 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

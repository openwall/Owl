# $Id: Owl/packages/popa3d/popa3d.spec,v 1.1 2000/12/06 12:04:02 solar Exp $

Summary: A small POP3 server with security as its primary design goal
Name: popa3d
Version: 0.4.4
Release: 1owl
Copyright: GPL
Group: System Environment/Daemons
Source0: ftp://ftp.openwall.com/popa3d/popa3d-0.4.tar.gz
Source1: popa3d.pam
Source2: popa3d.init
Patch0: popa3d-0.4-%{version}.diff.gz
Patch1: popa3d-0.4.4-owl-params.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: pam_userpass
Prereq: /sbin/chkconfig, /dev/null, grep, shadow-utils

%description
popa3d is a small POP3 server with security as its primary design goal.

%prep
%setup -q -n popa3d-0.4
%patch0 -p1
%patch1 -p1

%build
make CFLAGS="-c -Wall $RPM_OPT_FLAGS" LDFLAGS="-s -lcrypt -lpam"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{usr/sbin,etc/{pam.d,rc.d/init.d}}

install -m 700 popa3d $RPM_BUILD_ROOT/usr/sbin/
install -m 600 $RPM_SOURCE_DIR/popa3d.pam \
	$RPM_BUILD_ROOT/etc/pam.d/popa3d
install -m 700 $RPM_SOURCE_DIR/popa3d.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/popa3d

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep ^popa3d: /etc/group &> /dev/null || groupadd -g 184 popa3d
grep ^popa3d: /etc/passwd &> /dev/null ||
	useradd -g popa3d -u 184 -d / -s /bin/false -M popa3d
rm -f /var/run/popa3d.restart
if [ $1 -ge 2 ]; then
	/etc/rc.d/init.d/popa3d status && touch /var/run/popa3d.restart || :
	/etc/rc.d/init.d/popa3d stop || :
fi

%post
test -f /var/run/popa3d.restart && /etc/rc.d/init.d/popa3d start || :
rm -f /var/run/popa3d.restart

%preun
if [ $1 -eq 0 ]; then
	/etc/rc.d/init.d/popa3d stop || :
	/sbin/chkconfig --del popa3d
fi

%files
%defattr(-,root,root)
/usr/sbin/popa3d
%config(noreplace) /etc/pam.d/popa3d
%config /etc/rc.d/init.d/popa3d
%doc DESIGN COPYING

%changelog
* Wed Dec 06 2000 Solar Designer <solar@owl.openwall.com>
- 0.4.4 with pam_userpass support.
- Wrote this spec file, popa3d.pam, and popa3d.init.

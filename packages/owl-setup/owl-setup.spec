# $Id: Owl/packages/owl-setup/owl-setup.spec,v 1.8 2001/07/27 20:13:48 solar Exp $

Summary: Owl configuration tool
Name: owl-setup
Version: 0.4
Release: 3owl
Copyright: mostly public domain, passwdlg is under GPL
Group: System Environment/Base
Source0: Makefile
Source1: passwdlg.c
Source2: setup.pam
Source3: owl-setup.conf
Source4: owl-setup
Source5: mkfstab
Source6: netcfg
Source10: README
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: owl-startup
Requires: dialog
Requires: bash >= 2.0, sh-utils, util-linux, sed, mktemp
Conflicts: setuptool

%description
This is a configuration tool to initially setup fstab, networking,
root password, and timezone.  This is temporary solution and will be
replaced with a more consistent and reliable tool in the future.

%prep
%setup -n owl-setup -c -T
cp $RPM_SOURCE_DIR/{Makefile,passwdlg.c,README} .
chmod 644 README

%build
make CFLAGS="$RPM_OPT_FLAGS -Wall"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{etc/pam.d,usr/lib/owl-setup,usr/sbin}
install -m 600 $RPM_SOURCE_DIR/owl-setup.conf $RPM_BUILD_ROOT/etc/
install -m 700 passwdlg $RPM_BUILD_ROOT/usr/lib/owl-setup
install -m 600 $RPM_SOURCE_DIR/setup.pam $RPM_BUILD_ROOT/etc/pam.d/setup
install -m 700 $RPM_SOURCE_DIR/owl-setup $RPM_BUILD_ROOT/usr/lib/owl-setup
install -m 700 $RPM_SOURCE_DIR/mkfstab $RPM_BUILD_ROOT/usr/lib/owl-setup
install -m 700 $RPM_SOURCE_DIR/netcfg $RPM_BUILD_ROOT/usr/lib/owl-setup
install -m 644 $RPM_SOURCE_DIR/README $RPM_BUILD_ROOT/usr/lib/owl-setup
ln -s /usr/lib/owl-setup/owl-setup $RPM_BUILD_ROOT/usr/sbin/setup

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config /etc/pam.d/setup
%config /etc/owl-setup.conf
%dir %attr(755,root,root) /usr/lib/owl-setup
/usr/lib/owl-setup/*
/usr/sbin/setup
%doc README

%changelog
* Wed Jul 25 2001 Michail Litvak <mci@owl.openwall.com>
- add --cr-wrap option in netcfg to fix broken
  displaying (cause - changes in new dialog version)
- fix bug in mkfstab, now it is possible to add unlisted partitions
  and properly set their type

* Sat Jun 23 2001 Solar Designer <solar@owl.openwall.com>
- Grammar/spelling fix for a netcfg message.
- Ensure the newly created /etc/resolv.conf and /etc/hosts are mode 644.

* Wed Jun 06 2001 Michail Litvak <mci@owl.openwall.com>
- write domain into resolv.conf

* Tue Dec 26 2000 Michail Litvak <mci@owl.openwall.com>
- Initial version.

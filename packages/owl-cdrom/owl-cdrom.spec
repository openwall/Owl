# $Id: Owl/packages/owl-cdrom/owl-cdrom.spec,v 1.1 2001/07/27 20:17:22 solar Exp $

Summary: Directory hierarchy changes and files needed for bootable CD-ROM's.
Name: owl-cdrom
Version: 0.0
Release: 1owl
Copyright: GPL
Group: System Environment/Base
Source0: rc.ramdisk
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: owl-startup >= 0.8-1owl

%description
This package applies directory hierarchy changes and provides additional
startup scripts needed for Owl bootable CD-ROM's.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{etc/rc.d,rom,ram}

cd $RPM_BUILD_ROOT
touch .Owl-CD-ROM
install -m 700 $RPM_SOURCE_DIR/rc.ramdisk etc/rc.d/
ln -s ../rom/{dev,etc,home,root,tmp,var} ram/

%post
set -e

chmod 755 /
chown root.root /

for DIR in dev etc home root tmp var; do
	test -d /$DIR -a ! -e /rom/$DIR
	mv /$DIR /rom/
	ln -s ram/$DIR /
done

%preun
set -e

if [ $1 -eq 0 ]; then
	for DIR in dev etc home root tmp var; do
		test -L /$DIR -a -d /rom/$DIR
		rm /$DIR
		mv /rom/$DIR /
	done
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/.Owl-CD-ROM
%config /etc/rc.d/rc.ramdisk
%dir /rom
/ram

%changelog
* Fri Jul 27 2001 Solar Designer <solar@owl.openwall.com>
- Initial version.

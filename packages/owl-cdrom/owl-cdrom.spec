# $Id: Owl/packages/owl-cdrom/owl-cdrom.spec,v 1.5 2001/11/25 23:52:48 solar Exp $

Summary: Directory hierarchy changes and files needed for bootable CD-ROM's.
Name: owl-cdrom
Version: 0.3
Release: 1owl
License: public domain
Group: System Environment/Base
Source0: rc.ramdisk
Source1: lilo.conf
Source2: dot-config
Source3: floppy.update
Requires: owl-startup >= 0.8-1owl
BuildRoot: /override/%{name}-%{version}

%description
This package applies directory hierarchy changes and provides additional
startup scripts needed for Owl bootable CD-ROM's.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{etc/rc.d,boot,rom,ram,owl}

cd $RPM_BUILD_ROOT
touch .Owl-CD-ROM
install -m 700 $RPM_SOURCE_DIR/rc.ramdisk etc/rc.d/
install -m 600 $RPM_SOURCE_DIR/lilo.conf etc/
install -m 600 $RPM_SOURCE_DIR/dot-config boot/.config
install -m 700 $RPM_SOURCE_DIR/floppy.update boot/
ln -s ../rom/{dev,etc,home,root,tmp,var,world} ram/

%pre
if [ "$CDROM" != "yes" ]; then
	echo "Please set CDROM=yes if you know what you're doing"
	exit 1
fi

%post
set -e

chmod 755 /
chown root.root /

for DIR in dev etc home root tmp var; do
	test -d /$DIR -a ! -e /rom/$DIR
	mv /$DIR /rom/
	ln -s ram/$DIR /
done

test -d /usr/src/world -a ! -e /rom/world
mv /usr/src/world /rom/
ln -s ../../ram/world /usr/src/

%preun
set -e

if [ $1 -eq 0 ]; then
	for DIR in dev etc home root tmp var; do
		test -L /$DIR -a -d /rom/$DIR
		rm /$DIR
		mv /rom/$DIR /
	done

	test -L /usr/src/world -a -d /rom/world
	rm /usr/src/world
	mv /rom/world /usr/src/
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/.Owl-CD-ROM
%config /etc/rc.d/rc.ramdisk
%config /etc/lilo.conf
%config /boot/.config
/boot/floppy.update
%dir /rom
/ram
%dir /owl

%changelog
* Mon Nov 26 2001 Solar Designer <solar@owl.openwall.com>
- Updated .config for Linux 2.2.20-ow1.

* Wed Oct 03 2001 Solar Designer <solar@owl.openwall.com>
- Create an inode per 1024 bytes on the ramdisk or we would get out of
inodes with a 4 MB ramdisk.
- The timeout for root device choice is now 1 minute, not 5 seconds as
the default choice will very often be wrong.

* Sat Sep 15 2001 Solar Designer <solar@owl.openwall.com>
- Packaged lilo.conf, .config, and a script to create or update floppy
images for use with CD-ROM's.
- Move /usr/src/world to /ram such that "make installworld" may create
its symlinks and write to its log file.

* Sat Jul 28 2001 Solar Designer <solar@owl.openwall.com>
- Require CDROM=yes such that this package isn't installed by mistake.

* Fri Jul 27 2001 Solar Designer <solar@owl.openwall.com>
- Initial version.

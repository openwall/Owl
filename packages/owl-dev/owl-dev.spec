# $Id: Owl/packages/owl-dev/owl-dev.spec,v 1.5 2001/02/04 22:22:35 solar Exp $

Summary: Initial set of device files and MAKEDEV, a script to manage them
Name: owl-dev
Version: 0.4
Release: 1owl
Copyright: public domain
Group: System Environment/Base
Source: MAKEDEV-2.5.2.tar.gz
Patch: MAKEDEV-2.5.2-owl.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: owl-etc fileutils sh-utils
BuildArchitectures: noarch

%description
Unix-like operating systems use a special kind of filesystem entries
to represent various hardware devices (such as disk drives) and provide
access to a number of kernel facilities.  This package creates the
initial set of device files to be placed into /dev.  It also provides
/dev/MAKEDEV, a script to create and manage the device files.

%prep
%setup -q -n MAKEDEV-2.5.2
%patch -p1

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/dev
install -m 700 MAKEDEV $RPM_BUILD_ROOT/dev

# Create regular files with the proper names and permissions (not device
# files, yet).  This idea (but not the implementation) is taken from iNs.
cd $RPM_BUILD_ROOT/dev
./MAKEDEV --touch generic

# Restrict the permissions as we don't set the correct groups, yet
chmod -R go-rwx $RPM_BUILD_ROOT/dev

# Build the filelist
cd $RPM_BUILD_DIR/MAKEDEV-2.5.2
echo '%defattr(-,root,root)' > filelist
find $RPM_BUILD_ROOT/dev ! -type d ! -size 0 | \
	sed "s,^$RPM_BUILD_ROOT,," >> filelist
find $RPM_BUILD_ROOT/dev ! -type d -size 0 | \
	sed "s,^$RPM_BUILD_ROOT,%ghost ," >> filelist

%clean
rm -rf $RPM_BUILD_ROOT

%post
cd /dev
./MAKEDEV -p generic

%files -f filelist

%changelog
* Mon Feb 05 2001 Solar Designer <solar@owl.openwall.com>
- Create devices of more categories by default (st, scd, sg, md, loop, audio).

* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- /dev/sunmouse.

* Mon Dec 04 2000 Solar Designer <solar@owl.openwall.com>
- Create device files for 4 IDE and 8 SCSI devices with up to 15 partitions
by default.
- Use %ghost.

* Sun Dec 03 2000 Solar Designer <solar@owl.openwall.com>
- Unix98 pty's support.

* Sat Jul 29 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.

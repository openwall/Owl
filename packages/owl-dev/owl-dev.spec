# $Owl: Owl/packages/owl-dev/owl-dev.spec,v 1.23 2006/04/19 04:31:16 solar Exp $

Summary: Initial set of device files and MAKEDEV, a script to manage them.
Name: owl-dev
Version: 0.11
Release: owl1
License: public domain
Group: System Environment/Base
Source: MAKEDEV-2.5.2.tar.gz
Patch: MAKEDEV-2.5.2-owl.diff
PreReq: grep
PreReq: owl-etc >= 0.18-owl1, fileutils, sh-utils
Provides: dev
Obsoletes: MAKEDEV, dev
BuildArchitectures: noarch
BuildRoot: /override/%name-%version

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
rm -rf %buildroot
mkdir -p -m 700 %buildroot/dev
mkdir -p %buildroot%_mandir/man8
install -m 700 MAKEDEV %buildroot/dev/
install -m 644 MAKEDEV.man %buildroot%_mandir/man8/MAKEDEV.8

# Create regular files with the proper names and permissions (not device
# files, yet).  This idea (but not the implementation) is taken from iNs.
cd %buildroot/dev
./MAKEDEV --touch generic

# Restrict the permissions as we don't set the correct groups, yet
find %buildroot/dev ! -type d -size 0 -print0 | xargs -0 chmod go-rwx

# Build the filelist
cd $RPM_BUILD_DIR/MAKEDEV-2.5.2
cat > filelist << EOF
%%defattr(-,root,root)
%%_mandir/man8/MAKEDEV.8*
EOF
find %buildroot/dev ! -type d ! -size 0 | \
	sed "s,^%buildroot,," >> filelist
find %buildroot/dev -type d -mindepth 1 | \
	sed "s,^%buildroot,%%ghost %%dir ," >> filelist
find %buildroot/dev ! -type d -size 0 | \
	sed "s,^%buildroot,%%ghost %%verify(not group mode rdev) ," \
	>> filelist

%post
grep -q ^audio: /etc/group || groupadd -g 120 audio
grep -q ^video: /etc/group || groupadd -g 121 video
grep -q ^radio: /etc/group || groupadd -g 122 radio

cd /dev || exit 1
echo "Creating device files"
/dev/MAKEDEV -p generic

%files -f filelist

%changelog
* Tue Apr 18 2006 Gremlin from Kremlin <gremlin-at-owl.openwall.com> 0.11-owl1
- /dev/cciss/cXdYpZ for HP CCISS RAID

* Wed Mar 10 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.10-owl2
- Added "dev" to Provides.

* Sat Oct 25 2003 Solar Designer <solar-at-owl.openwall.com> 0.10-owl1
- /dev/rtc (but restricted to just root, unlike on Red Hat Linux).
- Make the /dev/core and /dev/fd symlinks relative.

* Thu Jul 31 2003 Solar Designer <solar-at-owl.openwall.com> 0.9-owl1
- /dev/kbd.

* Fri Jul 25 2003 Solar Designer <solar-at-owl.openwall.com> 0.8-owl1
- /dev/openprom.

* Sun Jun 09 2002 Solar Designer <solar-at-owl.openwall.com> 0.7-owl1
- Support Linux 2.4.x's /proc/devices entries.
- Support and create frame buffer devices.
- Support up to 8 IDE controllers (16 devices).
- Create device files for 8 IDE devices by default.
- Echo a message when running the script in %%post.
- Install the MAKEDEV(8) man page.
- List /dev subdirectories in the package.

* Wed Feb 06 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Nov 18 2001 Solar Designer <solar-at-owl.openwall.com>
- Don't verify file type (as well as permissions, because of an RPM
limitation), device, and group for the device files.

* Mon Nov 05 2001 Solar Designer <solar-at-owl.openwall.com>
- Don't PreReq: shadow-utils, the post-install script is smart enough
to not depend on groupadd when the groups already exist (which is the
case for new installs due to owl-etc).

* Thu Nov 01 2001 Solar Designer <solar-at-owl.openwall.com>
- audio, video and radio groups to manage access to devices.

* Sun Apr 08 2001 Solar Designer <solar-at-owl.openwall.com>
- Obsoletes: MAKEDEV, dev

* Sun Mar 04 2001 Solar Designer <solar-at-owl.openwall.com>
- USB printers and mice.

* Mon Feb 05 2001 Solar Designer <solar-at-owl.openwall.com>
- Create devices of more categories by default (st, scd, sg, md, loop, audio).

* Sat Jan 06 2001 Solar Designer <solar-at-owl.openwall.com>
- /dev/sunmouse.

* Mon Dec 04 2000 Solar Designer <solar-at-owl.openwall.com>
- Create device files for 4 IDE and 8 SCSI devices with up to 15 partitions
by default.
- Use %%ghost.

* Sun Dec 03 2000 Solar Designer <solar-at-owl.openwall.com>
- Unix98 pty's support.

* Sat Jul 29 2000 Solar Designer <solar-at-owl.openwall.com>
- Initial version.

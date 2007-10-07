# $Owl: Owl/packages/mdadm/mdadm.spec,v 1.4 2007/10/07 01:40:17 solar Exp $

Summary: mdadm is used for controlling Linux md devices (aka RAID arrays).
Name: mdadm
Version: 2.6.3
%define version_howto 1.1
Release: owl1
License: GPL
Group: System Environment/Base
URL: http://neil.brown.name/blog/mdadm
# http://www.cse.unsw.edu.au/~neilb/source/mdadm/mdadm-%version.tgz (no bz2)
Source0: ftp://ftp.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%version.tar.bz2
# http://unthought.net/Software-RAID.HOWTO/Software-RAID.HOWTO.txt
Source1: Software-RAID.HOWTO-%version_howto.txt.bz2
Source2: %name.conf
#Source3: %name.init
Obsoletes: mdctl, raidtools
BuildRequires: groff
BuildRoot: /override/%name-%version

%description
mdadm is a program that can be used to create, manage, and monitor Linux
MD (Software RAID) devices.  As such it provides functionality similar
to that of the raidtools package, which may be found on older versions
of Owl and on some other Linux systems.  The particular differences to
raidtools are that mdadm is a single program and it can perform (almost)
all functions without a configuration file (yet a configuration file can
be used to help with some common tasks).

%prep
%setup -q

# this is a system tool and will go into /sbin
%define _exec_prefix %{nil}

bzip2 -9fk ChangeLog
install -pm 644 %_sourcedir/Software-RAID.HOWTO-%version_howto.txt.bz2 \
	Software-RAID.HOWTO.txt.bz2

%build
%__make \
	CXFLAGS='%optflags' \
	SYSCONFDIR=%_sysconfdir \
	CONFFILE=%_sysconfdir/%name.conf \
	CONFFILE2=/dev/null

%install
rm -rf %buildroot
%__make install \
	DESTDIR=%buildroot \
	MANDIR=%_mandir \
	BINDIR=%_sbindir

install -Dp -m644 %_sourcedir/%name.conf %buildroot%_sysconfdir/%name.conf

%post
## this block will be enabled once we have a working mdadm.init script
#if [ $1 -ge 2 ]; then
#	/sbin/service %name status &>/dev/null && \
#		/sbin/service %name restart || :
#fi
#/sbin/chkconfig %name || /sbin/chkconfig --add %name

%preun
## this block will be enabled once we have a working mdadm.init script
#if [ $1 -eq 0 ]; then
#	# TODO: need to check whether any /dev/md* is mounted and abort if
#	#       it is. -- (GM)
#	/sbin/service %name stop || :
#	if /sbin/chkconfig %name; then
#		/sbin/chkconfig --del %name
#	fi
#fi

%triggerun -- raidtools
if [ -e /etc/raidtab ]; then
	cat << EOF
Warning: the raidtools package is being replaced with mdadm, so your
/etc/raidtab will no longer be used.

Install will continue in 10 seconds...
EOF
	sleep 10
fi

%files
%defattr(-,root,root)
%doc ChangeLog.bz2 README.initramfs COPYING
%doc Software-RAID.HOWTO.*
%attr(0700,root,root) %_sbindir/mdadm
%attr(0600,root,root) %config(noreplace,missingok) %_sysconfdir/%name.conf
%_mandir/man*/md*

%changelog
* Sun Oct 07 2007 Solar Designer <solar-at-owl.openwall.com> 2.6.3-owl1
- Assorted changes to meet the current Owl conventions.
- Changes to the package description.
- Use .tar.bz2's off kernel.org rather than original .tgz's.
- Corrected some comments in mdadm.conf and adjusted them for Owl specifics.
- Added the Software-RAID HOWTO (version 1.1, June 2004).
- Added a trigger and warning on upgrades from raidtools with /etc/raidtab.

* Tue Aug 28 2007 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.6.3-gm0
- Initial build (missing mdadm.init).

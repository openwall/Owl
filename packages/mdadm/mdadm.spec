# $Owl: Owl/packages/mdadm/mdadm.spec,v 1.1 2007/10/07 00:03:28 solar Exp $

Summary: mdadm is used for controlling Linux md devices (aka RAID arrays)
Name: mdadm
Version: 2.6.3
Release: gm0
License: GPL
Group: Utilities/System
URL: http://neil.brown.name/blog/mdadm
Source0: http://www.cse.unsw.edu.au/~neilb/source/mdadm/mdadm-%version.tgz
Source1: %name.conf
#Source2: %name.init
#Patch0: <placeholder>
BuildRequires: groff
BuildRoot: /override/%name-%version
Obsoletes: mdctl, raidtools

%description
mdadm is a program that can be used to create, manage, and monitor Linux
MD (Software RAID) devices.  As such it provides similar functionality
to the raidtools packages.  The particular differences to raidtools is
that mdadm is a single program, and it can perform (almost) all
functions without a configuration file (that a config file can be used
to help with some common tasks).

%prep
%setup -q

# this is a system tool and will go into /sbin
%define _exec_prefix %{nil}

bzip2 -9fk ChangeLog

%build
%__make \
	'CXFLAGS=%optflags' \
	'SYSCONFDIR=%_sysconfdir' \
	'CONFFILE=%_sysconfdir/%name.conf' \
	'CONFFILE2=/dev/null'

%install
rm -rf -- '%buildroot'
%__make install \
	'DESTDIR=%buildroot' \
	'MANDIR=%_mandir' \
	'BINDIR=%_sbindir'

install -Dp -m644 '%_sourcedir/%name.conf' '%buildroot%_sysconfdir/%name.conf'

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

%files
%defattr(0644,root,root,0755)
%doc ChangeLog.bz2 README.initramfs COPYING
%attr(0700,root,root) %_sbindir/mdadm
%attr(0600,root,root) %config(noreplace,missingok) %_sysconfdir/%name.conf
%_mandir/man*/md*

%changelog
* Tue Aug 28 2007 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.6.3-gm0
- Initial build (missing mdadm.init).

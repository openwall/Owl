# $Id: Owl/packages/util-linux/util-linux.spec,v 1.1 2000/07/13 09:25:30 solar Exp $

Summary: A collection of basic system utilities.
Name: util-linux
Version: 2.10h
Release: 1owl
Copyright: distributable
Group: System Environment/Base
Source0: ftp://ftp.kernel.org/pub/linux/utils/util-linux/util-linux-%{version}.tar.gz
Source1: chsh-chfn-pam
Patch0: util-linux-2.10h-owl-MCONFIG.diff
Patch1: util-linux-2.10h-owl-Makefiles.diff
Patch2: util-linux-2.10h-owl-restrict-locale.diff
Patch3: util-linux-2.10h-owl-write.diff
Patch4: util-linux-2.10h-rh-locale-overflow.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Obsoletes: fdisk tunelp
%ifarch sparc alpha
Obsoletes: clock
%endif
Requires: kernel >= 2.2.12

%description
The util-linux package contains a large variety of low-level system
utilities that are necessary for a Linux system to function.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
unset LINGUAS || :
./configure
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{bin,sbin,etc/pam.d}
mkdir -p $RPM_BUILD_ROOT/usr/{bin,info,lib,man/man1,man/man6,man/man8,sbin}

make install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf $RPM_BUILD_ROOT/usr/info/ipc.info
gzip -9nf $RPM_BUILD_ROOT/usr/man/man*/*

for i in /usr/bin/chfn /usr/bin/chsh /usr/bin/newgrp ; do
	strip $RPM_BUILD_ROOT/$i
done

strip $RPM_BUILD_ROOT/sbin/fdisk || :

install -m 600 ${RPM_SOURCE_DIR}/chsh-chfn-pam $RPM_BUILD_ROOT/etc/pam.d/chsh
install -m 600 ${RPM_SOURCE_DIR}/chsh-chfn-pam $RPM_BUILD_ROOT/etc/pam.d/chfn

rm -f $RPM_BUILD_ROOT/sbin/clock
ln -s hwclock $RPM_BUILD_ROOT/sbin/clock

# We do not want dependencies on csh
chmod 644 $RPM_BUILD_ROOT/usr/lib/getopt/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/sbin/clock
/sbin/hwclock
/usr/man/man8/hwclock.8*

/usr/sbin/tunelp
/usr/man/man8/tunelp.8*

%config /etc/pam.d/chfn
%config /etc/pam.d/chsh

/sbin/fdisk
%ifarch i386 alpha armv4l
/sbin/cfdisk
%endif

%ifarch i386 alpha
/sbin/fsck.minix
/sbin/mkfs.minix
%endif

/sbin/mkfs
/sbin/mkswap

/usr/bin/fdformat
/usr/bin/setfdprm
%config /etc/fdprm

/usr/man/man8/fdformat.8*
/usr/man/man8/mkswap.8*
/usr/man/man8/setfdprm.8*

/usr/bin/ddate
/usr/man/man1/ddate.1*

%ifarch i386 alpha sparc
%attr(700,root,root)	/usr/bin/chfn
%attr(700,root,root)	/usr/bin/chsh
%attr(4711,root,root)	/usr/bin/newgrp
%attr(700,root,root)	/usr/sbin/vipw
%attr(700,root,root)	/usr/sbin/vigr
/usr/man/man1/chfn.1*
/usr/man/man1/chsh.1*
/usr/man/man1/newgrp.1*
/usr/man/man8/vipw.8*
/usr/man/man8/vigr.8*
%endif

/bin/kill
/usr/bin/cal
/usr/bin/logger
/usr/bin/look
/usr/bin/mcookie
/usr/bin/namei
/usr/bin/script
/usr/bin/setterm
/usr/bin/whereis
%attr(2711,root,tty)	/usr/bin/write
/usr/bin/getopt
/usr/man/man1/cal.1*
/usr/man/man1/kill.1*
/usr/man/man1/logger.1*
/usr/man/man1/look.1*
/usr/man/man1/mcookie.1*
/usr/man/man1/namei.1*
/usr/man/man1/script.1*
/usr/man/man1/setterm.1*
/usr/man/man1/whereis.1*
/usr/man/man1/write.1*
/usr/man/man1/getopt.1*

/usr/lib/getopt

/bin/dmesg

/sbin/ctrlaltdel
/sbin/kbdrate
/bin/arch
/usr/bin/ipcrm
/usr/bin/ipcs
/usr/bin/renice
/usr/sbin/readprofile
/usr/bin/setsid
%ifarch i386 alpha armv4l
/usr/bin/cytune
%endif

/usr/man/man1/arch.1*
/usr/man/man1/readprofile.1*
%ifarch i386 alpha armv4l
/usr/man/man8/cytune.8*
%endif
/usr/man/man8/ctrlaltdel.8*
/usr/man/man8/dmesg.8*
/usr/man/man8/ipcrm.8*
/usr/man/man8/ipcs.8*
/usr/man/man8/kbdrate.8*
/usr/man/man8/renice.8*
/usr/man/man8/setsid.8*

%ifarch i386
/usr/sbin/rdev
/usr/sbin/ramsize
/usr/sbin/rootflags
/usr/sbin/swapdev
/usr/sbin/vidmode
/usr/man/man8/rdev.8*
/usr/man/man8/ramsize.8*
/usr/man/man8/rootflags.8*
/usr/man/man8/swapdev.8*
/usr/man/man8/vidmode.8*
%endif

/usr/info/ipc.info.gz

/usr/bin/col
/usr/bin/colcrt
/usr/bin/colrm
/usr/bin/column
/usr/bin/hexdump
/usr/bin/rename
/usr/bin/rev
/usr/bin/ul

/usr/man/man1/col.1*
/usr/man/man1/colcrt.1*
/usr/man/man1/colrm.1*
/usr/man/man1/column.1*
/usr/man/man1/hexdump.1*
/usr/man/man1/rename.1*
/usr/man/man1/rev.1*
/usr/man/man1/ul.1*

/bin/more
/usr/man/man1/more.1*
/usr/lib/more.help

%ifarch i386 alpha
/usr/man/man8/fsck.minix.8*
/usr/man/man8/mkfs.minix.8*
/usr/man/man8/mkfs.8*
%endif

/usr/man/man8/fdisk.8*

%ifarch i386 alpha armv4l
/usr/man/man8/cfdisk.8*
%endif

%doc */README.*

%ifarch i386 alpha
/sbin/sfdisk
/usr/man/man8/sfdisk.8*
%doc fdisk/sfdisk.examples
%endif

%changelog
* Thu Jul 13 2000 Solar Designer <solar@false.com>
- Imported this spec file from RH, and changed it heavily.
- Updated one of the RH patches for 2.10h, removed the rest.
- Removed login as we use one from SimplePAMApps.
- Added two security patches.

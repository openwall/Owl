# $Owl: Owl/packages/raidtools/Attic/raidtools.spec,v 1.6 2005/11/16 13:31:51 solar Exp $

Summary: Tools for creating and maintaining software RAID devices.
Name: raidtools
Version: 1.00.3
Release: owl1
License: GPL
Group: System Environment/Base
Source0: http://people.redhat.com/mingo/raidtools/raidtools-%version.tar.gz
# http://unthought.net/Software-RAID.HOWTO/Software-RAID.HOWTO.txt
Source1: Software-RAID.HOWTO.txt.bz2
Patch0: raidtools-1.00.3-owl-Makefile.diff
Patch1: raidtools-1.00.3-owl-no-include.diff
Patch2: raidtools-1.00.3-rh-raidstop.diff
Patch3: raidtools-1.00.3-deb-man.diff
Patch4: raidtools-1.00.3-deb-fixes.diff
Obsoletes: md, md-tools
BuildRequires: popt
BuildRoot: /override/%name-%version

%description
The raidtools package includes the tools you need to set up and
maintain a software RAID device (using two or more disk drives in
combination for fault tolerance and improved performance) on a Linux
system.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
install -m 644 %_sourcedir/Software-RAID.HOWTO.txt.bz2 .

%build
%configure --sbindir=/sbin
make

%install
rm -rf %buildroot
make install_bin install_doc ROOTDIR=%buildroot MAN=%_mandir

%files
%defattr(-,root,root)
%doc README raidreconf-HOWTO *.sample
%doc Software-RAID.HOWTO.*
/sbin/*
%_mandir/man*/*

%changelog
* Wed Sep 10 2003 Michail Litvak <mci-at-owl.openwall.com> 1.00.3-owl1
- Initial packaging for Owl.
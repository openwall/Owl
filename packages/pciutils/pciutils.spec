# $Owl: Owl/packages/pciutils/pciutils.spec,v 1.4 2010/01/26 15:03:16 solar Exp $

Summary: Linux PCI utilities.
Name: pciutils
Version: 3.1.6
Release: owl1
License: GPLv2
Group: Applications/System
URL: http://mj.ucw.cz/pciutils.html
Source0: ftp://atrey.karlin.mff.cuni.cz/pub/linux/pci/%name-%version.tar.gz
# http://pci-ids.ucw.cz
#Patch0: pciutils-%version-pci.ids-20YYMMDD.diff.bz2
BuildRequires: zlib-devel
BuildRoot: /override/%name-%version

%description
The pciutils package contains various utilities for inspecting and
setting up devices connected to the PCI bus.

%prep
%setup -q
#%patch0 -p1

%build
%__make SHARED=no ZLIB=yes STRIP='' OPT='%optflags' PREFIX=%_prefix \
	IDSDIR=%_datadir/hwdata PCI_IDS=pci.ids

%install
rm -rf %buildroot
%makeinstall SHARED=no DESTDIR=%buildroot PREFIX=%_prefix \
	IDSDIR=%_datadir/hwdata install

%files
%defattr(-,root,root)
%_sbindir/lspci
%_sbindir/setpci
%exclude %_sbindir/update-pciids
%_mandir/man8/*
%exclude %_mandir/man8/update-pciids.8*
%exclude %_mandir/man7/*
%doc README ChangeLog TODO pciutils.lsm
%_datadir/hwdata/pci.ids.gz

%changelog
* Tue Jan 26 2010 Solar Designer <solar-at-owl.openwall.com> 3.1.6-owl1
- Updated to 3.1.6.

* Thu Jan 21 2010 Solar Designer <solar-at-owl.openwall.com> 3.1.5-owl1
- Updated to 3.1.5.

* Fri May 29 2009 Michail Litvak <mci-at-owl.openwall.com> 3.1.2-owl1
- Initial packaging for Owl.

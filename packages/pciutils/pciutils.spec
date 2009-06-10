# $Owl: Owl/packages/pciutils/pciutils.spec,v 1.2 2009/06/10 15:11:30 mci Exp $

Summary: Linux PCI utilities.
Name: pciutils
Version: 3.1.2
Release: owl1
License: GPL
Group: Applications/System
Source0: ftp://atrey.karlin.mff.cuni.cz/pub/linux/pci/%name-%version.tar.gz
Patch0: pciutils-3.1.2-pci.ids-20090519.diff.bz2
Prefix: %_prefix
BuildRequires: zlib-devel
BuildRoot: /override/%name-%version

%description
The pciutils package contains various utilities for inspecting and
setting up devices connected to the PCI bus.

%prep
%setup -q
%patch0 -p1

%build
%__make SHARED=no ZLIB=yes STRIP='' OPT='%optflags' PREFIX=/usr \
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
* Fri May 29 2009 Michail Litvak <mci-at-owl.openwall.com> 3.1.2-owl1
- Initial packaging for Owl.

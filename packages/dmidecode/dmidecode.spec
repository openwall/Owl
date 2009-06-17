# $Owl: Owl/packages/dmidecode/dmidecode.spec,v 1.2 2009/06/17 18:06:05 solar Exp $

Summary: Tool to analyze BIOS DMI data.
Name: dmidecode
Version: 2.10
Release: owl1
License: GPLv2
Group: Applications/System
URL: http://www.nongnu.org/dmidecode/
Source0: http://download.savannah.gnu.org/releases/dmidecode/%name-%version.tar.bz2
# Signature: http://download.savannah.gnu.org/releases/dmidecode/%name-%version.tar.bz2.sig
Prefix: %_prefix
ExclusiveArch: %ix86 x86_64
BuildRoot: /override/%name-%version

%description
dmidecode reports information about x86 & x86-64 hardware as described
in the system BIOS according to the SMBIOS/DMI standard.  This
information typically includes system manufacturer, model name, serial
number, BIOS version, asset tag as well as a lot of other details of
varying level of interest and reliability depending on the manufacturer.
This will often include usage status for the CPU sockets, expansion
slots (e.g. AGP, PCI, ISA) and memory module slots, and the list of I/O
ports (e.g. serial, parallel, USB).

Three additional tools come with dmidecode:
* biosdecode prints all BIOS-related information it can find;
* ownership retrieves the "ownership tag" on Compaq computers;
* vpddecode prints the "vital product data" on IBM computers.

%prep
%setup -q

%build
%__make CFLAGS='%optflags'

%install
rm -rf %buildroot
%__make DESTDIR=%buildroot prefix=%_prefix install-bin install-man

%files
%defattr(-,root,root)
%_sbindir/dmidecode
%_sbindir/vpddecode
%_sbindir/ownership
%_sbindir/biosdecode
%_mandir/man8/*
%doc AUTHORS CHANGELOG LICENSE README

%changelog
* Thu Jun 11 2009 Michail Litvak <mci-at-owl.openwall.com> 2.10-owl1
- Initial packaging for Owl, based upon Red Hat's spec.

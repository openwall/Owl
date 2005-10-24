# $Id: Owl/packages/prtconf/prtconf.spec,v 1.5 2005/10/24 02:22:13 solar Exp $

Summary: Utilities to dump and modify SPARC OpenPROM.
Name: prtconf
Version: 1.3
Release: owl1
License: GPL
Group: Applications/System
Source: ftp://ftp.auxio.org/pub/linux/SOURCES/%name-%version.tgz
ExclusiveArch: sparc sparcv9 sparc64
BuildRoot: /override/%name-%version

%description
Utilities to dump SPARC OpenPROM device tree in a format similar to
Solaris prtconf (that is, in a nicely readable compact format) and for
changing OpenPROM options.

%prep
%setup -q

%build
make CFLAGS="%optflags"

%install
rm -rf %buildroot
mkdir -p %buildroot{%_sbindir,%_mandir/man8}
install -m 755 prtconf %buildroot%_sbindir/
install -m 755 eeprom %buildroot%_sbindir/
install -m 644 prtconf.8 %buildroot%_mandir/man8/
install -m 644 eeprom.8 %buildroot%_mandir/man8/

gzip -9n examples/*

%files
%defattr(-,root,root)
%doc COPYING examples
%_sbindir/prtconf
%_sbindir/eeprom
%_mandir/man8/prtconf.8*
%_mandir/man8/eeprom.8*

%changelog
* Thu Jul 24 2003 Solar Designer <solar@owl.openwall.com> 1.3-owl1
- Adjusted according to our spec file conventions.
- Compress the examples.

* Wed Apr 23 2003 Maxim Timofeyev <tma@tma.spb.ru>
- Wrote this spec file.

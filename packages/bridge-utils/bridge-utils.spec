# $Owl: Owl/packages/bridge-utils/bridge-utils.spec,v 1.5 2011/01/28 17:08:07 segoon Exp $

Summary: Utilities for configuring the Linux Ethernet bridge.
Name: bridge-utils
Version: 1.4
Release: owl2
License: GPLv2+
Group: System Environment/Base
URL: http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge
Source: http://dl.sf.net/bridge/bridge-utils-%version.tar.gz
Patch0: bridge-utils-1.4-owl-segfault.diff
BuildRoot: /override/%name-%version

%description
This package contains utilities for configuring the Linux Ethernet
bridge.  The Linux Ethernet bridge can be used for connecting multiple
Ethernet devices together.  The connection is fully transparent: hosts
connected to one Ethernet device see hosts connected to the other
Ethernet devices directly.

%prep
%setup -q
%patch0 -p1
sed -i 's/^CFLAGS =.*$/CFLAGS = -Wall @CFLAGS@/' libbridge/Makefile.in

%build
autoconf
%configure
%__make

%install
rm -rf %buildroot
%__make DESTDIR=%buildroot SUBDIRS="brctl doc" install

%files
%defattr(-,root,root,0755)
%doc AUTHORS COPYING THANKS doc/FAQ doc/HOWTO
%_sbindir/brctl
%_mandir/man8/brctl.8*

%changelog
* Fri Jan 28 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.4-owl2
- Fixed segfault of "brctl show" if one bridge has name "bridge".
Differs from Debian fix:
http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=431860 

* Thu Jan 27 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.4-owl1
- Initial import from Fedora.
- Updated to 1.4.

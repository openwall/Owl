# $Owl: Owl/packages/bridge-utils/bridge-utils.spec,v 1.3 2011/01/28 07:38:40 solar Exp $

Summary: Utilities for configuring the Linux Ethernet bridge.
Name: bridge-utils
Version: 1.4
Release: owl1
License: GPLv2+
Group: System Environment/Base
URL: http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge
Source: http://dl.sf.net/bridge/bridge-utils-%version.tar.gz
BuildRoot: /override/%name-%version

%description
This package contains utilities for configuring the Linux Ethernet
bridge.  The Linux Ethernet bridge can be used for connecting multiple
Ethernet devices together.  The connection is fully transparent: hosts
connected to one Ethernet device see hosts connected to the other
Ethernet devices directly.

%prep
%setup -q

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
* Thu Jan 27 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.4-owl1
- Initial import from Fedora.
- Updated to 1.4.

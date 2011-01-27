Summary: Utilities for configuring the linux ethernet bridge
Name: bridge-utils
Version: 1.4
Release: owl1
License: GPLv2+
Group: System Environment/Base
URL: http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge
Source: http://dl.sf.net/bridge/bridge-utils-%version.tar.gz
BuildRoot: /override/%name-%version

%description
This package contains utilities for configuring the linux ethernet
bridge. The linux ethernet bridge can be used for connecting multiple
ethernet devices together. The connecting is fully transparent: hosts
connected to one ethernet device see hosts connected to the other
ethernet devices directly.

Install bridge-utils if you want to use the linux ethernet bridge.

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
%defattr (-,root,root,0755)
%doc AUTHORS COPYING doc/FAQ doc/HOWTO
%_sbindir/brctl
%_mandir/man8/brctl.8*

%changelog
* Thu Jan 27 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.4-owl1
- Initial import from Fedora.
- Updated to 1.4.

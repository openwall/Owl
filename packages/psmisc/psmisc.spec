# $Id: Owl/packages/psmisc/psmisc.spec,v 1.3 2002/02/07 18:30:38 solar Exp $

Summary: Utilities for managing processes on your system.
Name: psmisc
Version: 19
Release: owl4
License: BSD
Group: Applications/System
Source: ftp://lrcftp.epfl.ch/pub/linux/local/psmisc/psmisc-%{version}.tar.gz
Patch0: psmisc-17-rh-buildroot.diff
Patch1: psmisc-19-rh-noroot.diff
BuildRoot: /override/%{name}-%{version}

%description
The psmisc package contains utilities for managing processes on your
system: pstree, killall and fuser.  The pstree command displays a tree
structure of all of the running processes on your system.  The killall
command sends a specified signal (SIGTERM if nothing is specified) to
processes identified by name.  The fuser command identifies the PIDs
of processes that are using specified files or filesystems.

%prep
%setup -q -n psmisc
%patch0 -p1
%patch1 -p1

%build
make CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -DPSMISC_VERSION=\\\"`cat VERSION`\\\"" 'LDFLAGS=-s'

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/bin
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
make INSTPREFIX="$RPM_BUILD_ROOT" MANDIR="%{_mandir}/man1" install
cd $RPM_BUILD_ROOT
mv bin/fuser sbin/
chmod 755 sbin/fuser usr/bin/killall usr/bin/pstree

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGES COPYING README psmisc-%{version}.lsm
/sbin/fuser
/usr/bin/killall
/usr/bin/pstree
%{_mandir}/man1/fuser.1*
%{_mandir}/man1/killall.1*
%{_mandir}/man1/pstree.1*

%changelog
* Wed Feb 06 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.
- Package the documentation.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

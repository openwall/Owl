# $Owl: Owl/packages/tzdata/tzdata.spec,v 1.5.2.1 2015/01/03 05:59:36 solar Exp $

Summary: Timezone data.
Name: tzdata
%define tzdata_version 2014i
%define tzcode_version 2014i
Version: %tzdata_version
Release: owl1
License: public domain
Group: System Environment/Base
URL: http://www.iana.org/time-zones
Source0: ftp://ftp.iana.org/tz/releases/tzdata%tzdata_version.tar.gz
Source1: ftp://ftp.iana.org/tz/releases/tzcode%tzcode_version.tar.gz
BuildRequires: /usr/sbin/zic
BuildRequires: hardlink
BuildArchitectures: noarch
BuildRoot: /override/%name-%version

%description
This package contains data files with rules for various timezones around
the world.

%prep
%setup -q -n tzdata -c -a 1

%build
%__make CC=%__cc CFLAGS='%optflags'

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot TZDIR=%_datadir/zoneinfo
hardlink -vc %buildroot

%check
%__make check_character_set check_white_space check_sorted check_tables

%files
%defattr(-,root,root)
%_datadir/zoneinfo
%doc README NEWS Theory *.htm*
%exclude %_datadir/zoneinfo-leaps
%exclude /usr/local

%changelog
* Sat Oct 25 2014 Solar Designer <solar-at-owl.openwall.com> 2014i-owl1
- Updated to 2014i.

* Mon Jul 07 2014 Solar Designer <solar-at-owl.openwall.com> 2014e-owl1
- Updated to 2014e.

* Wed Oct 26 2011 Solar Designer <solar-at-owl.openwall.com> 2011m-owl1
- Updated to 2011m.

* Sat Oct 15 2011 Solar Designer <solar-at-owl.openwall.com> 2011l-owl1
- Updated to 2011l.
- Run hardlink(1) on the target tree to save disk space.

* Sun Oct 09 2011 Solar Designer <solar-at-owl.openwall.com> 2011k-owl1
- Initial packaging for Owl based on cut-down spec file and
tzdata-base-0.tar.bz2 from Fedora, with review of the tzdata package in
ALT Linux Sisyphus.

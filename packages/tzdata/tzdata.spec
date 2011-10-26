# $Owl: Owl/packages/tzdata/tzdata.spec,v 1.3.2.3 2011/10/26 02:07:09 solar Exp $

Summary: Timezone data.
Name: tzdata
%define tzdata_version 2011m
%define tzcode_version 2011i
Version: %tzdata_version
Release: owl1
License: public domain
Group: System Environment/Base
URL: http://www.iana.org/time-zones
# The tzdata-base-0.tar.bz2 is a simple building infrastructure and
# a test suite.  It is occasionally updated from glibc sources, and as
# such is under LGPLv2+, but none of this ever gets to be part of
# final zoneinfo files.
Source0: tzdata-base-0.tar.bz2
# These are official upstream.
Source1: ftp://munnari.oz.au/pub/tzdata%tzdata_version.tar.gz
Source2: ftp://munnari.oz.au/pub/tzcode%tzcode_version.tar.gz
BuildRequires: /usr/sbin/zic
BuildRequires: hardlink
BuildRequires: sed >= 4.0.9
BuildArchitectures: noarch
BuildRoot: /override/%name-%version

%description
This package contains data files with rules for various timezones around
the world.

%prep
%setup -q -n tzdata
mkdir tzdata%tzdata_version
tar xzf %SOURCE1 -C tzdata%tzdata_version
mkdir tzcode%tzcode_version
tar xzf %SOURCE2 -C tzcode%tzcode_version
sed -e 's|@objpfx@|'`pwd`'/obj/|' \
    -e 's|@datadir@|%_datadir|' \
	Makeconfig.in > Makeconfig

%build
%__make
fgrep -v tz-art.htm tzcode%tzcode_version/tz-link.htm > \
	tzcode%tzcode_version/tz-link.html

%install
rm -rf %buildroot
sed -i 's|@install_root@|%buildroot|' Makeconfig
%__make install
hardlink -vc %buildroot

%check
%__make check

%files
%defattr(-,root,root)
%_datadir/zoneinfo
%doc tzcode%tzcode_version/README
%doc tzcode%tzcode_version/Theory
%doc tzcode%tzcode_version/tz-link.html

%changelog
* Wed Oct 26 2011 Solar Designer <solar-at-owl.openwall.com> 2011m-owl1
- Updated to 2011m.

* Sat Oct 15 2011 Solar Designer <solar-at-owl.openwall.com> 2011l-owl1
- Updated to 2011l.
- Run hardlink(1) on the target tree to save disk space.

* Sun Oct 09 2011 Solar Designer <solar-at-owl.openwall.com> 2011k-owl1
- Initial packaging for Owl based on cut-down spec file and
tzdata-base-0.tar.bz2 from Fedora, with review of the tzdata package in
ALT Linux Sisyphus.

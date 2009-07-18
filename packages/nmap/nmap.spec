# $Owl: Owl/packages/nmap/nmap.spec,v 1.31 2009/07/18 17:11:19 solar Exp $

%define BUILD_NSE_ENABLED 1
%define BUILD_NCAT 1
%define BUILD_NDIFF 0

Summary: Network exploration tool and security scanner.
Name: nmap
Version: 5.00
Release: owl3
Epoch: 2
License: GPL
Group: Applications/System
URL: http://nmap.org
%define srcname nmap-%version
Source: %srcname-stripped-for-owl-1.tar.bz2
# The following subdirectories have been removed from the above tarball:
# mswin32 macosx zenmap libpcap libpcre
# and a README-stripped file has been added.
# The size reduced from 8.7 MB to 2.2 MB.
# Source: http://nmap.org/dist/%srcname.tar.bz2
# Signature: http://nmap.org/dist/sigs/%srcname.tar.bz2.asc
Patch0: nmap-5.00-owl-nse_ldflags.diff
Patch1: nmap-5.00-alt-owl-autoheader.diff
Patch2: nmap-5.00-up-20090718-nse_open.diff
Patch3: nmap-5.00-alt-owl-drop-priv.diff
Patch4: nmap-5.00-alt-owl-dot-dir.diff
Patch5: nmap-5.00-alt-owl-fileexistsandisreadable.diff
Patch6: nmap-5.00-owl-include.diff
PreReq: grep, shadow-utils
Requires: /var/empty
%if %BUILD_NDIFF
# The configure script checks for the Python interpreter, which is why
# this dependency is not just runtime, but also build-time.
Requires: python >= 2.4
BuildRequires: python-devel >= 2.4
%endif
BuildRequires: openssl-devel >= 0.9.7g-owl1
BuildRequires: gcc-c++, libpcap-devel, libcap-devel, pcre-devel
BuildRoot: /override/%name-%version

%description
Nmap is an utility for network exploration or security auditing.  Many
systems and network administrators also find it useful for tasks such as
network inventory, managing service upgrade schedules, and monitoring
host or service uptime.  Nmap uses raw IP packets in novel ways to
determine what hosts are available on the network, what services
(application name and version) those hosts are offering, what operating
systems (and OS versions) they are running, what type of packet
filters/firewalls are in use, and dozens of other characteristics.
Nmap was designed to rapidly scan large networks, but it also works fine
against single hosts.

%if %BUILD_NCAT
%package -n ncat
Summary: Nmap's remake of netcat - a feature-packed networking utility.
Group: Applications/System

%description -n ncat
Ncat is a feature-packed networking utility, which will read and write
data across a network from the command line.  It uses both TCP and UDP
for communication and is designed to be a reliable back-end tool to
instantly provide network connectivity to other applications and users.
Ncat will not only work with IPv4 and IPv6 but provides the user with a
virtually limitless number of potential uses.
%endif

%prep
%setup -q -n %srcname
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
bzip2 -9 CHANGELOG ncat/ChangeLog doc/TODO*

%if !%BUILD_NSE_ENABLED
%define nseflag --without-liblua
%endif

%if !%BUILD_NCAT
%define ncatflag --without-ncat
%endif

%if %BUILD_NDIFF
%define ndiff_flag --with-ndiff
%endif

%build
aclocal
autoheader
autoconf
%configure \
	--without-zenmap %nseflag %ncatflag %ndiff_flag \
	--with-user=nmap \
	--with-chroot-empty=/var/empty
touch makefile.dep
%__make

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot

%pre
grep -q ^nmap: /etc/group || groupadd -g 189 nmap
grep -q ^nmap: /etc/passwd ||
	useradd -g nmap -u 189 -d / -s /bin/false -M nmap

%files
%defattr(-,root,root)
%doc CHANGELOG.bz2 COPYING HACKING docs/{README,TODO*,*.txt}
%attr(750,root,wheel) %_bindir/nmap
%_mandir/man1/nmap.1*
%_datadir/nmap

%if %BUILD_NDIFF
%_bindir/ndiff
%_mandir/man1/ndiff.1*
%endif

%if %BUILD_NCAT
%files -n ncat
%defattr(-,root,root)
%doc ncat/ChangeLog.bz2 ncat/COPYING
%_bindir/ncat
%_mandir/man1/ncat.1*
%_datadir/ncat
%endif

%changelog
* Sat Jul 18 2009 Solar Designer <solar-at-owl.openwall.com> 5.00-owl3
- Replaced the NSE initialization patch with its corrected revision that went
upstream (by Patrick Donnelly).
- Moved Ncat to a subpackage.
- Based the descriptions on those found in upstream's sample spec file.
- Set Epoch to 2 to match RHEL 4 and upstream's sample spec file.

* Fri Jul 17 2009 Michail Litvak <mci-at-owl.openwall.com> 5.00-owl2
- Added a patch to prevent NSE initialization when no scripts are to be used.
- Fixed the -drop-priv patch to initialize NSE before privileges dropping.

* Thu Jul 16 2009 Michail Litvak <mci-at-owl.openwall.com> 5.00-owl1
- Updated to 5.00.
- Updated patches.
- Added possibility to build with NSE enabled, ncat and ndiff.

* Mon May 18 2009 Michail Litvak <mci-at-owl.openwall.com> 4.76-owl1
- Updated to 4.76.
- Updated patches.

* Sun May 18 2008 Michail Litvak <mci-at-owl.openwall.com> 4.62-owl1
- Updated to 4.62.
- Updated patches.

* Fri Oct 19 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.20-owl3
- Use 1st generation OS detection system by default.

* Wed Oct 17 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.20-owl2
- Simplified lowering privileges algorithm.

* Sun Oct 07 2007 Solar Designer <solar-at-owl.openwall.com> 4.20-owl1
- Updated to 4.20.

* Sun Jun 25 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.11-owl1
- Updated to 4.11.

* Wed Apr 26 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.03-owl1
- Updated to 4.03.

* Sun Mar 05 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.02-owl0.1
- Updated to 4.02 Alpha1.
- Synced patches with ALT's nmap-4.02-alt0.1 package.
- Reworked lowering root privileges patch for submission upstream.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.95-owl2
- Compressed CHANGELOG file.

* Fri Jan 13 2006 Michail Litvak <mci-at-owl.openwall.com> 3.95-owl1
- Updated to 3.95.
- Updated patches.

* Mon Nov 07 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.48-owl5
- Build with system PCRE library.

* Sat Jun 25 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.48-owl4
- Rebuilt with libssl.so.5.

* Sun Dec 25 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.48-owl3
- Bumped up release to satisfy dependency resolver (fix for openssl
upgrading issue).

* Sun Oct 26 2003 Solar Designer <solar-at-owl.openwall.com> 3.48-owl2
- Added a reduced version of the drop privileges patch from ALT Linux,
without chrooting if DNS resolver is required.

* Sat Oct 11 2003 Solar Designer <solar-at-owl.openwall.com> 3.48-owl1
- Updated to 3.48 (from Simon with minor changes; the use of included
libpcre is now forced).

* Fri Oct 02 2003 Simon B <simonb-at-owl.openwall.com> 3.45-owl1
- Upgrade

* Mon Jun 02 2003 Solar Designer <solar-at-owl.openwall.com> 3.27-owl1
- Initial packaging for Owl, spec file very loosely based on one found
in the official Nmap package.

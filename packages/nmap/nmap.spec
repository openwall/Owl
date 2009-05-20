# $Owl: Owl/packages/nmap/nmap.spec,v 1.23 2009/05/20 19:42:57 mci Exp $

Summary: Network exploration tool and security scanner.
Name: nmap
Version: 4.76
Release: owl1
License: GPL
Group: Applications/System
URL: http://nmap.org/
%define srcname nmap-%version
Source: http://download.insecure.org/nmap/dist/%srcname.tar.bz2
Patch0: nmap-4.76-owl-nse_ldflags.diff
Patch1: nmap-4.76-alt-owl-autoheader.diff
Patch2: nmap-4.76-owl-warnings.diff
Patch3: nmap-4.76-alt-owl-drop-priv.diff
Patch4: nmap-4.76-alt-owl-dot-dir.diff
Patch5: nmap-4.76-alt-owl-fileexistsandisreadable.diff
Patch6: nmap-4.76-owl-include.diff
PreReq: grep, shadow-utils
Requires: /var/empty
BuildRequires: openssl-devel >= 0.9.7g-owl1
BuildRequires: gcc-c++, libpcap-devel, libcap-devel, pcre-devel
BuildRoot: /override/%name-%version

%description
Nmap is an utility for network exploration or security auditing.
It supports ping scanning (determine which hosts are up), many port
scanning techniques, version detection (determine service protocols and
application versions listening behind ports), and TCP/IP fingerprinting
(remote host OS or device identification).  Nmap also offers flexible
target and port specification, decoy/stealth scanning, Sun RPC scanning,
and more.

%prep
%setup -q -n %srcname
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
bzip2 -9 CHANGELOG

%build
aclocal
autoheader
autoconf
%configure \
	--without-zenmap \
	--without-liblua \
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
%doc CHANGELOG.bz2 COPYING HACKING docs/{README,*.txt}
%attr(750,root,wheel) %_bindir/nmap
%_mandir/man1/nmap.1*
%_datadir/nmap

%changelog
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

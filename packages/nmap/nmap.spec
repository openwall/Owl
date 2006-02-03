# $Owl: Owl/packages/nmap/nmap.spec,v 1.14 2006/02/03 22:05:17 ldv Exp $

Summary: Network exploration tool and security scanner.
Name: nmap
Version: 3.95
Release: owl2
License: GPL
Group: Applications/System
URL: http://www.insecure.org/nmap/
Source: http://download.insecure.org/nmap/dist/nmap-%version.tar.bz2
Patch0: nmap-3.95-alt-owl-init.diff
Patch1: nmap-3.95-alt-owl-drop-root.diff
Patch2: nmap-3.95-alt-owl-libpcap.diff
Requires: /var/empty
BuildRequires: openssl-devel >= 0.9.7g-owl1
BuildRequires: libpcap-devel, libcap-devel, pcre-devel
BuildRoot: /override/%name-%version

%description
Nmap is an utility for network exploration or security auditing.  It
supports ping scanning (determine which hosts are up), many port
scanning techniques, version detection (determine service protocols
and application versions listening behind ports), and TCP/IP
fingerprinting (remote host OS or device identification).  Nmap also
offers flexible target and port specification, decoy/stealth scanning,
Sun RPC scanning, and more.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
bzip2 -9 CHANGELOG

%build
aclocal
autoconf
%configure --without-nmapfe
%__make

%install
rm -rf %buildroot

%makeinstall nmapdatadir=%buildroot%_datadir/%name

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

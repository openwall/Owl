# $Id: Owl/packages/nmap/nmap.spec,v 1.8 2005/06/24 23:36:36 ldv Exp $

Summary: Network exploration tool and security scanner.
Name: nmap
Version: 3.48
Release: owl4
License: GPL
Group: Applications/System
URL: http://www.insecure.org/nmap/
Source: http://download.insecure.org/nmap/dist/nmap-%version.tar.bz2
Patch0: nmap-3.48-alt-owl-libpcap.diff
Patch1: nmap-3.48-alt-owl-no-local-libs.diff
Patch2: nmap-3.48-up-no-external-libpcre.diff
Patch3: nmap-3.48-alt-owl-drop-root.diff
Requires: /var/empty
BuildRequires: openssl-devel, libpcap-devel, libcap-devel
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
rm -r libpcap-possiblymodified
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure --without-nmapfe --with-libpcre=included
make LIBS='-lm -lssl -lcrypto -lpcap -lcap -lnbase -lnsock libpcre/libpcre.a'

%install
rm -rf %buildroot

%makeinstall nmapdatadir=%buildroot%_datadir/%name

%pre
grep -q ^nmap: /etc/group || groupadd -g 189 nmap
grep -q ^nmap: /etc/passwd ||
	useradd -g nmap -u 189 -d / -s /bin/false -M nmap

%files
%defattr(-,root,root)
%doc COPYING CHANGELOG HACKING docs/{README,*.{txt,html}}
%attr(750,root,wheel) %_bindir/nmap
%_mandir/man1/nmap.1*
%_datadir/nmap

%changelog
* Sat Jun 25 2005 Dmitry V. Levin <ldv@owl.openwall.com> 3.48-owl4
- Rebuilt with libssl.so.5.

* Sun Dec 25 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 3.48-owl3
- Bumped up release to satisfy dependency resolver (fix for openssl
upgrading issue).

* Sun Oct 26 2003 Solar Designer <solar@owl.openwall.com> 3.48-owl2
- Added a reduced version of the drop privileges patch from ALT Linux,
without chrooting if DNS resolver is required.

* Sat Oct 11 2003 Solar Designer <solar@owl.openwall.com> 3.48-owl1
- Updated to 3.48 (from Simon with minor changes; the use of included
libpcre is now forced).

* Fri Oct 02 2003 Simon B <simonb@owl.openwall.com> 3.45-owl1
- Upgrade

* Mon Jun 02 2003 Solar Designer <solar@owl.openwall.com> 3.27-owl1
- Initial packaging for Owl, spec file very loosely based on one found
in the official Nmap package.

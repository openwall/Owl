# $Id: Owl/packages/nmap/nmap.spec,v 1.2 2003/10/11 19:54:07 solar Exp $

Summary: Network exploration tool and security scanner.
Name: nmap
Version: 3.48
Release: owl1
License: GPL
Group: Applications/System
URL: http://www.insecure.org/nmap/
Source: http://download.insecure.org/nmap/dist/nmap-%{version}.tar.bz2
Patch0: nmap-3.48-alt-owl-libpcap.diff
Patch1: nmap-3.48-alt-owl-no-local-libs.diff
Patch2: nmap-3.48-up-no-external-libpcre.diff
BuildRoot: /override/%{name}-%{version}

%description
Nmap is an utility for network exploration or security auditing.  It
supports ping scanning (determine which hosts are up), many port
scanning techniques (determine what services the hosts are offering),
and TCP/IP fingerprinting (remote host operating system
identification).  Nmap also offers flexible target and port
specification, decoy scanning, determination of TCP sequence numbers
predictability characteristics, Sun RPC scanning, reverse-identd
scanning, and more.

%prep
%setup -q
rm -r libpcap-possiblymodified
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure --without-nmapfe --with-libpcre=included
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall nmapdatadir=$RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING CHANGELOG HACKING docs/{README,*.{txt,html}}
%attr(750,root,wheel) %{_bindir}/nmap
%{_mandir}/man1/nmap.1*
%{_datadir}/nmap

%changelog
* Sat Oct 11 2003 Solar Designer <solar@owl.openwall.com> 3.48-owl1
- Updated to 3.48 (from Simon with minor changes; the use of included
libpcre is now forced).

* Fri Oct 02 2003 Simon B <simonb@owl.openwall.com> 3.45-owl1
- Upgrade

* Mon Jun 02 2003 Solar Designer <solar@owl.openwall.com> 3.27-owl1
- Initial packaging for Owl, spec file very loosely based on one found
in the official Nmap package.

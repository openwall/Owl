# $Id: Owl/packages/nmap/nmap.spec,v 1.1 2003/06/02 05:37:07 solar Exp $

Summary: Network exploration tool and security scanner.
Name: nmap
Version: 3.27
Release: owl1
License: GPL
Group: Applications/System
URL: http://www.insecure.org/nmap/
Source: http://download.insecure.org/nmap/dist/nmap-%{version}.tar.bz2
Patch0: nmap-3.27-owl-fixes.diff
Patch1: nmap-3.27-owl-tmp.diff
Patch2: nmap-3.27-alt-owl-libpcap.diff
Patch3: nmap-3.27-alt-owl-no-local-libs.diff
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
%patch3 -p1
ln -s configure.ac configure.in
autoconf

%build
%configure --without-nmapfe
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
* Mon Jun 02 2003 Solar Designer <solar@owl.openwall.com> 3.27-owl1
- Initial packaging for Owl, spec file very loosely based on one found
in the official Nmap package.

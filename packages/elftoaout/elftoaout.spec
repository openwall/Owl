# $Id: Owl/packages/elftoaout/elftoaout.spec,v 1.4 2002/01/30 10:18:50 mci Exp $

Summary: A utility for converting ELF binaries to a.out binaries.
Name: elftoaout
Version: 2.3
Release: owl1
License: GPL
Group: System Environment/Kernel
Source:	ftp://sunsite.mff.cuni.cz/OS/Linux/Sparc/local/elftoaout/elftoaout-%{version}.tgz
ExclusiveArch: sparc sparcv9 sparc64
BuildRoot: /override/%{name}-%{version}

%description
The elftoaout utility converts a static ELF binary to a static a.out
binary.  If you're using Linux on a SPARC, you'll need to run elftoaout
on the kernel image so that the SPARC PROM can netboot the image.

elftoaout is also used to build the SPARC boot loader (SILO).

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m 0755 -s elftoaout $RPM_BUILD_ROOT/usr/bin/elftoaout

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -m 0644 elftoaout.1 $RPM_BUILD_ROOT/%{_mandir}/man1/elftoaout.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/elftoaout
%{_mandir}/man1/elftoaout.*

%changelog
* Wed Jan 30 2002 Michail Litval <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Jan  7 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- spec cleanup

# $Owl: Owl/packages/elftoaout/elftoaout.spec,v 1.10 2005/11/16 12:21:36 solar Exp $

Summary: A utility for converting ELF binaries to a.out binaries.
Name: elftoaout
Version: 2.3
Release: owl1
License: GPL
Group: System Environment/Kernel
Source:	ftp://sunsite.mff.cuni.cz/OS/Linux/Sparc/local/elftoaout/elftoaout-%version.tgz
ExclusiveArch: sparc sparcv9 sparc64
BuildRoot: /override/%name-%version

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
rm -rf %buildroot

mkdir -p %buildroot/usr/bin
install -m 755 -s elftoaout %buildroot/usr/bin/

mkdir -p %buildroot%_mandir/man1
install -m 644 elftoaout.1 %buildroot%_mandir/man1/

%files
%defattr(-,root,root)
/usr/bin/elftoaout
%_mandir/man1/elftoaout.*

%changelog
* Wed Jan 30 2002 Michail Litvak <mci-at-owl.openwall.com> 2.3-owl1
- Enforce our new spec file conventions.

* Sun Jan 07 2001 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- spec cleanup

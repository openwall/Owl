# $Id: Owl/packages/elftoaout/elftoaout.spec,v 1.3 2001/01/10 05:01:29 solar Exp $

Summary: A utility for converting ELF binaries to a.out binaries.
Name: 		elftoaout
Version:	2.3
Release: 	1owl
Copyright: 	GPL
Group: 		System Environment/Kernel
Source: 	ftp://sunsite.mff.cuni.cz/OS/Linux/Sparc/local/elftoaout/elftoaout-%{version}.tgz
ExclusiveArch:  sparc sparcv9 sparc64
BuildRoot:      /var/rpm-buildroot/%{name}-root

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
* Sun Jan  7 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- spec cleanup

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- use %%{_mandir}

* Sat Jun  3 2000 Jakub Jelinek <jakub@redhat.com>
- 2.3 - -c support by Pete Zaitcev

* Tue Feb 22 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 3)

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- rebuild for Raw Hide.

* Fri Jul 10 1998 Jeff Johnson <jbj@redhat.com>
- repackage ultrapenguin with build root.

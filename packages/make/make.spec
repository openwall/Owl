# $Id: Owl/packages/make/make.spec,v 1.2 2001/01/06 14:42:39 solar Exp $

Summary: A GNU tool which simplifies the build process for users.
Name: 		make
Version: 	3.79.1
Release: 	3owl
Copyright: 	GPL
Group: 		Development/Tools
Source: 	ftp://ftp.gnu.org/gnu/make/make-%{version}.tar.gz
Prereq: 	/sbin/install-info
Prefix: 	%{_prefix}
Buildroot: 	/var/rpm-buildroot/%{name}-root

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files.  Make
allows users to build and install packages without any significant
knowledge about the details of the build process.  The details about
how the program should be built are provided for make in the program's
makefile.

The GNU make tool should be installed on your system because it is
commonly used to simplify the process of installing programs.

%prep
%setup -q

%build
export ac_cv_func_mkstemp=yes \
%configure
make

%install
rm -f ${RPM_BUILD_ROOT}

%makeinstall

cd ${RPM_BUILD_ROOT}
ln -sf make .%{_bindir}/gmake
gzip -9nf .%{_infodir}/make.info*
rm -f .%{_infodir}/dir

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/make.info.gz %{_infodir}/dir --entry="* GNU make: (make).           The GNU make utility."

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/make.info.gz %{_infodir}/dir --entry="* GNU make: (make).           The GNU make utility."
fi

%files
%defattr(-,root,root)
%doc NEWS README
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/*.info*

%changelog
* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- Enable mkstemp explicitly, not rely on configure.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH rawhide

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 24 2000 Preston Brown <pbrown@redhat.com>
- 3.79.1 bugfix release

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Sun May  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build for some odd situations, such as
  - previously installed make != GNU make
  - /bin/sh != bash

* Mon Apr 17 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.79

* Thu Feb 24 2000 Cristian Gafton <gafton@redhat.com>
- add patch from Andreas Jaeger to fix dtype lookups (for glibc 2.1.3
  builds)

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man page.

* Fri Jan 21 2000 Cristian Gafton <gafton@redhat.com>
- apply patch to fix a /tmp race condition from Thomas Biege
- simplify %install

* Sat Nov 27 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.78.1.

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- added a serial tag so it upgrades right

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Sep 16 1998 Cristian Gafton <gafton@redhat.com>
- added a patch for large file support in glob
 
* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.77

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- udpated from 3.75 to 3.76
- various spec file cleanups
- added install-info support

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

# $Id: Owl/packages/gawk/gawk.spec,v 1.1.2.1 2001/06/23 13:31:46 solar Exp $

Summary: 	The GNU version of the awk text processing utility.
Name: 		gawk
Version: 	3.0.6
Release: 	2owl
License: 	GPL
Group: 		Applications/Text
Source0: 	ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.gz
Source1: 	ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}-ps.tar.gz
# The "unaligned" patch should be obsolete with glibc 2.1+
Patch0:		gawk-3.0-rh-unaligned.diff
Patch1:		gawk-3.0.6-jh-owl-igawk-tmp.diff
Prereq: 	/sbin/install-info
Requires:	mktemp
BuildRequires:	texinfo
Buildroot: 	/var/rpm-buildroot/%{name}-root

%description
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs.

Install the gawk package if you need a text processing utility. Gawk is
considered to be a standard Linux tool for processing text.

%prep
%setup -q -b 1
%patch0 -p1
%patch1 -p1

%build
rm -f doc/gawk.info awklib/eg/prog/igawk.sh
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=${RPM_BUILD_ROOT}/bin \
	mandir=${RPM_BUILD_ROOT}%{_mandir}/man1 \
	libexecdir=${RPM_BUILD_ROOT}%{_libexecdir}/awk \
	datadir=${RPM_BUILD_ROOT}%{_datadir}/awk

cd $RPM_BUILD_ROOT
rm -f .%{_infodir}/dir
gzip -9nf .%{_infodir}/gawk.info*
mkdir -p .%{_prefix}/bin
ln -sf gawk.1.gz .%{_mandir}/man1/awk.1.gz
cd bin
ln -sf ../../bin/gawk ../usr/bin/awk
ln -sf ../../bin/gawk ../usr/bin/gawk

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/gawk.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/gawk.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root,-)
%doc README COPYING ACKNOWLEDGMENT FUTURES INSTALL LIMITATIONS NEWS PORTS
%doc README_d POSIX.STD doc/gawk.ps doc/awkcard.ps
/bin/*
/usr/bin/*
%{_mandir}/man1/*
%{_infodir}/gawk.info*
%{_libexecdir}/awk
%{_datadir}/awk

%changelog
* Sun May 27 2001 Solar Designer <solar@owl.openwall.com>
- Patched unsafe temporary file handling in igawk, based on report and
patch from Jarno Huuskonen.
- Make sure gawk.info and igawk.sh are re-generated from gawk.texi on
package builds.

* Sun Oct  1 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH

* Wed Aug 16 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.06

* Tue Aug 15 2000 Trond Eivind Glomsrød <teg@redhat.com>
- /usr/bin/gawk can't point at gawk - infinite symlink
- /usr/bin/awk can't point at gawk - infinite symlink

* Mon Aug 14 2000 Preston Brown <pbrown@redhat.com>
- absolute --> relative symlinks

* Tue Aug  8 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- fix paths for "configure" call

* Thu Jul 13 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- add another bugfix

* Thu Jul 13 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.0.5 with bugfix

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 30 2000 Matt Wilson <msw@redhat.com>
- revert to 3.0.4.  3.0.5 misgenerates e2fsprogs' test cases

* Wed Jun 28 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.0.5

* Mon Jun 19 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- add defattr

* Mon Jun 19 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- FHS

* Tue Mar 14 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- add bug-fix

* Thu Feb  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix man page symlinks
- Fix description
- Fix download URL

* Wed Jun 30 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.0.4.

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- make sure all binaries are stripped

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 6)

* Fri Feb 19 1999 Jeff Johnson <jbj@redhat.com>
- Install info pages (#1242).

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1
- don't package /usr/info/dir

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 3.0.3
- added documentation and buildroot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
